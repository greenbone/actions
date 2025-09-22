# Docker CLIENT TLS Login

GitHub Action to configure Docker with client TLS certificates for registry authentication.

## Example

```yml
name: Docker TLS Login

on:
  workflow_dispatch:

jobs:
  docker-operations:
    name: Docker Operations with TLS
    runs-on: ubuntu-latest
    steps:
      - uses: greenbone/actions/docker-client-tls-login@v1
        with:
          client-cert: ${{ secrets.GREENBONE_CLIENT_CERT }}
          client-key: ${{ secrets.GREENBONE_CLIENT_KEY }}
      - name: Pull Docker image
        run: |
          docker pull packages.greenbone.net/some-greenbone-image:latest
```

## Action Configuration

| Input Variable | Description                                                           |                                      |
|----------------|-----------------------------------------------------------------------|--------------------------------------|
| registry       | Docker registry URL                                                  | Optional: (Default is `"packages.greenbone.net"`) |
| client-cert    | Client certificate in PEM format                                     |                                      |
| client-key     | Client private key in PEM format                                     |                                      |
| ca-cert        | CA certificate in PEM format                                         | Optional                             |
| logout         | Clean up certificates at the end of the job                          | Optional: (Default is `true`)        |
