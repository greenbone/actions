# Build and push helm chart

- Build and push helm chart

#### Use Case

```yaml
jobs:
  manual-build-chart:
    name: Build and push helm chart
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and push chart
        uses: greenbone/actions/helm-build-push@v3
        with:
          chart-name: Chart folder name
          registry_user: Registry username
          registry_token: Registry user password/token
```

## Action Configuration

| Input Variable          | Description                                                                     |          |
|-------------------------|---------------------------------------------------------------------------------|----------|
| charts-path             | Path to charts base folder. Default: ./charts                                   | Optional |
| chart-name              | Chart to build and push.                                                        | Required |
| registry                | registry name. Default: ghcr.io                                                 | Optional |
| registry-subpath        | Registry subpath to push the helm chart to.                                     | Optional |
| registry-user           | Registry login user.                                                            | Required |
| registry-token          | Registry login password/token.                                                  | Required |
| gpg-secret-name         | Gpg secret key name from gpg secret key. Needed to use gpg sign.                | Optional |
| gpg-secret-key          | Base64 encoded gpg secret key for chart sign. Needed if gpg-secret-name is set. | Optional |
| gpg-secret-key-password | The password for the gpg secret key. Needed if gpg-secret-name is set.          | Optional |
| enable-chart-test       | Enable testing of Helm charts. Default is true                                  | Optional |

## Action Output

|Output Variable|Description|
|--------------|-----------|
| tag | Helm chart url's with tag |
| digest | The helm chart digest |
