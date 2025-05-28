#!/bin/env python

# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Script to generate a dependabot config file that ensures all actions are properly checked for all dependency updates,
language-specific as well as dependencies on other actions or workflows.
"""

import os
from os.path import join

from jinja2 import Environment, PackageLoader, select_autoescape


class DependabotConfigGenerator:
    def __init__(self, repository_path, template_file="dependabot.tmpl.yml.j2"):
        self.repository_path = repository_path
        self.template_file = template_file

    def generate_dependabot_config(self):
        # Get the list of all github actions in the repo
        github_action_dirs = list()
        python_project_dirs = list()

        ignore_dirs = list()
        ignore_dirs.append(".git")
        ignore_dirs.append(".github")
        ignore_dirs.append("__pycache__")

        for root, dirs, files in os.walk(self.repository_path):
            print(f"checking dir {root}")
            print(f"dirs: {dirs}")
            print(f"files: {files}")

            # remove ignored dirs from the list of dirs to walk into
            for ignored in ignore_dirs:
                try:
                    dirs.remove(ignored)
                except ValueError:
                    # Allowed to fail if that dir is not there
                    pass

            path_to_add = os.path.relpath(root.strip(), self.repository_path)
            if "action.yml" in files:
                github_action_dirs.append(path_to_add)
            if "pyproject.toml" in files:
                python_project_dirs.append(path_to_add)

        github_action_dirs.sort()
        python_project_dirs.sort()
        print("github_action_dirs:", github_action_dirs)
        print("python_project_dirs:", python_project_dirs)

        # load the template and render it giving it the previously created lists
        env = Environment(
            loader=PackageLoader("action"),
            keep_trailing_newline=True,
            autoescape=select_autoescape(['html', 'xml']),
        )

        template = env.get_template(self.template_file)

        dependabot_file_content = template.render(
            github_action_dirs=github_action_dirs,
            python_project_dirs=python_project_dirs,
        )

        with open(join(self.repository_path, ".github/dependabot.yml"), "w") as f:
            f.write(dependabot_file_content)


def main() -> None:
    generator = DependabotConfigGenerator("..")
    generator.generate_dependabot_config()

if __name__ == "__main__":
    main()
