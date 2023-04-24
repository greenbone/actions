Action to build a Python distributable via Poetry and upload it to PyPI

#### Example using as a Workflow

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