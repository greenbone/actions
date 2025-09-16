# Detect hidden unicode

Detects hidden unicode in newly committed files.

## Examples

### Usage:

```yml
name: Detect hidden unicode

on:
  pull_request:

  jobs:
    runs-on: ubuntu-latest
    steps:
      - name: Detect hidden unicode
        uses: greenbone/actions/detect-hidden-unicode@3.33.5
        with:
          github-token: ${{ secrets.GREENBONE_BOT_TOKEN }}
```

## Action Configuration

|Input Variable|Description| |
|--------------|-----------|-|
| python-version | Python version that should be installed and used. | Optional (default: "3.10") |
| poetry-version | Use a specific poetry version. By default the latest release is used. | Optional (default is `latest` version) |
| cache-poetry-installation | Cache poetry and its dependencies by setting it to 'true'. | Optional. Disabled by default. |
| github-token | GH Token for writing/editing a comment to/in a PR | |
| pr-comment | Write a summary of the scan as comment to the PR | |

## Run detect-hidden-unicode python script locally

### Requirements
- install poetry

### Installation
```
cd actions/detect-hidden-unicode
poetry install
```

### Run
```
poetry run detect-hidden-unicode
```

### Tests
```
poetry run pytest
```

### Code Coverage
```
poetry run coverage report -m pytest
```
