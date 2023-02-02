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

import os
import sys
from typing import NoReturn

import httpx
from pontos.git import ConfigScope, Git, GitError
from pontos.github.actions.core import ActionIO, Console
from pontos.github.actions.env import GitHubEnvironment
from pontos.github.actions.event import GitHubEvent
from pontos.github.api import GitHubRESTApi

from action.config import Config

DEFAULT_CONFIG_FILE = "backport.toml"


class BackportError(Exception):
    pass


class Backport:
    def __init__(self) -> None:
        self.token = ActionIO.input("token")
        self.env = GitHubEnvironment()
        self.event = GitHubEvent(self.env.event_path)
        self.api = GitHubRESTApi(self.token, self.env.api_url)
        self.username = ActionIO.input("username") or self.env.actor

    def backport_branch_name(
        self, pull_request: str, destination_branch: str
    ) -> str:
        return f"backport/{destination_branch}/pr-{pull_request}"

    def backport_branch_exists(self, branch_name: str) -> bool:
        return self.api.branch_exists(self.env.repository, branch_name)

    def backport_pull_request(self, pull_request: str, destination_branch: str):
        new_branch = self.backport_branch_name(pull_request, destination_branch)

        # check if backport branch already exists. return if it exists
        if self.backport_branch_exists(new_branch):
            Console.log(f"Backport branch {new_branch} exists. Stopping here.")
            return

        git = Git(cwd=self.env.workspace)

        head = self.env.head_ref
        head_sha = self.event.pull_request.head.sha
        base_sha = self.event.pull_request.base.sha

        # checkout new branch
        Console.log(f"Creating branch {new_branch}")
        git.create_branch(new_branch, start_point=head_sha)

        # rebase
        Console.log(f"Rebasing {new_branch} onto {destination_branch}")
        try:
            git.rebase(
                base_sha,
                head=new_branch,
                onto=f"origin/{destination_branch}",
            )
        except GitError as e:
            Console.error(str(e))
            comment = f"""Failed to backport `{head}` to `{destination_branch}`.

To backport it manually, run these commands in your terminal:

```bash
git checkout -b {new_branch} {head_sha}
git rebase --onto origin/{destination_branch} {base_sha} {new_branch}
```

Afterwards fix the conflicts, push the changes via

```bash
git push origin
```

and create a new pull request where the base is `{destination_branch}` and compare `{new_branch}`.
"""
            self.api.add_pull_request_comment(
                self.env.repository, pull_request, comment
            )
            raise BackportError(
                f"Failed to rebase {new_branch} onto {destination_branch}"
            ) from None

        # push
        Console.log(f"Pushing {new_branch}")
        git.push(remote="origin", branch=new_branch)

        # create PR
        title = f"[Backport #{pull_request}] {self.event.pull_request.title}"
        body = f"This is an automatic backport of pull request #{pull_request}"

        try:
            self.api.create_pull_request(
                self.env.repository,
                head_branch=new_branch,
                base_branch=destination_branch,
                title=title,
                body=body,
            )
        except httpx.HTTPStatusError as e:
            Console.log(f"Error response was {e.response.json()}")
            raise BackportError(
                f"Could not create pull request. Error was {e}"
            ) from None

    def run(self) -> int:
        pull_request = self.event.pull_request

        if not pull_request:
            Console.warning("Not a pull request.")
            return 1

        config_file = ActionIO.input("config", DEFAULT_CONFIG_FILE)

        if not self.token:
            Console.error("Authentication token not provided as input.")

        if not self.env.workspace:
            Console.error("GITHUB_WORKSPACE not set.")
            return 1

        workspace = self.env.workspace.absolute()

        git = Git()
        if not (workspace / ".git").exists():
            Console.log(
                f"Cloning repository {self.env.repository} into {workspace}"
            )

            url = f"https://{self.env.actor}:{self.token}@github.com/{self.env.repository}.git"
            git.clone(url, workspace)

            Console.log(
                f"Cloned repository {self.env.repository} into {workspace}"
            )

            with Console.group(f"Workspace directory content {workspace}"):
                for path in workspace.iterdir():
                    Console.log(path)

            # add extra check to be safe
            if not (workspace / ".git").exists():
                Console.error(
                    "Something went wrong while cloning the repository."
                )
                return 1

        config_path = workspace / config_file
        if not config_path.is_file():
            Console.warning(
                f"No {config_file} file found for backport configuration."
            )
            return 1

        config = Config(config_path)
        has_error = False
        for issue in config.verify():
            has_error = True
            Console.error(str(issue), name=config_file)

        if has_error:
            return 2

        if not pull_request.merged:
            Console.log("Pull Request not merged yet.")
            return 0

        backport_config = config.load()

        labels = [label.name for label in self.event.pull_request.labels]

        with Console.group("Backport config"):
            Console.log(f"Labels: {labels}")
            Console.log(f"Config: {backport_config}")

        if not labels or not backport_config:
            Console.log("Nothing to backport.")
            return 0

        git = Git(cwd=workspace)
        os.chdir(workspace)

        email = f"{self.username}@users.noreply.github.com"
        git.config("user.name", self.username, scope=ConfigScope.LOCAL)
        git.config("user.email", email, scope=ConfigScope.LOCAL)

        is_backport = False
        for bp in backport_config:
            if bp.label in labels and bp.source == self.env.base_ref:
                is_backport = True
                pull_request = self.event.pull_request.number

                try:
                    with Console.group(
                        f"Backporting PR {pull_request} to {bp.destination}"
                    ):
                        self.backport_pull_request(pull_request, bp.destination)
                except BackportError as e:
                    has_error = True
                    Console.error(str(e))
                except Exception as e:  # pylint: disable=broad-except
                    has_error = True
                    Console.error(
                        f"Failed backporting PR {pull_request}. Error was {e}"
                    )

        if has_error:
            return 3

        if not is_backport:
            Console.log("Nothing to backport.")

        return 0


def main() -> NoReturn:
    backport = Backport()

    with Console.group("Settings"):
        Console.log(f"Workspace: {backport.env.workspace}")
        Console.log(f"Ref: {backport.env.ref}")
        Console.log(f"Ref name: {backport.env.ref_name}")
        Console.log(f"Base ref: {backport.env.base_ref}")
        Console.log(f"Head ref: {backport.env.head_ref}")
        Console.log(f"Run ID: {backport.env.run_id}")
        Console.log(f"Action ID: {backport.env.action_id}")

    sys.exit(backport.run())


if __name__ == "__main__":
    main()
