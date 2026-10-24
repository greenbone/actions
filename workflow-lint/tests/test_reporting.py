"""Reporting safety and comment lifecycle, without GitHub writes."""
import contextlib
import hashlib
import importlib.util
import io
import json
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
        report.publish_comment(report.report_body("[]", status), status, self.event, self.api)

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

    def finding(self, **overrides):
        return dict(filepath=".github/workflows/a.yml", line=12, column=3,
                    kind="expression", message="Unknown property", **overrides)

    def test_grouped_counts_links_and_no_source_dump(self):
        first = self.finding()
        first["snippet"] = "SOURCE MUST NOT APPEAR"
        second = dict(first, filepath=".github/workflows/a #[]().yml", line=25)
        body = report.report_body(json.dumps([first, first, second]), 1, "abc123")
        self.assertIn("Workflow lint: 3 findings across 2 files", body)
        self.assertEqual(body.count("<details>"), 2)
        self.assertIn("| Location | Rule | Finding |", body)
        self.assertIn("[<code>12:3</code>](https://github.com/owner/repo/blob/abc123/.github/workflows/a.yml#L12)", body)
        self.assertIn("a%20%23%5B%5D%28%29.yml#L25", body)
        self.assertNotIn("SOURCE MUST NOT APPEAR", body)
        self.assertIn("[Full workflow run](https://github.com/owner/repo/actions/runs/123)", body)

    def test_untrusted_output_is_escaped_and_bounded(self):
        finding = self.finding()
        finding.update(message='</details><script>x</script> `code` @someone | [link](url)\nnewline',
                       filepath='@bad/<details>|[file].yml', kind='evil|`<script>')
        body = report.report_body(json.dumps([finding]), 1, "abc123")
        self.assertNotIn("<script>", body)
        self.assertNotIn("@someone", body)
        self.assertNotIn("`code`", body)
        self.assertIn("&#60;&#47;details&#62;", body)
        self.assertEqual(body.count("<details>"), body.count("</details>"))
        finding["message"] = "<&" * 60000
        body = report.report_body(json.dumps([finding] * 1000), 1, "abc123")
        self.assertLess(len(body), 48000)
        self.assertIn("1000 findings across 1 files", body)
        self.assertIn("Truncated", body)
        self.assertEqual(body.count("<details>"), body.count("</details>"))
        self.assertIn("Full workflow run", body)

    def test_code_formatting_preserves_prose_and_escaping(self):
        finding = self.finding()
        finding["message"] = 'property "nvd_api_key" is unknown; SC2086: Double quote'
        body = report.report_body(json.dumps([finding]), 1)
        self.assertIn('<code>expression</code>', body)
        self.assertIn('<summary><code>' + report.plain(finding["filepath"]) + '</code>', body)
        self.assertIn('property <code>&#34;nvd&#95;api&#95;key&#34;</code> is unknown', body)
        self.assertIn('<code>SC2086</code>&#58; Double quote', body)
        hostile = '"</code>`|[x](url)&"'
        self.assertEqual(report.message_text(hostile), '<code>' + report.plain(hostile) + '</code>')
        escaped = r'label "a\"b" is unknown'
        self.assertEqual(report.message_text(escaped),
                         'label <code>' + report.plain(r'"a\"b"') + '</code> is unknown')
        self.assertEqual(report.message_text("can't parse `input`"), report.plain("can't parse `input`"))
        # A quoted token cut by the existing message limit stays safe, plain text.
        truncated = 'property "' + 'x' * 400
        self.assertEqual(report.message_text(truncated), report.plain(truncated))

    def test_execution_errors_are_not_misreported_as_clean(self):
        for output in ("[]", "null", "not json", '[{"line": "bad"}]'):
            body = report.report_body(output, 42)
            self.assertIn("exited 42", body)
            self.assertNotIn("Passed", body)
            self.assertIn("execution diagnostics", body)
        self.assertIn("findings unavailable", report.report_body("not json", 42))

    def test_messages_are_short_and_locations_without_revision_are_unlinked(self):
        finding = self.finding()
        finding["message"] = "x" * 1000
        body = report.report_body(json.dumps([finding]), 1)
        self.assertIn("x" * 300 + "&#8230;", body)
        self.assertNotIn("x" * 301, body)
        self.assertIn("| <code>12:3</code> |", body)

    def test_diagnostic_replay_matches_upstream_annotation_pattern(self):
        import re
        matcher = json.loads((Path(report.__file__).parent / "actionlint-matcher.json").read_text())
        pattern = matcher["problemMatcher"][0]["pattern"][0]["regexp"]
        with contextlib.redirect_stdout(io.StringIO()) as output:
            report.print_diagnostics(json.dumps([self.finding()]))
        match = re.match(pattern, output.getvalue().strip())
        self.assertIsNotNone(match)
        self.assertEqual(match.groups(), (".github/workflows/a.yml", "12", "3", "Unknown property", "expression"))


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
