# Is Latest Tag

GitHub Action to check if a git tag is the latest tag.

Please keep in mind that the full history (`checkout with fetch-depth 0`) is
required for the `is-latest-tag` action. A tag is considered latest if its
version is greater or equal as the latest existing tag.

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
        - uses: actions/checkout@v4
          with:
            fetch-depth: 0
        - uses: greenbone/actions/is-latest-tag@v3
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

## Input Arguments

| Input Variable    | Description                                                                       | Default                   |
| ----------------- | --------------------------------------------------------------------------------- | ------------------------- |
| tag-name          | Name of the tag to check if it is the latest tag                                  | `${{ github.ref_name }}`  |
| working-directory | Working directory for the action. Has to reference the directory of the checkout. | `${{ github.workspace }}` |

## Output Arguments

| Output Variable | Description                                                |
| --------------- | ---------------------------------------------------------- |
| is-latest-tag   | Evaluates to true if the created tag is the latest git tag |
