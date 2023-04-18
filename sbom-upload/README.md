SPDX to Dependency Graph Action

This action makes it easy to upload an SPDX 2.2 formatted SBOM to GitHub's dependency submission API. This lets you quickly receive Dependabot alerts for package manifests which GitHub doesn't directly support like pnpm or Paket by using existing off-the-shelf SBOM generators.

More information availabe in [spdx-dependency-submission](https://github.com/marketplace/actions/spdx-dependency-submission-action)


#### Example using as a Workflow

```yaml
name: SBOM upload
on:
  workflow_dispatch:
  push:
    branches: ["main"]
jobs:
    SBOM-upload:
    runs-on: ubuntu-latest
    permissions:
        id-token: write
        contents: write
    steps:
      - name: 'SBOM upload'
        uses: greenbone/actions/sbom-upload@v2
```
