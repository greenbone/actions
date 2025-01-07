# Greenbone Pull Request Backport Action

GitHub Action to backport pull requests.

## Examples

To run this action you need to add the following code to your workflow file
(for example `.github/workflows/backport.yml`):

```yml
name: Backport

on:
  pull_request:
    types:
      - closed
      - labeled

permissions:
  pull-requests: write
  contents: read

jobs:
  backport:
    name: Backport Pull Requests
    runs-on: ubuntu-latest
    steps:
        - name: Backport Pull Request
          uses: greenbone/actions/backport-pull-request@v3
          with:
            token: ${{ secrets.GITHUB_TOKEN }}
```

The workflow file must be present in each branch that should be backported.

Besides the workflow file a backport configuration file must be present in the
default branch (most of the time the `main` branch). The backport configuration
file uses the [TOML](https://toml.io/en/) format and by default the file name is
`backport.toml`. The file name can be adjusted by setting the `config` input in
workflow file of the backport action.

```yaml
        - name: Backport Pull Request
          uses: greenbone/actions/backport-pull-request@v3
          with:
            token: ${{ secrets.GITHUB_TOKEN }}
            config: pyproject.toml
```

## Action Configuration

|Input Variable|Description| |
|--------------|-----------|-|
| token          | Token required to create the backport pull request          | Optional (default is `${{ github.token }}`) |
| config         | TOML based configuration file for backporting pull requests | Optional (default is `backport.toml`) |
| username       | GitHub user name to use for the backported commits          | Optional (by default github.actor is used) |
| python-version | Python version to use for running the action                | Optional (default is `3.10`) |
| poetry-version | Poetry version to use for running the action                | Optional (default is `1.8.0`) |

## TOML Configuration

The TOML configuration specifies when and where a pull request should be
backported. The backport configuration file requires at least a section
([a TOML table](https://toml.io/en/v1.0.0#table)) using the schema
`[backport.<id>]` where `<id>` is a randomly chosen identifier (for example
`rule-1`). The section takes three key/value pairs

* label
* destination
* source

The `label` defines which GitHub needs to be set to activate the backporting
procedure.

The `destination` sets the branch to where to backport the pull request (the
base branch of the to be created backport pull request).

The `source` is optional. If set the backport rule is only applied if the
`source` matches the name of the branch from where to backport the pull request
(the base branch of the current pull request).

Example:
```TOML
[backport.rule-1]
label = "backport-to-main"
source = "develop"
destination = "main"

[backport.rule-2]
label = "backport-to-staging"
destination = "staging"
```

`rule-1` is only applied if the label `backport-to-main` is set and the base
branch is named `develop`. A new backport pull request gets created against the
`main` branch.

`rule-2` is only applied if the label `backport-to-staging` is set. The base
branch of the pull request is not considered. A new backport pull request gets
created against the `staging` branch.
