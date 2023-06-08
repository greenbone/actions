# Is Latest Tag

GitHub Action to check if a git tag is the latest tag

## Example

```yml
name: Check Tag

on:
  tag:

jobs:
  check:
    name: Check Tag
    runs-on: ubuntu-latest
    steps:
        - uses: greenbone/actions/is-latest-tag@v2
          id: latest
        - name:
          if: steps.latest.outputs.is-latest-tag
          run: |
            # do something if the current tag is the latest tag
```

## Output Arguments

|Output Variable|Description|
|---------------|-----------|
| is-latest-tag | Evaluates to true if the created tag is the latest git tag |
