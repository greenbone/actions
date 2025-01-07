# Greenbone Conventional Commits Action

GitHub Action to check for conventional commits. It looks for commits between
a range of git references or git commit IDs. By default it starts looking at the
base commit up to the head commit of a pull request.

## Examples

```yml
name: Conventional Commits

on:
  pull_request:

permissions:
  pull-requests: write
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
  pull-requests: write
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
| token | GitHub token to create the pull request comments. | Optional (default is [`${{ github.token }}`](https://docs.github.com/en/actions/learn-github-actions/contexts#github-context)) |
| python-version | Python version to use for running the action. | Optional (default is `3.10`) |
| poetry-version | Poetry version to use for running the action. | Optional (default is `1.8.0`) |
| cache-poetry-installation | Cache poetry and its dependencies. | Optional (default is `"true"`) |
| head-ref | End ref where to look for conventional commits. | Optional (default is`${{ github.event.pull_request.head.sha }}`). |
| base-ref | Start ref where to look for conventional commits. | Optional (default is `${{ github.event.pull_request.base.sha }}`). |
