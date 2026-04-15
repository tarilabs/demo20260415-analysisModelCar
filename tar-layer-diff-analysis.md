# TAR Layer Digest Difference Analysis

**Image:** `registry.redhat.io/rhai/modelcar-qwen3-5-35b-a3b-fp8-dynamic:3.0`
**Date of analysis:** 2026-04-15

## Objective

Investigate why the ARM64 and AMD64 variants of this modelcar image have different TAR layer digests for model-artifact layers, despite containing byte-identical file content (as confirmed by the `olot.layer.content.digest` annotations).

Excluded from analysis: base image layer (Layer 1) and safetensor layer (Layer 6).

## Methodology

### 1. Download TAR blobs via ORAS

Blobs were fetched for all 10 differing layers + 1 shared control layer from both architecture variants:

```bash
REPO="registry.redhat.io/rhai/modelcar-qwen3-5-35b-a3b-fp8-dynamic"

# Example for one layer (repeated for all 11 layers, both architectures):
# ARM64
oras blob fetch "$REPO@sha256:937db2ada81431c0ffeea04d05f2e493415b307b74c3e2281fdeea5be0a85d48" \
  -o /tmp/modelcar-analysis/arm64/chat_template.tar

# AMD64
oras blob fetch "$REPO@sha256:49e690345fa6f811a1064b41f79fa4fca7b83844b6ecf1350750e822151847f3" \
  -o /tmp/modelcar-analysis/amd64/chat_template.tar
```

Full list of digests used:

| Layer | File | ARM64 TAR digest | AMD64 TAR digest | Same? |
|-------|------|------------------|------------------|-------|
| 2 | `chat_template.jinja` | `sha256:937db2ad...` | `sha256:49e69034...` | **No** |
| 3 | `config.json` | `sha256:3658974d...` | `sha256:d7aa49b5...` | **No** |
| 4 | `generation_config.json` | `sha256:f644d17f...` | `sha256:ea7d8dae...` | **No** |
| 5 | `merges.txt` | `sha256:8a0e9e3f...` | `sha256:21597f70...` | **No** |
| 7 | `preprocessor_config.json` | `sha256:5f6c1389...` | `sha256:6c028b9b...` | **No** |
| 8 | `recipe.yaml` | `sha256:d46cef14...` | `sha256:2e2c1062...` | **No** |
| 9 | `tokenizer_config.json` | `sha256:3d2bcefa...` | `sha256:abb5d0be...` | **No** |
| 10 | `tokenizer.json` | `sha256:acc73149...` | `sha256:2dbb4788...` | **No** |
| 11 | `video_preprocessor_config.json` | `sha256:24e33086...` | `sha256:88f5fc43...` | **No** |
| 12 | `vocab.json` | `sha256:e8caa8b1...` | `sha256:088570ae...` | **No** |
| 13 | `modelcard.md` | `sha256:19160baa...` | `sha256:19160baa...` | **Yes** |

### 2. Inspect TAR metadata with Python `tarfile`

```python
import tarfile, hashlib

with tarfile.open(path, 'r') as tf:
    for m in tf.getmembers():
        print(m.name, m.mode, m.uid, m.gid, m.uname, m.gname, m.mtime, m.pax_headers)
        # Also compute content SHA256 to verify file identity
        content = tf.extractfile(m).read()
        print(hashlib.sha256(content).hexdigest())
```

### 3. Hex-level byte comparison

```python
with open(arm_path, 'rb') as f: arm = f.read()
with open(amd_path, 'rb') as f: amd = f.read()
diffs = [i for i in range(len(arm)) if arm[i] != amd[i]]
```

## Findings

### Root Cause: File Modification Timestamp (`mtime`)

The **only** difference between ARM64 and AMD64 TAR layers is the **file modification timestamp** (`mtime`) embedded in the TAR headers. Every other attribute is identical.

#### Per-layer comparison (all 10 differing layers)

| File | ARM64 mtime | AMD64 mtime | Delta |
|------|-------------|-------------|-------|
| `chat_template.jinja` | `1773601725.9484088` (19:08:45.948) | `1773601701.9776669` (19:08:21.978) | ~24.0s |
| `config.json` | `1773601725.9594092` (19:08:45.959) | `1773601702.020668` (19:08:22.021) | ~24.0s |
| `generation_config.json` | `1773601725.952409` (19:08:45.952) | `1773601702.0126677` (19:08:22.013) | ~24.0s |
| `merges.txt` | `1773601726.0154104` (19:08:46.015) | `1773601702.2236736` (19:08:22.224) | ~23.8s |
| `preprocessor_config.json` | `1773601726.0604115` (19:08:46.060) | `1773601702.1826725` (19:08:22.183) | ~23.9s |
| `recipe.yaml` | `1773601726.0724118` (19:08:46.072) | `1773601702.2866755` (19:08:22.287) | ~23.8s |
| `tokenizer_config.json` | `1773601726.130413` (19:08:46.130) | `1773601702.3956785` (19:08:22.396) | ~23.7s |
| `tokenizer.json` | `1773601726.3204174` (19:08:46.320) | `1773601703.119699` (19:08:23.120) | ~23.2s |
| `video_preprocessor_config.json` | `1773601726.1814141` (19:08:46.181) | `1773601702.477681` (19:08:22.478) | ~23.7s |
| `vocab.json` | `1773601726.2954168` (19:08:46.295) | `1773601702.6766865` (19:08:22.677) | ~23.6s |

All timestamps are from **2026-03-15**, with AMD64 layers created ~24 seconds before ARM64.

#### Attributes that are IDENTICAL across both architectures

| Attribute | Value (both variants) |
|-----------|----------------------|
| File path | `models/<filename>` |
| File permissions | `0o664` (rw-rw-r--) |
| UID | `0` |
| GID | `0` |
| uname | `''` (empty) |
| gname | `''` (empty) |
| File content SHA256 | Matches `olot.layer.content.digest` annotation |

### Control Case: `modelcard.md` (Layer 13)

The modelcard layer has an **identical** TAR digest across both variants. Key differences from the OLOT layers:

| Attribute | modelcard.md | OLOT layers |
|-----------|-------------|-------------|
| TAR digest | Same on ARM64 & AMD64 | Different |
| `mtime` | `1773601689.0` (integer, 19:08:09) | Sub-second precision, arch-dependent |
| `uname` | `root` | `''` (empty) |
| Built by | modelcar build (once, shared) | OLOT (per-arch, separately) |

The modelcard was built **once** at 19:08:09 and the resulting layer blob was referenced by both architecture manifests. The OLOT layers were built **separately per architecture** ~12-36 seconds later.

### Byte-level TAR structure (example: `generation_config.json`)

Examining the raw bytes of the `generation_config.tar` (10,240 bytes per variant):

```
Total differing bytes: 14 out of 10,240
```

The 14 differing bytes are located in:

| Location | # bytes | Field | Why it differs |
|----------|---------|-------|----------------|
| Block 0, offset 134 | 1 | PAX header `size` field | PAX mtime string is 27 vs 28 chars |
| Block 0, offset 153 | 1 | PAX header `checksum` | Recomputed due to size change |
| Block 1 (offsets 513-539) | 10 | PAX extended data | The mtime value string itself |
| Block 2 (offsets 1169, 1177) | 2 | Real file header `mtime` | Integer-second mtime in octal |

The TAR uses **PAX format** (typeflag `x`), which stores the full nanosecond-precision mtime as a text string in an extended header block. The structure is:

```
Block 0: PAX header entry (typeflag='x', points to PAX data)
Block 1: PAX data payload:
          ARM64: "27 mtime=1773601725.952409\n"
          AMD64: "28 mtime=1773601702.0126677\n"  (note: "28" because string is 1 char longer)
Block 2: Real file header (typeflag='0', contains standard octal mtime)
          ARM64: mtime=15155601676 (octal) = 1773601726 (decimal)
          AMD64: mtime=15155601646 (octal) = 1773601702 (decimal)
Block 3+: File data (identical between variants)
```

### Content Integrity Verification

For every layer, the SHA256 of the extracted file content **matches exactly** the `olot.layer.content.digest` annotation:

| File | Content SHA256 (both variants) | Matches annotation? |
|------|-------------------------------|---------------------|
| `chat_template.jinja` | `a4aee8afcf2e0711942cf848899be66016f8d14a889ff9ede07bca099c28f715` | Yes |
| `config.json` | `dba2fc8960ae3d03922c8ecd97c477ddc2560f65b867ea70e7a683df8efe568a` | Yes |
| `generation_config.json` | `4f25002776b741773666203dcea8f54619f177ace3ae483d311102092a4658e0` | Yes |
| `merges.txt` | `a9d356d7bdf1ef4949e3e748e95b8e10ad9d4e2e838eddc38a0a7b6b94d1db8d` | Yes |
| `preprocessor_config.json` | `27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` | Yes |
| `recipe.yaml` | `7a15656336d245b85904013a55a1f3df190302a0141c161682a4b0727e56435c` | Yes |
| `tokenizer_config.json` | `316230d6a809701f4db5ea8f8fc862bc3a6f3229c937c174e674ff3ca0a64ac8` | Yes |
| `tokenizer.json` | `5f9e4d4901a92b997e463c1f46055088b6cca5ca61a6522d1b9f64c4bb81cb42` | Yes |
| `video_preprocessor_config.json` | `7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` | Yes |
| `vocab.json` | `ce99b4cb2983d118806ce0a8b777a35b093e2000a503ebde25853284c9dfa003` | Yes |
| `modelcard.md` | `15bef5797954ec4f49e2d6ec419fe7813820ef2a4a35bdc33e6d28b63989508a` | Yes |

## Build Timeline Reconstruction

```
2026-03-15T19:08:09.000  modelcard.md layer built (shared, used by both manifests)
2026-03-15T19:08:21-23   AMD64 OLOT layers built (model files packaged into TAR layers)
2026-03-15T19:08:45-46   ARM64 OLOT layers built (same files, ~24s later)
```

## Conclusions

1. **The TAR digest difference is caused exclusively by the `mtime` (modification timestamp)** embedded in the TAR headers. The OLOT tool packages model files into TAR layers using the current filesystem timestamp at build time. Since the AMD64 and ARM64 variants were built sequentially (~24 seconds apart), each file gets a different mtime, producing a different TAR byte stream and therefore a different SHA256 digest.

2. **File content is byte-identical across architectures.** The `olot.layer.content.digest` annotation accurately reflects the true content hash, and both variants contain the exact same file bytes. Only the TAR metadata wrapper differs.

3. **The `modelcard.md` layer is shared because it was built once.** Unlike the OLOT layers, the modelcard was produced by a separate step in the build pipeline, likely before the per-architecture OLOT packaging began. Its TAR blob was built once and referenced by both architecture manifests, so it has the same digest.

4. **Only 14 bytes differ in a typical 10 KB TAR layer.** The differences are:
   - The PAX extended header `mtime` string (the nanosecond-precision timestamp value)
   - The PAX header entry `size` and `checksum` fields (adjusted for the mtime string length)
   - The standard TAR header `mtime` field (integer-second precision in octal)

5. **This is a reproducibility issue.** If the build tool (OLOT) used a fixed/zeroed timestamp (e.g., `SOURCE_DATE_EPOCH`), the TAR layers would be byte-identical across architectures, enabling cross-platform layer deduplication and saving registry storage. The `modelcard.md` layer demonstrates that a shared blob is achievable when the timestamp is consistent.

## Extended Build Timeline (from OCI image config history)

Fetching the OCI image config blobs reveals a richer timeline than the layer mtimes alone:

```bash
# Fetch config blobs
oras blob fetch registry.redhat.io/rhai/modelcar-qwen3-5-35b-a3b-fp8-dynamic@sha256:4b223b806e10f43abe5ddcf3b6408afe4bf489db7acdb196311a0021a5ff6c33 \
  -o /tmp/modelcar-analysis/amd64-config.json   # AMD64 config
oras blob fetch registry.redhat.io/rhai/modelcar-qwen3-5-35b-a3b-fp8-dynamic@sha256:082fd27262914984a87fad07b77b7d00be46f6cb8ee473241ab3358f0aee9300 \
  -o /tmp/modelcar-analysis/arm64-config.json   # ARM64 config
```

The config history entries show `olot oci_layers_on_top <filename>` for each model file, with their own timestamps recording when OLOT processed each file. Combined with the TAR layer mtimes (which record when `oras pull` downloaded the files), the full timeline is:

```
2026-03-15T19:08:09.000  [SHARED]  modelcard.md created (mtime in TAR layer)

--- PHASE 1: File download (oras pull) ---
  19:08:21.977 - 19:08:23.119  [AMD64]  oras pull downloads all model files
  19:08:45.948 - 19:08:46.320  [ARM64]  oras pull downloads all model files (~24s later)

--- ~15-20 minute gap (other pipeline steps) ---

--- PHASE 2: OLOT layer creation ---
  19:24:11  [ARM64]  olot starts processing (small files: chat_template, config, gen_config, merges)
  19:28:56  [AMD64]  olot starts processing (same small files)
  19:44:38  [ARM64]  olot finishes (model.safetensors + remaining files + modelcard) ~20min total
  19:58:32  [AMD64]  olot finishes (same) ~30min total
```

Key observations:
- There is a **~15-20 minute gap** between `oras pull` and `olot` invocation on each arch.
  This is where the `touch -t` mtime fix from PR #3358 would execute, if the fix were active.
- ARM64 OLOT **started before** AMD64 (19:24 vs 19:28), despite downloading files later.
  This confirms independent, parallel pipeline runs with no ordering dependency.
- AMD64 OLOT took ~30 minutes vs ARM64's ~20 minutes (different hardware performance).

### Image Config Labels

Neither variant's config contains Konflux-specific build labels:

```
Labels found (both variants):
  build-date:          2025-08-04T22:14:43   (from UBI9 base image, NOT the 2026-03-15 model build)
  com.redhat.component: ubi9-micro-container
  io.buildah.version:  1.41.0-dev
  name:                ubi9/ubi-micro
  vendor:              Red Hat, Inc.

Labels NOT found:
  build.appstudio.openshift.io/*   (Konflux provenance)
  build.appstudio.redhat.com/*     (Konflux provenance)
  io.tekton.*                      (Tekton pipeline metadata)
  Any reference to build-definitions, task versions, or pipeline runs
```

The only labels present are inherited from the **UBI9 micro base image** (built 2025-08-04). OLOT adds model layers on top but does not inject build-system labels.

---

## PR Analysis

### PR #1: [containers/olot#165](https://github.com/containers/olot/pull/165) -- "test: add simulation for Konflux-like behaviour"

- **State:** Merged on 2026-03-18
- **Author:** tarilabs (Matteo Mortari)
- **Included in:** OLOT v0.1.16+

**This PR does NOT add any mtime-fixing feature to OLOT.** It is a documentation and test PR that:

1. **Documents the root cause** in `docs/analysis-165-oras-pull-mtime.md`: when `oras pull` downloads individual file blobs, the pulled files get the **current system timestamp** as their mtime (not the original file's mtime). Since OLOT preserves filesystem mtimes when creating TAR layers, separate pipeline runs produce different layer digests for identical content.

2. **Adds a demonstration test** (`test_tarball_from_file_oras_pull_nondeterministic`) that:
   - Pulls the same OCI artifact twice with a 1-second delay
   - Creates tarballs from each -- **asserts the digests differ** (proving the problem)
   - Applies `touch -t` to normalize mtimes using the `org.opencontainers.image.created` annotation
   - Re-creates tarballs -- **asserts the digests now match** (proving the workaround)

3. **Catalogs upstream ORAS issues**: oras#1464 (deterministic packing), oras-go#712 (non-deterministic digests). Notes that `oras pull` has `--preserve-permissions` but no `--preserve-mtime`.

4. **Explicitly states** the fix lives outside OLOT: _"Did not consider adding a feature to Olot to 'pin the mtime', since the Konflux workaround can fix the mtime of the files to the OCI Artifact created time, which is meaningful."_

**No new CLI flag, API parameter, or runtime code was added.** The test and documentation prove the problem exists and validate the external workaround.

### PR #2: [konflux-ci/build-definitions#3358](https://github.com/konflux-ci/build-definitions/pull/3358) -- "core(modelcar-oci-ta): fix mtime to OCI Artifact manifest"

- **State:** Merged on 2026-03-13
- **Author:** tarilabs (Matteo Mortari)
- **Modifies:** `task/modelcar-oci-ta/0.1/modelcar-oci-ta.yaml`

**This PR implements the actual mtime fix**, but in the **Konflux Tekton Task**, not in OLOT itself. It adds a `touch -t` step after `oras pull` and before `olot` invocation:

```bash
# Extract the OCI artifact's created timestamp
MTIME=$(oras manifest fetch "$MODEL_IMAGE" \
  --registry-config /model-secret/.dockerconfigjson \
  | jq -r '.annotations["org.opencontainers.image.created"]' \
  | tr -d 'TZ:-' \
  | sed 's/\(..\)$/.\1/')

# Fallback to fixed default if annotation is missing
if [ -z "$MTIME" ] || [ "$MTIME" = "null" ]; then
  MTIME="$MTIME_DEFAULT"   # Default: "202601011200.00" (2026-01-01 12:00:00)
fi

# Apply fixed mtime to all model files
find models -exec touch -t "$MTIME" {} +
```

The fix is designed so that when separate per-architecture Konflux pipeline runs download and process the same model files, all files get the same deterministic mtime (derived from the source OCI artifact's `org.opencontainers.image.created` annotation), resulting in identical TAR layers and enabling cross-architecture layer deduplication.

**OLOT version in the task:** `0.1.14` (predates olot#165, but olot#165 added no runtime code anyway).

---

## Why the Fix Did Not Apply to This Image

The image `registry.redhat.io/rhai/modelcar-qwen3-5-35b-a3b-fp8-dynamic:3.0` was built on **2026-03-15**, two days after PR #3358 was merged (2026-03-13). Yet the model file mtimes are clearly **raw `oras pull` download timestamps** (19:08:21-46), not fixed values. The fix was not in effect.

### Evidence: the fix was NOT active

| Expected if fix active | Observed | Match? |
|------------------------|----------|--------|
| All model file mtimes = source artifact's `org.opencontainers.image.created` value | mtimes = 19:08:21-46 (download time, sub-second precision) | **No** |
| Or fallback mtime = `202601011200.00` (2026-01-01T12:00:00) | mtimes from 2026-03-15, not 2026-01-01 | **No** |
| All model TAR layer digests identical across arches | 10 of 11 model layers have different digests | **No** |
| Konflux provenance labels in image config | No `build.appstudio.*` or Tekton labels present | **No** |

### Conclusion: the image was NOT built through the Konflux `modelcar-oci-ta` task

The fix from PR #3358 is specific to the `modelcar-oci-ta` Tekton Task in the konflux-ci/build-definitions repository. The evidence strongly indicates that this particular image was **not built using that Konflux task**:

1. **No Konflux metadata.** The image config contains zero Konflux/AppStudio/Tekton labels or annotations. Konflux builds typically inject extensive provenance metadata (`build.appstudio.openshift.io/*`, `build.appstudio.redhat.com/*`). Their absence suggests a different build system.

2. **Label provenance is exclusively from the UBI9 base image.** All labels (`com.redhat.component`, `build-date`, `io.buildah.version`) originate from the base image built on 2025-08-04, not from the 2026-03-15 model layer build.

3. **The mtimes are raw download timestamps.** If the `touch -t` step had executed, ALL model files would share a single fixed timestamp. Instead, each file has a unique nanosecond-precision mtime corresponding to its individual download moment.

4. **The build likely used `olot` directly** (via CLI or a non-Konflux pipeline) to layer model files onto the UBI9 micro base image. The config history entries confirm `olot oci_layers_on_top` was used, but nothing indicates the Konflux task wrapper was involved.

### What would change if the fix WERE active

If this image were rebuilt using the Konflux `modelcar-oci-ta` task with PR #3358's changes:

- All model file mtimes would be set to the source OCI artifact's `org.opencontainers.image.created` value (or the `202601011200.00` fallback)
- OLOT would create TAR layers with identical mtimes across architectures
- The resulting TAR layer digests would be **identical** for ARM64 and AMD64
- The registry could deduplicate ~23 MB of small model-file layers (config, tokenizer, vocab, etc.)
- The 35.1 GB `model.safetensors` layer would also be deduplicated (it already has identical content)
- Total registry savings: up to ~35.1 GB per additional architecture variant

---

## Tools Used

- **ORAS CLI v1.2.3** -- `oras manifest fetch`, `oras blob fetch`
- **Python 3** -- `tarfile` module for TAR header inspection, `hashlib` for SHA256 verification
- **Raw byte comparison** -- hex-level diff of TAR files to pinpoint exact differing bytes
- **GitHub CLI (`gh`)** -- PR metadata, diffs, reviews, release tags
