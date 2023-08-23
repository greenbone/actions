SPDX to Dependency Graph Action

This action makes it easy to upload an SPDX 2.2 formatted SBOM to GitHub's dependency submission API. This lets you quickly receive Dependabot alerts for package manifests which GitHub doesn't directly support like pnpm or Paket by using existing off-the-shelf SBOM generators.

More information available in [spdx-dependency-submission](https://github.com/marketplace/actions/spdx-dependency-submission-action)


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
        uses: greenbone/actions/sbom-upload@v3
```

## Inputs

| Name                | Description                                                                                              |          |
|---------------------|----------------------------------------------------------------------------------------------------------|----------|
| git-user      | Git user name for commit, set only if autocommit is desired. Default: empty                                    | Optional |
| git-user-email  | Git user email for commit, set only if autocommit is desired. Default: empty                                 | Optional |
| token  | Github token for commit, set only if autocommit is desired. Default: empty                                            | Optional |
| bypass-branch-protection  | Branch name to bypass protection for admin user, set only if autocommit is desired. Default: empty | Optional |
