#!/usr/bin/env python3
"""
Inspect a multi-arch modelcar OCI image for cross-architecture layer deduplication.

Verifies that the mtime normalization fix (build-definitions#3358) is active by:
  1. Fetching the manifest index and per-platform manifests
  2. Comparing layer digests across all architectures
  3. Downloading a small shared TAR layer and inspecting its mtime metadata

Requires: oras CLI (https://oras.land)

Usage:
  ./inspect_modelcar_layers.py IMAGE_REF
  ./inspect_modelcar_layers.py registry.redhat.io/rhai/modelcar-redhatai-tinyllama-1-1b-chat-v1-0:3.0
"""

import argparse
import json
import os
import subprocess
import sys
import tarfile
import tempfile
from collections import defaultdict
from datetime import datetime, timezone


def run(cmd, check=True):
    result = subprocess.run(cmd, capture_output=True, text=True, check=check)
    return result.stdout.strip()


def oras_manifest_fetch(ref):
    return json.loads(run(["oras", "manifest", "fetch", ref]))


def oras_blob_fetch(ref, digest, output_path):
    run(["oras", "blob", "fetch", f"{ref}@{digest}", "-o", output_path])


def fetch_platform_manifests(image_ref):
    index = oras_manifest_fetch(image_ref)

    media_type = index.get("mediaType", "")
    if "manifest.list" not in media_type and "image.index" not in media_type:
        print(f"ERROR: Expected a manifest index, got mediaType={media_type}")
        sys.exit(1)

    platforms = {}
    for m in index.get("manifests", []):
        p = m.get("platform", {})
        arch = p.get("architecture", "unknown")
        variant = p.get("variant", "")
        key = f"{arch}/{variant}" if variant else arch
        platforms[key] = {
            "digest": m["digest"],
            "manifest": oras_manifest_fetch(f"{image_ref}@{m['digest']}"),
        }

    return platforms


def analyze_layers(platforms):
    platform_keys = sorted(platforms.keys())
    max_layers = max(len(p["manifest"]["layers"]) for p in platforms.values())

    layer_data = []
    for idx in range(max_layers):
        entry = {"index": idx, "digests": {}, "title": None, "size": None, "annotations": {}}
        for key in platform_keys:
            layers = platforms[key]["manifest"]["layers"]
            if idx >= len(layers):
                continue
            layer = layers[idx]
            entry["digests"][key] = layer["digest"]
            entry["size"] = entry["size"] or layer["size"]
            annotations = layer.get("annotations", {})
            if not entry["title"]:
                entry["title"] = annotations.get("org.opencontainers.image.title", f"layer-{idx}")
            if not entry["annotations"]:
                entry["annotations"] = annotations
        entry["shared"] = len(set(entry["digests"].values())) == 1
        layer_data.append(entry)

    return layer_data


def pick_mtime_inspection_layer(layer_data):
    """Pick a small shared layer for mtime inspection — avoid large blobs like .safetensors."""
    shared = [l for l in layer_data if l["shared"] and l["annotations"].get("olot.layer.content.digest")]
    if not shared:
        return None
    preferred = [l for l in shared if l["size"] and l["size"] < 100_000]
    if preferred:
        return preferred[0]
    smallest = sorted(shared, key=lambda l: l["size"] or float("inf"))
    return smallest[0]


def inspect_tar_mtime(image_ref, layer):
    with tempfile.NamedTemporaryFile(suffix=".tar", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        digest = next(iter(layer["digests"].values()))
        oras_blob_fetch(image_ref, digest, tmp_path)

        results = []
        with tarfile.open(tmp_path, "r") as tf:
            for member in tf.getmembers():
                results.append({
                    "name": member.name,
                    "mtime": member.mtime,
                    "mtime_human": datetime.fromtimestamp(member.mtime, tz=timezone.utc).strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    ),
                    "mode": oct(member.mode),
                    "uid": member.uid,
                    "gid": member.gid,
                    "uname": member.uname,
                })
        return results
    finally:
        os.unlink(tmp_path)


def fetch_config_labels(image_ref, platforms):
    first = next(iter(platforms.values()))
    config_digest = first["manifest"]["config"]["digest"]
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as tmp:
        tmp_path = tmp.name
    try:
        oras_blob_fetch(image_ref, config_digest, tmp_path)
        with open(tmp_path) as f:
            config = json.load(f)
        return config.get("config", {}).get("Labels", {})
    finally:
        os.unlink(tmp_path)


def print_report(image_ref, platforms, layer_data, mtime_info, mtime_layer, labels):
    platform_keys = sorted(platforms.keys())
    shared_count = sum(1 for l in layer_data if l["shared"])
    total_count = len(layer_data)
    model_shared = sum(1 for l in layer_data if l["shared"] and l["annotations"].get("olot.layer.content.digest"))

    print("=" * 80)
    print("CROSS-ARCHITECTURE LAYER DEDUPLICATION REPORT")
    print("=" * 80)
    print(f"\nImage: {image_ref}")
    print(f"Platforms: {', '.join(platform_keys)} ({len(platform_keys)} total)")
    print(f"Layers per platform: {total_count}")

    # Platform manifests
    print(f"\n{'Platform':<16} {'Manifest Digest':<75}")
    print("-" * 91)
    for key in platform_keys:
        print(f"{key:<16} {platforms[key]['digest']}")

    # Layer comparison
    print(f"\n{'Layer':<6} {'Title':<45} {'Size':>14} {'Shared?':<10} {'Digest'}")
    print("-" * 150)
    for l in layer_data:
        size_str = format_size(l["size"]) if l["size"] else "?"
        status = "YES" if l["shared"] else "NO"
        is_olot = bool(l["annotations"].get("olot.layer.content.digest"))
        marker = "" if l["shared"] else " (expected)" if not is_olot else " *** PROBLEM ***"
        digest = next(iter(l["digests"].values())) if l["digests"] else "?"
        digest_note = "" if l["shared"] else " (amd64)"
        print(f"{l['index']:<6} {l['title']:<45} {size_str:>14} {status:<10}{digest}{digest_note}{marker}")

    # Deduplication summary
    base_not_shared = sum(1 for l in layer_data if not l["shared"] and not l["annotations"].get("olot.layer.content.digest"))
    print(f"\nShared layers: {shared_count}/{total_count}")
    print(f"  Model layers shared (OLOT): {model_shared}")
    print(f"  Base layers differing (expected): {base_not_shared}")

    # mtime inspection
    if mtime_info:
        print(f"\n{'=' * 80}")
        print("MTIME NORMALIZATION CHECK")
        print(f"{'=' * 80}")
        print(f"\nInspected layer: {mtime_layer['title']} ({format_size(mtime_layer['size'])})")
        mtimes = set()
        for entry in mtime_info:
            mtimes.add(entry["mtime"])
            print(f"  {entry['name']}")
            print(f"    mtime: {entry['mtime']} ({entry['mtime_human']})")
            print(f"    mode: {entry['mode']}  uid/gid: {entry['uid']}/{entry['gid']}  uname: '{entry['uname']}'")

        has_subsecond = any(entry["mtime"] != int(entry["mtime"]) for entry in mtime_info)
        if len(mtimes) == 1 and not has_subsecond:
            print(f"\n  PASS: mtime is normalized (integer-second, single value)")
        elif has_subsecond:
            print(f"\n  FAIL: mtime has sub-second precision (raw download timestamp)")
        else:
            print(f"\n  WARN: multiple distinct mtimes found")

    # Config labels
    print(f"\n{'=' * 80}")
    print("IMAGE CONFIG LABELS")
    print(f"{'=' * 80}")
    if labels:
        for k, v in sorted(labels.items()):
            print(f"  {k}: {v}")
    else:
        print("  (none)")

    konflux = {k: v for k, v in labels.items() if "appstudio" in k or "tekton" in k}
    if konflux:
        print(f"\n  Konflux labels: found ({len(konflux)})")
    else:
        print(f"\n  Konflux labels: not found")

    # Storage impact
    print(f"\n{'=' * 80}")
    print("STORAGE IMPACT")
    print(f"{'=' * 80}")
    total_per_arch = sum(l["size"] for l in layer_data if l["size"])
    shared_size = sum(l["size"] for l in layer_data if l["shared"] and l["size"])
    unshared_size = sum(l["size"] for l in layer_data if not l["shared"] and l["size"])
    n = len(platform_keys)

    without_dedup = total_per_arch * n
    with_dedup = shared_size + (unshared_size * n)
    ratio = without_dedup / with_dedup if with_dedup else 0
    pct = (1 - with_dedup / without_dedup) * 100 if without_dedup else 0

    print(f"\n  Without deduplication: {n} arches x {format_size(total_per_arch)} = {format_size(without_dedup)}")
    print(f"  With deduplication:    {format_size(with_dedup)}")
    print(f"  Savings:               {format_size(without_dedup - with_dedup)} — {ratio:.1f}x more storage efficient ({pct:.1f}% reduction)")

    # Verdict
    print(f"\n{'=' * 80}")
    all_model_shared = all(
        l["shared"] for l in layer_data if l["annotations"].get("olot.layer.content.digest")
    )
    mtime_ok = mtime_info and not any(
        entry["mtime"] != int(entry["mtime"]) for entry in mtime_info
    )
    if all_model_shared and mtime_ok:
        print("VERDICT: PASS — mtime fix is ACTIVE, all model layers deduplicated")
    elif all_model_shared:
        print("VERDICT: PARTIAL — layers are shared but mtime could not be verified")
    else:
        print("VERDICT: FAIL — model layers are NOT fully deduplicated across architectures")
    print("=" * 80)


def format_size(n):
    if n >= 1_000_000_000:
        return f"{n / 1_000_000_000:.1f} GB"
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f} MB"
    if n >= 1_000:
        return f"{n / 1_000:.1f} KB"
    return f"{n} B"


def main():
    parser = argparse.ArgumentParser(
        description="Inspect a multi-arch modelcar image for cross-architecture layer deduplication."
    )
    parser.add_argument("image", help="OCI image reference (e.g. registry.redhat.io/rhai/modelcar-...:3.0)")
    parser.add_argument(
        "--skip-mtime",
        action="store_true",
        help="Skip TAR blob download and mtime inspection (faster, digest-only check)",
    )
    args = parser.parse_args()

    print(f"Fetching manifest index for {args.image} ...")
    platforms = fetch_platform_manifests(args.image)
    print(f"Found {len(platforms)} platforms: {', '.join(sorted(platforms.keys()))}")

    print("Analyzing layers ...")
    layer_data = analyze_layers(platforms)

    mtime_info = None
    mtime_layer = None
    if not args.skip_mtime:
        mtime_layer = pick_mtime_inspection_layer(layer_data)
        if mtime_layer:
            print(f"Downloading {mtime_layer['title']} ({format_size(mtime_layer['size'])}) for mtime inspection ...")
            mtime_info = inspect_tar_mtime(args.image, mtime_layer)
        else:
            print("No suitable shared model layer found for mtime inspection.")

    print("Fetching image config labels ...")
    labels = fetch_config_labels(args.image, platforms)

    print()
    print_report(args.image, platforms, layer_data, mtime_info, mtime_layer, labels)


if __name__ == "__main__":
    main()
