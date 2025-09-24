# Docker Client TLS Login

GitHub Action to configure Docker with client TLS certificates for registry authentication.

## Example

```yaml
name: Docker TLS Login

on:
  workflow_dispatch:

jobs:
  docker-operations:
    name: Docker Operations with TLS
    runs-on: ubuntu-latest
    steps:
      - name: Login to Greenbone Registry
        uses: greenbone/actions/docker-client-tls-login@v1
        with:
          registry: packages.greenbone.net
        env:
          GREENBONE_CLIENT_CERT: ${{ secrets.GREENBONE_CLIENT_CERT }}
          GREENBONE_CLIENT_KEY: ${{ secrets.GREENBONE_CLIENT_KEY }}
          GREENBONE_REGISTRY_USER: ${{ secrets.GREENBONE_REGISTRY_USER }}
          GREENBONE_REGISTRY_TOKEN: ${{ secrets.GREENBONE_REGISTRY_TOKEN }}
      
      - name: Pull Docker image
        run: |
          docker pull packages.greenbone.net/some-greenbone-image:latest
```

## Action Configuration

### Inputs

| Input Variable | Description                           | Required | Default                    |
|----------------|---------------------------------------|----------|----------------------------|
| registry       | Docker registry URL                   | No       | `packages.greenbone.net`   |
| logout         | Clean up certificates at end of job   | No       | `true`                     |

### Environment Variables

| Environment Variable      | Description                           | Required |
|---------------------------|---------------------------------------|----------|
| GREENBONE_CLIENT_CERT     | Client certificate in PEM format     | Yes      |
| GREENBONE_CLIENT_KEY      | Client private key in PEM format     | Yes      |
| GREENBONE_CA_CERT         | CA certificate in PEM format         | No       |
| GREENBONE_REGISTRY_USER   | Username for basic authentication    | No       |
| GREENBONE_REGISTRY_TOKEN  | Password/token for basic auth        | No       |
