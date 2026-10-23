"""Exercise the actual action helper with real actionlint and fault injection."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ACTION = Path(__file__).resolve().parents[1]
VALID = """name: Fixture
on: workflow_call
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - run: echo hello
      - shell: python
        run: print('hello')
"""


class WorkflowLintTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.download = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.download.cleanup)
        filename = (ACTION / "checksums.txt").read_text().split()[1]
        cls.archive = Path(cls.download.name) / filename
        cached = os.environ.get("ACTIONLINT_TEST_ARCHIVE")
        if cached:
            shutil.copyfile(cached, cls.archive)
        else:
            version = filename.split("_")[1]
            subprocess.run([
                "curl", "--fail", "--silent", "--show-error", "--location",
                "--proto", "=https", "--proto-redir", "=https",
                f"https://github.com/rhysd/actionlint/releases/download/v{version}/{filename}",
                "-o", str(cls.archive),
            ], check=True)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="workflow lint ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.repo = self.root / "repo"
        workflows = self.repo / ".github" / "workflows"
        workflows.mkdir(parents=True)
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        self.workflow = workflows / "fixture.yml"
        self.workflow.write_text(VALID)
        self.marker = self.root / "marker"
        self.env = dict(os.environ, ACTION_PATH=str(ACTION),
                        GITHUB_WORKSPACE=str(self.repo), SHELLCHECK="", PYFLAKES="",
                        PATH=f"{self.bin}:{os.environ['PATH']}",
                        TEST_ARCHIVE=str(self.archive), TEST_MARKER=str(self.marker))
        self.stub("curl", 'cp "$TEST_ARCHIVE" "${@: -1}"')

    def stub(self, name, script):
        path = self.bin / name
        path.write_text("#!/usr/bin/env bash\nset -eu\n" + script + "\n")
        path.chmod(0o755)

    def run_action(self):
        return subprocess.run(["bash", str(ACTION / "run.sh")], env=self.env,
                              cwd=self.root, text=True, capture_output=True)

    def test_valid_workflow(self):
        result = self.run_action()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("OK", result.stdout)
        self.assertNotIn("::warning::", result.stdout)

    def test_summary_and_command_injection_guard(self):
        summary = self.root / "summary.md"
        self.env["GITHUB_STEP_SUMMARY"] = str(summary)
        self.stub("tar", """cat > "$4/actionlint" <<'SH'
#!/bin/sh
echo '::error::injected'
echo called >> "$TEST_MARKER"
echo '</pre>@someone'
exit 42
SH
chmod +x "$4/actionlint"
""")
        result = self.run_action()
        self.assertEqual(result.returncode, 42)
        self.assertIn("exited 42", summary.read_text())
        self.assertEqual(self.marker.read_text(), "called\n")
        self.assertIn("&lt;/pre&gt;&#64;someone", summary.read_text())
        lines = result.stdout.splitlines()
        stop = next(line for line in lines if line.startswith("::stop-commands::"))
        token = stop.split("::")[-1]
        self.assertLess(lines.index(stop), lines.index("::error::injected"))
        self.assertGreater(lines.index(f"::{token}::"), lines.index("::error::injected"))
        self.assertIn("::add-matcher::", result.stdout)
        self.assertIn("::remove-matcher owner=actionlint::", result.stdout)

    def test_reporting_failure_does_not_mask_exit(self):
        self.stub("python3", "exit 99")
        self.assertEqual(self.run_action().returncode, 0)
        self.stub("tar", """printf '#!/bin/sh\\nexit 42\\n' > "$4/actionlint"
chmod +x "$4/actionlint"
""")
        self.assertEqual(self.run_action().returncode, 42)

    def test_missing_comment_token_still_summarizes_and_lints(self):
        event = self.root / "event.json"
        event.write_text('{"pull_request":{"number":1,"head":{"repo":{"full_name":"owner/repo"}}}}')
        summary = self.root / "summary.md"
        self.env.update(PR_COMMENT="true", GH_TOKEN="", GITHUB_EVENT_PATH=str(event),
                        GITHUB_STEP_SUMMARY=str(summary), GITHUB_REPOSITORY="owner/repo")
        result = self.run_action()
        self.assertEqual(result.returncode, 0)
        self.assertIn("comment skipped", result.stdout)
        self.assertIn("Passed", summary.read_text())

    def test_invalid_workflow(self):
        self.workflow.write_text(VALID.replace("echo hello", "echo '${{ nonexistent.value }}'"))
        result = self.run_action()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("nonexistent", result.stdout + result.stderr)
        self.assertIn("fixture.yml", result.stdout + result.stderr)

    def test_download_failure_stops_before_extraction(self):
        self.stub("curl", "exit 22")
        self.stub("tar", 'touch "$TEST_MARKER"')
        self.assertEqual(self.run_action().returncode, 22)
        self.assertFalse(self.marker.exists())

    def test_tampered_archive_never_extracted_or_executed(self):
        tampered = self.root / "tampered.tar.gz"
        tampered.write_bytes(self.archive.read_bytes() + b"tampered")
        self.env["TEST_ARCHIVE"] = str(tampered)
        self.stub("tar", 'touch "$TEST_MARKER"')
        result = self.run_action()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAILED", result.stdout + result.stderr)
        self.assertFalse(self.marker.exists())

    def test_execution_failure_propagates(self):
        self.stub("tar", "printf '#!/bin/sh\\nexit 42\\n' > \"$4/actionlint\"\nchmod +x \"$4/actionlint\"")
        self.assertEqual(self.run_action().returncode, 42)

    def test_unsupported_platform_stops_before_download(self):
        for platform in ("Darwin", "aarch64"):
            with self.subTest(platform=platform):
                self.stub("uname", f"echo {platform}")
                self.stub("curl", 'touch "$TEST_MARKER"')
                result = self.run_action()
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("only Linux x86_64", result.stderr)
                self.assertFalse(self.marker.exists())

    def test_missing_optional_tools_are_reported(self):
        self.env.update(SHELLCHECK="missing-shellcheck-for-test", PYFLAKES="missing-pyflakes-for-test")
        result = self.run_action()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Optional executable 'missing-shellcheck-for-test' unavailable", result.stdout)
        self.assertIn("Optional executable 'missing-pyflakes-for-test' unavailable", result.stdout)

    def test_available_optional_tools_are_invoked(self):
        self.stub("shellcheck", 'touch "$TEST_MARKER.shellcheck"\necho "[]"')
        self.stub("pyflakes", 'touch "$TEST_MARKER.pyflakes"')
        self.env.update(SHELLCHECK="shellcheck", PYFLAKES="pyflakes")
        result = self.run_action()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(Path(f"{self.marker}.shellcheck").exists())
        self.assertTrue(Path(f"{self.marker}.pyflakes").exists())


if __name__ == "__main__":
    unittest.main()
