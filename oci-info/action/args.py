# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Module to parse command-line arguments.
"""

from argparse import ArgumentParser, Namespace
from typing import Optional, Sequence

import shtab


def parse_args(args: Optional[Sequence[str]] = None) -> Namespace:
    """
    Parse command-line arguments.

    Args:
        args: List of command-line arguments.

    Returns:
        Parsed arguments.
    """

    parser = ArgumentParser(
        description="Interact with OCI (Open Container Initiative) compliant registries."
    )
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands", required=True
    )
    shtab.add_argument_to(parser)

    parser.add_argument("--repository", help="Repository name", required=True)
    parser.add_argument(
        "--namespace",
        help="Namespace for the registry",
        required=True,
    )
    parser.add_argument(
        "--user",
        help="User for the registry login",
    )
    parser.add_argument(
        "--password",
        help="Password for the registry login",
    )
    parser.add_argument(
        "--reg-domain",
        help="Registry domain",
        default="ghcr.io",
    )
    parser.add_argument(
        "--reg-auth-domain",
        help="Registry authentication domain",
        default="ghcr.io",
    )
    parser.add_argument(
        "--reg-auth-service",
        help="Registry authentication service",
        default="ghcr.io",
    )

    # list_tags_parser
    list_tags_parser = subparsers.add_parser(
        "list-tags",
        help="List tags of an repository in an OCI compliant registry",
    )

    # compare_annotations_parser
    compare_annotations_parser = subparsers.add_parser(
        "compare-tag-annotation",
        help="Compare repository annotations in different registries",
    )
    compare_annotations_parser.add_argument(
        "--tag", help="Tag to compare", required=True
    )
    compare_annotations_parser.add_argument(
        "--architecture",
        help="Annotation from architecture to compare",
        default="amd64",
    )
    compare_annotations_parser.add_argument(
        "--compare-repository",
        help="Compare repository name",
        required=True,
    )
    compare_annotations_parser.add_argument(
        "--annotation",
        help="Annotation to compare",
        default="org.opencontainers.image.created",
    )
    compare_annotations_parser.add_argument(
        "--mode",
        help="Annotation to compare",
        default="eq",
        choices=["eq", "lt", "gt"],
    )
    compare_annotations_parser.add_argument(
        "--compare-namespace",
        help="Compare registry Namespace",
        default="library",
    )
    compare_annotations_parser.add_argument(
        "--compare-reg-domain",
        help="Compare registry domain",
        default="registry-1.docker.io",
    )
    compare_annotations_parser.add_argument(
        "--compare-reg-auth-domain",
        help="Compare registry authentication domain",
        default="auth.docker.io",
    )
    compare_annotations_parser.add_argument(
        "--compare-reg-auth-service",
        help="Compare registry authentication service",
        default="registry.docker.io",
    )
    compare_annotations_parser.add_argument(
        "--compare-user",
        help="User for the compare registry login",
        default=None,
    )
    compare_annotations_parser.add_argument(
        "--compare-password",
        help="Password for the compare registry login",
        default=None,
    )

    return parser.parse_args(args)
