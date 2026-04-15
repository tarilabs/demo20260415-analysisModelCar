# Layers - ARM64 (aarch64) Variant

**Image:** `registry.redhat.io/rhai/modelcar-qwen3-5-35b-a3b-fp8-dynamic:3.0`
**Platform:** `linux/arm64/v8`
**Manifest Digest:** `sha256:ec31fc9f4499fac62fd98f321320ca8ad62e4d7c24082703194c9c20e2732ddd`
**Schema Version:** 2
**Media Type:** `application/vnd.oci.image.manifest.v1+json`

## Config

| Field | Value |
|-------|-------|
| Digest | `sha256:082fd27262914984a87fad07b77b7d00be46f6cb8ee473241ab3358f0aee9300` |
| Size | 6,082 bytes |
| Media Type | `application/vnd.oci.image.config.v1+json` |

## Layers (13 total)

### Layer 1 - Base Layer

| Field | Value |
|-------|-------|
| Digest | `sha256:f74c16b8beabd92ba8d26a94b4eb0ed9f9ea14494e6112d6d677b08f5a69567f` |
| Size | 6,618,646 bytes (~6.3 MB) |
| Media Type | `application/vnd.oci.image.layer.v1.tar+gzip` |

No annotations.

### Layer 2 - chat_template.jinja

| Field | Value |
|-------|-------|
| Digest | `sha256:937db2ada81431c0ffeea04d05f2e493415b307b74c3e2281fdeea5be0a85d48` |
| Size | 20,480 bytes (~20 KB) |
| Media Type | `application/vnd.oci.image.layer.v1.tar` |

**Annotations:**

| Key | Value |
|-----|-------|
| `org.opencontainers.image.title` | `chat_template.jinja` |
| `olot.layer.content.digest` | `sha256:a4aee8afcf2e0711942cf848899be66016f8d14a889ff9ede07bca099c28f715` |
| `olot.layer.content.type` | `file` |
| `olot.layer.content.inlayerpath` | `/models/chat_template.jinja` |
| `olot.layer.content.name` | `chat_template.jinja` |

### Layer 3 - config.json

| Field | Value |
|-------|-------|
| Digest | `sha256:3658974d0d38f268adfc8d9ed4b632d2cef704de5c59bd52b6642bb31e246c65` |
| Size | 30,720 bytes (~30 KB) |
| Media Type | `application/vnd.oci.image.layer.v1.tar` |

**Annotations:**

| Key | Value |
|-----|-------|
| `org.opencontainers.image.title` | `config.json` |
| `olot.layer.content.digest` | `sha256:dba2fc8960ae3d03922c8ecd97c477ddc2560f65b867ea70e7a683df8efe568a` |
| `olot.layer.content.type` | `file` |
| `olot.layer.content.inlayerpath` | `/models/config.json` |
| `olot.layer.content.name` | `config.json` |

### Layer 4 - generation_config.json

| Field | Value |
|-------|-------|
| Digest | `sha256:f644d17ff6bdcaef0bc4e677bf2577437def7f2a6e53b59ba39214b09d372498` |
| Size | 10,240 bytes (~10 KB) |
| Media Type | `application/vnd.oci.image.layer.v1.tar` |

**Annotations:**

| Key | Value |
|-----|-------|
| `org.opencontainers.image.title` | `generation_config.json` |
| `olot.layer.content.digest` | `sha256:4f25002776b741773666203dcea8f54619f177ace3ae483d311102092a4658e0` |
| `olot.layer.content.type` | `file` |
| `olot.layer.content.inlayerpath` | `/models/generation_config.json` |
| `olot.layer.content.name` | `generation_config.json` |

### Layer 5 - merges.txt

| Field | Value |
|-------|-------|
| Digest | `sha256:8a0e9e3fd3c7e0251750be6ebaf4f451578f9d18cc8cb76b9e2954a0dc6aa5c3` |
| Size | 3,358,720 bytes (~3.2 MB) |
| Media Type | `application/vnd.oci.image.layer.v1.tar` |

**Annotations:**

| Key | Value |
|-----|-------|
| `org.opencontainers.image.title` | `merges.txt` |
| `olot.layer.content.digest` | `sha256:a9d356d7bdf1ef4949e3e748e95b8e10ad9d4e2e838eddc38a0a7b6b94d1db8d` |
| `olot.layer.content.type` | `file` |
| `olot.layer.content.inlayerpath` | `/models/merges.txt` |
| `olot.layer.content.name` | `merges.txt` |

### Layer 6 - model.safetensors

| Field | Value |
|-------|-------|
| Digest | `sha256:e0d9597a410e767d91cf42d5b7fc7b33e5e79666b2fd72f5f1d4b9a7f68b1004` |
| Size | 37,676,011,520 bytes (~35.1 GB) |
| Media Type | `application/vnd.oci.image.layer.v1.tar` |

**Annotations:**

| Key | Value |
|-----|-------|
| `org.opencontainers.image.title` | `model.safetensors` |
| `olot.layer.content.digest` | `sha256:755ecad64384831d0041ce5024118e8977c7b22c45d78b47d78bbb84cfbdcb2a` |
| `olot.layer.content.type` | `file` |
| `olot.layer.content.inlayerpath` | `/models/model.safetensors` |
| `olot.layer.content.name` | `model.safetensors` |

### Layer 7 - preprocessor_config.json

| Field | Value |
|-------|-------|
| Digest | `sha256:5f6c138931a0be213fe7b262a6f1a825bb5c9647c7993943966b4ab0ded1a2c4` |
| Size | 10,240 bytes (~10 KB) |
| Media Type | `application/vnd.oci.image.layer.v1.tar` |

**Annotations:**

| Key | Value |
|-----|-------|
| `org.opencontainers.image.title` | `preprocessor_config.json` |
| `olot.layer.content.digest` | `sha256:27225450ac9c6529872ee1924fcb0962ff5634834f817040f444118116f4e516` |
| `olot.layer.content.type` | `file` |
| `olot.layer.content.inlayerpath` | `/models/preprocessor_config.json` |
| `olot.layer.content.name` | `preprocessor_config.json` |

### Layer 8 - recipe.yaml

| Field | Value |
|-------|-------|
| Digest | `sha256:d46cef14a0fad6b6b0384dd0c37440fd96224fdf23cb37e3a4b6675d904e80c6` |
| Size | 10,240 bytes (~10 KB) |
| Media Type | `application/vnd.oci.image.layer.v1.tar` |

**Annotations:**

| Key | Value |
|-----|-------|
| `org.opencontainers.image.title` | `recipe.yaml` |
| `olot.layer.content.digest` | `sha256:7a15656336d245b85904013a55a1f3df190302a0141c161682a4b0727e56435c` |
| `olot.layer.content.type` | `file` |
| `olot.layer.content.inlayerpath` | `/models/recipe.yaml` |
| `olot.layer.content.name` | `recipe.yaml` |

### Layer 9 - tokenizer_config.json

| Field | Value |
|-------|-------|
| Digest | `sha256:3d2bcefa8c4af1d7712f1fd837fd583c1ae72c74806aea439c03176a2873bf01` |
| Size | 20,480 bytes (~20 KB) |
| Media Type | `application/vnd.oci.image.layer.v1.tar` |

**Annotations:**

| Key | Value |
|-----|-------|
| `org.opencontainers.image.title` | `tokenizer_config.json` |
| `olot.layer.content.digest` | `sha256:316230d6a809701f4db5ea8f8fc862bc3a6f3229c937c174e674ff3ca0a64ac8` |
| `olot.layer.content.type` | `file` |
| `olot.layer.content.inlayerpath` | `/models/tokenizer_config.json` |
| `olot.layer.content.name` | `tokenizer_config.json` |

### Layer 10 - tokenizer.json

| Field | Value |
|-------|-------|
| Digest | `sha256:acc73149409f198e37a572a0e68ea9dc1cfacc1afde5c957af692239a1a90972` |
| Size | 12,820,480 bytes (~12.2 MB) |
| Media Type | `application/vnd.oci.image.layer.v1.tar` |

**Annotations:**

| Key | Value |
|-----|-------|
| `org.opencontainers.image.title` | `tokenizer.json` |
| `olot.layer.content.digest` | `sha256:5f9e4d4901a92b997e463c1f46055088b6cca5ca61a6522d1b9f64c4bb81cb42` |
| `olot.layer.content.type` | `file` |
| `olot.layer.content.inlayerpath` | `/models/tokenizer.json` |
| `olot.layer.content.name` | `tokenizer.json` |

### Layer 11 - video_preprocessor_config.json

| Field | Value |
|-------|-------|
| Digest | `sha256:24e330862bdb57aa11e8e7355160a220cf11c5fd7164bdef4683b0b29c124dd1` |
| Size | 10,240 bytes (~10 KB) |
| Media Type | `application/vnd.oci.image.layer.v1.tar` |

**Annotations:**

| Key | Value |
|-----|-------|
| `org.opencontainers.image.title` | `video_preprocessor_config.json` |
| `olot.layer.content.digest` | `sha256:7768af27c1fafa9cc9011c1dc20067e03f8915e03b63504550e11d5066986d13` |
| `olot.layer.content.type` | `file` |
| `olot.layer.content.inlayerpath` | `/models/video_preprocessor_config.json` |
| `olot.layer.content.name` | `video_preprocessor_config.json` |

### Layer 12 - vocab.json

| Field | Value |
|-------|-------|
| Digest | `sha256:e8caa8b1bb1c5ff2e7830a5d98717657e8c97e7d366d5e167624069e95efedd1` |
| Size | 6,727,680 bytes (~6.4 MB) |
| Media Type | `application/vnd.oci.image.layer.v1.tar` |

**Annotations:**

| Key | Value |
|-----|-------|
| `org.opencontainers.image.title` | `vocab.json` |
| `olot.layer.content.digest` | `sha256:ce99b4cb2983d118806ce0a8b777a35b093e2000a503ebde25853284c9dfa003` |
| `olot.layer.content.type` | `file` |
| `olot.layer.content.inlayerpath` | `/models/vocab.json` |
| `olot.layer.content.name` | `vocab.json` |

### Layer 13 - modelcard.md

| Field | Value |
|-------|-------|
| Digest | `sha256:19160baa5465938faa871b0954d08a2c299acd6a3aff03fd045856f85a325df9` |
| Size | 225 bytes |
| Media Type | `application/vnd.oci.image.layer.v1.tar+gzip` |

**Annotations:**

| Key | Value |
|-----|-------|
| `org.opencontainers.image.title` | `modelcard.md` |
| `io.opendatahub.modelcar.layer.type` | `modelcard` |
| `olot.layer.content.digest` | `sha256:15bef5797954ec4f49e2d6ec419fe7813820ef2a4a35bdc33e6d28b63989508a` |
| `olot.layer.content.type` | `file` |
| `olot.layer.content.inlayerpath` | `/models/modelcard.md` |
| `olot.layer.content.name` | `modelcard.md` |

## Manifest-Level Annotations

| Key | Value |
|-----|-------|
| `org.opencontainers.image.base.digest` | _(empty)_ |
| `org.opencontainers.image.base.name` | _(empty)_ |
| `io.opendatahub.author` | `olot` |
| `io.opendatahub.layers.modelcard` | `sha256:19160baa5465938faa871b0954d08a2c299acd6a3aff03fd045856f85a325df9` |
