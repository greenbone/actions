# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from argparse import ArgumentParser, Namespace
from typing import Optional, Sequence

import shtab


def parse_args(args: Optional[Sequence[str]] = None) -> Namespace:
    parser = ArgumentParser()
    shtab.add_argument_to(parser)

    parser.add_argument("--some-arg", help="Something")

    return parser.parse_args(args)

def main():
    parse_args
if __name__ == "__main__":
    main()
