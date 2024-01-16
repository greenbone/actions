# Validate Helm Chart Action

This GitHub Action is designed to validate Helm charts by executing the `helm template` command. It ensures that Helm charts are well-formed and adhere to Helm standards, making it an essential tool for Helm chart development and maintenance.


## Inputs

| Input                         | Description                                                  | Required | Default  |
|-------------------------------|--------------------------------------------------------------|----------|----------|
| `chart-path`                  | Path to the Helm chart to validate                           | Yes      | N/A      |
| `chart-name`                  | Name of the chart to validate                                | Yes      | N/A      |
| `registry`                    | Name of the registry                                         | No       | `ghcr.io`|
| `registry-user`               | Registry login user                                          | Yes      | N/A      |
| `registry-token`              | Registry login password/token                                | Yes      | N/A      |
| `chart-values-path`           | Path to the main values.yaml file                            | No       | ""       |
| `repository-name`             | Name of the repository to clone (format: {owner}/{repo})     | No       | N/A      |
| `repository-branch`           | Branch of the repository to clone                            | No       | N/A      |
| `additional-chart-values-path`| Path to additional values.yaml file within cloned repo       | No       | N/A      |
| `token`                       | Token for cloning repositories                               | Yes      | N/A      |

## Example Usage

```yml
name: Validate Helm Chart
on:
  workflow_dispatch:

jobs:
  helm-chart-validation:
    name: Helm Chart Validation
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Validate Helm Chart
        uses: greenbone/actions/helm-chart-validation@00xkhaled/helm-chart-validation
        with:
          chart-path: 'charts'
          chart-name: 'asset-management-backend'
          registry-user: ${{ secrets.REGISTRY_USER }}
          registry-token: ${{ secrets.REGISTRY_TOKEN }}
          chart-values-path: 'charts/asset-management-backend/values.yaml'
          repository-name: 'greenbone/product-helm-chart'
          repository-branch: 'dev-opensight-asset-management'
          additional-chart-values-path: 'opensight-asset/values.yaml'
          token: ${{ secrets.TOKEN }}
