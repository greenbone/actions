# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import unittest
import sys

from src.main import parse_args


class ParseArgsTestCase(unittest.TestCase):
    def test_parse_args(self):
        sys.argv.append("filepath")
        sys.argv.append("foo")
        args = parse_args()

        self.assertEqual(args.some_arg, "foo")
