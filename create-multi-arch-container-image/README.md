# Create multi arch container image

A action to create a multi arch container image to and upload it to one or more
container registries.

Requires the single-arch images are already pushed to the registry and existing
login in to the registries.

> [!NOTE]
> For uploading OCI images to the GitHub Container Registry the annotations need
> to be index annotations.

> [!TIP]
> The action can also be used to tag a single image

## Examples

Create a new multi arch image from two existing images and upload it to two
different registries.

```yml
name: Create multi arch image

on:
  push:

jobs:
  build:
    runs-on: "ubuntu-latest"
    steps:
      - name: Create multi arch image
        uses: greenbone/actions/create-multi-arch-container-image@v3
        with:
          tags: |
            ghcr.io/greenbone/some-service:latest
            some-registry.org/greenbone/some-service:1.2.3
          annotations: |
            index:org.opencontainers.image.description=Some Service
            index:org.opencontainers.image.licenses=AGPL-3.0
          digests: |
            ghcr.io/greenbone/some-service@sha256:12345
            ghcr.io/greenbone/some-service@sha256:54321
```

Tag an existing container image as latest by its digest.

```yml
name: Tag latest container image

on:
  workflow_dispatch:
    inputs:
      digest:
        type: string
        required: true

jobs:
  build:
    runs-on: "ubuntu-latest"
    steps:
      - name: Tag container image
        uses: greenbone/actions/create-multi-arch-container-image@v3
        with:
          tags: |
            ghcr.io/greenbone/some-service:latest
          annotations: |
            index:org.opencontainers.image.description=Some Service
            index:org.opencontainers.image.licenses=AGPL-3.0
          digests: |
            ghcr.io/greenbone/some-service@${{ inputs.digest }}
```

## Inputs

| Name        | Description                                                                            |                          |
| ----------- | -------------------------------------------------------------------------------------- | ------------------------ |
| digests     | New line separated list of container image digests to merge into the multi-arch image. | Required                 |
| tags        | New line separated list of tags for the created multi-arg image.                       | Required                 |
| annotations | New line separated list of annotations for the created multi-arch image.               | Optional                 |
| inspect     | Whether to display inspect information of the created multi-arch image                 | Optional (default: true) |

## Output

| Output Variable | Description                                 |
| --------------- | ------------------------------------------- |
| digest          | The digest of the created multi-arch image. |
