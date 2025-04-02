# Push and sign an artifact

GitHub Action that pushes an artifact with oras and signs it with cosign.

## Examples

```yml
name: Push and sign an artifact

on:
  push:

jobs:
  push-and-sign:
    name: Push and sign an artifact
    runs-on: ubuntu-latest
    steps:
      - uses: greenbone/actions/push-and-sign-artifact@v3
        with:
          artifact-file: < artifact-file >
          artifact-url: < artifact-url >
          artifact-folder: < artifact-folder >
          registry-user: < registry-user >
          registry-domain: < registry-domain >
          registry-token: < registry-token >
          cosign-key: < cosign-key >
          cosign-password: < cosign-password >
          oras-version: < oras-version >
          oras-md5sum: < oras-md5sum >
```

## Action Configuration

|Input Variable|Description| |
|--------------|-----------|-|
| artifact-file | The artifact to build. | |
| artifact-url | The artifact-url to upload the artifact into (with tag). | |
| artifact-folder | The path to the system folder to save the artifact file. Default is /tmp. | |
| registry-user | Registry user name. | |
| registry-domain | Registry domain. | |
| registry-token | Registry user token. Set is input only if you want to upload an artifact. | |
| cosign-key | Key for Signing artifacts/containers. | |
| cosign-password | Password for COSIGN key. | |
| oras-version | Version of oras. | |
| oras-md5sum | md5sum of oras. | |
