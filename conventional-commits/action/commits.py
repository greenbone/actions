# SPDX-FileCopyrightText: 2023 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import NoReturn

from pontos.changelog.conventional_commits import ConventionalCommits


def parse_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("--base-ref", required=True)
    parser.add_argument("--head-ref", required=True)
    parser.add_argument("--working-directory", type=Path, required=True)
    return parser.parse_args()


def run(base_ref: str, head_ref: str, working_directory: Path) -> int:
    working_directory = working_directory.resolve()
    os.chdir(working_directory)
    config_file = working_directory / "changelog.toml"
    collector = ConventionalCommits(
        config=config_file if config_file.exists() else None,
    )
    commit_dict = collector.get_commits(from_ref=base_ref, to_ref=head_ref)

    lines = ["## Conventional Commits Report"]
    if commit_dict:
        lines.extend(["", "| Type | Number |", "|------|-------:|"])

    has_cc = False
    for key, commits in commit_dict.items():
        count = len(commits)
        has_cc = has_cc or bool(count)
        lines.append(f"| {key} | {count} |")

    if has_cc:
        lines.extend(["", ":rocket: Conventional commits found."])
    else:
        lines.extend(
            [
                "",
                ":cry: No conventional commits found.",
                "",
                (
                    ":point_right: [Learn more](https://github.com/greenbone/.github/"
                    "blob/main/conventional-commits/README.md) about the conventional "
                    "commits usage at [Greenbone](https://github.com/greenbone/)."
                ),
            ]
        )

    with Path(os.environ["GITHUB_STEP_SUMMARY"]).open(
        "a", encoding="utf-8"
    ) as summary:
        summary.write("\n".join(lines) + "\n")
    return 0 if has_cc else 1


def main() -> NoReturn:
    args = parse_arguments()
    sys.exit(run(args.base_ref, args.head_ref, args.working_directory))


if __name__ == "__main__":
    main()
