import unittest
import tempfile
import shutil
from pathlib import Path
from action.helm_chart_version_upgrade import (
    yaml_file_read,
    yaml_file_write,
    parse_arguments,
    ChartVersionUpgrade,
)


class TestChartVersionUpgrade(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.chart_dir = Path(self.temp_dir) / "test_chart"
        self.chart_dir.mkdir()
        # Setup test files
        chart_path = self.chart_dir / "Chart.yaml"
        chart_content = {
            "version": "0.0.0",
            "appVersion": "0.0.0",
            "dependencies": [{"name": "test-dependency", "version": "0.0.0"}],
        }
        yaml_file_write(chart_path, chart_content)
        values_path = self.chart_dir / "values.yaml"
        values_content = {"image": {"tag": "latest"}}
        yaml_file_write(values_path, values_content)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_chart_version_upgrade(self):
        chart_path = str(self.chart_dir)
        chart_version = "1.0.0"
        cvu = ChartVersionUpgrade(chart_path, chart_version=chart_version)
        cvu.chart_run()
        chart_data = yaml_file_read(self.chart_dir / "Chart.yaml")
        self.assertEqual(chart_data["version"], chart_version)

    def test_values_upgrade(self):
        chart_path = str(self.chart_dir)
        image_tag = "1.0.0"
        cvu = ChartVersionUpgrade(chart_path, image_tag=image_tag)
        cvu.values_run()
        values_data = yaml_file_read(self.chart_dir / "values.yaml")
        self.assertEqual(values_data["image"]["tag"], image_tag)

    def test_dependency_upgrade(self):
        chart_path = str(self.chart_dir)
        dependency_name = "test-dependency"
        dependency_version = "1.0.0"
        cvu = ChartVersionUpgrade(
            chart_path,
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
        chart_path = str(self.chart_dir)
        cvu = ChartVersionUpgrade(chart_path, chart_version_increase=True)
        cvu.chart_increase_run()
        cvu.chart_run()
        chart_data = yaml_file_read(self.chart_dir / "Chart.yaml")
        expected_version = "0.0.1"
        self.assertEqual(chart_data["version"], expected_version)


if __name__ == "__main__":
    unittest.main()
