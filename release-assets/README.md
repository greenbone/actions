# Manage Release Assets

GitHub Action to manage github release assets.

## Example

```yml
on:
  push:
    tags:
      - v*

permissions:
  contents: write

jobs:
  assets:
    name: upload
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: upload
        id: tags
        uses: greenbone/actions/release-assets@pholthaus/release-assets
        with:
          files: test1,test2
          tag: ${{ github.ref_name }}
          token: ${{ secrets.GITHUB_TOKEN }}
```

## Action Configuration

| Input Variable            | Description                                                                                                    |          |
| ------------------------- | -------------------------------------------------------------------------------------------------------------- | -------- |
| mode                      | Available modes are upload. Default is upload .                                                                | Optional |
| repository                | Repository name. Default is ${{ github.repository }}                                                           | Optional |
| files                     | Comma seprated list of asset file paths.                                                                       | Required |
| tag                       | The release tag to manage assets on.                                                                           | Required |
| python-version            | Python version to use for running the action. Default is 3.11 .                                                | Optional |
