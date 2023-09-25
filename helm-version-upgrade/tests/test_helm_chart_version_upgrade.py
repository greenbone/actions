# Copyright (C) 2023 Greenbone AG
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
import tempfile
import shutil
from pathlib import Path
from action.helm_chart_version_upgrade import (
    yaml_file_read,
    yaml_file_write,
    ChartVersionUpgrade,
)


class TestChartVersionUpgrade(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.chart_dir = Path(self.temp_dir) / "test_chart"
        self.chart_dir.mkdir()
        self.chart_path = str(self.chart_dir)

        # Setup test Chart.yaml
        chart_path = self.chart_dir / "Chart.yaml"
        chart_content = {
            "version": "0.0.0",
            "appVersion": "0.0.0",
            "dependencies": [{"name": "test-dependency", "version": "0.0.0"}],
        }
        yaml_file_write(chart_path, chart_content)

        # Setup test values.yaml
        values_path = self.chart_dir / "values.yaml"
        values_content = {"image": {"tag": "latest"}}
        yaml_file_write(values_path, values_content)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_chart_version_upgrade(self):
        chart_version = "1.0.0"

        cvu = ChartVersionUpgrade(self.chart_path, chart_version=chart_version)
        cvu.chart_run()

        chart_data = yaml_file_read(self.chart_dir / "Chart.yaml")
        self.assertEqual(chart_data["version"], chart_version)

    def test_values_upgrade(self):
        image_tag = "1.0.0"

        cvu = ChartVersionUpgrade(self.chart_path, image_tag=image_tag)
        cvu.values_run()

        values_data = yaml_file_read(self.chart_dir / "values.yaml")
        self.assertEqual(values_data["image"]["tag"], image_tag)

    def test_dependency_upgrade(self):
        dependency_name = "test-dependency"
        dependency_version = "1.0.0"

        cvu = ChartVersionUpgrade(
            self.chart_path,
            dependency_name=dependency_name,
            dependency_version=dependency_version,
        )
        cvu.dependency_run()

        chart_data = yaml_file_read(self.chart_dir / "Chart.yaml")
        self.assertEqual(
            chart_data["dependencies"][0]["version"],
            dependency_version,
        )

    def test_chart_version_increase(self):
        expected_version = "0.0.1"

        cvu = ChartVersionUpgrade(self.chart_path, chart_version_increase=True)
        cvu.chart_increase_run()
        cvu.chart_run()

        chart_data = yaml_file_read(self.chart_dir / "Chart.yaml")
        self.assertEqual(chart_data["version"], expected_version)


if __name__ == "__main__":
    unittest.main()
