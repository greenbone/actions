# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import unittest

from action.oci_model import OciImageTags, OciIndex, OciManifest, OciPlatform


class TestOciModels(unittest.TestCase):
    def test_oci_image_tags(self):
        tags_data = ["1", "2", "3"]
        image_tags = OciImageTags(name="test_image", tags=tags_data)

        self.assertEqual(image_tags.name, "test_image")
        self.assertEqual(image_tags.tags, tags_data)

    def test_oci_platform(self):
        platform = OciPlatform(architecture="x86_64", os="linux")

        self.assertEqual(platform.architecture, "x86_64")
        self.assertEqual(platform.os, "linux")

    def test_oci_manifest(self):
        manifest = OciManifest(
            mediaType="application/vnd.oci.image.manifest.v1+json",
            digest="sha256:abcd",
            size=12345,
            annotations={"bla": "blub"},
            platform=OciPlatform(architecture="x86_64", os="linux"),
        )

        self.assertEqual(
            manifest.mediaType, "application/vnd.oci.image.manifest.v1+json"
        )
        self.assertEqual(manifest.digest, "sha256:abcd")
        self.assertEqual(manifest.size, 12345)
        self.assertEqual(manifest.annotations, {"bla": "blub"})
        self.assertEqual(manifest.platform.architecture, "x86_64")
        self.assertEqual(manifest.platform.os, "linux")

    def test_oci_index(self):
        manifest1 = OciManifest(
            mediaType="application/vnd.oci.image.manifest.v1+json",
            digest="sha256:abcd",
            size=12345,
        )
        manifest2 = OciManifest(
            mediaType="application/vnd.oci.image.manifest.v1+json",
            digest="sha256:efgh",
            size=67890,
        )
        index = OciIndex(
            schemaVersion=2,
            mediaType="application/vnd.oci.image.index.v1+json",
            manifests=[manifest1, manifest2],
        )

        self.assertEqual(index.schemaVersion, 2)
        self.assertEqual(
            index.mediaType, "application/vnd.oci.image.index.v1+json"
        )
        self.assertEqual(index.manifests, [manifest1, manifest2])


if __name__ == "__main__":
    unittest.main()
