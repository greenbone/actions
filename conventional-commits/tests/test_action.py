import base64
import os
import re
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

ACTION = Path(__file__).resolve().parents[1] / "action.yml"


def get_step(name):
    action = ACTION.read_text(encoding="utf-8")
    match = re.search(
        rf"^    - name: {re.escape(name)}\n(.*?)(?=^    - name: |\Z)",
        action,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise ValueError(f"Missing action step: {name}")
    return match.group(1)


def get_script(step):
    match = re.search(
        r"^      run: \|\n((?:^        .*\n)+)", step, re.MULTILINE
    )
    if not match:
        raise ValueError("Missing action script")
    return textwrap.dedent(match.group(1))


class ActionShellTest(unittest.TestCase):
    def test_step_environment_bindings(self):
        expected = {
            "Refs": {
                "REF": "github.ref",
                "REF_NAME": "github.ref_name",
                "HEAD_REF": "github.head_ref",
                "BASE_REF": "github.base_ref",
                "PR_NUMBER": "github.event.pull_request.number",
                "MERGE_COMMIT_SHA": "github.event.pull_request.merge_commit_sha",
                "PR_HEAD_REF": "github.event.pull_request.head.ref",
                "PR_HEAD_SHA": "github.event.pull_request.head.sha",
                "PR_BASE_REF": "github.event.pull_request.base.ref",
                "PR_BASE_SHA": "github.event.pull_request.base.sha",
            },
            "Fetch commits": {
                "HEAD_REF": "inputs.head-ref",
                "FETCH_TOKEN": "github.token",
                "SERVER_URL": "github.server_url",
            },
            "Run conventional commits": {
                "BASE_REF": "inputs.base-ref",
                "HEAD_REF": "inputs.head-ref",
                "WORKSPACE": "github.workspace",
            },
        }
        for name, bindings in expected.items():
            with self.subTest(step=name):
                step = get_step(name)
                actual = dict(
                    re.findall(
                        r"^        (\w+): \$\{\{\s*(.*?)\s*\}\}$",
                        step,
                        re.MULTILINE,
                    )
                )
                self.assertEqual(actual, bindings)

    def test_untrusted_values_are_not_executed_or_split(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = Path(temp_dir)
            marker = directory / "executed"
            args_file = directory / "args"
            payload = f'branch";touch${{IFS}}{marker};#$(touch${{IFS}}{marker})'
            for command in ("git", "uv"):
                executable = directory / command
                executable.write_text(
                    '#!/bin/bash\nprintf "%s\\0" "$@" > "$ARGS_FILE"\n'
                    'if [[ "$0" == */git ]]; then\n'
                    '  printf "%s\\0" "$GIT_CONFIG_COUNT" "$GIT_CONFIG_KEY_0" '
                    '"$GIT_CONFIG_VALUE_0" > "$CONFIG_FILE"\n'
                    "fi\n",
                    encoding="utf-8",
                )
                executable.chmod(0o755)

            env = os.environ | {
                "PATH": f"{directory}:{os.environ['PATH']}",
                "ARGS_FILE": str(args_file),
                "CONFIG_FILE": str(directory / "config"),
                "FETCH_TOKEN": "test-token",
                "SERVER_URL": "https://github.example",
                "REF": payload,
                "REF_NAME": payload,
                "HEAD_REF": payload,
                "BASE_REF": payload,
                "PR_HEAD_REF": payload,
                "PR_BASE_REF": payload,
                "PR_NUMBER": "1",
                "MERGE_COMMIT_SHA": "sha",
                "PR_HEAD_SHA": "sha",
                "PR_BASE_SHA": "sha",
                "WORKSPACE": "workspace with spaces",
            }
            expected_args = {
                "Fetch commits": ["fetch", "--", "origin", payload],
                "Run conventional commits": [
                    "run",
                    "conventional-commits",
                    "--base-ref",
                    payload,
                    "--head-ref",
                    payload,
                    "--working-directory",
                    "workspace with spaces",
                ],
            }
            for name in ("Refs", "Fetch commits", "Run conventional commits"):
                with self.subTest(step=name):
                    script = get_script(get_step(name))
                    self.assertNotIn("${{", script)
                    result = subprocess.run(
                        ["bash", "-e", "-c", script],
                        env=env,
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertFalse(
                        marker.exists(), f"{name} executed the payload"
                    )
                    if name in expected_args:
                        args = (
                            args_file.read_bytes()
                            .decode()
                            .rstrip("\0")
                            .split("\0")
                        )
                        self.assertEqual(args, expected_args[name])
                    if name == "Fetch commits":
                        auth = base64.b64encode(
                            b"x-access-token:test-token"
                        ).decode()
                        config = (
                            (directory / "config")
                            .read_bytes()
                            .decode()
                            .split("\0")
                        )
                        self.assertEqual(
                            config,
                            [
                                "1",
                                "http.https://github.example/.extraheader",
                                f"AUTHORIZATION: basic {auth}",
                                "",
                            ],
                        )

    def test_checkout_does_not_persist_credentials(self):
        self.assertIn(
            "        persist-credentials: false\n",
            get_step("Checkout repository"),
        )


if __name__ == "__main__":
    unittest.main()
