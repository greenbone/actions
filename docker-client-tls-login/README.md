# Docker TLS Certificate Login Action

This GitHub Action configures Docker to use client TLS certificates for secure registry authentication (mutual TLS).

## Example Usage

```yaml
name: Docker TLS Login

on:
  workflow_dispatch:

jobs:
  docker-operations:
    name: Docker Operations with TLS
    runs-on: ubuntu-latest
    steps:
      - name: Setup Docker TLS Certificates
        uses: ./.github/actions/docker-tls-login
        with:
          registry-url: packages.greenbone.net
          client-cert: ${{ secrets.GREENBONE_CLIENT_CERT }}
          client-key: ${{ secrets.GREENBONE_CLIENT_KEY }}
          # Optional: ca-cert if not using system CA bundle
          # ca-cert: ${{ secrets.GREENBONE_CA_CERT }}
          debug: 'true'

      - name: Login to Greenbone Registry (Read-Only)
        uses: docker/login-action@v3
        with:
          registry: packages.greenbone.net
          username: ${{ secrets.GREENBONE_REGISTRY_READ_USER }}
          password: ${{ secrets.GREENBONE_REGISTRY_READ_TOKEN }}

      - name: Pull Docker image
        run: |
          docker pull packages.greenbone.net/opensight/opensight-postgres:17.5.3@sha256:2e28556d0dceec5880f2104e35db6002d64d6e7e756e7fbf2b618d4d660f0d31
```

## Inputs

| Input Variable | Description                           | Required | Default   |
|----------------|---------------------------------------|----------|-----------|
| registry-url   | Docker registry URL                   | Yes      |           |
| client-cert    | Base64-encoded client certificate     | Yes      |           |
| client-key     | Base64-encoded client private key     | Yes      |           |
| ca-cert        | Base64-encoded CA certificate         | No       | ''        |
| debug          | Enable debug output (true/false)      | No       | 'false'   |

## Outputs

| Output Variable | Description                           |
|-----------------|---------------------------------------|
| cert-directory  | Path to the Docker certificate directory |
