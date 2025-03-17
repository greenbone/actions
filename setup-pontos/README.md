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
        - uses: greenbone/actions/setup-pontos@v3
```

## Action Configuration

| Input Variable  | Description                                   |                                 |
| --------------- | --------------------------------------------- | ------------------------------- |
| python-version  | Python version to use for running the action. | Optional (default is `3.10`)    |
| virtualenv-path |                                               | Deprecated and will be ignored. |
| cache-key       |                                               | Deprecated and will be ignored. |

| Output Variable | Description                                    |                            |
| --------------- | ---------------------------------------------- | -------------------------- |
| virtualenv-path | Path to the created virtual Python environment | Deprecated. Will be empty. |
| activate        | Path to the activate environment script        | Deprecated. Will be empty. |
