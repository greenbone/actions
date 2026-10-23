"""Reporting safety and comment lifecycle, without GitHub writes."""
import contextlib
import hashlib
import importlib.util
import io
import os
from pathlib import Path
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("report", Path(__file__).resolve().parents[1] / "report.py")
report = importlib.util.module_from_spec(spec)
spec.loader.exec_module(report)


class ReportingTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, GH_TOKEN="test", GITHUB_REPOSITORY="owner/repo",
                              GITHUB_WORKFLOW="Lint", GITHUB_JOB="lint", GITHUB_RUN_ID="123")
        self.env.start()
        self.addCleanup(self.env.stop)
        self.event = {"pull_request": {"number": 7, "head": {"repo": {"full_name": "owner/repo"}}}}
        self.marker = "<!-- greenbone-workflow-lint:" + hashlib.sha256(b"Lint:lint").hexdigest()[:20] + " -->"
        self.comments = []
        self.writes = []
        self.pages = []

    def api(self, path, data=None, method=None):
        if path == "/graphql":
            return {"data": {"viewer": {"login": "bot"}}}
        if method:
            self.writes.append((path, data, method))
            return {}
        self.pages.append(path)
        return self.comments

    def comment(self, number, author, body):
        return {"id": number, "user": {"login": author}, "body": body}

    def publish(self, status=1):
        report.publish_comment(report.report_body("diagnostic", status), status, self.event, self.api)

    def test_create_ignores_other_authors_and_unrelated_bot_comments(self):
        self.comments = [self.comment(1, "someone", self.marker + "\nforged"),
                         self.comment(2, "bot", "hidden unicode report")]
        self.publish()
        self.assertEqual(self.writes[0][2], "POST")
        self.assertTrue(self.writes[0][1]["body"].startswith(self.marker + "\n"))

    def test_update_only_own_marked_comment(self):
        self.comments = [self.comment(1, "someone", self.marker + "\nforged"),
                         self.comment(2, "bot", self.marker + "\nold"),
                         self.comment(3, "bot", "unrelated last comment")]
        self.publish()
        self.assertEqual(len(self.writes), 1)
        self.assertEqual(self.writes[0][0], "/repos/owner/repo/issues/comments/2")
        self.assertEqual(self.writes[0][2], "PATCH")

    def test_clean_run_resolves_existing_but_does_not_create(self):
        self.publish(0)
        self.assertFalse(self.writes)
        self.comments = [self.comment(2, "bot", self.marker + "\nold")]
        self.publish(0)
        self.assertIn("Resolved", self.writes[0][1]["body"])

    def test_pagination_finds_own_comment(self):
        def paginated(path, data=None, method=None):
            if path.endswith("&page=1"):
                return [self.comment(i, "other", "text") for i in range(100)]
            return self.api(path, data, method)
        self.comments = [self.comment(200, "bot", self.marker + "\nold")]
        report.publish_comment("report", 1, self.event, paginated)
        self.assertTrue(self.writes[0][0].endswith("/200"))

    def test_no_token_fork_and_non_pr_skip_api(self):
        def forbidden(*args):
            self.fail("API must not be called")
        with contextlib.redirect_stdout(io.StringIO()):
            with patch.dict(os.environ, GH_TOKEN=""):
                report.publish_comment("text", 1, self.event, forbidden)
            self.event["pull_request"]["head"]["repo"]["full_name"] = "fork/repo"
            report.publish_comment("text", 1, self.event, forbidden)
            report.publish_comment("text", 1, {}, forbidden)

    def test_untrusted_output_is_escaped_and_bounded(self):
        body = report.report_body('</pre><script>x</script>\n```\n@someone\n::error::oops', 1)
        self.assertNotIn("<script>", body)
        self.assertNotIn("@someone", body)
        self.assertIn("&lt;/pre&gt;", body)
        body = report.report_body("<&" * 60000, 1)
        self.assertLess(len(body), 50000)
        self.assertIn("Truncated", body)


if __name__ == "__main__":
    unittest.main()

class UnavailableApiTests(unittest.TestCase):
    def test_denied_comment_still_writes_summary(self):
        import tempfile
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            diagnostics = root / 'diagnostics'
            diagnostics.write_text('a finding')
            event = root / 'event.json'
            event.write_text('{"pull_request":{"number":1,"head":{"repo":{"full_name":"owner/repo"}}}}')
            summary = root / 'summary'
            with patch.dict(os.environ, PR_COMMENT='true', GH_TOKEN='test',
                            GITHUB_EVENT_PATH=str(event), GITHUB_STEP_SUMMARY=str(summary),
                            GITHUB_REPOSITORY='owner/repo'), \
                    patch.object(report.sys, 'argv', ['report.py', str(diagnostics), '42']), \
                    patch.object(report.urllib.request, 'urlopen', side_effect=PermissionError('denied')), \
                    contextlib.redirect_stdout(io.StringIO()) as output:
                report.main()
            self.assertIn('exited 42', summary.read_text())
            self.assertIn('comment unavailable', output.getvalue())
