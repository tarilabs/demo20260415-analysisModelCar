# Production Batch Layer Deduplication Analysis

**Date of analysis:** 2026-06-18
**Images analyzed:** 8 production modelcar images from `registry.redhat.io/rhai/`
**Tool:** [`inspect_modelcar_layers.py`](inspect_modelcar_layers.py)

## Summary

All 8 images **PASS** — the mtime normalization fix ([build-definitions#3358](https://github.com/konflux-ci/build-definitions/pull/3358)) is active and working correctly across all production modelcar images tested. Every model layer is shared across all 4 architectures (amd64, arm64/v8, ppc64le, s390x).

| # | Image | Platforms | Layers | Shared | mtime | Verdict |
|---|-------|-----------|--------|--------|-------|---------|
| 1 | `modelcar-redhatai-gemma-4-31b-it-nvfp4:3.0` | 4 | 11 | 10/11 | `1781613335` (2026-06-16T12:35:35) | **PASS** |
| 2 | `modelcar-redhatai-gemma-4-31b-it-fp8-block:3.0` | 4 | 12 | 11/12 | `1781613250` (2026-06-16T12:34:10) | **PASS** |
| 3 | `modelcar-redhatai-gemma-4-26b-a4b-it-nvfp4:3.0` | 4 | 12 | 11/12 | `1781613290` (2026-06-16T12:34:50) | **PASS** |
| 4 | `modelcar-redhatai-gemma-4-31b-it-fp8-dynamic:3.0` | 4 | 12 | 11/12 | `1781613262` (2026-06-16T12:34:22) | **PASS** |
| 5 | `modelcar-redhatai-qwen3-6-35b-a3b-nvfp4:3.0` | 4 | 14 | 13/14 | `1781613262` (2026-06-16T12:34:22) | **PASS** |
| 6 | `modelcar-redhatai-gemma-4-26b-a4b-it-fp8-dynamic:3.0` | 4 | 11 | 10/11 | `1781613302` (2026-06-16T12:35:02) | **PASS** |
| 7 | `modelcar-redhatai-qwen3-6-35b-a3b-fp8:3.0` | 4 | 57 | 56/57 | `1781613281` (2026-06-16T12:34:41) | **PASS** |
| 8 | `modelcar-redhatai-qwen3-6-35b-a3b-fp8-dynamic:3.0` | 4 | 13 | 12/13 | `1781613296` (2026-06-16T12:34:56) | **PASS** |

In every case, the only non-shared layer is the base container image (layer-0), which is expected to differ per architecture.

## Storage Impact

| # | Image | Per-arch size | Without dedup (4 arches) | With dedup | Savings |
|---|-------|--------------|--------------------------|------------|---------|
| 1 | gemma-4-31b-it-nvfp4 | 23.3 GB | 93.2 GB | 23.3 GB | **69.9 GB** (4.0x) |
| 2 | gemma-4-31b-it-fp8-block | 33.3 GB | 133.2 GB | 33.3 GB | **99.9 GB** (4.0x) |
| 3 | gemma-4-26b-a4b-it-nvfp4 | 16.5 GB | 65.9 GB | 16.5 GB | **49.4 GB** (4.0x) |
| 4 | gemma-4-31b-it-fp8-dynamic | 33.3 GB | 133.2 GB | 33.3 GB | **99.9 GB** (4.0x) |
| 5 | qwen3-6-35b-a3b-nvfp4 | 25.1 GB | 100.3 GB | 25.1 GB | **75.2 GB** (4.0x) |
| 6 | gemma-4-26b-a4b-it-fp8-dynamic | 28.7 GB | 114.7 GB | 28.7 GB | **86.0 GB** (4.0x) |
| 7 | qwen3-6-35b-a3b-fp8 | 37.5 GB | 150.0 GB | 37.5 GB | **112.5 GB** (4.0x) |
| 8 | qwen3-6-35b-a3b-fp8-dynamic | 39.4 GB | 157.6 GB | 39.4 GB | **118.2 GB** (4.0x) |
| | **Total** | **237.1 GB** | **948.1 GB** | **237.1 GB** | **711.0 GB** (4.0x) |

**Total registry savings across all 8 images: ~711 GB (75.0% reduction)**

---

## Per-Image Details

### 1. gemma-4-31b-it-nvfp4:3.0

```
================================================================================
CROSS-ARCHITECTURE LAYER DEDUPLICATION REPORT
================================================================================

Image: registry.redhat.io/rhai/modelcar-redhatai-gemma-4-31b-it-nvfp4:3.0
Platforms: amd64, arm64/v8, ppc64le, s390x (4 total)
Layers per platform: 11

Platform         Manifest Digest
-------------------------------------------------------------------------------------------
amd64            sha256:89bd852f0f9da9655608afb298d957856b2b76b7ff6b70d486b6ec6ac136820c
arm64/v8         sha256:faa48935243083350b28f963d017f368d2defa42cec0dbcb53ecea0733980095
ppc64le          sha256:304caf25f9e44b725943e7d841044db1e0ba87b140bbc37ddf1138bc3542bde4
s390x            sha256:84faa7dfa1d10baca25999a0d35668471a3fec90a25dab40a975471a0dd3a653

Layer  Title                                                   Size Shared?    Digest
------------------------------------------------------------------------------------------------------------------------------------------------------
0      layer-0                                               7.2 MB NO        sha256:4e5861c970ccfcb3472d3a98e0a6ac292281a42a5a90a7d45e1fa246cd38d2bf (amd64) (expected)
1      chat_template.jinja                                  20.5 KB YES       sha256:72a45c3ef4510b777e96bfb22c5ae0fc0677bc99d39a44f366f75d095333eb36
2      config.json                                          30.7 KB YES       sha256:f484e4303ec535f137d69f065738b8956da004148fdc9b45d701aec47293fc80
3      generation_config.json                               10.2 KB YES       sha256:cf0b913068f70269c89188cdbecda7877d5c0e7ecc7ddcadae821c1f89754cb1
4      model.safetensors                                    23.3 GB YES       sha256:a4c856fb0e00fd03f16954603f15ecffc47a4935a1ab37f6894eb20f49a2025a
5      processor_config.json                                10.2 KB YES       sha256:ff49c0a7640254dfd1fe2c9054e9d4b6482b04e21ad6be7f001e10087ccaf681
6      README.md                                            20.5 KB YES       sha256:589d84715c440ff4fc48c64a0e72088aa02a254beaf18fe81e16d5ca0bb2c37e
7      recipe.yaml                                          10.2 KB YES       sha256:0cdd9d1926e1878fac50bb0c0f2a3f4e1c64f9310f67915d15a97d8704fbb24d
8      tokenizer_config.json                                10.2 KB YES       sha256:f67f1a03d95c0b52d6ab70f092d90d4504ae5bacfba6586fafbe6355cc126fb4
9      tokenizer.json                                       32.2 MB YES       sha256:033e0999588e35df2a80549777062a9e61dfa928d4a60c4551e755bcdca601e5
10     modelcard.md                                          3.2 KB YES       sha256:0877d9f48463fbe46adb8e6da0f85c4cacf066b9bc73a3293f544afa202c0eb8

Shared layers: 10/11
  Model layers shared (OLOT): 10
  Base layers differing (expected): 1

MTIME: 1781613335.0 (2026-06-16T12:35:35) — PASS
SAVINGS: 69.9 GB — 4.0x more storage efficient (75.0% reduction)
VERDICT: PASS
```

### 2. gemma-4-31b-it-fp8-block:3.0

```
================================================================================
CROSS-ARCHITECTURE LAYER DEDUPLICATION REPORT
================================================================================

Image: registry.redhat.io/rhai/modelcar-redhatai-gemma-4-31b-it-fp8-block:3.0
Platforms: amd64, arm64/v8, ppc64le, s390x (4 total)
Layers per platform: 12

Platform         Manifest Digest
-------------------------------------------------------------------------------------------
amd64            sha256:1f77ede9c05ae7eeea753632ee832a76093740f5562254625ca556f5f2135e08
arm64/v8         sha256:87ddf049d24caf6fce43af50963d16746fbbd1b9c7d233996ea805d50594367d
ppc64le          sha256:7b33dadcad102bee82157912eb53752188825d1fd436f0e57eaee537cd9caa96
s390x            sha256:c1a217d6a7960cd05b3ba85a079b02574cb7c3310cdef2365560b3f1b53810bb

Layer  Title                                                   Size Shared?    Digest
------------------------------------------------------------------------------------------------------------------------------------------------------
0      layer-0                                               7.2 MB NO        sha256:4e5861c970ccfcb3472d3a98e0a6ac292281a42a5a90a7d45e1fa246cd38d2bf (amd64) (expected)
1      chat_template.jinja                                  20.5 KB YES       sha256:1a9df656adf92d8b26e7b9c0dac0c3cc5d07f7dfce3352af375280b38f7c41cc
2      config.json                                          10.2 KB YES       sha256:174c762eee6dca688f1f25666f1d945b2785feb333bcbba38e51fd3519fa1ce8
3      generation_config.json                               10.2 KB YES       sha256:f293b6cc304cccfb1c30b58561212d42789841cbbc0e3314f791b364511db6cf
4      model-00001-of-00002.safetensors                     26.9 GB YES       sha256:c897f89e3d993c840cd26a29eb539f6e0079200c6aac553eb5e8300222c113b5
5      model-00002-of-00002.safetensors                      6.4 GB YES       sha256:3d9dacb7651feaee52446cd285b0c6005c311538e47fd81ff0913097da37dea2
6      model.safetensors.index.json                        174.1 KB YES       sha256:cb558722404bc952563fae7e0cbeb03ff0e1f804ca298e0af93fd59b8b2b20e5
7      processor_config.json                                10.2 KB YES       sha256:c1bbc3709af856bde226a21f713755be5102bb362b2e6acccc2df19138b66875
8      README.md                                            20.5 KB YES       sha256:b0ebf9407accbf5f12f9df9f5bd1633adc43ef387af9a3d04f2d7087619cadac
9      tokenizer_config.json                                10.2 KB YES       sha256:9fb7677fd73246405c55d79ed5524f0b40c59099019eb075c9cd1c6049ae4ff3
10     tokenizer.json                                       32.2 MB YES       sha256:73e29b0946da5c9b6a66da8c9e782b88977439654208fc6f9d701be853e0c692
11     modelcard.md                                          2.8 KB YES       sha256:1b57fe75dcd9e8fee56ffee8ef46547c82d964ac892d85210f0e86de9c4509cb

Shared layers: 11/12
  Model layers shared (OLOT): 11
  Base layers differing (expected): 1

MTIME: 1781613250.0 (2026-06-16T12:34:10) — PASS
SAVINGS: 99.9 GB — 4.0x more storage efficient (75.0% reduction)
VERDICT: PASS
```

### 3. gemma-4-26b-a4b-it-nvfp4:3.0

```
================================================================================
CROSS-ARCHITECTURE LAYER DEDUPLICATION REPORT
================================================================================

Image: registry.redhat.io/rhai/modelcar-redhatai-gemma-4-26b-a4b-it-nvfp4:3.0
Platforms: amd64, arm64/v8, ppc64le, s390x (4 total)
Layers per platform: 12

Platform         Manifest Digest
-------------------------------------------------------------------------------------------
amd64            sha256:14130b36ea9947a8a38d7d702a4ee48054d7feab00bb19f0c1380e39d111231e
arm64/v8         sha256:ae6c54a5ef076b6e43b786ce40933e22f7f6dbfffa0eb580c05ea0a52d7e3618
ppc64le          sha256:5fe01a6cc26da2b674a1e39e1d19c6a1f217e5c15d44826b5bddf111ba43a85b
s390x            sha256:3d49b6b397458f87c82c6a78bc6d304e8ad4b2f20802a68a812310c421489475

Layer  Title                                                   Size Shared?    Digest
------------------------------------------------------------------------------------------------------------------------------------------------------
0      layer-0                                               7.2 MB NO        sha256:4e5861c970ccfcb3472d3a98e0a6ac292281a42a5a90a7d45e1fa246cd38d2bf (amd64) (expected)
1      chat_template.jinja                                  20.5 KB YES       sha256:4fd1bff6ba76fdeefd21b0586a592407eb2c6ca87c1cd02f772ac402e00285f6
2      config.json                                          30.7 KB YES       sha256:0ed873a07a8301fa5f7cef6d29290f16090070a1277993a787ead07b5f37ee92
3      generation_config.json                               10.2 KB YES       sha256:f76790276270b803af2c55ef906660fa18dcd64f0f5e469f5263d37253721b5c
4      model.safetensors                                    16.4 GB YES       sha256:9e968a21651f0b8935016b82be4df008ac6ac3b6e83d308a898bce28568713fd
5      model.safetensors.index.json                          4.6 MB YES       sha256:d201827dc3e757eebb7c99ab1cb30e66ca37b82e1ee06c880772502d6952d35b
6      processor_config.json                                10.2 KB YES       sha256:6a9eff3a83861d4992f84a0c18dc53619a786641d630f00109202233f7d708ba
7      README.md                                            10.2 KB YES       sha256:1dc0f9aba11e3d6d61acc707004e33990db565247240bec3d1b5cb33b4f27aea
8      recipe.yaml                                          10.2 KB YES       sha256:75bfa3f5274a25fe18a45b12672e42886f5dac8576c02106178001664479e247
9      tokenizer_config.json                                10.2 KB YES       sha256:bd0df817f8075fd4e4cbee9ed05b0ca0fb7aee999f45213aa7cd2b10f12ccdf0
10     tokenizer.json                                       32.2 MB YES       sha256:17423c032d987956e28e9be367bf43055a9e8ddf53b29cd8b3ee4fb7f6c2170f
11     modelcard.md                                           960 B YES       sha256:ab3a6be9916102432406f5bb43ea0802fb95286af0f692521bd38a616029bfd9

Shared layers: 11/12
  Model layers shared (OLOT): 11
  Base layers differing (expected): 1

MTIME: 1781613290.0 (2026-06-16T12:34:50) — PASS
SAVINGS: 49.4 GB — 4.0x more storage efficient (75.0% reduction)
VERDICT: PASS
```

### 4. gemma-4-31b-it-fp8-dynamic:3.0

```
================================================================================
CROSS-ARCHITECTURE LAYER DEDUPLICATION REPORT
================================================================================

Image: registry.redhat.io/rhai/modelcar-redhatai-gemma-4-31b-it-fp8-dynamic:3.0
Platforms: amd64, arm64/v8, ppc64le, s390x (4 total)
Layers per platform: 12

Platform         Manifest Digest
-------------------------------------------------------------------------------------------
amd64            sha256:bdc7bdede3b84556bfb9cd73e5ea2cfa6aebfbd2c6a529c9caa5aaa207afb1c9
arm64/v8         sha256:fae34632dd12d8e23432b15b153ad1585c77cacee8ec86db7b91f1db6c416d3d
ppc64le          sha256:2a9d75fd807702b8cdbbbd5dba905e397350d11f8e2536d9446477fc1d9ff1d7
s390x            sha256:1cb5b47ef6ce6334b0fca8c18dd777e4185a24613fbe535fcd3b3806a3286eb2

Layer  Title                                                   Size Shared?    Digest
------------------------------------------------------------------------------------------------------------------------------------------------------
0      layer-0                                               7.2 MB NO        sha256:4e5861c970ccfcb3472d3a98e0a6ac292281a42a5a90a7d45e1fa246cd38d2bf (amd64) (expected)
1      chat_template.jinja                                  20.5 KB YES       sha256:d3bc32e62b99bda69b62c452e6c3b2360482c6e444f428713a464ce179f71160
2      config.json                                          10.2 KB YES       sha256:c1fd7e41a8a368f897ec361616211508a1bf94c065c3278194bb59212b3800e5
3      generation_config.json                               10.2 KB YES       sha256:93f729c9b5e12d380eba044a75e56e5db8dda7b0d8ebfb36a4583531efc009ba
4      model-00001-of-00002.safetensors                     26.9 GB YES       sha256:1523a06541dc4d15c4f45b1251285a3a0e889c8e36cd9adba13f213fb26d6fa0
5      model-00002-of-00002.safetensors                      6.4 GB YES       sha256:b4360494ad79911fc1815320def203155131ae4ae651f01edfc5e8fb967856c5
6      model.safetensors.index.json                        122.9 KB YES       sha256:4d95234a0d276279ed32efe6b35bbd9496d165e9786e45094661e025f09bf068
7      processor_config.json                                10.2 KB YES       sha256:30fd0db5f09231b0ce3421f7680abbf64ab7f7efca86286323abd69de9e4f2de
8      README.md                                            10.2 KB YES       sha256:ae0797c310ebf31d304fff3a6469d7ab85954df6c41256a4fe30b21209448d42
9      tokenizer_config.json                                10.2 KB YES       sha256:df92889e1c5f10bf70273ea33eaa965dbeff95903a5b7f03bcfa9d8211cd20f0
10     tokenizer.json                                       32.2 MB YES       sha256:0a1e0864f0fc4c8fe5061fab46c80dc333f16f4e75365316ebd11608f88660c5
11     modelcard.md                                          1.3 KB YES       sha256:0b7f12f91200020a35e12839bea6f710c13a74d7cbbc127849f9f3893aea42f6

Shared layers: 11/12
  Model layers shared (OLOT): 11
  Base layers differing (expected): 1

MTIME: 1781613262.0 (2026-06-16T12:34:22) — PASS
SAVINGS: 99.9 GB — 4.0x more storage efficient (75.0% reduction)
VERDICT: PASS
```

### 5. qwen3-6-35b-a3b-nvfp4:3.0

```
================================================================================
CROSS-ARCHITECTURE LAYER DEDUPLICATION REPORT
================================================================================

Image: registry.redhat.io/rhai/modelcar-redhatai-qwen3-6-35b-a3b-nvfp4:3.0
Platforms: amd64, arm64/v8, ppc64le, s390x (4 total)
Layers per platform: 14

Platform         Manifest Digest
-------------------------------------------------------------------------------------------
amd64            sha256:3f420afa3af445426f8263162176401f2d90e439ee14522f6be087fec84cf16a
arm64/v8         sha256:bf8116ef80c1f580b4bc869af3393377737651771bfdaa101f65d285d5144c9f
ppc64le          sha256:ed65b6e2917dcf22b95f28e10cfbf26ad02e54ab3e8ac1ecea5e5453bd78289f
s390x            sha256:3ade5180744ff3fe46878d8a41378e049348e3198003a0acb96738d993234539

Layer  Title                                                   Size Shared?    Digest
------------------------------------------------------------------------------------------------------------------------------------------------------
0      layer-0                                               7.2 MB NO        sha256:4e5861c970ccfcb3472d3a98e0a6ac292281a42a5a90a7d45e1fa246cd38d2bf (amd64) (expected)
1      chat_template.jinja                                  20.5 KB YES       sha256:f8680f0cffb175ccda64ec98a2c9a1356d43aa4a059783b1ac9919d11a446e91
2      config.json                                          30.7 KB YES       sha256:7bf78b8de1aaced681f9a41160566de1b36b026a562fe2046c49c109b7bb4796
3      generation_config.json                               10.2 KB YES       sha256:c28181c80125d3acf6f0f9af09dde79f431a2a0c3028654efe20acd994c27d56
4      model_mtp.safetensors                                 1.7 GB YES       sha256:f27c48b498164c1d22cca46e1adc01a7db9d44016cb587f71151a8a7edb0e484
5      model.safetensors                                    22.5 GB YES       sha256:db1d17adb86aaa8785e50a9130b7f12db4bef06d5b9062904b213cc4b6d80bfd
6      model.safetensors.index.json                         12.4 MB YES       sha256:dd44242a458a272d39185c81755405a8d6189a2cd98063f25cefe809ee92d597
7      model_visual.safetensors                            893.2 MB YES       sha256:dcf1856604b1a4042c31c535d435c4106c6bca6e3a2fbd63feb1095f4391f486
8      processor_config.json                                10.2 KB YES       sha256:51e01e5a2d011d3293e869fadf1931b7e454d7e1290c14c987a353b5c3b4b0a3
9      README.md                                            10.2 KB YES       sha256:c7a10b0231f9db7b86d9b2f3103d85532912e2ac8e7157d58676203f43c63f8a
10     recipe.yaml                                          10.2 KB YES       sha256:d47c3e74a08f0d4a6464d1e12f01afd0a00cab6dae5b69274519ce2bf7cd74aa
11     tokenizer_config.json                                10.2 KB YES       sha256:1529356b2cd6bfddafe6af3558da6bfc8fbef0c505d7ce1174dc0dbc0edbc94c
12     tokenizer.json                                       20.0 MB YES       sha256:38267d96fb364d872c2a855151f01f8debaa980894f089abf39a36d43a8ef949
13     modelcard.md                                          2.1 KB YES       sha256:b5e710f4fff478db9d965797cb7a9fd13f0f53c194ceec38752260c74e94c1a6

Shared layers: 13/14
  Model layers shared (OLOT): 13
  Base layers differing (expected): 1

MTIME: 1781613262.0 (2026-06-16T12:34:22) — PASS
SAVINGS: 75.2 GB — 4.0x more storage efficient (75.0% reduction)
VERDICT: PASS
```

### 6. gemma-4-26b-a4b-it-fp8-dynamic:3.0

```
================================================================================
CROSS-ARCHITECTURE LAYER DEDUPLICATION REPORT
================================================================================

Image: registry.redhat.io/rhai/modelcar-redhatai-gemma-4-26b-a4b-it-fp8-dynamic:3.0
Platforms: amd64, arm64/v8, ppc64le, s390x (4 total)
Layers per platform: 11

Platform         Manifest Digest
-------------------------------------------------------------------------------------------
amd64            sha256:b72e7e67e996ebdf67db999682ae01d5aecb02b6f16433ecdf925339fe3dd428
arm64/v8         sha256:86021aebfbe91272679a20f863c9d19a30db687e79d0790d2afcb548de36a52a
ppc64le          sha256:1a67298242e6aff1c3a64e858c1aef20360e0123622ff08eb3011145c742861e
s390x            sha256:2906516f396111f0f19a2164d1ec7b2c97018a7f25341d394b70efebd28ab118

Layer  Title                                                   Size Shared?    Digest
------------------------------------------------------------------------------------------------------------------------------------------------------
0      layer-0                                               7.2 MB NO        sha256:4e5861c970ccfcb3472d3a98e0a6ac292281a42a5a90a7d45e1fa246cd38d2bf (amd64) (expected)
1      chat_template.jinja                                  20.5 KB YES       sha256:b9e50545dfabff1192f324ebb2270b9c43d4f3fa66585352e3229e8a19e2d7c9
2      config.json                                          30.7 KB YES       sha256:22b9475ea9ce591b278543ea9f214182b33a1c4b12cfb7ffa43db465184888cb
3      generation_config.json                               10.2 KB YES       sha256:6bca95fed964feb2679a59e72d78cd10a9ce8582a0b6b965b9e894c15a88ee5a
4      model.safetensors                                    28.6 GB YES       sha256:f6b590c102a3eb39fe237497d9513f9f5cc625ac52e763fd3a178e7253ab1f5e
5      processor_config.json                                10.2 KB YES       sha256:3589d3af8c7c8aeea4955eb7cc1c82e18ca6cafb106b5dd7e0d4fd3187dcc692
6      README.md                                            10.2 KB YES       sha256:6f9805746b2453aad8975c29cb4611709c9c13715fedee075214979e343ee942
7      recipe.yaml                                          10.2 KB YES       sha256:e2ee91c65f2e0b7b9c25c30cb504368b69618edf282907990a7792e988ae6a45
8      tokenizer_config.json                                10.2 KB YES       sha256:bc1ce16d75e0d6390eee59e5c2cdf99a890f50c347b8b267dfdeceb6ccabf5b0
9      tokenizer.json                                       32.2 MB YES       sha256:1623c1d738d6633a43dce9cb4e7153f42a97e78590129e83792aad5cfd2f845c
10     modelcard.md                                           917 B YES       sha256:ea008d86f9098f366b8b9de702709e1d50e8e8031a872c5c4cd09436d8da1e5f

Shared layers: 10/11
  Model layers shared (OLOT): 10
  Base layers differing (expected): 1

MTIME: 1781613302.0 (2026-06-16T12:35:02) — PASS
SAVINGS: 86.0 GB — 4.0x more storage efficient (75.0% reduction)
VERDICT: PASS
```

### 7. qwen3-6-35b-a3b-fp8:3.0

```
================================================================================
CROSS-ARCHITECTURE LAYER DEDUPLICATION REPORT
================================================================================

Image: registry.redhat.io/rhai/modelcar-redhatai-qwen3-6-35b-a3b-fp8:3.0
Platforms: amd64, arm64/v8, ppc64le, s390x (4 total)
Layers per platform: 57

Platform         Manifest Digest
-------------------------------------------------------------------------------------------
amd64            sha256:7accdc7613971df7a79f83db82ae99d99f77270124fed227f50b447bbab23bf3
arm64/v8         sha256:451b27fa866e96ae4eda1789f620215e3d31d1f128167064491583f51487dc86
ppc64le          sha256:3d98ab80f0387f416364c930f20074fc0b31fec3de875ea0852a829e71456c5f
s390x            sha256:36e4ee6b17566ff69b9676f9379a19a2d253d9bed5bbd46276d2ed913e13ea40

Layer  Title                                                   Size Shared?    Digest
------------------------------------------------------------------------------------------------------------------------------------------------------
0      layer-0                                               7.2 MB NO        sha256:4e5861c970ccfcb3472d3a98e0a6ac292281a42a5a90a7d45e1fa246cd38d2bf (amd64) (expected)
1      chat_template.jinja                                  20.5 KB YES       sha256:5ca71b4f4f780c5b375797b440d13a9c9d1ebf9552716ac9a62fe2130cb87b37
2      config.json                                          41.0 KB YES       sha256:a21837a7945632d48c11a690fafd4be2bf2b1c5dd31d50f9222820fce8b681b2
3      configuration.json                                   10.2 KB YES       sha256:466c3555af10ccbc118803249a05f8967f568214c4018fde40f77a370bdfb493
4      generation_config.json                               10.2 KB YES       sha256:70ebf5b6c6ab905117b9b57f9d0dfc235d061bafd2745b8d67f5e33801548711
5      layers-0.safetensors                                843.7 MB YES       sha256:c95bd052be8af8106de8348531beab1dc57c9a7f90254fad1aa2589aeae8dda3
6      layers-10.safetensors                               843.7 MB YES       sha256:58adbe4556cecbe9589585f069e7dc2e77bcf24ed8e01c8a6664a90ae261fc58
7      layers-11.safetensors                               837.1 MB YES       sha256:8ea5a7b5b3da6042f445bfc75440c77edcb8f378ebf0aecf8ff766b23528c24e
8      layers-12.safetensors                               843.7 MB YES       sha256:746c38622e6aba3a493c506ef290a5718cf70c92f592827c2b43bd7ccde13d07
9      layers-13.safetensors                               843.7 MB YES       sha256:45f6ff92d2ba8e512da6a4c3ba2202315c7beda6f25f95076b11a7307b2fd5ad
10     layers-14.safetensors                               843.7 MB YES       sha256:0de994fcc6181a08f0ff99f7630b27c15e805891f03e5d458052fd7e37796961
11     layers-15.safetensors                               837.1 MB YES       sha256:0eb9d3f873f1280a526a3573fb89d73bba3ac4cf91dd65f9f8b62e2a997551f5
12     layers-16.safetensors                               843.7 MB YES       sha256:0c596c88859c4d36ab115a1d2049d3fa73895bee6ec456cb4ecf3c9929c5ac27
13     layers-17.safetensors                               843.7 MB YES       sha256:bc25f23ece98942f04397fabd41d13942a31ac98db41e3dbbf2b698b8996ebab
14     layers-18.safetensors                               843.7 MB YES       sha256:cb1e7181ebd1d7d2543ef3a779313d825cc5aef0f572521ea09174f00b970ffb
15     layers-19.safetensors                               837.1 MB YES       sha256:a33c9a5c49edf68e955cd14ff81fef9fa8e504b71f859573dc350c5904a99106
16     layers-1.safetensors                                843.7 MB YES       sha256:47c411fe79f3b1c4a2a7c49661c124f9dbb3f1e297570341b379ea83faed9188
17     layers-20.safetensors                               843.7 MB YES       sha256:6cb666965bfcb0d8081cd8781b1f930687aa24d392f3c0b1e9aa12059ace469b
18     layers-21.safetensors                               843.7 MB YES       sha256:765a90ad1968bb40925a957631d6c2c4f8368fffec02012bd7be11b7d0ef48b6
19     layers-22.safetensors                               843.7 MB YES       sha256:309e1bc8d02043c7f53c29a26aaec26995e03c90c2e6977ab9cf548c036db8a5
20     layers-23.safetensors                               837.1 MB YES       sha256:a1890738573f3574e12c224fb244f640e314bfc2062b4914aaf0b37b4a3a2f3c
21     layers-24.safetensors                               843.7 MB YES       sha256:09705a6a6037d15c0d7f2ae8f44448c3f19cb90aeb30a7d98276fb0aa2d1d8ff
22     layers-25.safetensors                               843.7 MB YES       sha256:f0e63784e054178d3f0b097f3b25bc906e788a05ce0e8a183ec7c6b1a7c1dd14
23     layers-26.safetensors                               843.7 MB YES       sha256:758124a4a39795f0587add8454d4a3135ba515453b5d58affa3a6eeb251cd3e2
24     layers-27.safetensors                               837.1 MB YES       sha256:4184bc633173cd7b6d2ac59d40679ab254f5230fcd8f9e2946d7edecd6d7f320
25     layers-28.safetensors                               843.7 MB YES       sha256:f109e19232d1364c333264e865b3135e63d03de64985e4a5551014bea67458fd
26     layers-29.safetensors                               843.7 MB YES       sha256:b708552a54c15719e64452aed83eeff16510d342db472fb269bc2dfc0cf88c09
27     layers-2.safetensors                                843.7 MB YES       sha256:1f502cbd7210383652bc15fb1685171ecb4f7ed8201fe45154e2f78ae096e944
28     layers-30.safetensors                               843.7 MB YES       sha256:3b28f035adfe21fca27879a97c418f072a16db446aeb96872e558a6ab6f2c72e
29     layers-31.safetensors                               837.1 MB YES       sha256:ab0d65b8bba69aeaaaa055d243fa2783f3fd11a9ad6cb1d0e9bbb7e5ae1e2287
30     layers-32.safetensors                               843.7 MB YES       sha256:5ca04903bb58459cc2513678358488685a9c54b45b261596ced7ea9d5bc9acab
31     layers-33.safetensors                               843.7 MB YES       sha256:851126d73b4d3aaee96a63d3ddeb0e01b42b601ee8a99a900a6b6e818cb23d5c
32     layers-34.safetensors                               843.7 MB YES       sha256:b603b0787717cf73ee7f9dce8fa1ff9eb285c4ea236b8e6a7f26a0bdbaf3d571
33     layers-35.safetensors                               837.1 MB YES       sha256:0a1dfc1f66c38b4ac18908bf8826b78e2b4bfa91df90b5ad75fccf00f8556a3a
34     layers-36.safetensors                               843.7 MB YES       sha256:700386f7ce78617063dab50fd458264be4826d64e971575e74922f9378a38f13
35     layers-37.safetensors                               843.7 MB YES       sha256:4be5595d581dc325cb1e048759024618cc815d39485b44516fbe7ebce0b32c32
36     layers-38.safetensors                               843.7 MB YES       sha256:09c7ca7b3776c3b8e96a2f546b65629fb2a5e1da41435eaef7567edbd9415c8a
37     layers-39.safetensors                               837.1 MB YES       sha256:9aceef249e391ad5b480302e1abd77c330fcc18227760c278ae93174b63bfc18
38     layers-3.safetensors                                837.1 MB YES       sha256:d62e53aca397d1d3620039ce7a6e9b8a47eaa6d945deaf7441da980c06f7476f
39     layers-4.safetensors                                843.7 MB YES       sha256:09afc1e4cd834c30761a1cf91cc737d784b90eec9799382f232ddadffadba282
40     layers-5.safetensors                                843.7 MB YES       sha256:b8fd42cf15c86bd137b0922456c85737809402e2f71c9645330d31f31dc64362
41     layers-6.safetensors                                843.7 MB YES       sha256:37ec6ce33f2d9cef95a657767e816163f7366fa50e92a54f6ca6463360f55068
42     layers-7.safetensors                                837.1 MB YES       sha256:d86b471cbe39ba9b1005bc959a06dd3262194516a3280b3ad10a93214a7bcac7
43     layers-8.safetensors                                843.7 MB YES       sha256:2aaf7cf967c80d5bd18fcd2da5399816e98ef35a47f95a1c47b2322e2c434b1d
44     layers-9.safetensors                                843.7 MB YES       sha256:8f7957a1c6e5d8d5525dbe136071a0de1b7f9972e03b4595ce65d7218257618e
45     LICENSE                                              20.5 KB YES       sha256:7f823fb05951171a3aaed258ca57454d28d8b963d4e7b79332a56feb29430bb7
46     merges.txt                                            3.4 MB YES       sha256:3dfb6ccc98287df141b9731f6667ef472ecc3c7ce88a78125c3695113f610fea
47     model.safetensors.index.json                          6.3 MB YES       sha256:40332d61a6ac4c335bdd5012dbaf6c150659626a2dca0d7056ff19d7cce75cd7
48     mtp.safetensors                                     853.9 MB YES       sha256:90f3afe815179bad2a2e01dde2f8afcd407f027f664ff2ac6ba0012ede26aeb6
49     outside.safetensors                                   2.9 GB YES       sha256:a2d78cbd9c1f766bdaf4ba0c394dc37d5008d91733678974c280d9a9eb4960ff
50     preprocessor_config.json                             10.2 KB YES       sha256:a1b84baed7dbb6851b2a97cd9382887ccc29c5c4177d5802e34d7129566470e1
51     README.md                                            71.7 KB YES       sha256:ae1d366b41dcd0f23eab833e6ebddcd86eb67ad7595e20822d79d56e2b98fc40
52     tokenizer_config.json                                20.5 KB YES       sha256:18e6f9732b4d81f9914db3b82e55e6ce3cd5fcf694c27f0ea860d90e8e57d370
53     tokenizer.json                                       12.8 MB YES       sha256:44a56205681739f6ce10c62e7aac881925a6f8ddd03efce2fc67685eed9e9938
54     video_preprocessor_config.json                       10.2 KB YES       sha256:6ba7d1d4bc21633044b141f96e3a767d3e9029e309f2a093610592596356b261
55     vocab.json                                            6.7 MB YES       sha256:dad91cb421e620f1359a8c0dd93349e4e6277d4bd4ff4b2d601e386d8b00a097
56     modelcard.md                                         11.1 KB YES       sha256:53c01e10eac79e2cf6734c3453de9f152d277bc61b4f06c0674f6fa9595ecc75

Shared layers: 56/57
  Model layers shared (OLOT): 56
  Base layers differing (expected): 1

MTIME: 1781613281.0 (2026-06-16T12:34:41) — PASS
SAVINGS: 112.5 GB — 4.0x more storage efficient (75.0% reduction)
VERDICT: PASS
```

### 8. qwen3-6-35b-a3b-fp8-dynamic:3.0

```
================================================================================
CROSS-ARCHITECTURE LAYER DEDUPLICATION REPORT
================================================================================

Image: registry.redhat.io/rhai/modelcar-redhatai-qwen3-6-35b-a3b-fp8-dynamic:3.0
Platforms: amd64, arm64/v8, ppc64le, s390x (4 total)
Layers per platform: 13

Platform         Manifest Digest
-------------------------------------------------------------------------------------------
amd64            sha256:f8786f2dba4ed5bcd355fb3156f7d3f13efb478acfaa607ff51597739d4bff6f
arm64/v8         sha256:aa8f9d13b97561ff40a645e98163de3214fb4a1bada29be1630ece786185004b
ppc64le          sha256:e9bbbd6d168a104858f6c915e884709f6eec3011a9b10fd6256a185295a0fba5
s390x            sha256:de3090a7e0d4859319c0516547265d6258ac8fa9352092e9393d7710402adc1c

Layer  Title                                                   Size Shared?    Digest
------------------------------------------------------------------------------------------------------------------------------------------------------
0      layer-0                                               7.2 MB NO        sha256:4e5861c970ccfcb3472d3a98e0a6ac292281a42a5a90a7d45e1fa246cd38d2bf (amd64) (expected)
1      chat_template.jinja                                  20.5 KB YES       sha256:6bbb521e09833189d172cf9f394625d74ed98bcb1d2ffcc325da4782eb817cf7
2      config.json                                          30.7 KB YES       sha256:625a851ae2cb1144e24fb1a4e16c1c62c5c116c8559350abe94450672b43f613
3      generation_config.json                               10.2 KB YES       sha256:0eacecc78e5110d4daab2117d314f86005eba29905ec067c75b84b3cd4464e37
4      model_mtp.safetensors                                 1.7 GB YES       sha256:7f4cfb2a4f51ab3885d85e6bbc70edd4ba791dd6a2a960361dd5b5c1257c0062
5      model.safetensors                                    37.7 GB YES       sha256:a59e528569a0a7b65c9a5c22eaa77764e54d380a5b4b6d1cd9a204ab2da7ebca
6      model.safetensors.index.json                          5.9 MB YES       sha256:4c1adb7be3931de66c6d1f6006aef3625d8907c5f28d695443896b96192e57e7
7      processor_config.json                                10.2 KB YES       sha256:23c3977c82ad3aabaaa25b6e70a3ab389ad9c9c3613ee033c037450692c2b036
8      README.md                                            10.2 KB YES       sha256:ded939e508be1b1b1c879e813d498640cba09341f0682e9138326e51f5e55c7e
9      recipe.yaml                                          10.2 KB YES       sha256:81a1d40a027a5015a4114e2de0d06bd66b5cfe52e191c0f81f72389853b9af78
10     tokenizer_config.json                                10.2 KB YES       sha256:499e3269d991af44ea857bb86907468976ac2912f7d269cfbb4fe0f0a06e2d2d
11     tokenizer.json                                       20.0 MB YES       sha256:e765107c04b3d8be2aadf48e5e0d5546da82e62d6106d5c2f334c8186f8c3173
12     modelcard.md                                           969 B YES       sha256:7eef9ebc1dccba33fc9f6257d0abe8993e7c673420fa1000316afedf155b96ff

Shared layers: 12/13
  Model layers shared (OLOT): 12
  Base layers differing (expected): 1

MTIME: 1781613296.0 (2026-06-16T12:34:56) — PASS
SAVINGS: 118.2 GB — 4.0x more storage efficient (75.0% reduction)
VERDICT: PASS
```

---

## Observations

1. **All mtimes cluster around 2026-06-16T12:34-12:35 UTC.** This is the `org.opencontainers.image.created` timestamp of the source OCI artifacts, not the image build date (2026-06-17). The `touch -t` normalization is correctly using the artifact creation time.

2. **The qwen3-6-35b-a3b-fp8 image has 57 layers** (40 sharded safetensor files + config/tokenizer files + modelcard). Even at this scale, all 56 model layers are perfectly shared across 4 architectures.

3. **All images share the same base image** (UBI9 Micro, release 1754345610), though the base layer digest differs per architecture as expected.

4. **No Konflux build labels** were found on any image. All labels originate from the UBI9 Micro base image.

## Conclusion

The mtime normalization fix ([build-definitions#3358](https://github.com/konflux-ci/build-definitions/pull/3358)) is **fully operational** across all 8 tested production modelcar images. Cross-architecture layer deduplication is working correctly, saving a total of **~711 GB** of registry storage across these images alone.
