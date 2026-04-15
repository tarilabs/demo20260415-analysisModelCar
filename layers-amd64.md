# Layers - AMD64 (x86_64) Variant

**Image:** `registry.redhat.io/rhai/modelcar-qwen3-5-35b-a3b-fp8-dynamic:3.0`
**Platform:** `linux/amd64`
**Manifest Digest:** `sha256:0e32c9f9b996bd339552d10ee2da1a1afa9ad41726102d93419fd97870b28b77`
**Schema Version:** 2
**Media Type:** `application/vnd.oci.image.manifest.v1+json`

## Config

| Field | Value |
|-------|-------|
| Digest | `sha256:4b223b806e10f43abe5ddcf3b6408afe4bf489db7acdb196311a0021a5ff6c33` |
| Size | 6,066 bytes |
| Media Type | `application/vnd.oci.image.config.v1+json` |

## Layers (13 total)

### Layer 1 - Base Layer

| Field | Value |
|-------|-------|
| Digest | `sha256:4e5861c970ccfcb3472d3a98e0a6ac292281a42a5a90a7d45e1fa246cd38d2bf` |
| Size | 7,241,176 bytes (~6.9 MB) |
| Media Type | `application/vnd.oci.image.layer.v1.tar+gzip` |

No annotations.

### Layer 2 - chat_template.jinja

| Field | Value |
|-------|-------|
| Digest | `sha256:49e690345fa6f811a1064b41f79fa4fca7b83844b6ecf1350750e822151847f3` |
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
| Digest | `sha256:d7aa49b5d4a29de95e581f9a7094daf5fe4186a0759becd90adf9c9a29599381` |
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
| Digest | `sha256:ea7d8daeb8d9fe070705b0f29e5ea3475fd6c2db995c5b999a379a0387c2ceba` |
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
| Digest | `sha256:21597f70af2a7d3fc32f81587b2a57c5ddf7d73d82480a0021b44a06d55a66fa` |
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
| Digest | `sha256:f926e2c5e17da2ed2144a6459604641ed56cdb085329eb55812328ed3340d40f` |
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
| Digest | `sha256:6c028b9b40d874db0a5b99e14c49e4d7e483b8dd2067ba455c4f3e7bec9d6439` |
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
| Digest | `sha256:2e2c10620dc3080e88f6c001c37a8a5b5b2e3bd5962f0aa066966060b321ac13` |
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
| Digest | `sha256:abb5d0be9f3091ac50d4af4e45fcfbdb50e6f1625522da791a79bd1e81ae5c7a` |
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
| Digest | `sha256:2dbb4788596b43345e51ec53648285c24ecbcad50eabda0e5865d6c7d8216eca` |
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
| Digest | `sha256:88f5fc43a918749dca561fd69908b96961c92dd278f5320aed218ac924318346` |
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
| Digest | `sha256:088570ae971fb22b2a5ced451d18ade28531b48bdefc877f0457641b93dbb286` |
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
