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
