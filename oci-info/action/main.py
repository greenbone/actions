# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Main module
"""

import sys

from .args import parse_args
from .oci import Oci


def main() -> int:
    """
    Main function.

    Parses command-line arguments and performs actions accordingly.

    Returns:
        int: Exit status code.
    """

    arg = parse_args(sys.argv[1:])

    reg = Oci(
        namespace=arg.namespace,
        reg_domain=arg.reg_domain,
        reg_auth_domain=arg.reg_auth_domain,
        reg_auth_service=arg.reg_auth_service,
        user=arg.user,
        password=arg.password,
    )

    if arg.command == "list-tags":
        for tag in reg.get_tags(arg.repository).tags:
            print(tag)
    elif arg.command == "compare-tag-annotation":
        reg_com = Oci(
            namespace=arg.compare_namespace,
            reg_domain=arg.compare_reg_domain,
            reg_auth_domain=arg.compare_reg_auth_domain,
            reg_auth_service=arg.compare_reg_auth_service,
            user=arg.compare_user,
            password=arg.compare_password,
        )

        ano: dict = reg.get_oci_annotations(
            arg.repository, arg.tag, arg.architecture
        ).dict(by_alias=True)
        ano_com: dict = reg_com.get_oci_annotations(
            arg.compare_repository, arg.tag, arg.architecture
        ).dict(by_alias=True)

        if arg.mode == "eq":
            print(ano[arg.annotation] == ano_com[arg.annotation])
        elif arg.mode == "lt":
            print(ano[arg.annotation] < ano_com[arg.annotation])
        elif arg.mode == "gt":
            print(ano[arg.annotation] > ano_com[arg.annotation])

    return 0


if __name__ == "__main__":
    sys.exit(main())
