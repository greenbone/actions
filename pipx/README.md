# pipx

A GitHub action for using pipx

Applications are installed without restoring cached virtual environments. pipx
application environments depend on shared libraries and runner-specific Python
installations, so restoring only the application environment can leave it broken.
The deprecated `cache` input is accepted but ignored, including `cache: "true"`.
The `cache-hit` output is retained and always returns `false`.

## Examples

```yaml
name: Install Python application

on:
  push:

jobs:
  pipx:
    name: Install latest poetry on system Python
    steps:
      - uses: greenbone/actions/pipx@v3
        with:
          install: poetry
```

Install a specific Python application version on Python 3.10

```yaml
name: Install Python application

on:
  push:

jobs:
  pipx:
    name: Install poetry 1.5.0 on Python 3.10
    steps:
      - uses: greenbone/actions/pipx@v3
        with:
          python-version: "3.10"
          install: poetry
          install-version: "1.5.0"
```

## Action Configuration

| Input Variable  | Description                                                                                                                                                            |          |
|-----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|
| python-version  | Setup a specific Python version.                                                                                                                                       | Optional |
| python-path     | Path to the Python binary to use. Passing python-path allows for setting up a Python version before using this action and running pipx with the set up Python version. | Optional |
| install         | Python application to install.                                                                                                                                         | Required |
| install-version | Use a specific version of the application to install. For example '1.2.3'.                                                                                             | Optional |
| include-deps    | Enable dependency installations for pipx applications. Disabled by default. 'true' to enable.                                                                          | Optional |
| cache           | Deprecated. Accepted but ignored; application virtual environments are not cached. | Optional |

## Outputs

| Output Variable | Description                                                        |
|-----------------|--------------------------------------------------------------------|
| home            | Path to the pipx python application.                               |
| bin             | Path to the bin directory where all applications can be run from.  |
| venvs           | Path to the directory where the virtual environments are stored.   |
| shared          | Path where shared python packages like pip or wheel are installed. |
| cache-hit       | Deprecated. Always `false`.                                  |
