# Checkout

Extends the [GitHub Checkout Action](https://github.com/actions/checkout/) by
providing some additional output parameters for git repository information.

## Example

```yml
name: Do Something

on:
  push:

jobs:
  check:
    name: Do Something
    runs-on: ubuntu-latest
    steps:
        - uses: greenbone/checkout@v2
          id: checkout
        - run: |
          echo ${{ steps.checkout.outputs.sha }}
          echo ${{ steps.checkout.outputs.ref }}
          echo ${{ steps.checkout.outputs.repository-name }}
```

## Action Configuration

See [https://github.com/actions/checkout/](actions/checkout/) for the details
about the action inputs.

## Output Arguments

|Output Variable|Description|
|---------------|-----------|
| sha | Git commit ID (SHA1) of the last commit (HEAD) |
| ref | Reference of the last commit (HEAD). For example `my-branch` |
| repository-name | Name of the repository (stripped leading `github/`) |
