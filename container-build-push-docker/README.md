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

jobs:
  build:
    runs-on: "ubuntu-latest"
    steps:
      - name: Container build and push docker.io
        uses: greenbone/actions/container-build-push-docker@v2
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

| Name                | Description                                         |          |
|---------------------|-----------------------------------------------------|----------|
| build-context       | Path to image build context. Default "."            | Optional |
| build-docker-file   | Path to the docker file. Default "./Dockerfile"     | Optional |
| build-args          | Use these build-args for the docker build process.  | Optional |
| cosign-key          | cosign key to sign the image.                       | Optional |
| cosign-key-password | cosign key password.                                | Optional |
| image-labels        | Image labels.                                       | Required |
| image-url           | Image url/name without registry.                    | Required |
| image-platforms     | Image platforms to build for. Default "linux/amd64" | Optional |
| image-tags          | Image tags.                                         | Required |
| registry-username   | Login registry username.                            | Required |
| registry-password   | Login registry password.                            | Required |