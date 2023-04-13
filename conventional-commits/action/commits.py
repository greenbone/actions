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


import asyncio
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import NoReturn, Optional

from pontos.changelog import ChangelogBuilder
from pontos.github.actions import Console, GitHubEvent
from pontos.github.api import GitHubAsyncRESTApi

CONVENTIONAL_COMMIT_REPORT_LINE = "<!-- conventional commit report -->"


def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--token", required=True)
    parser.add_argument("--base-ref", required=True)
    parser.add_argument("--repository", required=True)
    pr_group = parser.add_mutually_exclusive_group(required=True)
    pr_group.add_argument("--event-path")
    pr_group.add_argument("--pull-request")
    return parser.parse_args()


class CommitsError(Exception):
    pass


class Commits:
    def __init__(
        self,
        *,
        repository: str,
        token: str,
        base_ref: str,
        event_path: Optional[str] = None,
        pull_request: Optional[str] = None,
    ) -> None:
        self.repository = repository
        self.token = token
        self.base_ref = base_ref
        self.api = GitHubAsyncRESTApi(token)
        if pull_request:
            self.pull_request = pull_request
        else:
            event = GitHubEvent(event_path)
            self.pull_request = event.pull_request.number

    async def run(self) -> int:
        space, project = self.repository.split("/", 1)
        config_file = Path("changelog.toml").absolute()
        builder = ChangelogBuilder(
            git_tag_prefix="",
            space=space,
            project=project,
            config=config_file if config_file.exists() else None,
        )
        commit_dict = builder.get_commits(self.base_ref)

        comment_lines = [
            CONVENTIONAL_COMMIT_REPORT_LINE,
            "## Conventional Commits Report",
        ]
        if commit_dict:
            comment_lines.append("| Type | Number |")
            comment_lines.append("|------|--------|")

        has_cc = False
        for key, commits in commit_dict.items():
            length = len(commits)
            has_cc = has_cc or bool(length)
            comment_lines.append(f"| {key} | {len(commits)} ")

        if has_cc:
            comment_lines.append(":rocket: Conventional commits found.")
        else:
            comment_lines.append(":cry: No conventional commits found.")

        cc_report_comment = None

        async with self.api as api:
            async for comment in api.pull_requests.comments(
                self.repository, self.pull_request
            ):
                if comment.body and comment.body.startswith(
                    CONVENTIONAL_COMMIT_REPORT_LINE
                ):
                    cc_report_comment = comment.id

            if cc_report_comment is None:
                await api.pull_requests.add_comment(
                    self.repository,
                    self.pull_request,
                    "\n".join(comment_lines),
                )
            else:
                await api.pull_requests.update_comment(
                    self.repository,
                    cc_report_comment,
                    "\n".join(comment_lines),
                )

        return 0 if has_cc else 1


def main() -> NoReturn:
    args = parse_arguments()
    try:
        asyncio.run(
            Commits(
                repository=args.repository,
                token=args.token,
                base_ref=args.base_ref,
                event_path=args.event_path,
                pull_request=args.pull_request,
            ).run()
        )
        sys.exit(0)
    except CommitsError as e:
        Console.error(f"{e} ❌.")
        sys.exit(1)


if __name__ == "__main__":
    main()
