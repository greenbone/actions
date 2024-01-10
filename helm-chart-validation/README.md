# Validate Helm Chart Action

This GitHub Action validates Helm charts by executing the `helm template test` command on the specified chart. It is designed to ensure that the chart is valid and adheres to Helm's standards.

## Inputs

| Input          | Description                                      | Required | Default  |
|----------------|--------------------------------------------------|----------|----------|
| `chart-path`   | Path to the Helm chart to validate               | Yes      | N/A      |
| `chart-name`   | Chart to validate                                | Yes      | N/A      |
| `registry`     | Registry name                                    | No       | `ghcr.io`|
| `registry-user`| Registry login user                              | Yes      | N/A      |
| `registry-token`| Registry login password/token                   | Yes      | N/A      |
| `values-path` | path to values.yaml file                          | No       | N/A      |

## Example Usage

```yml
name: validate-chart
on:
  workflow_dispatch:
jobs:
  helm-chart-validation:
    name: helm-chart-validation
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Validate Helm Chart
        uses: greenbone/actions/helm-chart-validation@v3
        with:
          chart-path: 'path/to/charts'
          chart-name: 'helm-chart-path'
          registry-user: ${{ secrets.REGISTRY_USER }}
          registry-token: ${{ secrets.REGISTRY_TOKEN }}
          
