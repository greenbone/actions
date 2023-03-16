# Greenbone Helm Version Upgrade

GitHub Action to upgrade a helm chart version.

## Example

```yml

name: helm-version-upgrade
on:
  workflow_dispatch:
jobs:
  helm-version-upgrade:
    name: helm-version-upgrade
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: run helm-version-upgrade
        uses: greenbone/actions/helm-version-upgrade@v2
        with:
          chart-path: ${{ github.workspace }}/charts/<YOUR-CHART>
          chart-version: <NEW-VERSION> e.g 0.1.1-a1
```
## Action Configuration

| Input Variable               | Description                                                                                                                     | Required / Optional      |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------ |
| chart-path                   | Full path to helm chart folder                                                                                                  | Required                 |
| chart-version                | New helm chart version                                                                                                          | Optional                 |
| app-version                  | New helm chart appVersion, optional default chart-version                                                                       | Optional                 |
| image-tag                    | New helm chart docker image tag, optional default chart-version                                                                 | Optional                 |
| no-tag                       | Do not upgrade an image tag in values                                                                                           | Optional                 |
| dependency-version          | New helm chart dependency version                                                                                              | Optional                 |
| dependency-name             | Helm chart dependency to upgrade                                                                                               | Optional                 |
| git-user                     | Git user name for commit, set only if autocommit is desired                                                                     | Optional                 |
| git-user-email               | Git user email for commit, set only if autocommit is desired                                                                    | Optional                 |
| token                        | Github token for commit, set only if autocommit is desired                                                                      | Optional                 |
