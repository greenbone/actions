#!/bin/env python

# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Script to generate a dependabot config file that ensures all actions are properly checked for all dependency updates,
language-specific as well as dependencies on other actions or workflows.

TODO:
* ensure the generated dependabot config works and solves the issue we have with the old one
* add tests
* make this an action that generates and also commits and pushes the newly generated dependabot file
* make the action generically useable?
    * That would require to use a user-specified template for the dependabot file!
"""

import os
from os.path import join

from jinja2 import Environment, PackageLoader, select_autoescape

# Get the list of all github actions in the repo
github_action_dirs = list()
python_project_dirs = list()

for root, dirs, files in os.walk('..'):
    for dirname in dirs:
        if os.path.exists(join(root, dirname, "action.yml")):
            github_action_dirs.append(dirname)
        if os.path.exists(join(root, dirname, "pyproject.toml")):
            python_project_dirs.append(dirname)

# load the template and render it giving it the previously created lists
env = Environment(
    loader=PackageLoader("action"),
)

template = env.get_template("dependabot.tmpl.yml.j2")

dependabot_file_content = template.render(
    github_action_dirs=github_action_dirs, python_project_dirs=python_project_dirs)

with open("../../.github/dependabot.yml","w") as f:
    f.write(dependabot_file_content)
