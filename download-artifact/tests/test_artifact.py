# Copyright (C) 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from datetime import datetime, timezone
from types import SimpleNamespace
from typing import Dict, Iterable
from unittest.mock import AsyncMock, patch

from action.artifact import (
    DownloadArtifacts,
    SuspiciousWorkflowRunsError,
)


def timestamp(day: int) -> datetime:
    return datetime(2026, 8, day, tzinfo=timezone.utc)


def workflow_run(run_id: int, day: int) -> SimpleNamespace:
    return SimpleNamespace(
        id=run_id,
        created_at=timestamp(day),
        html_url=f"https://example.invalid/runs/{run_id}",
        event=SimpleNamespace(value="schedule"),
    )


def artifact(
    artifact_id: int, name: str, day: int, *, expired: bool = False
) -> SimpleNamespace:
    return SimpleNamespace(
        id=artifact_id,
        name=name,
        created_at=timestamp(day),
        expired=expired,
    )


class Workflows:
    def __init__(self, runs: Iterable[SimpleNamespace]) -> None:
        self.runs = runs
        self.kwargs = None

    async def get_workflow_runs(self, *args, **kwargs):
        del args
        self.kwargs = kwargs
        for run in self.runs:
            yield run


class Artifacts:
    def __init__(self, artifacts: Dict[int, Iterable[SimpleNamespace]]) -> None:
        self.artifacts = artifacts

    async def get_workflow_run_artifacts(self, repository: str, run_id: int):
        del repository
        for stored_artifact in self.artifacts[run_id]:
            yield stored_artifact


class RetryingWorkflows:
    def __init__(self, run_sets: Iterable[Iterable[SimpleNamespace]]) -> None:
        self.run_sets = iter(run_sets)

    async def get_workflow_runs(self, *args, **kwargs):
        del args, kwargs
        for run in next(self.run_sets):
            yield run


class DownloadArtifactsTestCase(unittest.IsolatedAsyncioTestCase):
    def downloader(
        self,
        runs: Iterable[SimpleNamespace],
        artifacts: Dict[int, Iterable[SimpleNamespace]],
        name: str | None = "release-artifact",
        search_older_runs: bool = False,
    ) -> DownloadArtifacts:
        downloader = object.__new__(DownloadArtifacts)
        downloader.repository = "example/repository"
        downloader.workflow = "publish.yml"
        downloader.branch = "main"
        downloader.workflow_status = "success"
        downloader.workflow_events = ["schedule"]
        downloader.name = name
        downloader.search_older_runs = search_older_runs
        downloader.allow_not_found = False
        downloader.is_debug = False
        downloader.api = SimpleNamespace(
            workflows=Workflows(runs), artifacts=Artifacts(artifacts)
        )
        return downloader

    async def test_passes_success_status_to_github_unchanged(self) -> None:
        run = workflow_run(1, 25)
        downloader = self.downloader(
            [run], {run.id: [artifact(10, "release-artifact", 25)]}
        )

        await downloader._get_newest_workflow_run()

        self.assertEqual(downloader.api.workflows.kwargs["status"], "success")

    def test_rejects_duplicate_workflow_run_ids(self) -> None:
        run = workflow_run(1, 25)
        downloader = self.downloader([], {})

        with self.assertRaises(SuspiciousWorkflowRunsError):
            downloader._validate_workflow_runs([run, run])

    async def test_retries_duplicate_workflow_run_ids(self) -> None:
        duplicate = workflow_run(1, 25)
        usable = workflow_run(2, 24)
        downloader = self.downloader(
            [], {usable.id: [artifact(20, "release-artifact", 24)]}
        )
        downloader.api.workflows = RetryingWorkflows(
            [[duplicate, duplicate], [usable]]
        )

        with patch("action.artifact.asyncio.sleep", new=AsyncMock()):
            run, artifacts = await downloader.get_newest_workflow_run()

        self.assertEqual(run.id, usable.id)
        self.assertEqual([artifact.id for artifact in artifacts], [20])

    async def test_selects_newest_non_expired_named_artifact(self) -> None:
        old_run = workflow_run(1, 3)
        new_run = workflow_run(2, 25)
        downloader = self.downloader(
            [old_run, new_run],
            {
                old_run.id: [
                    artifact(10, "release-artifact", 3, expired=True),
                ],
                new_run.id: [artifact(20, "release-artifact", 25)],
            },
        )

        run, artifacts = await downloader.get_newest_workflow_run()

        self.assertEqual(run.id, new_run.id)
        self.assertEqual([artifact.id for artifact in artifacts], [20])

    async def test_selects_newest_run_when_runs_are_unordered(
        self,
    ) -> None:
        older_artifact_run = workflow_run(1, 25)
        newer_artifact_run = workflow_run(2, 24)
        downloader = self.downloader(
            [older_artifact_run, newer_artifact_run],
            {
                older_artifact_run.id: [
                    artifact(10, "release-artifact", 24),
                ],
                newer_artifact_run.id: [
                    artifact(20, "release-artifact", 25),
                ],
            },
            search_older_runs=True,
        )

        run, artifacts = await downloader.get_newest_workflow_run()

        self.assertEqual(run.id, newer_artifact_run.id)
        self.assertEqual([artifact.id for artifact in artifacts], [20])

    async def test_unnamed_download_skips_runs_with_only_expired_artifacts(
        self,
    ) -> None:
        old_run = workflow_run(1, 24)
        new_run = workflow_run(2, 25)
        downloader = self.downloader(
            [old_run, new_run],
            {
                old_run.id: [artifact(10, "available", 24)],
                new_run.id: [artifact(20, "expired", 25, expired=True)],
            },
            name=None,
            search_older_runs=True,
        )

        run, artifacts = await downloader.get_newest_workflow_run()

        self.assertEqual(run.id, old_run.id)
        self.assertEqual([artifact.id for artifact in artifacts], [10])

    async def test_does_not_search_older_runs_by_default(self) -> None:
        old_run = workflow_run(1, 24)
        new_run = workflow_run(2, 25)
        downloader = self.downloader(
            [old_run, new_run],
            {
                old_run.id: [artifact(10, "release-artifact", 24)],
                new_run.id: [
                    artifact(20, "release-artifact", 25, expired=True),
                ],
            },
        )

        run, artifacts = await downloader.get_newest_workflow_run()

        self.assertIsNone(run)
        self.assertIsNone(artifacts)


if __name__ == "__main__":
    unittest.main()
