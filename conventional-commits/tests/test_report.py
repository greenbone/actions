import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ReportTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.repo = self.directory / "repository with spaces"
        self.repo.mkdir()
        self.summary = self.directory / "summary.md"
        self.summary.write_text("Existing summary\n", encoding="utf-8")
        self.git("init", "-q")
        self.git("config", "user.email", "test@example.com")
        self.git("config", "user.name", "Test")
        self.git("config", "core.hooksPath", "/dev/null")
        self.git("config", "commit.gpgsign", "false")
        self.commit("Initial commit")
        self.base = self.git("rev-parse", "HEAD")

    def git(self, *args):
        result = subprocess.run(
            ["git", *args],
            cwd=self.repo,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()

    def commit(self, message):
        self.git("commit", "--allow-empty", "-q", "-m", message)

    def report(self, summary=True):
        env = os.environ.copy()
        if summary:
            env["GITHUB_STEP_SUMMARY"] = str(self.summary)
        else:
            env.pop("GITHUB_STEP_SUMMARY", None)
        return subprocess.run(
            [
                sys.executable,
                "-m",
                "action.commits",
                "--base-ref",
                self.base,
                "--head-ref",
                "HEAD",
                "--working-directory",
                str(self.repo),
            ],
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_writes_conventional_commits_to_summary(self):
        self.commit("Fix: Correct a problem")
        result = self.report()
        self.assertEqual(result.returncode, 0, result.stderr)
        summary = self.summary.read_text(encoding="utf-8")
        self.assertTrue(summary.startswith("Existing summary\n"))
        self.assertIn("## Conventional Commits Report", summary)
        self.assertIn("| Bug Fixes | 1 |", summary)
        self.assertIn("Conventional commits found.", summary)

    def test_reports_no_conventional_commits_and_fails(self):
        self.commit("Unrecognized change")
        result = self.report()
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn(
            "No conventional commits found.",
            self.summary.read_text(encoding="utf-8"),
        )

    def test_missing_summary_fails(self):
        self.commit("Fix: Correct a problem")
        result = self.report(summary=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("GITHUB_STEP_SUMMARY", result.stderr)


if __name__ == "__main__":
    unittest.main()
