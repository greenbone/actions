# ty Python Action

GitHub Action to check typings in Python project with [ty](https://docs.astral.sh/ty/).

This action supports both **Poetry** and **uv** dependency managers.

## Examples

### Poetry Project (Default)

```yml
name: Type checking

on:
  pull_request:

jobs:
  type-check:
    name: Check types with ty
    runs-on: ubuntu-latest
    steps:
 - uses: actions/checkout@v4
 - uses: greenbone/actions/ty-python@v3
        with:
          packages: my_project tests
```

### uv Project

```yml
name: Type checking

on:
  pull_request:

jobs:
  type-check:
    name: Check types with ty
    runs-on: ubuntu-latest
    steps:
 - uses: actions/checkout@v4
 - uses: greenbone/actions/ty-python@v3
        with:
          packages: my_project tests
          dependency-manager: uv
```

### Advanced Usage

```yml
name: Type checking

on:
  pull_request:

jobs:
  type-check:
    name: Check types with ty
    runs-on: ubuntu-latest
    steps:
 - uses: actions/checkout@v4
 - uses: greenbone/actions/ty-python@v3
        with:
          packages: my_project tests
          dependency-manager: poetry
          python-version: "3.11"
          ty-arguments: "--strict"
          cache: "true"
```

## Action Configuration

| Input Variable | Description | Required | Default |
|----------------|-------------|----------|---------|
| `packages` | Python packages to check with ty | **Required** | - |
| `dependency-manager` | Dependency manager to use: `poetry` or `uv` | Optional | `poetry` |
| `ty-arguments` | Additional arguments for running ty | Optional | `""` |
| `python-version` | Python version to use for running the action | Optional | `3.10` |
| `install-dependencies` | Install project dependencies. Set to another string than `"true"` to skip installation | Optional | `true` |
| `working-directory` | Working directory where to run the action | Optional | `${{ github.workspace }}` |
| `cache` | Cache dependencies by setting it to `"true"` | Optional | - |
| `cache-dependency-path` | Path to dependency files for caching. Supports wildcards or a list of file names | Optional | - |

### Poetry-Specific Inputs

| Input Variable | Description | Required | Default |
|----------------|-------------|----------|---------|
| `poetry-version` | Specific poetry version to use | Optional | latest |
| `cache-poetry-installation` | Cache poetry and its dependencies | Optional | `true` |

### uv-Specific Inputs

| Input Variable | Description | Required | Default |
|----------------|-------------|----------|---------|
| `uv-version` | Specific uv version to use | Optional | latest |

## Dependency Manager Support

### Poetry

- Uses the `greenbone/actions/poetry@v3` action for setup
- Runs ty via `poetry run ty check`
- Supports all poetry caching options

### uv

- Uses `astral-sh/setup-uv@v4` for setup
- Runs `uv sync --all-extras --dev` for dependency installation
- Runs ty via `uv run ty check`
- Supports uv's built-in caching

## Notes

- The action defaults to using Poetry if `dependency-manager` is not specified
- For uv projects, ensure your `pyproject.toml` includes ty as a dependency
- For poetry projects, ensure ty is in your dev dependencies
