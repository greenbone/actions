# Upload to PyPI action

Action to build a Python distributable via Poetry and upload it to [PyPI](https://pypi.org)

## Example 1

Use a token for uploading the package to PyPI.

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
        uses: greenbone/actions/pypi-upload@v3
        with:
          pypi-token: ${{ secrets.PYPI_TOKEN }}
```

## Example 1

Use [trusted publisher](https://docs.pypi.org/trusted-publishers/) for uploading
the package to PyPI. The trusted publisher mechanism uses OpenID Connect (OIDC)
to issue short term tokens. This requires `write` permissions for `id-token`.

```yaml
name: Deploy on PyPI

on:
  release:
    types: [created]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
    steps:
      - name: Build and publish to PyPI
        uses: greenbone/actions/pypi-upload@v3
        with:
          pypi-token: ${{ secrets.PYPI_TOKEN }}
```

## Action Configuration

| Input          | Description                           |                                                                                                                                                                        |
| -------------- | ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| pypi-token     | Token for uploading the build to PyPI | Optional. If not provided [trusted publisher](https://docs.pypi.org/trusted-publishers/) will be used. **MUST** be provided as a secret to be not visible in the logs. |
| python-version | Python version to use for this action | Optional (default: "3.10")                                                                                                                                             |
| ref            | The branch, tag or SHA to checkout.   | Optional (default depends on the [event](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows))                                            |
