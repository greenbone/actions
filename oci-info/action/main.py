# SPDX-FileCopyrightText: 2024 Greenbone AG
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Main module
"""

import sys

from .args import parse_args
from .oci import Oci
from .oci_model import OciAnnotations


def main() -> int:
    """
    Main function.

    Parses command-line arguments and performs actions accordingly.

    Returns:
        int: Exit status code.
    """

    arg = parse_args(sys.argv[1:])
    if arg.command == "list-tags":
        reg = Oci(
            namespace=arg.namespace,
            reg_domain=arg.reg_domain,
            reg_auth_domain=arg.reg_auth_domain,
            reg_auth_service=arg.reg_auth_service,
            user=arg.user,
            password=arg.password,
        )
        print(reg.get_tags(arg.repository))
    if arg.command == "compare-tags":
        reg = Oci(
            namespace=arg.namespace,
            reg_domain=arg.reg_domain,
            reg_auth_domain=arg.reg_auth_domain,
            reg_auth_service=arg.reg_auth_service,
            user=arg.user,
            password=arg.password,
        )
        ano: OciAnnotations = reg.get_oci_annotations(
            arg.repository, arg.tag, arg.architecture
        )
        reg_com = Oci(
            namespace=arg.compare_namespace,
            reg_domain=arg.compare_reg_domain,
            reg_auth_domain=arg.compare_reg_auth_domain,
            reg_auth_service=arg.compare_reg_auth_service,
            user=arg.compare_user,
            password=arg.compare_password,
        )
        ano_com: OciAnnotations = reg_com.get_oci_annotations(
            arg.compare_repository, arg.tag, arg.architecture
        )
        if ano.created < ano_com.created:
            print("True")
        else:
            print("False")

    return 0


if __name__ == "__main__":
    sys.exit(main())
