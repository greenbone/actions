# Build and push helm chart

- Build and push helm chart

#### Use Case

```yaml
jobs:
  manual-build-chart:
    name: Build and push helm chart
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and push chart
        uses: greenbone/actions/helm-build-push@v2
        with:
          CHART_NAME: Chart folder name
          CHARTS_PATH: Charts base folder || default ./charts
          REGISTRY: Registry to use || default ghcr.io
          REGISTRY_URL: Registry url to push to e.g oci://ghcr.io/greenbone/helm-charts/
          REGISTRY_USER: Registry username
          REGISTRY_PASSWORD: Registry user password
```

