# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import unittest

from src.main import parse_args, print_marker, scan_file

#class ParseArgsTestCase(unittest.TestCase):
#    def test_parse_args(self):
#        args = parse_args(["foo"])
#
#        self.assertEqual(args.filepath, "foo")
#
#class PrintMarkerTestCase(unittest.TestCase):
#    def test_print_marker(self):
#        detected_markers = 0
#        detected_markers = print_marker('b', 1, 1, "fakePath", detected_markers)
#
#        self.assertEqual(detected_markers, 1)
#
#class ScanFileTestCase(unittest.TestCase):
#    def test_scan_file(self):
#        file_path = "509_pillar-security_example"
#        detected_markers = 0
#        detected_markers = scan_file(file_path)
#
#        self.assertEqual(detected_markers, 509)
