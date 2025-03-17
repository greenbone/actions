# Install Python Applications with uv

GitHub Action to install applications from PyPI using [uv](https://docs.astral.sh/uv).

For details about the caching see [astral-sh/setup-uv](https://github.com/astral-sh/setup-uv?tab=readme-ov-file).

## Example

```yml
name: Install httpx

on:
  pull_request:

jobs:
  install-httpx:
    name: Install httpx
    runs-on: ubuntu-latest
    steps:
        - uses: greenbone/actions/uv@v3
          with:
            install: "httpx[cli]"
```

## Action Configuration

| Input Variable        | Description                                                        |                             |
| --------------------- | ------------------------------------------------------------------ | --------------------------- |
| python-version        | Python version to use for running the action.                      | Optional                    |
| install               | The package to install from PyPI                                   | Required                    |
| enable-cache          | Enable caching                                                     | Optional (default: true)    |
| cache-dependency-glob | Glob pattern to match dependencies to cache. Optional. Default: "" |
| cache-suffix          | Suffix to append to the cache key                                  | Optional                    |
| cache-local-path      | Path to the local cache                                            | Optional                    |
| uv-version            | The version of uv to install and use                               | Optional. Default is latest |

| Output Variable | Description                    |
| --------------- | ------------------------------ |
| version         | The installed version of uv    |
| major           | The major version of uv        |
| minor           | The minor version of uv        |
| patch           | The patch version of uv        |
| cache-hit       | true if the cache has been hit |
