# Build and push container action for docker.io

A action to build and push container into docker.io.

## Example

```yml
name: Build Container Image

on:
  workflow_dispatch:

permissions:
  contents: read
  packages: write
  id-token: write
  pull-requests: write

jobs:
  build:
    runs-on: "ubuntu-latest"
    steps:
      - name: Container build and push docker.io
        uses: greenbone/actions/container-build-push-docker@v3
        with:
          image-url: my/app
          image-labels: my-labels
          image-tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
          registry-username: my-user
          registry-password: my-passwort
```

## Inputs

| Name                | Description                                                                          |          |
|---------------------|--------------------------------------------------------------------------------------|----------|
| build-context       | Path to image build context. Default is "."                                          | Optional |
| build-docker-file   | Path to the docker file. Default is "./Dockerfile"                                   | Optional |
| build-args          | Use these build-args for the docker build process. Default is empty                  | Optional |
| build-secrets       | Use these build-secrets for the docker build process. Default is empty               | Optional |
| cosign-key          | Cosign key to sign the image. Will be skipped if empty. Default is empty             | Optional |
| cosign-key-password | Cosign key password. Will be skipped if empty. Default is empty                      | Optional |
| image-labels        | Image labels.                                                                        | Required |
| image-url           | Image url/name without registry.                                                     | Required |
| image-platforms     | Image platforms to build for. Default is "linux/amd64"                               | Optional |
| image-tags          | Image tags.                                                                          | Required |
| registry-username   | Login registry username.                                                             | Required |
| registry-password   | Login registry password.                                                             | Required |
| scout-user          | Dockerhub user for docker scout. Will be skipped if empty. Default is empty          | Optional |
| scout-password      | Dockerhub user password for docker scout. Will be skipped if empty. Default is empty | Optional |

## Action Output

| Output Variable | Description          |
|-----------------|----------------------|
| digest          | The container digest |
