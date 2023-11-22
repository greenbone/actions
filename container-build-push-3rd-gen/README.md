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

| Name                | Description                                                    |          |
|---------------------|----------------------------------------------------------------|----------|
| build-context       | Path to image build context. Default is the current directory. | Optional |
| build-docker-file   | Path to the docker file. Default is './Dockerfile'.            | Optional |
| build-args          | Use these build-args for the docker build process.             | Optional |
| cosign-key          | cosign key to sign the image.                                  | Optional |
| cosign-key-password | cosign key password.                                           | Optional |
| image-labels        | Image labels.                                                  | Required |
| image-url           | Image url/name without registry.                               | Required |
| image-regsitry      | "Image registry url."                  | Optional |
| image-platforms     | Image platforms to build for. Default is 'linux/amd64'.        | Optional |
| registry-password   | Registry password.                                             | Required |
