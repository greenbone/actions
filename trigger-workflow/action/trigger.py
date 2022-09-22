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
import sys
from datetime import datetime, timedelta, timezone
from enum import Enum
from time import time
from typing import Dict, List, Optional, Union

import httpx
from dateutil import parser as dateparser
from pontos.github.actions.core import ActionIO, Console
from pontos.github.actions.env import GitHubEnvironment
from pontos.github.api import GitHubRESTApi

WAIT_FOR_COMPLETION_TIMEOUT = 60 * 60 * 60  # one hour
WAIT_FOR_COMPLETION_INTERVAL = 60 * 60  # one minute

JSON_OBJECT = Dict[str, Union[str, int, bool]]  # pylint: disable=invalid-name
JSON = Union[List[JSON_OBJECT], JSON_OBJECT]


def filter_workflow_dispatch(run: JSON_OBJECT) -> bool:
    event = run.get("event")
    return event == "workflow_dispatch"


def filter_newer_runs(run: JSON_OBJECT, date: datetime) -> bool:
    iso_time: str = run.get("created_at")
    run_time = dateparser.isoparse(iso_time)
    return run_time > date


def parse_int(value: str):
    try:
        return int(value)
    except ValueError:
        return None


def json_dump(value: JSON) -> str:
    return json.dumps(value, indent=2)


def date_now() -> datetime:
    return datetime.now(timezone.utc)  # current time in UTC


class WorkflowRunStatus(Enum):
    ACTION_REQUIRED = "action_required"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    FAILURE = "failure"
    IN_PROGRESS = "in_progress"
    NEUTRAL = "neutral"
    QUEUED = "queued"
    REQUESTED = "requested"
    SKIPPED = "skipped"
    STALE = "stale"
    SUCCESS = "success"
    TIMED_OUT = "timed_out"
    WAITING = "waiting"


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
    ) -> None:
        token = token or ActionIO.input("token")

        self.workflow = workflow or ActionIO.input("workflow")
        self.ref = ref or ActionIO.input("ref")
        self.repository = repository or GitHubEnvironment.repository

        timeout = timeout or ActionIO.input("wait-for-completion-timeout")
        self.timeout = parse_int(timeout)

        interval = interval or ActionIO.input("wait-for-completion-interval")
        self.interval = parse_int(interval)

        self.trigger_date = date_now()
        self.timeout_date = self.trigger_date + timedelta(seconds=self.timeout)
        self.api = GitHubRESTApi(token)

    def get_workflow_runs_fallback(self) -> JSON:
        runs = self.api.get_workflow_runs(self.repository, self.workflow)
        return [run for run in runs if filter_workflow_dispatch(run)]

    def get_new_workflow_run(self) -> JSON_OBJECT:
        runs = self.api.get_workflow_runs(
            self.repository, self.workflow, event="workflow_dispatch"
        )
        if not runs:
            # in the past the backend at GitHub had issues with the event filter
            # we have been advised to remove the event filter until the backend
            # has rebuild some elastic search db indexes. Thus keep this
            # behavior as a fallback
            runs = self.get_workflow_runs_fallback()

        runs = [
            run for run in runs if filter_newer_runs(run, self.trigger_date)
        ]

        Console.debug(f"Filtered workflow runs: {json.dumps(runs, indent=2)}")

        if not runs:
            raise TriggerError("Could not find workflow run.")

        if len(runs) > 1:
            Console.warning(
                "Found more then one workflow run. Using the first one."
            )

        return runs[0]

    def wait_for_completion(self):
        if not self.timeout:
            return

        try:
            run = self.get_new_workflow_run()
        except httpx.HTTPStatusError as e:
            raise TriggerError(
                "Could not determine workflow run. Response was: "
                f"{e.response.status_code}\n{json_dump(e.response.json())}."
            ) from None

        while True:
            time.sleep(self.interval)
            try:
                run = self.api.get_workflow_run(self.repository, run["id"])
            except httpx.HTTPStatusError as e:
                raise TriggerError(
                    "Could not get workflow run information. Response was: "
                    f"{e.response.status_code}\n{json_dump(e.response.json())}."
                ) from None

            try:
                status = WorkflowRunStatus(run["status"])
            except KeyError:
                Console.warning(
                    "Wait for workflow completion. Ignoring unknown status for "
                    f"workflow run: {json_dump(run)}"
                )

            if status == WorkflowRunStatus.COMPLETED:
                break

            if date_now() > self.timeout_date:
                break

    def run(self) -> None:
        Console.log(
            f"Trigger Workflow '{self.workflow}' in repo {self.repository}' "
            f"using ref {self.ref} 🚀."
        )
        try:
            self.api.create_workflow_dispatch(
                self.repository, self.workflow, ref=self.ref
            )
        except httpx.HTTPStatusError as e:
            raise TriggerError(
                "Could not start workflow. Response was: "
                f"{e.response.status_code}\n{json_dump(e.response.json())}."
            ) from None

        self.wait_for_completion()


def main():
    try:
        trigger = Trigger()
        trigger.run()
        sys.exit(0)
    except TriggerError as e:
        Console.error(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
