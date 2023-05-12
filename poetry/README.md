# Poetry Action

A GitHub action to install python and project dependencies via [poetry](https://python-poetry.org/).

## Examples

```yaml
name: Setup Project

on:
  push:
  pull_request:

jobs:
  setup-python-project:
    name: Setup Python and install dependencies
    steps:
      - uses: greenbone/actions/poetry@v2
```

```yaml
name: Setup Project without dev Dependencies

on:
  push:
  pull_request:

jobs:
  setup-python-project:
    name: Setup Python and install main dependencies only
    steps:
      - uses: greenbone/actions/poetry@v2
        with:
          without-dev: "true"
```
## Action Configuration

| Input | Description | |
|-------|-------------|-|
| working-directory | A working directory where to run poetry install | Optional |
| install-dependencies | Install project dependencies. | Optional. Default is `"true"`. Set to an other string then `"true"` to not install the dependencies. |
| no-root | Do not install the project itself, only the dependencies | Optional |
| without-dev | Do not install the development dependencies | Optional |
| cache | Cache dependencies by setting it to 'true'. Leave unset or set to an other string then 'true' to disable the cache. | Optional |
| cache-dependency-path | Used to specify the path to dependency files. Supports wildcards or a list of file names for caching multiple dependencies. See [https://github.com/actions/setup-python#caching-packages-dependencies](https://github.com/actions/setup-python#caching-packages-dependencies) for more details. | Optional |
| cache-poetry-installation | "Cache poetry and its dependencies by setting it to 'true'. Leave unset or set to an other string then 'true' to disable the cache. | Optional |
| poetry-version | Use a specific poetry version. By default the latest release is used. | Optional (default is latest version) |
| python-version | Python version that should be installed and used. | Optional (default: "3.10") |
