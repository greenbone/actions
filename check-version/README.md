# Check Version

GitHub Action to check version information of a project via pontos

## Example

```yml
name: Check Versioning

on:
  push:
  pull_request:

jobs:
  check:
    name: Check Versioning
    runs-on: ubuntu-latest
    steps:
        - uses: greenbone/actions/check-version@v2
```

## Action Configuration

|Input Variable|Description| |
|--------------|-----------|-|
| python-version | Python version to use for running the action. | Optional (default is `3.10`) |
| working-directory | "A working directory where to check the versioning | Optional (default is `${{ github.workspace }}`) |
