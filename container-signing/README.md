# Container signing

Cosign based action to create container signatures.

Depending on the input public/private key or keyless signatures are created.

## Info

The docker/setup-buildx-action action is needed or we get a wrong digest from
 the docker/build-push-action action.

For keyless signatures with ghcr.io you have to set this permissions.

```yml
permissions:
  contents: read
  packages: write
  id-token: write
```

And use the docker/login-action action with this settings.

```yml
- uses: docker/login-action@v2
  registry: ghcr.io
  username: ${{ github.actor }}
  password: ${{ secrets.GITHUB_TOKEN }}
```

## Examples

```yml
name: Container signing

on:
  push:

permissions:
  contents: read
  packages: write
  id-token: write

jobs:
  container-signing:
    name: Container signing
    runs-on: ubuntu-latest
    steps:
      - uses: docker/login-action@v2
        registry: ghcr.io
        username: ${{ github.actor }}
        password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/setup-buildx-action@v2
      - uses: docker/metadata-action@v4
        id: meta
        ...
      - uses: docker/build-push-action@v3
        id: build-and-push
        ...
      - name: Container signing
        uses: greenbone/actions/container-signing@v3
        with:
          image-tags: ${{ steps.meta.outputs.tags }}
          image-digest: ${{ steps.build-and-push.outputs.digest }}
```

## Action Configuration

|Input Variable|Description| |
|--------------|-----------|--------|
|image-tags|Set the tags from the docker meta action e.g the output of steps.meta.outputs.tags.|Required|
|image-digest|Set the digest from the docker build and push action e.g the output of steps.build-and-push.outputs.digest.|Required|
|cosign-key-password|Set the cosign key password, if not set a keyless signature will be created.|Optional|
|cosign-key|Set the cosign key, if not set a keyless signature will be created.|Optional|
