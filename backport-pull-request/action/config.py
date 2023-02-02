# Copyright (C) 2022 Greenbone Networks GmbH
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

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator

import tomli


@dataclass
class BackportConfig:
    label: str
    source: str
    destination: str


class VerificationIssue:
    def __init__(self, message: str):
        self._message = message

    def __str__(self) -> str:
        return self._message


class Config:
    def __init__(self, config_path: Path):
        self._config_path = config_path

    def _load_backports(self) -> Dict[str, Any]:
        content = self._config_path.read_text(encoding="utf-8")
        data = tomli.loads(content)
        return data.get("backport")

    def verify(self) -> Iterable[VerificationIssue]:
        backports_data = self._load_backports()
        if not backports_data:
            yield VerificationIssue("No backport section found.")
            return

        for key, backport in backports_data.items():
            if not backport.get("label"):
                yield VerificationIssue(
                    f"Missing label entry in [backport.{key}] section."
                )
            if not backport.get("source"):
                yield VerificationIssue(
                    f"Missing source entry in [backport.{key}] section."
                )
            if not backport.get("destination"):
                yield VerificationIssue(
                    f"Missing destination entry in [backport.{key}] section."
                )

    def load(self) -> Iterable[BackportConfig]:
        backports_data = self._load_backports()
        if not backports_data:
            return []

        return [
            BackportConfig(
                label=b.get("label"),
                source=b.get("source"),
                destination=b.get("destination"),
            )
            for _, b in backports_data.items()
        ]
