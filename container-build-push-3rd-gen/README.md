# Build and push container action for 3rd gen

A action to build and push container image for 3rd gen.

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
      - name: Container build and push 3rd gen
        uses: greenbone/actions/container-build-push-3rd-gen@v3
        with:
          image-url: my/app
          image-labels: my-label
          registry-password: ${{ secrets.GITHUB_TOKEN }}
```

## Inputs

| Name                | Description                                                                          |          |
|---------------------|--------------------------------------------------------------------------------------|----------|
| build-context       | Path to image build context. Default is the current directory.                       | Optional |
| build-docker-file   | Path to the docker file. Default is './Dockerfile'.                                  | Optional |
| build-args          | Use these build-args for the docker build process. Default is empty                  | Optional |
| build-secrets       | Use these build-secrets for the docker build process. Default is empty               | Optional |
| cosign-key          | Cosign key to sign the image. Will be skipped if empty. Default is empty             | Optional |
| cosign-key-password | Cosign key password. Will be skipped if empty. Default is empty                      | Optional |
| image-labels        | Image labels.                                                                        | Required |
| image-url           | Image url/name without registry.                                                     | Required |
| image-platforms     | Image platforms to build for. Default is 'linux/amd64'.                              | Optional |
| registry-password   | Registry password.                                                                   | Required |
| scout-user          | Dockerhub user for docker scout. Will be skipped if empty. Default is empty          | Optional |
| scout-password      | Dockerhub user password for docker scout. Will be skipped if empty. Default is empty | Optional |

## Action Output

| Output Variable | Description          |
|-----------------|----------------------|
| digest          | The container digest |
