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
