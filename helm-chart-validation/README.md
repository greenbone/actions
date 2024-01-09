# Validate Helm Chart

GitHub Action to validate a Helm chart using the Helm template command.

## Description

This GitHub Action validates Helm charts by executing the `helm template test` command on the specified chart. It is designed to ensure that the chart is valid and adheres to Helm's standards.

## Inputs

| Input Variable | Description                               | Required |
| -------------- | ----------------------------------------- | -------- |
| chart-path     | Path to the directory containing Helm charts | Yes      |
| chart-name     | Name of the Helm chart to validate        | Yes      |

## Outputs

| Output Variable | Description                               |
| --------------- | ----------------------------------------- |
| test-result     | The result of the Helm chart test         |

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
      - name: Checkout
        uses: actions/checkout@v3
      - name: run helm-chart-validation
        uses: greenbone/actions/helm-chart-validation@v3
        with:
          chart-path: 'path-to-charts'
          chart-name: 'my-chart'
