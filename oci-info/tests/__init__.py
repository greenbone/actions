# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import unittest

from example.main import parse_args


class ParseArgsTestCase(unittest.TestCase):
    def test_parse_args(self):
        args = parse_args(["--some-arg", "foo"])

        self.assertEqual(args.some_arg, "foo")
