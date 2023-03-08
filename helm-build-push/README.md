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
          chart-name: Chart folder name
          chart-path: Charts base folder || default ./charts
          registry: Registry to use e.g ghcr.io
          registry_url: Registry url to push to e.g oci://ghcr.io/greenbone/helm-charts/
          registry_user: Registry username
          registry_token: Registry user password/token
```

