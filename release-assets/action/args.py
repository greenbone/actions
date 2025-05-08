# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Module to parse command-line arguments
  for managing GitHub release assets.
"""

from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Optional, Sequence

import shtab


def parse_args(args: Optional[Sequence[str]] = None) -> Namespace:
    """
    Parses command-line arguments for managing GitHub release assets.

    Args:
        args: A list of argument strings to parse.
            If None, defaults to sys.argv.

    Returns:
        Namespace: An argparse Namespace containing the parsed arguments:
            - repository: The GitHub repository name (e.g., "owner/repo").
            - tag: The release tag to operate on.
            - files: List of file paths to upload.
            - mode: Operation mode ("upload" or "download").
            - token: GitHub personal access token.
    """

    parser = ArgumentParser(description="Manage github release assets.")
    shtab.add_argument_to(parser)

    parser.add_argument("--repository", help="Repository name", required=True)
    parser.add_argument(
        "--tag", help="The release tag to manage assets on.", required=True
    )
    parser.add_argument(
        "--files",
        help="Comma seprated list of asset file paths.",
        required=True,
        type=lambda s: [Path(i.strip()) for i in s.split(",")],
    )
    parser.add_argument(
        "--mode",
        help="Available modes are upload. Default is upload.",
        required=True,
        choices=["upload"],
    )
    parser.add_argument("--token", help="Github auth token", required=True)

    return parser.parse_args(args)
