# Lint Python Action

GitHub Action to setup a Python project and lint it via pylint

## Example

```yml
name: Linting

on:
  pull_request:

jobs:
  lint-python:
    name: Setup Python and lint project
    runs-on: ubuntu-latest
    steps:
        - uses: greenbone/actions/lint-python@v2
          with:
            packages: my_project tests
```

## Action Configuration

|Input Variable|Description| |
|--------------|-----------|-|
| packages | Python packages to lint | Required |
| python-version | Python version to use for running the action. | Optional (default is `3.10`) |
| poetry-version | Use a specific poetry version. By default the latest release is used. | Optional (default latest poetry version) |
| cache | Cache dependencies by setting it to `"true"`. Leave unset or set to an other string then `"true"` to disable the cache. | Optional |
| cache-dependency-path | Used to specify the path to dependency files. Supports wildcards or a list of file names for caching multiple dependencies. | Optional |
| cache-poetry-installation | "Cache poetry and its dependencies. Default is `"true"`. Set to an other string then `"true"` to disable the cache." | Optional (default: `"true"`) |
| install-dependencies | Install project dependencies. Default is `"true"`. Set to an other string then `"true"` to not install the dependencies. | Optional (default: `"true"`) |
| linter | Linter to use. Default is 'pylint'. \[pylint, ruff\]| Optional (default: `"pylint")`|
| working-directory | Working directory where to run the action | Optional (default is `${{ github.workspace }}`) |

