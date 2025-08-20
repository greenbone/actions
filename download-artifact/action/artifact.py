# Copyright (C) 2022 Greenbone AG
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

import asyncio
import json
import os
import shutil
import stat
import sys
import tempfile
from argparse import ArgumentParser, Namespace
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Generator, Iterable, List, NoReturn, Optional, Union
from zipfile import ZipFile

import httpx
from pontos.github.actions.core import ActionIO, Console
from pontos.github.actions.env import GitHubEnvironment
from pontos.github.api import GitHubAsyncRESTApi
from pontos.github.models import Artifact, WorkflowRun, WorkflowRunStatus


def is_event(run: WorkflowRun, events: Iterable[str]) -> bool:
    """
    Return True if workflow run event is one of the events
    """
    return run.event.value in events


def created_at(run: WorkflowRun) -> datetime:
    return run.created_at


def parse_list(value: str) -> List[str]:
    """
    Parse a csv line into a list of strings.

    Spaces are stripped and removed.
    """
    values = value.split(",")
    values = (value.strip() for value in values)
    return [value for value in values if value]


def parse_int(value: str) -> Optional[int]:
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


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


def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--token", required=True)
    parser.add_argument("--repository", nargs="?")
    parser.add_argument("--workflow", required=True)
    parser.add_argument("--workflow-events", nargs="?")
    parser.add_argument("--branch", required=True)
    parser.add_argument("--name", nargs="?")
    parser.add_argument("--allow-not-found")
    parser.add_argument("--path", required=True)
    parser.add_argument("--user", nargs="?")
    parser.add_argument("--group", nargs="?")
    return parser.parse_args()


class DownloadArtifactsError(Exception):
    pass


class DownloadArtifacts:
    def __init__(
        self,
        *,
        token: Optional[str] = None,
        workflow: Optional[str] = None,
        workflow_events: Optional[str] = None,
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

        workflow_events = workflow_events or ActionIO.input("workflow-events")
        if not workflow_events:
            self.workflow_events = ["schedule", "workflow_dispatch"]
        else:
            self.workflow_events = parse_list(workflow_events)

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

        self.user = parse_int(user or ActionIO.input("user"))
        self.group = parse_int(group or ActionIO.input("group"))

        self.download_path = Path(download_path).absolute()

        allow_not_found = allow_not_found or ActionIO.input("allow-not-found")
        self.allow_not_found = allow_not_found == "true"

        self.is_debug = env.is_debug

        self.api = GitHubAsyncRESTApi(token)

        with Console.group("Settings"):
            Console.log(f"repository: {self.repository}")
            Console.log(f"workflow: {self.workflow}")
            Console.log(f"workflow-events: {self.workflow_events}")
            Console.log(f"branch: {self.branch}")
            Console.log(f"name: {self.name}")
            Console.log(f"path: {self.download_path}")
            Console.log(f"allow-not-found: {self.allow_not_found}")
            Console.log(f"user: {self.user}")
            Console.log(f"group: {self.group}")

    async def get_newest_workflow_run(
        self,
    ) -> Union[Optional[WorkflowRun], Optional[Iterable[Artifact]]]:
        try:
            runs = [
                run
                async for run in self.api.workflows.get_workflow_runs(
                    self.repository,
                    self.workflow,
                    branch=self.branch,
                    status=WorkflowRunStatus.SUCCESS,
                    exclude_pull_requests=True,
                )
                if not self.workflow_events
                or is_event(run, self.workflow_events)
            ]
        except httpx.HTTPStatusError as e:
            if self.allow_not_found and e.response.status_code == 404:
                return None, None

            raise DownloadArtifactsError(f"Could not find workflow. {e}") from e

        if self.is_debug:
            urls = "\n".join([run.html_url for run in runs])
            Console.debug(
                f"Workflow runs for events {self.workflow_events}:\n{urls}"
            )

        if not runs:
            return None, None

        # ensure that newest run is run[0]
        runs = sorted(runs, key=created_at, reverse=True)

        for run in runs:
            artifacts = [
                artifact
                async for artifact in self.api.artifacts.get_workflow_run_artifacts(
                    self.repository, run.id
                )
            ]

            if not self.name:
                return run, artifacts

            # Pick a run that actually contains the requested artifact, otherwise check the next one
            for artifact in artifacts:
                if self.name != artifact.name:
                    Console.log(
                        f"Skipping artifact '{artifact.name} with ID {artifact.id}' "
                        f"because it does not match {self.name}."
                    )
                    continue

                return run, [artifact]

        return None, None

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

    async def download_artifact(self, artifact: Artifact) -> Optional[Artifact]:
        with temp_directory() as temp_dir:
            temp_file = temp_dir / f"{artifact.name}.zip"

            if self.name:
                destination_dir = self.download_path
            else:
                destination_dir = self.download_path / artifact.name

            destination_dir.mkdir(parents=True, exist_ok=True)
            self.adjust_permissions(destination_dir)

            print(
                f"Downloading artifact '{artifact.name}' with ID {artifact.id}",
                end=" ",
            )

            with temp_file.open("wb") as f:
                try:
                    async with self.api.artifacts.download(
                        self.repository, artifact.id
                    ) as download:
                        async for content, _ in download:
                            f.write(content)
                            print(".", end="")
                except httpx.HTTPStatusError as e:
                    raise DownloadArtifactsError(
                        f"HTTP Error {e}: Failed to download '{artifact.name}' with ID "
                        f"{artifact.id}"
                    ) from e
                finally:
                    # add a newline to the print output
                    print()

                Console.log(
                    f"Extracting artifact '{artifact.name}' to "
                    f"'{destination_dir.absolute()}'."
                )

                f.flush()

                zipfile = ZipFile(temp_file)
                for zipinfo in zipfile.infolist():
                    file_path = destination_dir / zipinfo.filename

                    if self.is_debug:
                        Console.debug(f"Extracting '{file_path.absolute()}'")

                    zipfile.extract(zipinfo, destination_dir)
                    self.adjust_permissions(file_path)

            return artifact

    async def run(self) -> None:
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

        async with self.api:
            run, artifacts = await self.get_newest_workflow_run()

            if not run:
                if self.allow_not_found:
                    Console.log("No workflow run found.")
                    return
                else:
                    raise DownloadArtifactsError("No workflow run found.")

            Console.log(f"Using workflow run with ID {run.id} {run.html_url}")

            try:
                tasks = [
                    asyncio.create_task(self.download_artifact(artifact))
                    for artifact in artifacts
                ]
            except httpx.HTTPStatusError as e:
                raise DownloadArtifactsError(
                    f"Could not find workflow run artifacts. {e}"
                ) from e

            artifacts = []
            for task in asyncio.as_completed(tasks):
                artifact = await task
                if artifact:
                    artifacts.append(artifact.name)

            if not artifacts:
                if self.allow_not_found:
                    Console.log("No artifact found.")
                    return
                else:
                    raise DownloadArtifactsError(
                        f"No artifact found for workflow run '{run.id}' in "
                        f"repo '{self.repository}' for workflow "
                        f"'{self.workflow}' and branch '{self.branch}'."
                    )

        ActionIO.output("downloaded-artifacts", json.dumps(artifacts))
        ActionIO.output("total-downloaded-artifacts", len(artifacts))

        Console.log("Downloading artifacts completed successfully ✅.")


def main() -> NoReturn:
    args = parse_arguments()
    try:
        asyncio.run(
            DownloadArtifacts(
                token=args.token,
                repository=args.repository,
                workflow=args.workflow,
                workflow_events=args.workflow_events,
                branch=args.branch,
                name=args.name,
                allow_not_found=args.allow_not_found,
                path=args.path,
                user=args.user,
                group=args.group,
            ).run()
        )
        sys.exit(0)
    except DownloadArtifactsError as e:
        Console.error(f"{e} ❌.")
        sys.exit(1)


if __name__ == "__main__":
    main()
