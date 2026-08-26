# Copyright (C) 2026 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import unittest
from datetime import datetime, timezone
from types import SimpleNamespace
from typing import Dict, Iterable

from action.artifact import DownloadArtifacts


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

    async def get_workflow_runs(self, *args, **kwargs):
        del args, kwargs
        for run in self.runs:
            yield run


class Artifacts:
    def __init__(self, artifacts: Dict[int, Iterable[SimpleNamespace]]) -> None:
        self.artifacts = artifacts

    async def get_workflow_run_artifacts(self, repository: str, run_id: int):
        del repository
        for stored_artifact in self.artifacts[run_id]:
            yield stored_artifact


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
        downloader.is_debug = False
        downloader.api = SimpleNamespace(
            workflows=Workflows(runs), artifacts=Artifacts(artifacts)
        )
        return downloader

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
