# Helm login and installation

- Helm registry login and optional installation

#### Use Case

```yaml
jobs:
  chart:
    name: Helm chart push
    runs-on: ubuntu-latest
    steps:
      - ...
      - name: Helm login
        uses: greenbone/actions/helm-login@v3
      - ...
```

## Action Configuration

| Input Variable | Description                                                                                                                                           |          |
| ---------------| ----------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| registry       | Registry name. Default: ghcr.io .                                                                                                                     | Optional |
| registry-user  | Registry login user. Default is github.actor .                                                                                                        | Optional |
| registry-token | Registry login password/token. Default is github.token .                                                                                              | Optional |
| helm-version   | The Helm version for installation must be specified. If left unset, Helm will not be installed. Note that Helm is preinstalled on all GitHub runners. | Optional |
| helm-token     | GitHub token required if the Helm version is set to 'latest'. Default is github.token .                                                               | Optional |

## Action Output

| Output Variable | Description       |
| --------------- | ----------------- |
| helm-path       | Helm binary path. |
