# Build a Container Image and Push to Registry by Digest

An action to build a container image and optionally push it to a container
registry by digest only.

## Example

```yml
name: Create Image

on:
  push:

jobs:
  build:
    runs-on: "ubuntu-latest"
    steps:
      - name: Create Image
        uses: greenbone/actions/container-build-push-by-digest@v3
        with:
          images: |
            ghcr.io/${{ github.repository }}
            registry.org/foo/${{ github.event.repository.name }}
          labels: |
            org.opencontainers.image.description=Some Service
            org.opencontainers.image.licenses=AGPL-3.0
          dockerfile: ./Dockerfile
          context: ./build
          build-args: |
            FOO=bar
            LOREM=ipsum
```

## Inputs

| Name           | Description                                                                                                   |          |
| -------------- | ------------------------------------------------------------------------------------------------------------- | -------- |
| images         | Newline separated list of container image names                                                               | Requires |
| labels         | Newline separated list of labels for the built image.                                                         | Optional |
| annotations    | Newline separated list of annotations for the built image.                                                    | Optional |
| context        | The build context for the Docker build. Default is the current working directory.                             | Optional |
| dockerfile     | The path to the Dockerfile to use for the build. Default is {context}/Dockerfile.                             | Optional |
| provenance     | Whether to enable or disable provenance generation. Default is 'false'.                                       | Optional |
| oci-mediatypes | Whether to use OCI instead of docker media types. Default is 'true'.                                          | Optional |
| push           | Whether to push the built image to the registry. Default is 'true'.                                           | Optional |
| build-args     | A newline separated list of build arguments to pass to the Docker build. Example: 'ARG1=value1\nARG2=value2'. | Optional |
| platforms      | A comma-separated list of target platforms for the build. Default is 'linux/amd64'.                           | Optional |
| setup-qemu     | Whether to set up QEMU for cross-platform builds. Default is 'false'.                                         | Optional |

## Output

| Output Variable | Description                              |
| --------------- | ---------------------------------------- |
| digest          | The digest of the built container image. |
