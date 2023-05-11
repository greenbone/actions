# Setup Pontos Action

GitHub Action to setup [pontos](https://github.com/greenbone/pontos) for your
action or workflow.

## Example

```yml
name: Setup Pontos

on:
  pull_request:

jobs:
  setup-pontos:
    name: Setup Pontos
    runs-on: ubuntu-latest
    steps:
        - uses: greenbone/actions/setup-pontos@v2
```

## Action Configuration

|Input Variable|Description| |
|--------------|-----------|-|
| python-version | Python version to use for running the action. | Optional (default is `3.10`) |
| virtualenv-path |  | Optional (default is `${{ github.workspace }}/pontos-env`) |
| cache-key | Additional key to use for caching | Optional (default is `pontos-venv`) |

|Output Variable|Description|
|---------------|-----------|
| virtualenv-path | Path to the created virtual Python environment |
| activate | Path to the activate environment script |
