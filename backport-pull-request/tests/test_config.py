# Copyright (C) 2021 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest

from unittest.mock import patch

from action.config import Config


class ConfigTestCase(unittest.TestCase):
    @patch("pathlib.Path")
    def test_verify_missing_backport(self, path_mock):
        path_mock.read_text.return_value = """
        """
        config = Config(path_mock)
        verify_iterator = config.verify()
        verify_issue = next(verify_iterator)

        self.assertEqual(str(verify_issue), "No backport section found.")

        with self.assertRaises(StopIteration):
            verify_issue = next(verify_iterator)

    @patch("pathlib.Path")
    def test_verify_missing_label(self, path_mock):
        path_mock.read_text.return_value = """
        [backport.foo]
        source = "a"
        destination = "b"
        """
        config = Config(path_mock)
        verify_iterator = config.verify()
        verify_issue = next(verify_iterator)

        self.assertEqual(
            str(verify_issue), "Missing label entry in [backport.foo] section."
        )

        with self.assertRaises(StopIteration):
            verify_issue = next(verify_iterator)

    @patch("pathlib.Path")
    def test_verify_missing_source(self, path_mock):
        path_mock.read_text.return_value = """
        [backport.foo]
        label = "foo"
        destination = "b"
        """
        config = Config(path_mock)
        verify_iterator = config.verify()
        verify_issue = next(verify_iterator)

        self.assertEqual(
            str(verify_issue), "Missing source entry in [backport.foo] section."
        )

        with self.assertRaises(StopIteration):
            verify_issue = next(verify_iterator)

    @patch("pathlib.Path")
    def test_verify_missing_destination(self, path_mock):
        path_mock.read_text.return_value = """
        [backport.foo]
        label = "foo"
        source = "a"
        """
        config = Config(path_mock)
        verify_iterator = config.verify()
        verify_issue = next(verify_iterator)

        self.assertEqual(
            str(verify_issue), "Missing destination entry in [backport.foo] section."
        )

        with self.assertRaises(StopIteration):
            verify_issue = next(verify_iterator)

    @patch("pathlib.Path")
    def test_verify_missing(self, path_mock):
        path_mock.read_text.return_value = """
        [backport.foo]
        label = "foo"
        source = "a"
        destination = "b"

        [backport.bar]
        """
        config = Config(path_mock)
        verify_iterator = config.verify()
        verify_issue = next(verify_iterator)

        self.assertEqual(
            str(verify_issue), "Missing label entry in [backport.bar] section."
        )

        verify_issue = next(verify_iterator)
        self.assertEqual(
            str(verify_issue), "Missing source entry in [backport.bar] section."
        )

        verify_issue = next(verify_iterator)
        self.assertEqual(
            str(verify_issue), "Missing destination entry in [backport.bar] section."
        )

        with self.assertRaises(StopIteration):
            verify_issue = next(verify_iterator)

    @patch("pathlib.Path")
    def test_load(self, path_mock):
        path_mock.read_text.return_value = """
        [backport.foo]
        label="foo"
        source="a"
        destination="b"

        [backport.bar]
        label="bar"
        source="b"
        destination="a"
        """

        config = Config(path_mock)
        backport_config = config.load()

        self.assertEqual(len(backport_config), 2)
