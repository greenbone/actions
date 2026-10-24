"""Render captured diagnostics and optionally maintain this action's PR comment."""
import hashlib
import json
import os
from pathlib import Path
import sys
import subprocess
from urllib.parse import quote
import urllib.request


def findings_from(output):
    # actionlint's JSON template is a single array, not parsed human diagnostics.
    if not output.strip():
        return []
    try:
        findings = json.loads(output)
        if findings is None:
            return []
        if not isinstance(findings, list):
            return None
        for finding in findings:
            if not all(isinstance(finding.get(key), str) for key in ("filepath", "kind", "message")):
                return None
            if not all(type(finding.get(key)) is int and finding[key] > 0 for key in ("line", "column")):
                return None
        return findings
    except (ValueError, AttributeError):
        return None


def plain(value, limit=300):
    # Numeric entities prevent HTML, Markdown, table and mention injection.
    value = " ".join(value.split())
    if len(value) > limit:
        value = value[:limit] + "…"
    return "".join(c if c.isalnum() or c == " " else f"&#{ord(c)};" for c in value)


def run_url():
    if not os.environ.get("GITHUB_RUN_ID") or not os.environ.get("GITHUB_REPOSITORY"):
        return None
    return (os.environ.get("GITHUB_SERVER_URL", "https://github.com") + "/" +
            quote(os.environ["GITHUB_REPOSITORY"], safe="/") + "/actions/runs/" +
            quote(os.environ["GITHUB_RUN_ID"], safe=""))


def report_body(output, status, revision=None):
    findings = findings_from(output)
    groups = {}
    for finding in findings or []:
        groups.setdefault(finding["filepath"], []).append(finding)
    heading = (f"Workflow lint: {len(findings)} findings across {len(groups)} files"
               if findings is not None else "Workflow lint: findings unavailable")
    result = "Passed — no workflow lint findings." if status == 0 else f"Failed — actionlint exited {status}."
    body = f"## {heading}\n\n{result}\n\n"
    if findings is None or (status != 0 and not findings):
        body += "No structured findings available; see the workflow log for execution diagnostics.\n\n"
    run = run_url()
    footer = f"\n[Full workflow run]({run})\n" if run else "\nFull diagnostics are in the workflow log.\n"
    shown = 0
    for path, entries in groups.items():
        section = f"<details>\n<summary>{plain(path, 500)} — {len(entries)} findings</summary>\n\n"
        section += "| Location | Rule | Finding |\n| --- | --- | --- |\n"
        # Reserve room for a complete section ending and truncation/run notice.
        if len(body) + len(section) > 47000:
            break
        body += section
        group_start = shown
        for finding in entries:
            location = f'{finding["line"]}:{finding["column"]}'
            if revision and os.environ.get("GITHUB_REPOSITORY"):
                url = (os.environ.get("GITHUB_SERVER_URL", "https://github.com") + "/" +
                       quote(os.environ["GITHUB_REPOSITORY"], safe="/") + "/blob/" +
                       quote(revision, safe="") + "/" + quote(path, safe="/") +
                       f'#L{finding["line"]}')
                location = f"[{location}]({url})"
            row = f'| {location} | {plain(finding["kind"], 80)} | {plain(finding["message"])} |\n'
            if len(body) + len(row) > 47000:
                break
            body += row
            shown += 1
        body += "\n</details>\n\n"
        if shown - group_start < len(entries):
            break
    if findings is not None and shown < len(findings):
        body += f"Truncated: showing {shown} of {len(findings)} findings; see the full workflow run.\n"
    return body + footer


def print_diagnostics(output):
    findings = findings_from(output)
    if findings is None:
        print(output, end="")
        return
    for finding in findings:
        # Keep the upstream matcher's file:line:column: message [rule] format.
        message = " ".join(finding["message"].splitlines())
        print(f'{finding["filepath"]}:{finding["line"]}:{finding["column"]}: {message} [{finding["kind"]}]')


def api(path, data=None, method=None):
    request = urllib.request.Request(
        os.environ.get("GITHUB_API_URL", "https://api.github.com") + path,
        data=None if data is None else json.dumps(data).encode(),
        headers={"Authorization": "Bearer " + os.environ["GH_TOKEN"],
                 "Accept": "application/vnd.github+json", "Content-Type": "application/json"},
        method=method,
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def publish_comment(body, status, event, request=api):
    pr = event.get("pull_request")
    if not pr:
        return
    if not os.environ.get("GH_TOKEN") or pr["head"]["repo"]["full_name"] != os.environ["GITHUB_REPOSITORY"]:
        print("::warning::Workflow lint PR comment skipped: no token or fork pull request")
        return
    # Never edit the shared bot's last comment: require marker AND identity.
    viewer = request("/graphql", {"query": "query { viewer { login } }"})["data"]["viewer"]["login"]
    scope = os.environ.get("GITHUB_WORKFLOW", "") + ":" + os.environ.get("GITHUB_JOB", "")
    marker = "<!-- greenbone-workflow-lint:" + hashlib.sha256(scope.encode()).hexdigest()[:20] + " -->"
    endpoint = f'/repos/{os.environ["GITHUB_REPOSITORY"]}/issues/{pr["number"]}/comments'
    existing = None
    page = 1
    while True:
        comments = request(f"{endpoint}?per_page=100&page={page}")
        existing = next((c for c in comments if c.get("body", "").startswith(marker + "\n")
                         and c["user"]["login"] == viewer), None)
        if existing or len(comments) < 100:
            break
        page += 1
    if status == 0 and not existing:
        return
    if status == 0:
        body = body.replace("Passed —", "Resolved —")
    payload = {"body": marker + "\n" + body}
    if existing:
        request(f'/repos/{os.environ["GITHUB_REPOSITORY"]}/issues/comments/{existing["id"]}', payload, "PATCH")
    else:
        request(endpoint, payload, "POST")


def main():
    output = Path(sys.argv[1]).read_text(errors="replace")
    if sys.argv[2] == "--diagnostics":
        print_diagnostics(output)
        return
    status = int(sys.argv[2])
    try:
        revision = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        revision = None
    body = report_body(output, status, revision)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        try:
            with open(summary, "a", encoding="utf-8") as stream:
                stream.write(body)
            print("Workflow lint job summary written")
        except OSError:
            print("::warning::Unable to write workflow lint job summary")
    if os.environ.get("PR_COMMENT") == "true":
        try:
            event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
            publish_comment(body, status, event)
        except Exception:
            # API errors may contain untrusted data; never echo them as commands.
            print("::warning::Workflow lint PR comment unavailable; check token permissions")


if __name__ == "__main__":
    main()
