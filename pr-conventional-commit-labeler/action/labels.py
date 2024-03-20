# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later


import asyncio
import re
import os
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import NoReturn, Optional

from pontos.changelog.conventional_commits import ConventionalCommits
from pontos.github.actions import Console
from pontos.github.api import GitHubAsyncRESTApi
import tomlkit


def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--token", required=False)
    parser.add_argument("--label-config", required=True)
    parser.add_argument("--repository", required=True)
    parser.add_argument("--working-directory", type=Path, required=True)
    parser.add_argument("--pull-request", required=True)
    return parser.parse_args()


class LabelsError(Exception):
    pass


class Labels:
    def __init__(
        self,
        *,
        repository: str,
        token: Optional[str],
        working_directory: Path,
        group_label_config: str,
        pull_request: Optional[str] = None,
    ) -> None:
        self.repository = repository
        self.token = token
        self.working_directory = working_directory
        self.api = GitHubAsyncRESTApi(token)
        self.group_label_config = group_label_config
        self.pull_request = pull_request

    async def run(self) -> None:
        os.chdir(self.working_directory)
        config_file = (self.working_directory / "changelog.toml").absolute()
        Console.log(f"using change log: {config_file}")
        ccl_config = (
            self.working_directory / self.group_label_config
        ).absolute()
        Console.log(f"using label configuration: {ccl_config}")

        collector = ConventionalCommits(
            config=config_file if config_file.exists() else None,
        )

        changelog_groups = [
            x.get("group", "") for x in collector.commit_types()
        ]
        Console.debug(f"got conventional commit groups {changelog_groups}")
        cclc = tomlkit.parse(ccl_config.read_text(encoding="utf-8"))
        labels = cclc.get("labels", [])
        groups = cclc.get("groups", [])
        disable_on = cclc.get("disable_on")
        labels_key = set(map(lambda x: x.get("name", ""), labels))
        only_highest = cclc.get("only_highest_priority", False)
        # verify that groups and labels are known
        for x in groups:
            group = x["group"]
            if group not in changelog_groups:
                raise LabelsError(f"{group} not found in {changelog_groups}")
            label = x["label"]
            if label not in labels_key:
                raise LabelsError(f"{label} not found in {labels_key}")
        # create lookup:
        expressions = [
            (
                commit_type["group"],
                re.compile(rf'{commit_type["message"]}\s?[:|-]', flags=re.I),
            )
            for commit_type in collector.commit_types()
        ]
        lookup = []
        for g in groups:
            for l in labels:
                if g["label"] == l["name"]:
                    g_name = g["group"]
                    matcher = next(x for (g, x) in expressions if g == g_name)
                    lookup.append((matcher, l))
                    break

        async with self.api as api:
            if not self.pull_request:
                raise LabelsError("no PR identifier found")
            original_pr_labels = set(
                [
                    l
                    async for l in api.labels.get_all(
                        self.repository, self.pull_request
                    )
                ]
            )
            if disable_on and any(disable_on in x for x in original_pr_labels):
                Console.log(
                    f"skipping because {self.pull_request} contains {disable_on}"
                )
                return
            unique_labels = original_pr_labels.difference(labels_key)
            if unique_labels:
                Console.debug(f"keeping labels: {unique_labels}")
            commits = [
                c.commit.message
                async for c in api.pull_requests.commits(
                    self.repository, self.pull_request
                )
            ]

            labels = []
            for matcher, label in lookup:
                for c in commits:
                    if matcher.match(c):
                        labels.append(label)
                        break
            labels = sorted(
                labels, key=lambda x: x.get("priority", 0), reverse=True
            )
            if only_highest:
                labels = labels[:1]
            labels = set(l["name"] for l in labels)
            labels.update(unique_labels)
            Console.log(f"set labels: {labels}")
            await api.labels.delete_all(
               self.repository, self.pull_request
            )
            await api.labels.set_all(
                self.repository, self.pull_request, list(labels)
            )


def main() -> NoReturn:
    args = parse_arguments()
    try:
        asyncio.run(
            Labels(
                repository=args.repository,
                token=args.token or os.environ.get("TOKEN", ""),
                group_label_config=args.label_config,
                pull_request=args.pull_request,
                working_directory=args.working_directory,
            ).run()
        )
        sys.exit(0)
    except LabelsError as e:
        Console.error(f"❌ {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
