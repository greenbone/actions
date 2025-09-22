# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import unittest

from src.main import parse_args, get_changed_files_and_apply_filter, print_marker, scan_file, scan_multiple_changed_files, scan_single_changed_file, scan_changed_files

class ParseArgsTestCase(unittest.TestCase):
    def test_parse_args(self):
        args = parse_args(["foo", "-s", "--filter", ".*urgs.*"])

        self.assertEqual(args.repopath, "foo")
        self.assertEqual(args.filter, ".*urgs.*")
        self.assertEqual(args.silent, True)

class GetChangedFilesAndApplyFilterTestCase(unittest.TestCase):
    def test_get_changed_files_and_apply_filter(self):
        args = parse_args([".", "--filter", ".*detect-hidden-unicode.*"])
        changed_files = get_changed_files_and_apply_filter(args, "8897bd5e42ee2ca11ce2c939005563309a26278e", "3ec149b4224139e5a98736aa4c6e592e7a21e3c4")

        self.assertEqual(len(changed_files), 3)

class PrintMarkerTestCase(unittest.TestCase):
    def test_print_marker(self):
        detected_markers = 0
        detected_markers = print_marker('b', "description", 1, 1, "fakePath", detected_markers)

        self.assertEqual(detected_markers, 1)

class ScanFileTestCase(unittest.TestCase):
    def test_scan_file(self):
        file_path = "tests/509_pillar-security_example"
        detected_markers = 0
        detected_markers = scan_file(False, file_path)

        self.assertEqual(detected_markers, 509)

class ScanMultipleChangedFilesTestCase(unittest.TestCase):
    def test_scan_multiple_changed_files(self):
        detected_markers = scan_multiple_changed_files(True, ["tests/509_pillar-security_example", "tests/12_basic_example" ])

        self.assertEqual(detected_markers, 521)

class ScanSingleChangedFileTestCase(unittest.TestCase):
    def test_scan_single_changed_file(self):
        detected_markers = scan_single_changed_file(True, "tests/12_basic_example")

        self.assertEqual(detected_markers, 12)

class ScanChangedFilesTestCase(unittest.TestCase):
    def test_ChangedFilesTestCase(self):
        detected_markers = scan_changed_files(True, ["tests/509_pillar-security_example", "tests/12_basic_example" ])

        self.assertEqual(detected_markers, 521)
