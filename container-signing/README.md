# Container signing

Cosign based action to create container signatures.

Depending on the input public/private key or keyless signatures are created.

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
          image-tags: ${{ steps.meta.outputs.tags }}
```

## Action Configuration

|Input Variable|Description|Optional|
|--------------|-----------|--------|
|image-tags|Set the tags from the docker meta action e.g the output of steps.meta.outputs.tags.|false|
|image-digest|Set the digest from the docker build and push action e.g the output of steps.build-and-push.outputs.digest.|true|
|cosign-key-password|Set the cosign key password, if not set a keyless signature will be created.|true|
|cosign-key|Set the cosign key, if not set a keyless signature will be created.|true|
