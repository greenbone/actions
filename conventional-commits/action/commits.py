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
import os
import sys
from argparse import ArgumentParser, Namespace
from json import JSONDecodeError
from pathlib import Path
from typing import NoReturn, Optional

import httpx
from pontos.changelog.conventional_commits import ConventionalCommits
from pontos.github.actions import Console, GitHubEvent
from pontos.github.api import GitHubAsyncRESTApi

CONVENTIONAL_COMMIT_REPORT_LINE = "<!-- conventional commit report -->"


def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--token", required=True)
    parser.add_argument("--base-ref", required=True)
    parser.add_argument("--head-ref", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--working-directory", type=Path, required=True)
    pr_group = parser.add_mutually_exclusive_group(required=True)
    pr_group.add_argument("--event-path", type=Path)
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
        head_ref: str,
        working_directory: Path,
        event_path: Optional[Path] = None,
        pull_request: Optional[str] = None,
    ) -> None:
        self.repository = repository
        self.token = token
        self.base_ref = base_ref
        self.head_ref = head_ref
        self.working_directory = working_directory
        self.api = GitHubAsyncRESTApi(token)
        if pull_request:
            self.pull_request = pull_request
        else:
            event = GitHubEvent(event_path)
            self.pull_request = event.pull_request.number

    async def run(self) -> int:
        os.chdir(self.working_directory)

        config_file = (self.working_directory / "changelog.toml").absolute()
        collector = ConventionalCommits(
            config=config_file if config_file.exists() else None,
        )
        commit_dict = collector.get_commits(
            from_ref=self.base_ref, to_ref=self.head_ref
        )

        comment_lines = [
            CONVENTIONAL_COMMIT_REPORT_LINE,
            "## Conventional Commits Report",
        ]
        if commit_dict:
            comment_lines.append("| Type | Number |")
            comment_lines.append("|------|-------:|")

        has_cc = False
        for key, commits in commit_dict.items():
            length = len(commits)
            has_cc = has_cc or bool(length)
            comment_lines.append(f"| {key} | {len(commits)} ")

        if has_cc:
            comment_lines.append("")
            comment_lines.append(":rocket: Conventional commits found.")
        else:
            comment_lines.append(":cry: No conventional commits found.")
            comment_lines.append("")
            # pylint: disable=line-too-long
            comment_lines.append(
                ":point_right: [Learn more](https://github.com/greenbone/.github/blob/main/conventional-commits/README.md) "  # noqa: E501
                "about the conventional commits usage at [Greenbone](https://github.com/greenbone/)."
            )

        cc_report_comment = None

        async with self.api as api:
            async for comment in api.pull_requests.comments(
                self.repository, self.pull_request
            ):
                if comment.body and comment.body.startswith(
                    CONVENTIONAL_COMMIT_REPORT_LINE
                ):
                    cc_report_comment = comment.id

            try:
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
            except httpx.HTTPStatusError as e:
                try:
                    json = e.response.json()
                    message = json.get("message")
                except JSONDecodeError:
                    message = None

                if message:
                    raise CommitsError(
                        "Could not create Pull Request comment. A HTTP "
                        f"{e.response.status_code} error occurred while doing "
                        f"a {e.request.method} request to {e.request.url}. "
                        f"Error was {message}"
                    ) from e
                else:
                    raise CommitsError(
                        "Could not create Pull Request comment. A HTTP "
                        f"{e.response.status_code} error occurred while doing a "
                        f"{e.request.method} request to {e.request.url}."
                    ) from e

        return 0 if has_cc else 1


def main() -> NoReturn:
    args = parse_arguments()
    try:
        asyncio.run(
            Commits(
                repository=args.repository,
                token=args.token,
                base_ref=args.base_ref,
                head_ref=args.head_ref,
                event_path=args.event_path,
                pull_request=args.pull_request,
                working_directory=args.working_directory,
            ).run()
        )
        sys.exit(0)
    except CommitsError as e:
        Console.error(f"❌ {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
