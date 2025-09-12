# Download a Digest

This action downloads container image digest files as artifacts and determines
their contents. Because it is not possible to use outputs in a matrix strategy,
this action can be used to collect the digests of multiple images built in
parallel jobs.

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

| Name    | Description                                                                 |          |
| ------- | --------------------------------------------------------------------------- | -------- |
| path    | The path to download the digest files to. Default is a temporary directory. | Optional |
| pattern | The pattern to match digest files. Default is 'digests-*'.                  | Optional |

## Output

| Output Variable | Description                                  |
| --------------- | -------------------------------------------- |
| digest          | The downloaded digests separated by newline. |
