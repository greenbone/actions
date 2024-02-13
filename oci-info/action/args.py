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
        args (Optional[Sequence[str]]): List of command-line arguments.

    Returns:
        Namespace: Parsed arguments.
    """

    parser = ArgumentParser(
        description="Interact with OCI (Open Container Initiative) compliant registries."
    )
    subparsers = parser.add_subparsers(
        dest="command", help="Available commands"
    )
    shtab.add_argument_to(parser)

    parser.add_argument(
        "--repository", help="Repository name", type=str, required=True
    )
    parser.add_argument(
        "--namespace",
        help="Namespace for the registry",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--user",
        help="User for the registry login",
        type=str,
        required=False,
        default=None,
    )
    parser.add_argument(
        "--password",
        help="Password for the registry login",
        type=str,
        required=False,
        default=None,
    )
    parser.add_argument(
        "--reg-domain",
        help="Registry domain",
        type=str,
        required=False,
        default="ghcr.io",
    )
    parser.add_argument(
        "--reg-auth-domain",
        help="Registry authentication domain",
        type=str,
        required=False,
        default="ghcr.io",
    )
    parser.add_argument(
        "--reg-auth-service",
        help="Registry authentication service",
        type=str,
        required=False,
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
        "--tag", help="Tag to compare", type=str, required=True
    )
    compare_annotations_parser.add_argument(
        "--architecture",
        help="Annotation from architecture to compare",
        type=str,
        required=False,
        default="amd64",
    )
    compare_annotations_parser.add_argument(
        "--compare-repository",
        help="Compare repository name",
        type=str,
        required=True,
    )
    compare_annotations_parser.add_argument(
        "--annotation",
        help="Annotation to compare",
        type=str,
        required=False,
        default="org.opencontainers.image.created",
    )
    compare_annotations_parser.add_argument(
        "--mode",
        help="Annotation to compare",
        type=str,
        required=False,
        default="eq",
        choices=["eq", "lt", "gt"],
    )
    compare_annotations_parser.add_argument(
        "--compare-namespace",
        help="Compare registry Namespace",
        type=str,
        required=False,
        default="library",
    )
    compare_annotations_parser.add_argument(
        "--compare-reg-domain",
        help="Compare registry domain",
        type=str,
        required=False,
        default="registry-1.docker.io",
    )
    compare_annotations_parser.add_argument(
        "--compare-reg-auth-domain",
        help="Compare registry authentication domain",
        type=str,
        required=False,
        default="auth.docker.io",
    )
    compare_annotations_parser.add_argument(
        "--compare-reg-auth-service",
        help="Compare registry authentication service",
        type=str,
        required=False,
        default="registry.docker.io",
    )
    compare_annotations_parser.add_argument(
        "--compare-user",
        help="User for the compare registry login",
        type=str,
        required=False,
        default=None,
    )
    compare_annotations_parser.add_argument(
        "--compare-password",
        help="Password for the compare registry login",
        type=str,
        required=False,
        default=None,
    )

    return parser.parse_args(args)
