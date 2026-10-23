"""Render captured diagnostics and optionally maintain this action's PR comment."""
import hashlib
import html
import json
import os
from pathlib import Path
import sys
import urllib.request


def report_body(output, status):
    result = "Passed — no workflow lint findings." if status == 0 else f"Failed — actionlint exited {status}."
    # Escape before bounding: source cannot inject Markdown/HTML or mentions.
    details = html.escape(output).replace("@", "&#64;")
    if len(details) > 48000:
        details = details[:48000] + "\n[Truncated; see the workflow log for full diagnostics.]"
    return f"## Workflow lint\n\n{result}\n\n<pre>{details or 'No diagnostics.'}</pre>\n"


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
    run = (os.environ.get("GITHUB_SERVER_URL", "https://github.com") + "/" +
           os.environ["GITHUB_REPOSITORY"] + "/actions/runs/" + os.environ["GITHUB_RUN_ID"])
    payload = {"body": marker + "\n" + body + f"\n[Workflow run]({run})\n"}
    if existing:
        request(f'/repos/{os.environ["GITHUB_REPOSITORY"]}/issues/comments/{existing["id"]}', payload, "PATCH")
    else:
        request(endpoint, payload, "POST")


def main():
    output = Path(sys.argv[1]).read_text(errors="replace")
    status = int(sys.argv[2])
    body = report_body(output, status)
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
