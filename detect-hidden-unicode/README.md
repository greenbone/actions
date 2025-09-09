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
```

## Action Configuration

|Input Variable|Description| |
|--------------|-----------|-|
|              |           | |
