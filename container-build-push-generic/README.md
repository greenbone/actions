# Build and push container generic action

A action to build and push container image.

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
        uses: greenbone/actions/container-build-push-generic@v3
        with:
          image-url: docker.io/my-image
          image-labels: my-labels
          image-tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
          registry: "docker.io"
          registry-username: my-user
          registry-password: my-passwort
```

## Inputs

| Name                         | Description                                                                                                        |          |
|------------------------------|--------------------------------------------------------------------------------------------------------------------|----------|
| build-context                | Path to image build context. Default is "."                                                                        | Optional |
| build-docker-file            | Path to the docker file. Default is "./Dockerfile"                                                                 | Optional |
| build-args                   | Use these build-args for the docker build process. Default is empty                                                | Optional |
| build-secrets                | Use these build-secrets for the docker build process. Default is empty                                             | Optional |
| cosign-key                   | Cosign key to sign the image. Will be skipped if empty. Default is empty                                           | Optional |
| cosign-key-password          | Cosign key password. Will be skipped if empty. Default is empty                                                    | Optional |
| cosign-tlog-upload           | Turn on or turn off the cosign tlog upload function. Possible options: true/false Default is true                  | Optional |
| image-labels                 | Image labels.                                                                                                      | Required |
| image-url                    | Image url/name without registry.                                                                                   | Required |
| image-platforms              | Image platforms to build for. Default is "linux/amd64"                                                             | Optional |
| image-tags                   | Image tags.                                                                                                        | Required |
| registry                     | Registry url.                                                                                                      | Required |
| registry-username            | Login registry username.                                                                                           | Required |
| registry-password            | Login registry password.                                                                                           | Required |
| scout-user                   | Dockerhub user for docker scout. Will be skipped if empty. Default is empty                                        | Optional |
| scout-password               | Dockerhub user password for docker scout. Will be skipped if empty. Default is empty                               | Optional |
| scout-keep-previous-comments | Keep but hide previous comment. If not set, keep and update one single comment per job. Default is `false`           | Optional |
| sarif-retention-days         | Days to store the sarif artifact. Default is 1                                                                     | Optional |

## Action Output

| Output Variable | Description          |
|-----------------|----------------------|
| digest          | The container digest |
