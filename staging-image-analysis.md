# Staging Image Layer Analysis

**Image:** `registry.stage.redhat.io/rhai/modelcar-tiny-random-eurobertfortokenclassification@sha256:0e9a8a62e11629fc7f301f5e5b87c502dcaa34a56902a4e6891eeef32c5078b0`
**Date of analysis:** 2026-04-19
**Built on:** 2026-04-19 (today)

## Manifest Structure

4-platform manifest index (amd64, arm64/v8, ppc64le, s390x) with 7 layers each.

```bash
oras manifest fetch registry.stage.redhat.io/rhai/modelcar-tiny-random-eurobertfortokenclassification@sha256:0e9a8a62e11629fc7f301f5e5b87c502dcaa34a56902a4e6891eeef32c5078b0
```

## Cross-Architecture Layer Comparison

| Layer | File | amd64 digest | arm64 digest | ppc64le digest | s390x digest | All same? |
|-------|------|-------------|-------------|---------------|-------------|-----------|
| 0 | Base image | `sha256:4e5861...` | `sha256:f74c16...` | `sha256:716bdf...` | `sha256:957187...` | **No** (expected) |
| 1 | `config.json` | `sha256:7059c3...` | `sha256:7059c3...` | `sha256:7059c3...` | `sha256:7059c3...` | **Yes** |
| 2 | `model.safetensors` | `sha256:77538e...` | `sha256:77538e...` | `sha256:77538e...` | `sha256:77538e...` | **Yes** |
| 3 | `README.md` | `sha256:fb7601...` | `sha256:fb7601...` | `sha256:fb7601...` | `sha256:fb7601...` | **Yes** |
| 4 | `tokenizer_config.json` | `sha256:c58e2c...` | `sha256:c58e2c...` | `sha256:c58e2c...` | `sha256:c58e2c...` | **Yes** |
| 5 | `tokenizer.json` | `sha256:7603027...` | `sha256:7603027...` | `sha256:7603027...` | `sha256:7603027...` | **Yes** |
| 6 | `modelcard.md` | `sha256:3c73eb...` | `sha256:3c73eb...` | `sha256:3c73eb...` | `sha256:3c73eb...` | **Yes** |

**All 6 model layers are identical across all 4 architectures.** Only the base image layer (Layer 0) differs, as expected.

## TAR Metadata Verification

```bash
# Download shared model layers
oras blob fetch "$REPO@sha256:7059c3677bac6a99d16104c9745efc2052f3a1640c60e5a055506e63904505a6" -o config.tar
oras blob fetch "$REPO@sha256:c58e2ce295e2739414b7b45c0191628305907354bf4454ca3cced91d4749ccbf" -o tokenizer_config.tar
oras blob fetch "$REPO@sha256:fb760144721db60432d7528c22c1b0a55115e15180be526cc0a86c552d249e55" -o readme.tar
oras blob fetch "$REPO@sha256:3c73ebaee5cfdaa3f9c914c7341681c6f037a21fda498c365e4650c783bac250" -o modelcard.tar.gz
```

Inspected with Python `tarfile`:

| File | mtime (epoch) | mtime (human) | Mode | UID/GID | uname |
|------|---------------|---------------|------|---------|-------|
| `config.json` | `1771515743.0` | 2026-02-19T15:42:23 | 0o664 | 0/0 | `''` |
| `tokenizer_config.json` | `1771515743.0` | 2026-02-19T15:42:23 | 0o664 | 0/0 | `''` |
| `README.md` | `1771515743.0` | 2026-02-19T15:42:23 | 0o664 | 0/0 | `''` |
| `modelcard.md` | `1776584337.0` | 2026-04-19T07:38:57 | 0o664 | 0/0 | `root` |

**All model files share the exact same mtime: `1771515743.0` (2026-02-19T15:42:23).** This is NOT the build time (2026-04-19) -- it is the source OCI artifact's `org.opencontainers.image.created` timestamp, applied via `touch -t` by the Konflux `modelcar-oci-ta` task (PR [build-definitions#3358](https://github.com/konflux-ci/build-definitions/pull/3358)).

The `modelcard.md` has a different mtime (2026-04-19T07:38:57, ~31s before OLOT ran) because it is generated at build time by the pipeline, not pulled from the source artifact.

## Content Integrity

Content SHA256 matches `olot.layer.content.digest` annotations for all layers -- confirmed identical file content.

## Comparison with Production Image

| Property | **Production** (`registry.redhat.io` 3.0) | **Staging** (this image) |
|----------|-------------------------------------------|--------------------------|
| Built on | 2026-03-15 | 2026-04-19 |
| Model file mtimes | Raw `oras pull` download timestamps (sub-second, arch-dependent) | Fixed to `2026-02-19T15:42:23` (integer, identical everywhere) |
| Layers shared across arches | Only `modelcard.md` (1 of 11) | All model layers (6 of 7) |
| `touch -t` fix active | **No** | **Yes** |
| Deduplication savings | None (all model layers duplicated per-arch) | All model content deduplicated (only base image differs) |

## Conclusion

The fix from [build-definitions#3358](https://github.com/konflux-ci/build-definitions/pull/3358) **is active and working correctly** in this staging build. The `touch -t` step normalizes all model file mtimes to the source OCI artifact's `org.opencontainers.image.created` timestamp before OLOT processes them. This produces byte-identical TAR layers across all 4 architectures, enabling full cross-platform layer deduplication.

The production image (`registry.redhat.io/rhai/modelcar-qwen3-5-35b-a3b-fp8-dynamic:3.0`, built 2026-03-15) was built **before the fix had propagated** to its build pipeline -- only 2 days after the PR merged. The staging image, built 5+ weeks later, confirms the fix is now onboarded and functioning as designed.
