# Create multi arch manifest

A action to create a multi arch manifest.

## Example

```yml
name: Create multi arch manifest

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: "ubuntu-latest"
    steps:
      - name: Create multi arch manifest
        uses: greenbone/actions/container-multi-arch-manifest@v3
        with:
          tags: |
            ${{ needs.build-amd64.outputs.tags }}
            ${{ needs.build-arm64.outputs.tags }}
          digests: |
            ${{ needs.build-amd64.outputs.digest }}
            ${{ needs.build-arm64.outputs.digest }}
          url: ${{ inputs.image-url }}
          registry: ${{ secrets.REGISTRY }}
          registry-username: ${{ secrets.REGISTRY_USER }}
          registry-password: ${{ secrets.REGISTRY_TOKEN }}
```

## Inputs

| Name              | Description                                                    |          |
|-------------------|----------------------------------------------------------------|----------|
| tags              | New line seperated multi-arch tag list.                        | Required |
| digests           | New line seperated container image digest list.                | Required |
| url               | Image url/name without registry. Default is github.repository. | Required |
| registry          | Login registry username.                                       | Required |
| registry-username | Login registry username.                                       | Required |
| registry-password | Login registry password.                                       | Required |
