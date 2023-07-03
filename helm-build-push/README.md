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
          registry_user: Registry username
          registry_token: Registry user password/token
```

## Action Configuration

|Input Variable|Description| |
|--------------|-----------|-|
| charts-path | Path to charts base folder | Optional(default ./charts) |
| chart-name | Chart to build and push | Required |
| registry | registry to push | Optional(default ghcr.io) |
| registry-subpath| Registry subpath to place the helm chart in | Optional |
| registry-user | Registry login user | Required |
| registry-token | Registry login password/token | Required |
| gpg-secret-key | Gpg secret key for chart sign | Optional |
| gpg-secret-name | Gpg secret key name from gpg secret key | Optional |
