# Sign Release Files

GitHub Action to download all GitHub release asset files, create a signature for
all downloaded files and upload these signatures to the GitHub release.

## Example

```yml
name: Sign Release Files

on:
  release:
    types: [published]

jobs:
  sign:
    name: Sign Release Files
    runs-on: ubuntu-latest
    steps:
        - uses: greenbone/actions/sign-release-files@v2
          with:
            gpg-key: ${{ secrets.GPG_KEY }}
            gpg-fingerprint: ${{ secrets.GPG_FINGERPRINT }}
            gpg-passphrase: ${{ secrets.GPG_PASSPHRASE }}
```

## Action Configuration

|Input Variable|Description| |
|--------------|-----------|-|
| python-version  | Python version to use for running the action. | Optional (default is `3.10`) |
| git-tag-prefix  | Set git tag prefix to the passed input. Default: 'v' | Optional (default is `v`) |
| gpg-fingerprint | GPG fingerprint, represented as a string. | Required |
| gpg-key         | GPG key, represented as a string. | Required |
| gpg-passphrase  | GPG passphrase, represented as a string. | Required |
| release-version | Set an explicit version, that should be released. | Optional |
| release-series  | Allow to determine release versions for an older release series like `"22.4"`. | Optional |
| versioning-scheme | What versioning scheme should be used for the release? Supported: `"semver"`, `"pep440"` | Optional (default is `"pep440"`) |
| github-token | Token with write rights for releases to download and upload release asset files. | Optional (default is `${{ github.token }}`) |
