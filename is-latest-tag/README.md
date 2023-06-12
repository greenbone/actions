# Is Latest Tag

GitHub Action to check if a git tag is the latest tag.

Please keep in mind that the full history (`checkout with fetch-depth 0`) is
required for the `is-latest-tag` action.

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
        # the full history is required for is-latest-tag
        - uses: actions/checkout@v3
          with:
            fetch-depth: 0
        - uses: greenbone/actions/is-latest-tag@v2
          id: latest
        - name: Do something
          if: steps.latest.outputs.is-latest-tag == 'true'
          run: |
            # do something if the current tag is the latest tag
        - name: Do something else
          if: steps.latest.outputs.is-latest-tag == 'false'
          run: |
            # do something else if the current tag is not the latest tag
```

## Output Arguments

|Output Variable|Description|
|---------------|-----------|
| is-latest-tag | Evaluates to true if the created tag is the latest git tag |
