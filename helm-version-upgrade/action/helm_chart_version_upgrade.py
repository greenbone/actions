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
Simple script that upgrades dependency versions in
a Helm chart.
"""

import asyncio
import re
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Any, Optional
from pontos.github.api.api import GitHubAsyncRESTApi

from ruamel.yaml import YAML


PREFIX = "opensight-"
SERVICE_DEPENDENCIES = [
    "asset-management-backend",
    "asset-management-frontend",
    "job-system",
    "user-management-backend",
    "user-management-frontend",
    "scan-management-backend",
    "scan-management-frontend",
]
INFRASTRUCURE_DEPENDENCIES = [
    "job-system-postgres",
    "keycloak",
    "opensearch",
    "postgres",
    "rabbitmq",
    "scan-management-postgres",
]


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
        default="charts/",
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
        "-a",
        "--auto",
        type=str,
        help=(
            "Auto update by determining dependecies version by its lates tag. "
            "This will overwrite single dependencies passed as argument."
        ),
        choices=['rc', 'alpha', 'all'],
        default=None
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
    parser.add_argument(
        "--token",
        type=str,
        help="GitHub User Token",
    )
    return parser.parse_args()

def _check_tag(tag, release_type) -> bool:
    """ Check if tag matches required release type """
    alpha: str = r"^v?[0-9]+\.[0-9]+\.[0-9]+\-(a|alpha)[0-9]+$"
    rc: str = r"^v?[0-9]+\.[0-9]+\.[0-9]+\-rc[0-9]+$"
    all_tags: str = r"^v[0-9]+.[0-9]+.[0-9]+$"
    
    if release_type == "all":
        if re.match(all_tags, tag):
            return True
    if release_type == "rc":
        if re.match(rc, tag):
            return True
    if release_type == "alpha":
        if re.match(alpha, tag):
            return True

    return False

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
        *,
        app_version: Optional[str] = None,
        no_tag: Optional[bool] = False,
        release_type: Optional[str] = "all",
        api: Optional[GitHubAsyncRESTApi] = None,
        auto: Optional[str] = None,
    ) -> None:
        self.no_tag = no_tag
        self.api: GitHubAsyncRESTApi = api
        self.auto = auto
        self.release_type = release_type

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

        self.values_file = self.chart_dir / "values.yaml"
        if not self.no_tag:
            if not self.values_file.is_file():
                raise ChartVersionUpgradeError(
                    f"{self.values_file} does not exist, or is not a file."
                )

        if app_version:
            self.app_version = app_version

    def upgrade_all_services(self) -> None:
        """Upgrade all service dependencies (only for product helm chart"""
        for dependency in SERVICE_DEPENDENCIES:
            tag = self.determine_tag(dependency)
            self.update_dependency_version(dependency=dependency, version=tag)


    async def determine_tag(self, dependency: str) -> str:
        """Get the tag of the given dependency by checking latest git tag
        
        Args:
          dependency (str)  The dependency, that should be checked. 
                            Needs to be a repository name
            
        Returns:
            the tag in str
        """
        if not self.api:
            raise ChartVersionUpgradeError("Tags can't be determined without connection to GitHub API")
        async with self.api:
            git_tags = self.api.tags.get_all(f"greenbone/{dependency}")
        for tag in git_tags:
            # check next tag, until tag matches the desired dependency release type
            if _check_tag(tag, self.release_type):
                return tag.replace("v", '')
        raise ChartVersionUpgradeError("No matching tag found.")


    def update_values_file(self, version: str) -> None:
        """Run values.yaml version upgrade

        Args:
          version: Version of the helm chart that should be loaded
        """

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
        values_data["image"]["tag"] = version

        return yaml_file_write(self.values_file, values_data)

    def update_charts_file(self, version: str) -> None:
        """Run Chart.yaml version upgrade
        
        Args:
          version: Version of the helm chart that should be loaded
          
        """

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
        chart_data["version"] = version

        if not "appVersion" in chart_data:
            raise ChartVersionUpgradeError(
                f"{self.chart_file} has not entry >appVersion<"
            )
        chart_data["appVersion"] = version

        return yaml_file_write(self.chart_file, chart_data)

    def update_dependency_version(self, dependency: str, version: str) -> None:
        """Run Chart.yaml dependency version upgrade"""

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

        dependency_dict = None
        for dep in chart_data["dependencies"]:
            if "name" in dep and dep["name"] == f"{PREFIX}{dependency}":
                dependency_dict = dep
                break
        if not dependency_dict:
            raise ChartVersionUpgradeError(
                f"Dependency {self.dependency_name} not found in {self.chart_file}"
            )
        if not isinstance(dependency_dict, dict):
            raise ChartVersionUpgradeError(
                f"Entry >{dependency_dict['name']}< in {self.chart_file} is not type dict"
            )
        if "version" not in dependency_dict:
            raise ChartVersionUpgradeError(
                f"{dependency_dict['name']} has not entry >version<"
            )
        dependency_dict["version"] = version

        return yaml_file_write(self.chart_file, chart_data)

    def run(self, version: str,) -> None:
        """Run Chart.yaml and values.yaml version upgrade"""

        if self.auto:
            asyncio.run(self.upgrade_all_services)
            
        if (
            not self.dependency_name or not self.dependency_version
        ) and not version:
            raise ChartVersionUpgradeError(
                "Nothing to do! No chart version or dependency_version to upgrade"
            )

        if version:
            print("Upgrade Chart version", flush=True)
            self.update_charts_file()
            self.update_values_file()
            print(f"Chart version upgraded to {version}", flush=True)

        if self.dependency_name and self.dependency_version:
            print("Upgrade Chart dependency", flush=True)
            self.dependency_run()
            print(
                (
                    f"Chart dependency {self.dependency_name}"
                    f"upgraded to version {self.dependency_version}"
                ),
                flush=True,
            )


def main() -> int:
    """Upgrade Helm chart version"""

    args = parse_arguments()
    try:
        api = GitHubAsyncRESTApi(args.token)
        cvu = ChartVersionUpgrade(
            args.chart_path,
            app_version=args.app_version,
            image_tag=args.image_tag,
            dependency_name=args.dependency_name,
            dependency_version=args.dependency_version,
            no_tag=args.no_tag,
            api=api,
            auto=args.auto,
        )
        if args.dependency_name and args.dependency_version:
            cvu.run(version=args.version, )
        cvu.run(version=args.version)
        return 0
    except ChartVersionUpgradeError as upgrade_error:
        print(upgrade_error, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
