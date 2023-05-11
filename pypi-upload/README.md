# Upload to PyPI action

Action to build a Python distributable via Poetry and upload it to [PyPI](https://pypi.org)

## Example

```yaml
name: Deploy on PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Build and publish to PyPI
        uses: greenbone/actions/pypi-upload@v2
        with:
          pypi-token: ${{ secrets.PYPI_TOKEN }}
```

## Action Configuration

| Input | Description | |
|-------|-------------|-|
| pypi-token | Token for uploading the build to PyPI | Required |
| python-version | Python version to use for this action | Optional (default: "3.10") |
| ref | The branch, tag or SHA to checkout. | Optional (default depends on the [event](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)) |
