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

import asyncio
import json
import sys
from datetime import datetime, timedelta, timezone
from typing import Dict, Iterable, NoReturn, Optional

import httpx
from pontos.github.actions.core import ActionIO, Console
from pontos.github.actions.env import GitHubEnvironment
from pontos.github.api import JSON, GitHubAsyncRESTApi
from pontos.github.models import Event, WorkflowRun, WorkflowRunStatus

WAIT_FOR_COMPLETION_TIMEOUT = 60 * 60 * 60  # one hour
WAIT_FOR_COMPLETION_INTERVAL = 60 * 60  # one minute
WAIT_FOR_STARTUP_INTERVAL = 10  # 10 seconds


def is_workflow_dispatch(run: WorkflowRun) -> bool:
    return run.event == Event.WORKFLOW_DISPATCH


def is_newer_run(run: WorkflowRun, date: datetime) -> bool:
    return run.created_at > date


def parse_int(value: str) -> Optional[int]:
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


def json_dump(value: JSON) -> str:
    return json.dumps(value, indent=2)


def date_now() -> datetime:
    return datetime.now(timezone.utc)  # current time in UTC


class TriggerError(Exception):
    pass


class Trigger:
    def __init__(
        self,
        *,
        token: Optional[str] = None,
        workflow: Optional[str] = None,
        ref: Optional[str] = None,
        repository: Optional[str] = None,
        timeout: Optional[str] = None,
        interval: Optional[str] = None,
        inputs: Optional[Dict[str, str]] = None,
    ) -> None:
        token = token or ActionIO.input("token")
        if not token:
            raise TriggerError("Missing token.")

        self.workflow = workflow or ActionIO.input("workflow")
        if not self.workflow:
            raise TriggerError("Missing workflow.")

        self.ref = ref or ActionIO.input("ref")
        if not self.ref:
            raise TriggerError("Missing ref.")

        self.repository = repository or ActionIO.input("repository")
        if not self.repository:
            raise TriggerError("Missing repository.")

        timeout = timeout or ActionIO.input("wait-for-completion-timeout")
        self.timeout = parse_int(timeout)

        interval = interval or ActionIO.input("wait-for-completion-interval")
        self.interval = parse_int(interval)

        self.inputs = inputs or ActionIO.input("inputs")

        self.trigger_date = date_now()
        self.timeout_date = (
            self.trigger_date + timedelta(seconds=self.timeout)
            if self.timeout
            else None
        )

        self.is_debug = GitHubEnvironment().is_debug

        self.api = GitHubAsyncRESTApi(token)

    async def get_workflow_runs_fallback(self) -> Iterable[WorkflowRun]:
        # get all workflow runs and filter manually
        return [
            run
            async for run in self.api.workflows.get_workflow_runs(
                self.repository, self.workflow
            )
            if is_workflow_dispatch(run)
        ]

    async def get_new_workflow_run(self) -> Optional[WorkflowRun]:
        runs = [
            run
            async for run in self.api.workflows.get_workflow_runs(
                self.repository, self.workflow, event=Event.WORKFLOW_DISPATCH
            )
        ]

        if self.is_debug:
            Console.debug(f"Available workflow runs: {runs}")

        if not runs:
            # in the past the backend at GitHub had issues with the event filter
            # we have been advised to remove the event filter until the backend
            # has rebuild some elastic search db indexes. Thus keep this
            # behavior as a fallback
            runs = await self.get_workflow_runs_fallback()

        # add some time margin to mitigate system time differences
        trigger_date = self.trigger_date - timedelta(minutes=5)

        runs = [run for run in runs if is_newer_run(run, trigger_date)]

        if self.is_debug:
            Console.debug(f"Filtered workflow runs: {runs}")

        if not runs:
            return None

        if len(runs) > 1:
            Console.warning(
                "Found more then one workflow run. Using the first one."
            )

        # currently the workflows are sorted by creation date while the first
        # one is the newest. Thus if there are more then one runs found let us
        # pick the newest one
        return runs[0]

    async def wait_for_completion(self) -> None:
        if not self.timeout:
            Console.log(
                "Not waiting for workflow run completion. No timeout set."
            )
            return

        Console.log("Waiting for workflow run completion.")

        for _ in range(6):
            try:
                await asyncio.sleep(WAIT_FOR_STARTUP_INTERVAL)
                run = await self.get_new_workflow_run()
                if run:
                    break
            except httpx.HTTPStatusError as e:
                raise TriggerError(
                    "Could not determine workflow run. Response was: "
                    f"{e.response.status_code}\n{json_dump(e.response.json())}."
                ) from None

        if not run:
            raise TriggerError("Could not find workflow run.")

        Console.log(f"Found workflow run {run.id} {run.html_url}")

        while True:
            if self.is_debug:
                Console.debug(f"Checking status of workflow run\n{run}")

            if run.status == WorkflowRunStatus.COMPLETED:
                break

            if date_now() > self.timeout_date:
                raise TriggerError(f"Workflow run {run.id} run timed out.")

            await asyncio.sleep(self.interval)

            try:
                run = await self.api.workflows.get_workflow_run(
                    self.repository, run.id
                )
            except httpx.HTTPStatusError as e:
                raise TriggerError(
                    "Could not get workflow run information. Response was: "
                    f"{e.response.status_code}\n{json_dump(e.response.json())}."
                ) from None

        if run.conclusion != WorkflowRunStatus.SUCCESS.value:
            raise TriggerError(
                f"Workflow run failed with conclusion {run.conclusion}"
            )

        Console.log(f"Workflow run {run.id} completed successfully ✅.")

    async def trigger_workflow(self) -> None:
        Console.log(
            f"Trigger Workflow '{self.workflow}' in repo '{self.repository}' "
            f"using ref '{self.ref}' 🚀."
        )

        try:
            await self.api.workflows.create_workflow_dispatch(
                self.repository, self.workflow, ref=self.ref, inputs=self.inputs
            )
        except httpx.HTTPStatusError as e:
            raise TriggerError(
                "Could not start workflow. Response was: "
                f"{e.response.status_code}\n{json_dump(e.response.json())}."
            ) from None

    async def run(self) -> None:
        async with self.api:
            await self.trigger_workflow()
            await self.wait_for_completion()


def main() -> NoReturn:
    try:
        asyncio.run(Trigger().run())
        sys.exit(0)
    except TriggerError as e:
        Console.error(f"{e} ❌.")
        sys.exit(1)


if __name__ == "__main__":
    main()
