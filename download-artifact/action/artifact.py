# Copyright (C) 2022 Greenbone Networks GmbH
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

import json
import os
import shutil
import stat
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Generator, Iterable, Optional, Union
from zipfile import ZipFile

import httpx
from dateutil import parser as dateparser
from pontos.github.actions.core import ActionIO, Console
from pontos.github.actions.env import GitHubEnvironment
from pontos.github.api import (
    JSON,
    JSON_OBJECT,
    GitHubRESTApi,
    WorkflowRunStatus,
)


def is_event(run: JSON_OBJECT, events: Iterable[str]) -> bool:
    event = run.get("event")
    return event in events


def created_at(run: JSON_OBJECT):
    iso_time: str = run.get("created_at")
    return dateparser.isoparse(iso_time)


def json_dump(value: JSON) -> str:
    return json.dumps(value, indent=2)


@contextmanager
def temp_directory() -> Generator[Path, None, None]:
    """
    Context Manager to create a temporary directory
    """
    temp_dir = tempfile.TemporaryDirectory()
    dir_path = Path(temp_dir.name)
    try:
        yield dir_path
    finally:
        temp_dir.cleanup()


class DownloadArtifactsError(Exception):
    pass


class DownloadArtifacts:
    def __init__(
        self,
        *,
        token: Optional[str] = None,
        workflow: Optional[str] = None,
        repository: Optional[str] = None,
        branch: Optional[str] = None,
        name: Optional[str] = None,
        path: Optional[str] = None,
        allow_not_found: Optional[str] = None,
        user: Union[str, int] = None,
        group: Union[str, int] = None,
    ) -> None:
        env = GitHubEnvironment()

        token = token or ActionIO.input("token")
        if not token:
            raise DownloadArtifactsError("Missing token.")

        self.workflow = workflow or ActionIO.input("workflow")
        if not self.workflow:
            raise DownloadArtifactsError("Missing workflow.")

        self.branch = branch or ActionIO.input("branch")
        if not self.branch:
            raise DownloadArtifactsError("Missing branch.")

        self.repository = (
            repository or ActionIO.input("repository") or env.repository
        )
        if not self.repository:
            raise DownloadArtifactsError("Missing repository.")

        self.name = name or ActionIO.input("name")

        download_path = path or ActionIO.input("path")
        if not download_path:
            raise DownloadArtifactsError("Missing path.")

        self.user = user or ActionIO.input("user")
        try:
            # try to convert to int for a user id
            self.user = int(self.user)
        except (ValueError, TypeError):
            pass

        self.group = group or ActionIO.input("group")
        try:
            # try to convert to int for a group id
            self.group = int(self.group)
        except (ValueError, TypeError):
            pass

        self.download_path = Path(download_path)

        allow_not_found = allow_not_found or ActionIO.input("allow-not-found")
        self.allow_not_found = allow_not_found == "true"

        self.is_debug = env.is_debug

        self.api = GitHubRESTApi(token)

    def get_newest_workflow_run(self) -> Optional[JSON_OBJECT]:
        try:
            runs = self.api.get_workflow_runs(
                self.repository,
                self.workflow,
                branch=self.branch,
                status=WorkflowRunStatus.SUCCESS.value,
            )
        except httpx.HTTPStatusError as e:
            if self.allow_not_found and e.response.status_code == 404:
                return None

            raise DownloadArtifactsError(f"Could not find workflow. {e}") from e

        if self.is_debug:
            Console.debug(f"Available workflow runs: {json_dump(runs)}")

        runs = [
            run
            for run in runs
            if is_event(run, ["schedule", "workflow_dispatch"])
        ]

        if self.is_debug:
            Console.debug(f"Filtered workflow runs: {json_dump(runs)}")

        if not runs:
            return None

        # ensure that newest run is run[0]
        runs = sorted(runs, key=created_at, reverse=True)

        return runs[0]

    def adjust_permissions(self, file_path: Path) -> None:
        try:
            # should be made configurable via a input variable
            stat_result = os.stat(file_path)
            os.chmod(
                file_path,
                stat_result.st_mode
                | stat.S_IWUSR
                | stat.S_IRUSR
                | stat.S_IWGRP
                | stat.S_IRGRP
                | stat.S_IWOTH
                | stat.S_IROTH,
            )
        except OSError as e:
            Console.warning(
                f"Could not change permissions of '{file_path}'. Error was {e}."
            )

        if self.user:
            try:
                shutil.chown(file_path, self.user)
            except (OSError, LookupError) as e:
                Console.warning(
                    f"Could not change owner of '{file_path}' to user "
                    f"'{self.user}'. Error was {e}."
                )

        if self.group:
            try:
                shutil.chown(file_path, None, self.group)
            except (OSError, LookupError) as e:
                Console.warning(
                    f"Could not change owner of '{file_path}' to group "
                    f"'{self.group}'. Error was {e}."
                )

    def download_artifacts(
        self, artifacts: Iterable[JSON_OBJECT]
    ) -> Iterable[str]:
        artifact_names = []

        with temp_directory() as temp_dir:
            for artifact in artifacts:
                artifact_id = artifact["id"]
                artifact_name = artifact["name"]

                if self.name and self.name != artifact_name:
                    continue

                artifact_names.append(artifact_name)

                temp_file = temp_dir / f"{artifact_name}.zip"

                if self.name:
                    destination_dir: Path = self.download_path
                else:
                    destination_dir: Path = self.download_path / artifact_name

                destination_dir.mkdir(parents=True, exist_ok=True)
                self.adjust_permissions(destination_dir)

                print(
                    f"Downloading artifact '{artifact_name}' with ID "
                    f"{artifact_id}",
                    end=" ",
                )

                with self.api.download_repository_artifact(
                    self.repository, artifact_id, temp_file
                ) as progress_iterator:
                    for _ in progress_iterator:
                        print(".", end="")

                print(" done.")

                Console.log(
                    f"Extracting artifact '{artifact_name}' to "
                    f"'{destination_dir}'."
                )

                zipfile = ZipFile(temp_file)
                for zipinfo in zipfile.infolist():
                    file_path = destination_dir / zipinfo.filename

                    if self.is_debug:
                        Console.debug(f"Extracting '{file_path}'")

                    zipfile.extract(zipinfo, destination_dir)
                    self.adjust_permissions(file_path)

        return artifact_names

    def run(self) -> None:
        if self.name:
            Console.log(
                f"Download '{self.name}' artifact of workflow '{self.workflow}'"
                f" in repo '{self.repository}' using branch '{self.branch}' to "
                f"'{self.download_path}' 🚀."
            )
        else:
            Console.log(
                f"Download artifacts of workflow '{self.workflow}' in repo "
                f"'{self.repository}' using branch '{self.branch}' to "
                f"'{self.download_path}' 🚀."
            )

        run = self.get_newest_workflow_run()

        if not run:
            if self.allow_not_found:
                Console.log("No workflow run found.")
                return
            else:
                raise DownloadArtifactsError("No workflow run found.")

        Console.log(
            f"Using workflow run with ID {run['id']} {run.get('html_url')}"
        )

        try:
            artifacts = self.api.get_workflow_run_artifacts(
                self.repository, run["id"]
            )
        except httpx.HTTPStatusError as e:
            raise DownloadArtifactsError(
                f"Could not find workflow run artifacts. {e}"
            ) from e

        if not artifacts:
            if self.allow_not_found:
                Console.log("No artifact found.")
                return
            else:
                raise DownloadArtifactsError(
                    f"No artifact found for workflow run '{run['id']}' in repo "
                    f"'{self.repository}' for workflow '{self.workflow}' and "
                    f"branch '{self.branch}'."
                )

        downloaded_artifacts = self.download_artifacts(artifacts)

        ActionIO.output(
            "downloaded-artifacts", json.dumps(downloaded_artifacts)
        )
        ActionIO.output("total-downloaded-artifacts", len(downloaded_artifacts))

        Console.log("Downloading artifacts completed successfully ✅.")


def main():
    try:
        download = DownloadArtifacts()
        download.run()
        sys.exit(0)
    except DownloadArtifactsError as e:
        Console.error(f"{e} ❌.")
        sys.exit(1)


if __name__ == "__main__":
    main()
