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

|Input Variable|Description|Default value|
|--------------|-----------|-|
| python-version | Python version that should be installed and used. | Optional (default: "3.10") |
| github-token | GH Token for writing/editing a comment to/in a PR | |
| pr-comment | Write a summary of the scan as comment to the PR | true |
| filter | The regex filter being applied to the file selection | "^.*.(?<!png)(?<!jpg)(?<!jpeg)(?<!gif)(?<!tiff)(?<!tif)(?<!bmp)(?<!psd)(?<!heic)(?<!heif)(?<!svg)$" |
| pr-comment-level | The pr comment level of the detect-hidden-unicode action | NONE, WARNING, DEBUG |
| hide-scan-details | Hide the scan details(exact position where hidden unicode chars have been found) | false |

### pr-comment-level explained

#### NONE
Will not write a PR_COMMENT

#### WARNING
Will only write a PR_COMMENT when hidden unicode chars have been found.

#### DEBUG
Will always write a PR_COMMENT with all the scan results.
DEBUG is how the the Github Action log will always look.

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
