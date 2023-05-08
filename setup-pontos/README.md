# Setup Pontos Action

GitHub Action to setup [pontos](https://github.com/greenbone/pontos) for your
action or workflow.

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
          uses: greenbone/actions/conventional-commits@v2
          with:
            token: ${{ secrets.SOME_TOKEN }}
```

## Action Configuration

|Input Variable|Description| |
|--------------|-----------|-|
| token | GitHub token to create the pull request comments. | Optional (default is [`github.token`](https://docs.github.com/en/actions/learn-github-actions/contexts#github-context)) |
| python-version | Python version to use for running the action. | Optional (default is `3.10`) |
| poetry-version | Poetry version to use for running the action. | Optional (default is latest) |
| cache-poetry-installation | Cache poetry and its dependencies. | Optional (default is `true`) |
