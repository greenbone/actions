# Build and push container generic action

A action to build and push container image.

## Introduction

If you want to upload an image to a registry you have to give a registry e.g. GitHub Container Registry (`registry: "ghcr.io"`) or DockerHub registry (`registry: "docker.io"`).
You also need to have authentication for the registry, by passing `registry-username` and `registry-password` (which can be a Token ...).
The image URL will result in the repository `owner/name` scheme (e.g. `greenbone/actions` for this repository).
Set some `image-tags:`, e.g. a version or some best practice named labels like `nightly`, `latest`, `staging` and you are good to go! [See docker `metadata-action` for the whole fun!](https://github.com/docker/metadata-action?tab=readme-ov-file#tags-input)

### Example

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
          image-url: my-image
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

### Example for ARM64

> [!IMPORTANT]
> If you use `linux/arm64` directly as image platform, without QEMU, you will need a dedicated runner that runs on arm64 architecture!

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
    runs-on: self-hosted-generic-arm64
    steps:
      - name: Container build and push docker.io
        uses: greenbone/actions/container-build-push-generic@v3
        with:
          image-url: my-image
          image-labels: my-labels
          image-platforms: linux/arm64
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

### Required

| Name                         | Description                                                                                                                                 |          |
|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|----------|
| image-labels                 | Image labels.                                                                                                                               | Required |
| image-tags                   | Image tags. For format refer to [docker/metadata-action](https://github.com/docker/metadata-action?tab=readme-ov-file#tags-input).          | Required |
| registry                     | Registry url.                                                                                                                               | Required |
| registry-username            | Login registry username.                                                                                                                    | Required |
| registry-password            | Login registry password.                                                                                                                    | Required |

### Optional

| Name                         | Description                                                                                                                                 |          |
|------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|----------|
| build-context                | Path to image build context. Default is ".".                                                                                                | Optional |
| build-docker-file            | Path to the docker file. Default is "./Dockerfile".                                                                                         | Optional |
| build-args                   | Use these build-args for the docker build process. Default is empty.                                                                        | Optional |
| build-secrets                | Use these build-secrets for the docker build process. Default is empty.                                                                     | Optional |
| cosign-key                   | Cosign key to sign the image. Will be skipped if empty. Default is empty.                                                                   | Optional |
| cosign-key-password          | Cosign key password. Will be skipped if empty. Default is empty.                                                                            | Optional |
| cosign-tlog-upload           | Turn on or turn off the cosign tlog upload function. Options are true/false. Default is true.                                               | Optional |
| image-flavor                 | Global behavior for tags. Default is empty.                                                                                                 | Optional |
| image-url                    | Image url/name without registry. Default is github.repository.                                                                              | Optional |
| image-platforms              | Image platforms to build for. Default is "linux/amd64".                                                                                     | Optional |
| meta-annotations-levels      | Comma separated list. Options are manifest, index, manifest-descriptor, index-descriptor. Default is manifest,manifest-descriptor.          | Optional |
| scout-command                | Comma separated list of several commands. Options are quickview, compare, cves, recommendations, sbom, environment. Default is cves,sbom.   | Optional |
| scout-user                   | Dockerhub user for docker scout. Will be skipped if empty. Default is empty.                                                                | Optional |
| scout-password               | Dockerhub user password for docker scout. Will be skipped if empty. Default is empty.                                                       | Optional |
| scout-keep-previous-comments | Keep but hide previous comment. If not set, keep and update one single comment per job. Options are true/false. Default is false.           | Optional |
| sarif-retention-days         | Days to store the sarif artifact. Default is 1.                                                                                             | Optional |
| qemu                         | Install local QEMU static binaries. Options are true/false. Default is false.                                                               | Optional |
| qemu-platforms               | Comma separated list of platforms to install. Options are amd64, arm64, arm, riscv64, s390x, 386. Default is arm64 (amd64 is default arch). | Optional |
| buildx-container             | Use a buildx container to build images. Options are true/false. Default is false.                                                           | Optional |

## Action Output

| Output Variable | Description                     |
|-----------------|---------------------------------|
| annotations     | The container annotations.      |
| digest          | The container digest.           |
| labels          | The container labels.           |
| meta-tags       | The meta action container tags. |
| tags            | The container tags.             |
