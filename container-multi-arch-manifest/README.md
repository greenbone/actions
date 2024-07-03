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

| Name                | Description                                                                                    |          |
|---------------------|------------------------------------------------------------------------------------------------|----------|
| annotations         | New line seperated annotation list.                                                            | Required |
| cosign-key          | Cosign key to sign the image. Will be skipped if empty. Default is empty.                      | Required |
| cosign-key-password | Cosign key password. Will be skipped if empty. Default is empty.                               | Required |
| cosign-tlog-upload  | "Turn on or turn off the cosign tlog upload function. Options are true/false. Default is true. | Required |
| digests             | New line seperated container image digest list.                                                | Required |
| tags                | New line seperated multi-arch tag list.                                                        | Required |
| url                 | Image url/name without registry.                                                               | Required |
| registry            | Login registry username.                                                                       | Required |
| registry-username   | Login registry username.                                                                       | Required |
| registry-password   | Login registry password.                                                                       | Required |
