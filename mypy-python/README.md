# Mypy Python Action

GitHub Action to check typings in Python project with [mypy].

## Example

```yml
name: Type checking

on:
  pull_request:

jobs:
  lint-python:
    name: Setup and lint project
    runs-on: ubuntu-latest
    steps:
        - uses: greenbone/actions/mypy-python@v3
          with:
            packages: my_project tests
```

## Action Configuration

|Input Variable|Description| |
|--------------|-----------|-|
| packages | Python packages to check | Required |
| mypy-arguments | Additional arguments to mypy | Optional |
| python-version | Python version to use for running the action. | Optional (default is `3.10`) |
| poetry-version | Use a specific poetry version. By default the latest release is used. | Optional (default `1.8.0` poetry version) |
| cache | Cache dependencies by setting it to `"true"`. Leave unset or set to an other string then `"true"` to disable the cache. | Optional |
| cache-dependency-path | Used to specify the path to dependency files. Supports wildcards or a list of file names for caching multiple dependencies. | Optional |
| cache-poetry-installation | "Cache poetry and its dependencies. Default is `"true"`. Set to an other string then `"true"` to disable the cache." | Optional (default: `"true"`) |
| install-dependencies | Install project dependencies. Default is `"true"`. Set to an other string then `"true"` to not install the dependencies. | Optional (default: `"true"`) |
| working-directory | Working directory where to run the action | Optional (default is `${{ github.workspace }}`) |

[mypy]: https://mypy.readthedocs.io/en/stable/
