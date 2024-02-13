# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import unittest
from unittest.mock import patch

from action.oci import Oci, OciAnnotationsError
from action.oci_model import OciAnnotations, OciImageTags, OciIndex


class TestOci(unittest.TestCase):
    def setUp(self):
        self._tags = {
            "name": "greenbone/opensight-postgres",
            "tags": [
                "16",
                "15",
                "14",
                "13",
                "sha256-37436c4fad364b793c2e179fe952cbada009081cb7c1a51ea050cd34e1971b3d.sig",
                "sha256-4b6bc8f97f813b6ea3ebd05a95ab6975f4034d299f27936b1a6750d694af58bc.sig",
                "sha256-f3a0b06bd4c899036379864204a4220a7eecb90ac9ce69d1c8eb390f7de3c9e7.sig",
                "15.2",
                "sha256-d567b42df8e3338d1613ec1c687d1db76caf7598526a5e0cc4dce6cb2a4085b9.sig",
                "sha256-05bdd95e43dc4964928e457277f4c1d488a305829df4c438d14d5f18849a11cb.sig",
                "sha256-8a8652825472a83df3b079b26d943cd129abdb704c1adb3422feb5e80cb35e67.sig",
                "postgres-sha256-0599bafe1afb0762426091b894a1b47dc1043c84b480205c4768e523aa47b193",
                "sha256-b2e57e1ff019c367d6171859fe0659156e3847979bda1bd237f4d3687ae9d038.sig",
                "sha256-4f0c3405bd378b9ab1955b84f5ee27bf32cf2b0142bf8a49fe14a4fc517ecaeb.sig",
                "sha256-1f60cf408c2cf0d6f049229abb6b17b69c53dfec46c5efee636acc93dd8bab18.sig",
                "15.3",
                "sha256-9ccee894c2061b32cf22e884f2d7a5a76a2a4b941102879be455898a8917c8ba.sig",
                "sha256-ce6447ee4164a84badd1be97e0238c93d6dd382501a088731bda28c67a7a3da2.sig",
                "sha256-458bb6d9aaf8c3adced93d61b01816fcdd50ef64ddc58b677e12f849b32e10c1.sig",
                "sha256-a276fb5f164ac8f2bb02a8f4b3590bb02594779e01559dc7d75fa133bbfad638.sig",
                "sha256-5e80596af8df5534306aeaa27f41554e2803e166ba4908000f309a15b1a1e8a5.sig",
                "sha256-8d79af2d06087bdd8ce905dedda0606cfca0c0b2c956af1f458cc3438554986f.sig",
                "sha256-d2db8fd86231f0f8ec1f3eb3c715b7c8090638b9b9f1a222e0b03e9d4989f96e.sig",
                "sha256-8ffd10bb0a46070f34266786e7257db36ee13e330fa82a1aa78842bbef9497ab.sig",
                "sha256-fcdc4a219ff6dfabcd09b9a7c71ae3627cadca576dea41bb383acbd080e8d1c5.sig",
                "sha256-4d6a03301bb930db05eed607163c0bf64d3f1c5958c173dee9ceb0abe723d33f.sig",
                "sha256-e90ac864eafc7e38230f02076537f8c22af71e18183d6a3d0b71cae68c6811fd.sig",
                "sha256-8c81d32f9f19539e6915b8182f6bd7084c000ea1f4c4a5bc63fdd3f9d59bbf65.sig",
                "sha256-d26a07f58b268fb4ffca990da45bd13cfbb99e85f06221ad7cfb9c0d01fa0a79.sig",
                "sha256-c645a0a66d67e487a100e369c4f6bc86f6d9dc39a2e64995ea4d721b7dc8102c.sig",
                "sha256-479c89ecfc17d087c065210330398460cece6374e0435f6337d594c3f157e1da.sig",
                "sha256-192d3f178c34f194b73c1d95bb487128f6aa2fe19da51d625879881b81d946a7.sig",
                "sha256-f7874166f0dcb60dd7be3358434648be0b0c2867136ec1e3b7cc62c1f756c633.sig",
                "sha256-6854603a21b156343039f60902826f3da506ef518af43e2b4b218bf04260e930.sig",
                "sha256-f7face8929f7122424a0eee14693e7fbc3b5020d412158e1553f2be4a3972f40.sig",
                "sha256-f93b49c795edc594b0381caba6afe5b1ed2d778e92557422ab6934aded9955d9.sig",
                "sha256-b88154bc0ee816dda5e182cffbc408b726a3ad5f986f03c4a500342c6f266e7e.sig",
                "sha256-cc8b6d8c4a839f9a2fc89e4802224c0c62c30d14a7afa0b435fab9206978dd4e.sig",
                "sha256-cb181b220918a91a717fe1b62160f4c1a096d72fe822609461a29ad57d5218d7.sig",
                "sha256-ff3a73b495d734448bd6a190d98ea0fcecf8e4d98c13c6875c6c6138c7d0937d.sig",
                "sha256-e8cddd99c4b876be5cdd22748c021a78d26b85d058f79e25c0ad4a9ccef22254.sig",
                "sha256-867b6eafc37da7908072a3904c1919ecfda0f593f34bce295bc13dd0c6a9c3a3.sig",
                "sha256-b93d7957a258d98bd2a898e04fd11f89438cbe38d0b07271d4ec1d355c6526c1.sig",
                "sha256-8aeccd47e601f2a8d12ece45bd9a36b4689ddcf12cf3cdf83123035316a81944.sig",
                "sha256-704c2a18275b462091e95967296c216b9971fb65e99450311babffbf8294699c.sig",
                "sha256-26c0881713f63877e9a8e1eaea95b1cac2b18fed268cf80599d4dddff77eb8b5.sig",
                "sha256-a8710a201b40d5e677806207918d5974863c3cf7ebe0099918969b0ae9fe8237.sig",
                "sha256-ec3103d88fb2228d52e4655d6842ff5ddf15ed6752579ec0e09a2b6770d23332.sig",
                "sha256-078ee7f7ad53c4c86462781e5f4e7c5b150e76b2008d9e12304c4900a1ea49a2.sig",
                "sha256-467889cc0ac01c271741236add2636798fa88b3048f14472a0ece682f3a8bcc9.sig",
                "sha256-7937c32163bf800054c30bec8d0ca8c3374bb95e7f4046f03d5ab0e7f0593784.sig",
                "sha256-4da6f9b0afcb534844afca96c65a3b99725a4fcad817f3affc17d12ff9b4e80d.sig",
                "sha256-bc0cbe266e9ca8c676a90e494830bdbf577f00ce21ab7342bded0ed63e6289f4.sig",
                "sha256-5aa72435d4767a1cf78126fb625878e14bb82e1b9eda4fe1520f92a1d982830c.sig",
                "sha256-851471309948cdcee81060c4b865366a63daee55d4a09bd2e9d7b54d3c455888.sig",
                "sha256-3f5542175a3d31149c7c9356b5f980d77e0059057d0cd7f85d17d3175fd813b6.sig",
                "sha256-5058e15785d0e33b286c83b54d9e5a8ea6d2022ec0f5a09f989922d55e9a1a2d.sig",
                "sha256-9598cb952a3e6d9025276bc95b601a2133c7d4935dbd12eb18c1daa5641b0ef2.sig",
                "sha256-3a13d9cbcde10b806bef6306a2fc41acd0fc6a973e99e5aa72167adf8dde9714.sig",
                "sha256-788ffd14604f8e85c569e3768bb89cfd25f4b5b52818a3929e67b1cdb924153d.sig",
                "sha256-6c3fdcf8777a5edc2d5511d704fc08ebfec9d5f0568efef5efcd809a9456e3c8.sig",
                "sha256-8df43954021777c0d7b7cfae1d694c7d509551d5e4310889e1cda00ba34ba592.sig",
                "sha256-f672aef2288bec4328d92016c3320fb0ad7769ff1c3a97d7af07926f17e0cc2d.sig",
                "sha256-003fa465928e214ebbaac8e8f0d71dd9fb356347608d1405a45d624cc318f314.sig",
                "sha256-54dc5c61f96469c961d0e497d5fd3daf86945412a18b4b04d5278a44ffb6f13f.sig",
                "sha256-0ddd7a611c4dfb8bcdb35a546eee32fbe1aeab6af9ae8dc448fc39f8a25f7ec1.sig",
                "sha256-5920865859de937c9ec5fd771249909203c32598c2604f20ba83b0b91556753f.sig",
                "sha256-d26c3e2823934b43d7e252312d67c5819fb08830bb4f01b1cf5f40d1f84f2a95.sig",
                "sha256-236b74d90578137363aa4a994425cf01b8b48d5fa6140cb2f266be95b558836c.sig",
                "sha256-597a5acd6161e432a07c5b64339d565c79079f8ab6869fa268289e8c1e986b0e.sig",
                "sha256-b602d9d673fd2cfc720c27dbe355cef81c40529831394d44004ca12bd53cf8b3.sig",
                "sha256-cbe6ac420bd66b1edb46d1ddf44f5c6f18dca5de5c0754006d58e69e7185150a.sig",
                "sha256-59cb2a43ae8a1dcc07a3e32483034cb490f9dded919b5a4af499fc9f428bc477.sig",
                "sha256-0dc8f8793742bf3734d0f0c9c172c6ef170ff6e936338b975555a3f1b30f2486.sig",
                "sha256-fc15c337766bb548a0c9043dd75c0aa5e60ccc874bfc8b332b54baa1609f2e1c.sig",
                "sha256-d09a2bbfe9189ee22d613993bc836b2d38b3ef752cf698302ea8bccb3d4b033f.sig",
                "sha256-cbda3729f3e23662991c828d213b20eab3dda15033574ca2e976373ce6f3c19b.sig",
                "sha256-f5c7fcdc6187a26447f8be123a86c081536c120a364f74969df01ddbac7f910e.sig",
                "sha256-6c74d6560c4b119cdf72f912ae51c203ea3ee83098d015d77102b060301aef22.sig",
                "16.1",
                "sha256-3844a6e807f7fed24748ab154169bd5e574af51caa506248355479c05637a10e.sig",
                "sha256-96f41068b6c46bfc4e8bea908ce28eb39cc64c89eba50faf80b5686683bcbd5f.sig",
                "sha256-59e450d2463fc53f9d0e71b754f3e16ac0a410e78d319f0e948967c4368f1da8.sig",
                "sha256-2b9ac96e8f0f6db1c4a22df8e65d6cf0089dad9b69c9a5b0e78dd0bd5944b0f6.sig",
                "sha256-7419bc632716e34109e8b80a56459a8d1f1321b7a198630876fdd98a079e36a3.sig",
                "sha256-b1d4391fd13d600168a96cf4d4d61628e9017fa4cd9a85f9b42edbde03f15dd0.sig",
            ],
        }
        self._manifests = {
            "manifests": [
                {
                    "annotations": {
                        "org.opencontainers.image.base.digest": "sha256:36a9d3bcaaec706e27b973bb303018002633fd3be7c2ac367d174bafce52e84e",
                        "org.opencontainers.image.base.name": "debian:bookworm-slim",
                        "org.opencontainers.image.created": "2024-01-31T23:55:11Z",
                        "org.opencontainers.image.revision": "d416768b1a7f03919b9cf0fef6adc9dcad937888",
                        "org.opencontainers.image.source": "https://github.com/docker-library/postgres.git#d416768b1a7f03919b9cf0fef6adc9dcad937888:16/bookworm",
                        "org.opencontainers.image.url": "https://hub.docker.com/_/postgres",
                        "org.opencontainers.image.version": "16.1",
                    },
                    "digest": "sha256:021d7d217750a1b97b2232c1be9331eaa3f7d90a8a1bb2e9c25cd04a28e8306c",
                    "mediaType": "application/vnd.oci.image.manifest.v1+json",
                    "platform": {"architecture": "amd64", "os": "linux"},
                    "size": 3573,
                },
                {
                    "annotations": {
                        "vnd.docker.reference.digest": "sha256:021d7d217750a1b97b2232c1be9331eaa3f7d90a8a1bb2e9c25cd04a28e8306c",
                        "vnd.docker.reference.type": "attestation-manifest",
                    },
                    "digest": "sha256:02d4d832e34054f6bf19e5e67ad2e2745668326b1bc4665fa9d082288cd27472",
                    "mediaType": "application/vnd.oci.image.manifest.v1+json",
                    "platform": {"architecture": "unknown", "os": "unknown"},
                    "size": 841,
                },
                {
                    "annotations": {
                        "org.opencontainers.image.base.digest": "sha256:490dea635022ba0375b1e18f4b7add5c7dbc43cbed58e0e4211c65ccb1d1e0ea",
                        "org.opencontainers.image.base.name": "debian:bookworm-slim",
                        "org.opencontainers.image.created": "2024-02-01T15:25:54Z",
                        "org.opencontainers.image.revision": "d416768b1a7f03919b9cf0fef6adc9dcad937888",
                        "org.opencontainers.image.source": "https://github.com/docker-library/postgres.git#d416768b1a7f03919b9cf0fef6adc9dcad937888:16/bookworm",
                        "org.opencontainers.image.url": "https://hub.docker.com/_/postgres",
                        "org.opencontainers.image.version": "16.1",
                    },
                    "digest": "sha256:fbc14678ce9c35198353ca453f90e021f5f4ac4a33cc0375ec41e425b9e3af04",
                    "mediaType": "application/vnd.oci.image.manifest.v1+json",
                    "platform": {
                        "architecture": "arm",
                        "os": "linux",
                        "variant": "v5",
                    },
                    "size": 3573,
                },
                {
                    "annotations": {
                        "vnd.docker.reference.digest": "sha256:fbc14678ce9c35198353ca453f90e021f5f4ac4a33cc0375ec41e425b9e3af04",
                        "vnd.docker.reference.type": "attestation-manifest",
                    },
                    "digest": "sha256:70de7253dee6000094f849109f2c5d58ac706945f8083e56e6e3121cf814a355",
                    "mediaType": "application/vnd.oci.image.manifest.v1+json",
                    "platform": {"architecture": "unknown", "os": "unknown"},
                    "size": 841,
                },
                {
                    "annotations": {
                        "org.opencontainers.image.base.digest": "sha256:97c852e46d1cba5de1d079998a44f11dd25be64a84d58635bea2e55184685a18",
                        "org.opencontainers.image.base.name": "debian:bookworm-slim",
                        "org.opencontainers.image.created": "2024-02-02T02:44:31Z",
                        "org.opencontainers.image.revision": "d416768b1a7f03919b9cf0fef6adc9dcad937888",
                        "org.opencontainers.image.source": "https://github.com/docker-library/postgres.git#d416768b1a7f03919b9cf0fef6adc9dcad937888:16/bookworm",
                        "org.opencontainers.image.url": "https://hub.docker.com/_/postgres",
                        "org.opencontainers.image.version": "16.1",
                    },
                    "digest": "sha256:c8a800e4ff35869c29fb41718fe93f5fee267ebc72ea2a5e93ca156b9c51f314",
                    "mediaType": "application/vnd.oci.image.manifest.v1+json",
                    "platform": {
                        "architecture": "arm",
                        "os": "linux",
                        "variant": "v7",
                    },
                    "size": 3573,
                },
                {
                    "annotations": {
                        "vnd.docker.reference.digest": "sha256:c8a800e4ff35869c29fb41718fe93f5fee267ebc72ea2a5e93ca156b9c51f314",
                        "vnd.docker.reference.type": "attestation-manifest",
                    },
                    "digest": "sha256:2f370cad6edc29aff75ed51cba9898caf8589d77be6250a5b04c1ee9a135d5bd",
                    "mediaType": "application/vnd.oci.image.manifest.v1+json",
                    "platform": {"architecture": "unknown", "os": "unknown"},
                    "size": 841,
                },
                {
                    "annotations": {
                        "org.opencontainers.image.base.digest": "sha256:0102d8e816536746a71f0450e86e61fadd5298a89daa33fcf68b630dac766ee4",
                        "org.opencontainers.image.base.name": "debian:bookworm-slim",
                        "org.opencontainers.image.created": "2024-02-01T20:21:54Z",
                        "org.opencontainers.image.revision": "d416768b1a7f03919b9cf0fef6adc9dcad937888",
                        "org.opencontainers.image.source": "https://github.com/docker-library/postgres.git#d416768b1a7f03919b9cf0fef6adc9dcad937888:16/bookworm",
                        "org.opencontainers.image.url": "https://hub.docker.com/_/postgres",
                        "org.opencontainers.image.version": "16.1",
                    },
                    "digest": "sha256:2fd85ae4aa0d4746f6d8158d5d866aec850fad07f5814a374386471012d3d34f",
                    "mediaType": "application/vnd.oci.image.manifest.v1+json",
                    "platform": {
                        "architecture": "arm64",
                        "os": "linux",
                        "variant": "v8",
                    },
                    "size": 3573,
                },
                {
                    "annotations": {
                        "vnd.docker.reference.digest": "sha256:2fd85ae4aa0d4746f6d8158d5d866aec850fad07f5814a374386471012d3d34f",
                        "vnd.docker.reference.type": "attestation-manifest",
                    },
                    "digest": "sha256:8f38cacf42ce6f1b5eba740c06a48d1da4321c63233b63a10dcdb47d11a6e924",
                    "mediaType": "application/vnd.oci.image.manifest.v1+json",
                    "platform": {"architecture": "unknown", "os": "unknown"},
                    "size": 841,
                },
                {
                    "annotations": {
                        "org.opencontainers.image.base.digest": "sha256:906dc12e1f67c09fa9806d1ad179d05a6c812b252ace899a63e37faf7db39728",
                        "org.opencontainers.image.base.name": "debian:bookworm-slim",
                        "org.opencontainers.image.created": "2024-01-31T23:55:16Z",
                        "org.opencontainers.image.revision": "d416768b1a7f03919b9cf0fef6adc9dcad937888",
                        "org.opencontainers.image.source": "https://github.com/docker-library/postgres.git#d416768b1a7f03919b9cf0fef6adc9dcad937888:16/bookworm",
                        "org.opencontainers.image.url": "https://hub.docker.com/_/postgres",
                        "org.opencontainers.image.version": "16.1",
                    },
                    "digest": "sha256:132fbaa180790cebd92aa00aae73b0dbc6865d34cda2b70e7770e997a91e1e55",
                    "mediaType": "application/vnd.oci.image.manifest.v1+json",
                    "platform": {"architecture": "386", "os": "linux"},
                    "size": 3573,
                },
                {
                    "annotations": {
                        "vnd.docker.reference.digest": "sha256:132fbaa180790cebd92aa00aae73b0dbc6865d34cda2b70e7770e997a91e1e55",
                        "vnd.docker.reference.type": "attestation-manifest",
                    },
                    "digest": "sha256:eebb0dc8fed8edeaddc5f0ee0eb90010dc7df9a1006eda4e6c05a34f1c1438f6",
                    "mediaType": "application/vnd.oci.image.manifest.v1+json",
                    "platform": {"architecture": "unknown", "os": "unknown"},
                    "size": 841,
                },
                {
                    "annotations": {
                        "org.opencontainers.image.base.digest": "sha256:042b0e3d724430860e786268d78a4966afe49bbfed1ee44e2032faf1476b2335",
                        "org.opencontainers.image.base.name": "debian:bookworm-slim",
                        "org.opencontainers.image.created": "2024-02-02T10:48:27Z",
                        "org.opencontainers.image.revision": "d416768b1a7f03919b9cf0fef6adc9dcad937888",
                        "org.opencontainers.image.source": "https://github.com/docker-library/postgres.git#d416768b1a7f03919b9cf0fef6adc9dcad937888:16/bookworm",
                        "org.opencontainers.image.url": "https://hub.docker.com/_/postgres",
                        "org.opencontainers.image.version": "16.1",
                    },
                    "digest": "sha256:38ad0933c80949d38f27c31121a17c2222230b2941821c4b392097f2b9a79152",
                    "mediaType": "application/vnd.oci.image.manifest.v1+json",
                    "platform": {"architecture": "mips64le", "os": "linux"},
                    "size": 3573,
                },
                {
                    "annotations": {
                        "vnd.docker.reference.digest": "sha256:38ad0933c80949d38f27c31121a17c2222230b2941821c4b392097f2b9a79152",
                        "vnd.docker.reference.type": "attestation-manifest",
                    },
                    "digest": "sha256:23d466779991199506ace709b8e1d9d24e84cf3897f22be429e92857103f7c07",
                    "mediaType": "application/vnd.oci.image.manifest.v1+json",
                    "platform": {"architecture": "unknown", "os": "unknown"},
                    "size": 567,
                },
                {
                    "annotations": {
                        "org.opencontainers.image.base.digest": "sha256:cbc779028821aa74fe1e6b92b522dada4465eb9836e8097da23001780754b12e",
                        "org.opencontainers.image.base.name": "debian:bookworm-slim",
                        "org.opencontainers.image.created": "2024-02-01T16:00:15Z",
                        "org.opencontainers.image.revision": "d416768b1a7f03919b9cf0fef6adc9dcad937888",
                        "org.opencontainers.image.source": "https://github.com/docker-library/postgres.git#d416768b1a7f03919b9cf0fef6adc9dcad937888:16/bookworm",
                        "org.opencontainers.image.url": "https://hub.docker.com/_/postgres",
                        "org.opencontainers.image.version": "16.1",
                    },
                    "digest": "sha256:b2a03e9bce80beb60992626d368f73ae102906d64e834a9138d415e6dd574251",
                    "mediaType": "application/vnd.oci.image.manifest.v1+json",
                    "platform": {"architecture": "ppc64le", "os": "linux"},
                    "size": 3573,
                },
                {
                    "annotations": {
                        "vnd.docker.reference.digest": "sha256:b2a03e9bce80beb60992626d368f73ae102906d64e834a9138d415e6dd574251",
                        "vnd.docker.reference.type": "attestation-manifest",
                    },
                    "digest": "sha256:21f2948ecdab5fb15e7134a7811e3215c6f5e963922f5ef2e9024e416ebd4862",
                    "mediaType": "application/vnd.oci.image.manifest.v1+json",
                    "platform": {"architecture": "unknown", "os": "unknown"},
                    "size": 841,
                },
                {
                    "annotations": {
                        "com.docker.official-images.bashbrew.arch": "s390x",
                        "org.opencontainers.image.base.digest": "sha256:c485d955a42128743aabbe177fec3a27f33270cc4c6b4e2473bfc46f761ff79c",
                        "org.opencontainers.image.base.name": "debian:bookworm-slim",
                        "org.opencontainers.image.created": "2024-02-07T07:34:51Z",
                        "org.opencontainers.image.revision": "d416768b1a7f03919b9cf0fef6adc9dcad937888",
                        "org.opencontainers.image.source": "https://github.com/docker-library/postgres.git#d416768b1a7f03919b9cf0fef6adc9dcad937888:16/bookworm",
                        "org.opencontainers.image.url": "https://hub.docker.com/_/postgres",
                        "org.opencontainers.image.version": "16.1",
                    },
                    "digest": "sha256:5e427a57b963ff56d25d916e384131cb42a306175f93d527b736df47cb0d265d",
                    "mediaType": "application/vnd.oci.image.manifest.v1+json",
                    "platform": {"architecture": "s390x", "os": "linux"},
                    "size": 3630,
                },
                {
                    "annotations": {
                        "vnd.docker.reference.digest": "sha256:5e427a57b963ff56d25d916e384131cb42a306175f93d527b736df47cb0d265d",
                        "vnd.docker.reference.type": "attestation-manifest",
                    },
                    "digest": "sha256:33c2d29370634125c992d69b61fa21d13e35bc5306862e99219363700ed936be",
                    "mediaType": "application/vnd.oci.image.manifest.v1+json",
                    "platform": {"architecture": "unknown", "os": "unknown"},
                    "size": 841,
                },
            ],
            "mediaType": "application/vnd.oci.image.index.v1+json",
            "schemaVersion": 2,
        }
        self._manifests_no_annotations = {
            "schemaVersion": 2,
            "mediaType": "application/vnd.oci.image.index.v1+json",
            "manifests": [
                {
                    "mediaType": "application/vnd.oci.image.manifest.v1+json",
                    "digest": "sha256:7419bc632716e34109e8b80a56459a8d1f1321b7a198630876fdd98a079e36a3",
                    "size": 2953,
                    "platform": {"architecture": "amd64", "os": "linux"},
                },
                {
                    "mediaType": "application/vnd.oci.image.manifest.v1+json",
                    "digest": "sha256:b1d4391fd13d600168a96cf4d4d61628e9017fa4cd9a85f9b42edbde03f15dd0",
                    "size": 566,
                    "annotations": {
                        "vnd.docker.reference.digest": "sha256:7419bc632716e34109e8b80a56459a8d1f1321b7a198630876fdd98a079e36a3",
                        "vnd.docker.reference.type": "attestation-manifest",
                    },
                    "platform": {"architecture": "unknown", "os": "unknown"},
                },
            ],
        }

    @patch("action.oci.Oci._get_data_as_dict")
    def test_get_tags(self, mock_get_data_as_dict):
        expected_tags = OciImageTags(**self._tags)
        mock_get_data_as_dict.return_value = self._tags

        tags = Oci().get_tags("postgres")

        self.assertEqual(tags, expected_tags)

    @patch("action.oci.Oci._get_data_as_dict")
    def test_get_manifests(self, mock_get_data_as_dict):
        expected_manifests = OciIndex(**self._manifests)
        mock_get_data_as_dict.return_value = self._manifests

        manifests = Oci().get_manifests("postgres", "16.1")

        self.assertEqual(manifests, expected_manifests)

    @patch("action.oci.Oci._get_data_as_dict")
    def test_get_oci_annotations(self, mock_get_data_as_dict):
        expected_annotations = OciAnnotations(
            **self._manifests["manifests"][0]["annotations"]
        )
        mock_get_data_as_dict.return_value = self._manifests

        annotations = Oci().get_oci_annotations("postgres", "16.1", "amd64")

        self.assertEqual(annotations, expected_annotations)

    @patch("action.oci.Oci._get_data_as_dict")
    def test_get_oci_annotations_no_annotations(self, mock_get_data_as_dict):
        mock_get_data_as_dict.return_value = self._manifests_no_annotations

        with self.assertRaises(OciAnnotationsError):
            Oci().get_oci_annotations("postgres", "16.1", "amd64")


if __name__ == "__main__":
    unittest.main()
