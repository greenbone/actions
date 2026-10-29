# Workflow Lint Action

An internally maintained composite action wrapping the MIT-licensed
[rhysd/actionlint v1.7.12](https://github.com/rhysd/actionlint/releases/tag/v1.7.12).
It checks the caller's `.github/workflows` YAML files and repository actionlint
configuration, prints diagnostics, and fails on findings or execution errors.
It does not check out code or install a Go toolchain.

## Requirements and usage

Only **Linux x86_64** is supported initially (for example, `ubuntu-latest`).
Other operating systems and architectures fail explicitly. Runners need Bash,
`uname`, `curl` with HTTPS/CA certificates, `sha256sum`, `tar` with gzip support,
`mktemp`, and `rm` on PATH, network access to GitHub release downloads, and a
writable, executable temporary directory (`TMPDIR`, or the system default).
The caller must check out its repository at `github.workspace` first.

Example reusable workflow (`.github/workflows/workflow-lint.yml`):

```yaml
name: Workflow lint
on: workflow_call
permissions:
  contents: read
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - uses: greenbone/actions/workflow-lint@<reviewed-commit-sha>
```

Replace `<reviewed-commit-sha>` with a reviewed full commit SHA containing this
action before use; it is deliberately a placeholder, not a release reference.
The checkout revision above is the official action revision already used in this
repository. Approved official GitHub/Docker actions remain allowed; this action
avoids a third-party *wrapper action*, not the upstream actionlint CLI.

## Optional script checks

ShellCheck and pyflakes are **separate executables**, not bundled with actionlint
or installed by this action. By default actionlint uses `shellcheck` and
`pyflakes` from PATH to check supported shell and Python `run` scripts. If either
is absent, its checks are skipped and this wrapper prints a warning; a successful
workflow lint does not mean those optional checks ran.

Callers can install these tools before invoking the action, expose them on PATH,
or supply an executable path using the inputs below. Provision and pin them
according to the caller's tool policy. Use empty strings to explicitly disable
them (no missing-tool warning):

```yaml
      - uses: greenbone/actions/workflow-lint@<reviewed-commit-sha>
        with:
          shellcheck: ''
          pyflakes: ''
```

| Input | Default | Meaning |
| --- | --- | --- |
| `shellcheck` | `shellcheck` | Executable name/path, or empty to disable ShellCheck |
| `pyflakes` | `pyflakes` | Executable name/path, or empty to disable pyflakes |

## Integrity and updates

The action downloads `actionlint_1.7.12_linux_amd64.tar.gz` over HTTPS and verifies
it against **the digest committed in `checksums.txt` before extraction or
execution**. It never downloads checksums at runtime. Download, checksum,
extraction, and tool failures fail the step; temporary files are cleaned up.

The initial digest was checked against both the upstream v1.7.12 release checksum
asset and GitHub's release-asset SHA256 metadata, then against the downloaded
archive. These are upstream trust sources, not an independent reproducible-build
attestation.

To update:

1. Select and review an upstream release, its notes, source/tag provenance and
   publishing history. Validate any available upstream provenance/attestations;
   investigate unexpected ownership or artifact changes before proceeding.
2. Obtain the Linux amd64 archive from that release. During maintenance, compare
   its SHA256 with the upstream release checksums and release-asset digest (and
   provenance if available); do not trust only an arbitrary mirror or a freshly
   downloaded checksum at action runtime.
3. Update `version` in `run.sh`, the filename and digest in `checksums.txt`, and
   the version in this document together in a reviewed PR.
4. Rerun the focused tests below, including the tampered-archive check, and review
   changes in diagnostics before callers adopt the new reviewed action revision.

## Focused verification

From the repository root, with Python 3 and the runtime prerequisites installed:

```sh
python3 -m unittest discover -s workflow-lint/tests -v
bash -n workflow-lint/run.sh
```

The tests fetch the pinned archive once (or accept a local archive via
`ACTIONLINT_TEST_ARCHIVE`) and execute the real helper and actionlint on isolated
valid/invalid repository fixtures. They cover download/tool failures, unsupported
platforms, optional integrations and tampered downloads rejected before extraction.
Set `TMPDIR` to an executable filesystem if the default temporary directory is
mounted `noexec`. The focused CI workflow runs these tests without rolling this
action out to other CI workflows or repositories.

## Reporting

Diagnostics are annotated using the unmodified upstream
[v1.7.12 problem matcher](https://github.com/rhysd/actionlint/blob/v1.7.12/.github/actionlint-matcher.json),
vendored as `actionlint-matcher.json`. Update it alongside the pinned binary.
The matcher is removed on exit. A job summary is written by default using Python
3 (required on the runner; available on GitHub-hosted Ubuntu). Lint runs once;
its exact exit status is preserved even if reporting fails. Download/integrity
failures stop before lint and remain visible in the step log.

PR comments are **opt-in**. Set `pr-comment: 'true'`, pass `github-token`, and grant
`pull-requests: write` to the calling job. The token is not needed for annotations
or summaries. Example additions to the caller:

```yaml
permissions:
  contents: read
  pull-requests: write
# ... in the workflow-lint action step:
with:
  pr-comment: 'true'
  github-token: ${{ github.token }}
```

A unique hidden marker scoped to workflow name and job, plus the authenticated
token owner's login, identifies the action's comment. Reruns update that comment,
never an unrelated last comment from the same bot. A clean run marks an existing
comment resolved; it does not create a new success comment. Use a separate job
for independent reports (matrix entries in the same job share a comment).
Non-PR events do not comment; fork PRs and missing tokens skip with a warning.
Read-only or unavailable API access warns without changing lint's status. Keep
using `pull_request`; elevated `pull_request_target` is not needed.

Summaries and comments show total finding/file counts, collapsible sections per
file, and tables of location, rule, and short explanation (up to 300 characters).
Locations link to the actual checked-out Git commit when available, with
URL-encoded paths. They do not dump source excerpts. The same single lint run
provides structured JSON for reporting and matcher-compatible diagnostic lines
for annotations; full messages and execution errors remain in the log.

Untrusted text is entity-escaped for HTML, Markdown, tables, and mentions.
Reports are bounded below 48,000 characters, retaining accurate total counts,
complete sections, a truncation notice when needed, and a full run link.
Runner command parsing is suspended while replaying untrusted diagnostics;
the registered matcher still processes them. Comment reporting uses only Python's
standard library and GitHub's API, with no additional wrapper action.
