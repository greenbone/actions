# Greenbone Conventional Commits Action

GitHub Action to check for conventional commits

To run this action you need to add the following code to your workflow file
(for example `.github/workflows/backport.yml`):

```yml
name: Conventional Commits

on:
  pull_request:

jobs:
  conventional-commits:
    name: Report Conventional Commits
    runs-on: ubuntu-latest
    steps:
        - name: Report Conventional Commits
          uses: greenbone/actions/conventional-commits@v2
          with:
            token: ${{ secrets.GITHUB_TOKEN }}
```

## Action Configuration

|Input Variable|Description| |
|--------------|-----------|-|
| token          | Token required to create the pull request comments | Required |
| python-version | Python version to use for running the action       | Optional (default is `3.10`) |
| poetry-version | Poetry version to use for running the action       | Optional (default is latest) |
