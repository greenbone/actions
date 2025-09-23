# SPDX-FileCopyrightText: 2025 Greenbone AG
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import os
import tempfile
import unittest

import yaml

from action.dependabot_config_generator import DependabotConfigGenerator


def create_directories_with_file(target_directories, test_tmp_dir, filename):
    print(f"creating directories with file {filename}")

    for directory in target_directories:
        # in dependabot.yml we must have pathes starting with / but that doesn't work here... so remove it
        dir_path = os.path.join(test_tmp_dir, directory)
        print(f"creating directory {dir_path}")

        os.makedirs(dir_path, exist_ok=True)

        # create an empty file in that directory
        with open(os.path.join(dir_path, filename), 'w'):
            pass

class GeneratorTestCase(unittest.TestCase):
    def test_generator(self):
        """
        Ensure the generator delivers expected results.

        Given:
            * we have a directory structure with 4 directories containing an action.yml
            * 2 of these contain a pyproject.toml

        When:
            * we run the generator with the directory as a first parameter and the template file test_generator.tmpl as second parameter

        Then:
            * we find a file .github/dependabot.yml file in that directory
            * the files contains entries for each directory with an action.yml file in alphabetical order
            * the file contains entries for ech directory with a pyproject.toml file in alphabetical order
            * the entries are relative paths to the root of the directory prefixed with a /
        """

        action_directories = list()

        action_directories.append("a")
        action_directories.append("b")
        action_directories.append("b/a")
        action_directories.append("b/b")
        action_directories.append("c")
        action_directories.append("c/a")
        action_directories.append("c/a/a")
        action_directories.append("c/b/a")

        python_directories = list()
        python_directories.append("b")
        python_directories.append("b/c")
        python_directories.append("c/b")
        python_directories.append("c/b/a")
        python_directories.append("d")

        # other directories where we also put action files, but these should not get dependabot entries
        other_directories = list()
        other_directories.append(".git")
        other_directories.append(".git/a")
        other_directories.append(".github")
        other_directories.append(".github/a")
        other_directories.append(".github/b")
        other_directories.append("__pycache__")

        with tempfile.TemporaryDirectory(delete=False) as test_tmp_dir:
            create_directories_with_file(action_directories, test_tmp_dir, "action.yml")
            create_directories_with_file(python_directories, test_tmp_dir, "pyproject.toml")
            create_directories_with_file(other_directories, test_tmp_dir, "action.yml")

            generator = DependabotConfigGenerator(test_tmp_dir, "test_dependabot.tmpl.yml.j2")
            generator.generate_dependabot_config()

            result_file_path = os.path.join(test_tmp_dir, ".github", "dependabot.yml")
            with open(result_file_path, "r", encoding="utf-8") as result_file:
                test_result_data = yaml.safe_load(result_file.read())

            print(action_directories)
            print(python_directories)

            assert test_result_data["action_dirs"] == action_directories
            assert test_result_data["python_dirs"] == python_directories

if __name__ == '__main__':
    unittest.main()
