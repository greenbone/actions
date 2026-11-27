# Greenbone Conventional Commits Action

GitHub Action to check for conventional commits. It looks for commits between
a range of git references or git commit IDs. By default it starts looking at the
base commit up to the head commit of a pull request. The report is written to
the GitHub Actions job summary instead of a pull request comment. The action
fails if no conventional commits are found. Existing pull request comments are
not updated or removed.

Callers can switch from `pull_request_target` to `pull_request` and remove
`pull-requests: write` after updating to an action version with summary support.

## Examples

```yml
name: Conventional Commits

on:
  pull_request:

permissions:
  contents: read

jobs:
  conventional-commits:
    name: Report Conventional Commits
    runs-on: ubuntu-latest
    steps:
        - name: Report Conventional Commits
          uses: greenbone/actions/conventional-commits@v3
```

```yml
name: Conventional Commits ignore users foo and bar

on:
  pull_request:

permissions:
  contents: read

jobs:
  conventional-commits:
    if: (!contains(split('foo,bar', ','), github.actor))
    name: Report Conventional Commits
    runs-on: ubuntu-latest
    steps:
        - name: Report Conventional Commits
          uses: greenbone/actions/conventional-commits@v3
```

## Action Configuration

|Input Variable|Description| |
|--------------|-----------|-|
| token | Deprecated and unused; retained for compatibility. | Optional |
| python-version | Python version to use for running the action. | Optional (default is `3.14`) |
| uv-version | Version of uv to use. | Optional (default is the latest release) |
| head-ref | End ref where to look for conventional commits. | Optional (default is`${{ github.event.pull_request.head.sha }}`). |
| base-ref | Start ref where to look for conventional commits. | Optional (default is `${{ github.event.pull_request.base.sha }}`). |
