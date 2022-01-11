# Greenbone Pull Request Backport Action

GitHub Action to backport pull requests.

To run this action you need to add the following code to your workflow file
(for example `.github/workflows/backport.yml`):

```yml
name: Backport

on:
  pull_request:
    types:
      - closed
      - labeled

jobs:
  backport:
    name: Backport Pull Requests
    runs-on: ubuntu-latest
    steps:
        - name: Backport Pull Request
          uses: greenbone/actions/backport-pull-request@v1
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
          uses: greenbone/actions/backport-pull-request@v1
          with:
            token: ${{ secrets.GITHUB_TOKEN }}
            config: pyproject.toml
```

## Action Configuration

|Input Variable|Description| |
|--------------|-----------|-|
|token|Token required to create the backport pull request|Required|
|config|TOML based configuration file for backporting pull requests|Optional (default is `backport.toml`)|

## TOML Configuration

The TOML configuration specifies when a pull request and where it should be
backported. The backport configuration file requires at least a section
([a TOML table](https://toml.io/en/v1.0.0#table)) using the schema
`[backport.<id>]` where `<id>` is a randomly chosen identifier (for example
`rule-1`). The section takes three key/value pairs

* label
* source
* destination

The `label` defines which GitHub needs to be set to activate the backporting
procedure.
The `source` is the name of the branch from where to backport the pull request.
It is matched against the base branch of a pull request.
The `destination` sets the branch to where to backport the pull request.

Example:
```TOML
[backport.rule-1]
label = "backport-to-main"
source = "develop"
destination = "main"

[backport.rule-2]
label = "backport-to-staging"
source = "main"
destination = "staging"
```
