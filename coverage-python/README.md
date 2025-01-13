# Python Coverage Report

Action to setup Python, poetry, the project itself and afterwards to create a
test coverage report.

## Example

```yaml
name: Code Coverage

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Create Coverage Report
        uses: greenbone/actions/coverage-python@v3
```

## Action Configuration

| Input | Description | |
|-------|-------------|-|
| python-version | Python version that should be installed | Optional (default: "3.10") |
| test-command | Command to run the unit tests | Optional (default: `"-m unittest"`)
| poetry-version | Use a specific poetry version. By default the latest release is used. | Optional (default `latest`) |
| cache | Cache dependencies by setting it to `"true"`. | Optional |
| cache-dependency-path | "Used to specify the path to dependency files. Supports wildcards or a list of file names for caching multiple dependencies. | Optional |
| cache-poetry-installation | Cache poetry and its dependencies by setting it to `"true"`. | Optional |
| install-dependencies | Install project dependencies. Default is `"true"`. Set to an other string then `"true"` to not install the dependencies. | Optional (default: `"true"`) |
| working-directory | Working directory where to run the action | Optional (default is `${{ github.workspace }}`) |
| codecov-upload | "Upload coverage to codecov.io. Default is `"true"`. Set to an other string then `"true"` to disable the upload. | Optional (default: `"true"`)
| token | Upload token for codecov.io. | Required only if codecov-upload is `"true"` |
