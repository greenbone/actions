# Container signing

Cosign based action to create container signatures.

## Examples

```yml
name: Container signing

on:
  push:

jobs:
  container-signing:
    name: Container signing
    runs-on: ubuntu-latest
    steps:
      - uses: docker/login-action@v2
        ...
      - uses: docker/metadata-action@v4
        id: meta
        ...
      - uses: docker/build-push-action@v3
        id: build-and-push
        ...
      - name: Container signing
        uses: greenbone/actions/container-signing@v3
        with:
          docker-digest: ${{ steps.build-and-push.outputs.digest }}
          docker-tags: ${{ steps.meta.outputs.tags }}
```

## Action Configuration

|Input Variable|Description|Optional|
|--------------|-----------|--------|
|docker-digest|Set the digest from the docker build and push action e.g the output of steps.build-and-push.outputs.digest.|false|
|docker-tags|Set the tags from the docker meta action e.g the output of steps.meta.outputs.tags.|false|
|cosign-key-password|Set the cosign key password, it not set a keyless signature will be created.|true|
|cosign-key|Set the cosign key, it not set a keyless signature will be created.|true|
