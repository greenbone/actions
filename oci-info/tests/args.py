# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import unittest
from action.args import parse_args


class TestArgparse(unittest.TestCase):
    def test_parse_args_list_tags(self):
        args = parse_args(
            [
                "--repository",
                "test_repo",
                "--namespace",
                "test_namespace",
                "list-tags",
            ]
        )
        self.assertEqual(args.command, "list-tags")
        self.assertEqual(args.repository, "test_repo")
        self.assertEqual(args.namespace, "test_namespace")

    def test_parse_args_compare_annotations(self):
        args = parse_args(
            [
                "--repository",
                "test_repo",
                "--namespace",
                "test_namespace",
                "compare-tags",
                "--tag",
                "test_tag",
                "--compare-repository",
                "test_compare_repo",
            ]
        )
        self.assertEqual(args.command, "compare-tags")
        self.assertEqual(args.repository, "test_repo")
        self.assertEqual(args.namespace, "test_namespace")
        self.assertEqual(args.tag, "test_tag")
        self.assertEqual(args.compare_repository, "test_compare_repo")

    def test_parse_args_default_values(self):
        args = parse_args(
            [
                "--repository",
                "test_repo",
                "--namespace",
                "test_namespace",
                "list-tags",
            ]
        )
        self.assertIsNone(args.user)
        self.assertIsNone(args.password)
        self.assertEqual(args.reg_domain, "ghcr.io")
        self.assertEqual(args.reg_auth_domain, "ghcr.io")
        self.assertEqual(args.reg_auth_service, "ghcr.io")

        args = parse_args(
            [
                "--repository",
                "test_repo",
                "--namespace",
                "test_namespace",
                "compare-tags",
                "--tag",
                "test_tag",
                "--compare-repository",
                "test_compare_repo",
            ]
        )
        self.assertIsNone(args.compare_user)
        self.assertIsNone(args.compare_password)
        self.assertEqual(args.compare_reg_domain, "registry-1.docker.io")
        self.assertEqual(args.compare_reg_auth_domain, "auth.docker.io")
        self.assertEqual(args.compare_reg_auth_service, "registry.docker.io")


if __name__ == "__main__":
    unittest.main()
