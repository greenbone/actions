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

"""
Simple script that upgrades 
a Helm chart version.
"""

import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML


def yaml_file_read(yaml_path: Path) -> dict[Any, Any]:
    """Read yaml file into dict"""

    yaml = YAML()
    yaml.preserve_quotes = True
    return yaml.load(yaml_path)


def yaml_file_write(yaml_path: Path, data: dict[Any, Any]) -> None:
    """Write yaml file into dict"""

    yaml = YAML()
    yaml.preserve_quotes = True
    return yaml.dump(data, yaml_path)


def parse_arguments() -> Namespace:
    """Read arguments"""

    parser = ArgumentParser()
    parser.add_argument(
        "--chart-path",
        required=True,
        type=str,
        help="Set the path to chart folder",
    )
    parser.add_argument(
        "--chart-version", required=False, type=str, help="Set chart version"
    )
    parser.add_argument(
        "--app-version", required=False, type=str, help="Set appVersion"
    )
    parser.add_argument(
        "--image-tag", required=False, type=str, help="Set image tag"
    )
    parser.add_argument(
        "--dependency-name",
        required=False,
        type=str,
        help="Set dependency to upgrade",
    )
    parser.add_argument(
        "--dependency-version",
        required=False,
        type=str,
        help="Set dependency version",
    )
    parser.add_argument(
        "--no-tag",
        required=False,
        default=False,
        action="store_true",
        help="Do not upgrade image tag",
    )
    return parser.parse_args()


class ChartVersionUpgradeError(Exception):
    """Base Update error class"""


class ChartVersionUpgrade:
    """
    Upgrade chart version and app version in Charts.yaml
    Upgrade image tag in values.yaml
    """

    def __init__(
        self,
        chart_dir: str,
        chart_version: str = None,
        app_version: str = None,
        image_tag: str = None,
        dependency_name: str = None,
        dependency_version: str = None,
        no_tag: bool = False,
    ) -> None:
        self.no_tag = no_tag

        self.chart_dir = Path(chart_dir)
        if not self.chart_dir.is_dir():
            raise ChartVersionUpgradeError(
                f"{self.chart_dir} does not exist, or is not a dir."
            )

        self.chart_file = self.chart_dir / "Chart.yaml"
        if not self.chart_file.is_file():
            raise ChartVersionUpgradeError(
                f"{self.chart_file} does not exist, or is not a file."
            )

        self.chart_version = chart_version

        self.values_file = self.chart_dir / "values.yaml"
        if self.chart_version and not self.no_tag:
            if not self.values_file.is_file():
                raise ChartVersionUpgradeError(
                    f"{self.values_file} does not exist, or is not a file."
                )

        if app_version:
            self.app_version = app_version
        else:
            self.app_version = self.chart_version

        if image_tag:
            self.image_tag = image_tag
        else:
            self.image_tag = self.chart_version

        self.dependency_name = dependency_name
        self.dependency_version = dependency_version

    def values_run(self) -> None:
        """run values.yaml version upgrade"""

        if self.no_tag:
            print("Image tag upgrade disabled", flush=True)
            return None

        values_data = yaml_file_read(self.values_file)
        if not values_data:
            raise ChartVersionUpgradeError(f"{self.values_file} is empty")

        if not "image" in values_data:
            raise ChartVersionUpgradeError(
                f"{self.values_file} has not entry >image<"
            )
        if not isinstance(values_data["image"], dict):
            raise ChartVersionUpgradeError(
                f"entry >image< in {self.values_file} is not type dict"
            )
        if not "tag" in values_data["image"]:
            raise ChartVersionUpgradeError(
                f"{self.values_file} has not entry >tag< in entry >image<"
            )
        values_data["image"]["tag"] = self.image_tag

        return yaml_file_write(self.values_file, values_data)

    def chart_run(self) -> None:
        """Run Chart.yaml version upgrade"""

        chart_data = yaml_file_read(self.chart_file)
        if not chart_data:
            raise ChartVersionUpgradeError(f"{self.chart_file} is empty")
        if not isinstance(chart_data, dict):
            raise ChartVersionUpgradeError(
                f"{self.chart_file} is not type dict"
            )

        if not "version" in chart_data:
            raise ChartVersionUpgradeError(
                f"{self.chart_file} has not entry >version<"
            )
        chart_data["version"] = self.chart_version

        if not "appVersion" in chart_data:
            raise ChartVersionUpgradeError(
                f"{self.chart_file} has not entry >appVersion<"
            )
        chart_data["appVersion"] = self.app_version

        return yaml_file_write(self.chart_file, chart_data)

    def dependency_run(self) -> None:
        """Run Chart.yaml dependencie version upgrade"""

        chart_data = yaml_file_read(self.chart_file)
        if not chart_data:
            raise ChartVersionUpgradeError(f"{self.chart_file} is empty")
        if not isinstance(chart_data, dict):
            raise ChartVersionUpgradeError(
                f"{self.chart_file} is not type dict"
            )

        if not "dependencies" in chart_data:
            raise ChartVersionUpgradeError(
                f"{self.chart_file} has not entry >dependencies<"
            )
        if not isinstance(chart_data["dependencies"], list):
            raise ChartVersionUpgradeError(
                f"entry >dependencies< in {self.chart_file} is not type dict"
            )

        dependencie = None
        for dep in chart_data["dependencies"]:
            if "name" in dep and dep["name"] == self.dependency_name:
                dependencie = dep
                break
        if not dependencie:
            raise ChartVersionUpgradeError(
                f"Dependencie {self.dependency_name} not found in {self.chart_file}"
            )
        if not isinstance(dependencie, dict):
            raise ChartVersionUpgradeError(
                f"entry >{dependencie['name']}< in {self.chart_file} is not type dict"
            )
        if "version" not in dependencie:
            raise ChartVersionUpgradeError(
                f"{dependencie['name']} has not entry >version<"
            )
        dependencie["version"] = self.dependency_version

        return yaml_file_write(self.chart_file, chart_data)

    def run(self) -> None:
        """Run Chart.yaml and values.yaml version upgrade"""

        if (
            not self.dependency_name or not self.dependency_version
        ) and not self.chart_version:
            raise ChartVersionUpgradeError(
                "Nothing to do! No chart version or dependency_version to upgrade"
            )

        if self.chart_version:
            print("Upgrade Chart version", flush=True)
            self.chart_run()
            self.values_run()
            print(f"Chart version upgraded to {self.chart_version}", flush=True)

        if self.dependency_name and self.dependency_version:
            print("Upgrade Chart dependencie", flush=True)
            self.dependency_run()
            print(
                (
                    f"Chart dependencie {self.dependency_name}"
                    f"upgraded to version {self.dependency_version}"
                ),
                flush=True,
            )


def main() -> int:
    """Upgrade Helm chart version"""

    args = parse_arguments()
    try:
        cvu = ChartVersionUpgrade(
            args.chart_path,
            chart_version=args.chart_version,
            app_version=args.app_version,
            image_tag=args.image_tag,
            dependency_name=args.dependency_name,
            dependency_version=args.dependency_version,
            no_tag=args.no_tag,
        )
        cvu.run()
        return 0
    except ChartVersionUpgradeError as upgrade_error:
        print(upgrade_error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
