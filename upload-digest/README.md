# Upload a Digest

This action uploads a container image digest file as an artifact.

## Example

```yml
name: Create Images by Digest

on:
  push:

jobs:
  build:
    runs-on: "ubuntu-latest"
    strategy:
      matrix:
        arch:
          - linux/amd64
          - linux/arm64
    steps:
      - name: Create Image
        uses: greenbone/actions/container-build-push-by-digest@v3
        id: build
        with:
          images: |
            ghcr.io/${{ github.repository }}
            registry.org/foo/${{ github.event.repository.name }}
          labels: |
            org.opencontainers.image.description=Some Service
            org.opencontainers.image.licenses=AGPL-3.0
          dockerfile: ./Dockerfile
          context: ./build
          platforms: ${{ matrix.arch }}
          build-args: |
            FOO=bar
            LOREM=ipsum
      - name: Upload Digest
        uses: greenbone/actions/upload-digest@v3
        with:
          name: digests-${{ matrix.arch }}
          digest: ghcr.io/${{ github.repository }}@${{ steps.build.outputs.digest }}

  download:
    needs:
      - build
    runs-on: "ubuntu-latest"
    name: Download and display digests
    jobs:
      - name: Download digests
        id: download
        uses: greenbone/actions/download-digest@v3
        with:
          pattern: digests-*
      - name: Display digests
        run: |
          echo "${{ steps.download.outputs.digests }}
```

## Inputs

| Name   | Description                                                                                  |          |
| ------ | -------------------------------------------------------------------------------------------- | -------- |
| digest | The digest of the container image to upload (should include the image name).                 | Required |
| name   | The name of the artifact to create. Should fit to the pattern of the download-digest action. | Required |
