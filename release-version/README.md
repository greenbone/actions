# Release Version

GitHub Action to determine the release version

## Example

```yml
name: Determine Release version

on:
  workflow_dispatch:
      release-type:
        type: choice
        description: What kind of release do you want to do?
        options:
          - patch
          - minor
          - major
          - release-candidate
          - alpha
          - beta

jobs:
  check:
    name: Determine Release Version
    runs-on: ubuntu-latest
    steps:
        - uses: greenbone/actions/release-version@v3
          id: release-version
          with:
            release-type: ${{ inputs.release-type }}
        - name: Print release type and ref
          run: |
            echo ${{ steps.release-version.outputs.last-release-version }}
            echo ${{ steps.release-version.outputs.last-release-version-major }}
            echo ${{ steps.release-version.outputs.last-release-version-minor }}
            echo ${{ steps.release-version.outputs.last-release-version-patch }}
            echo ${{ steps.release-version.outputs.release-version }}
            echo ${{ steps.release-version.outputs.release-version-major }}
            echo ${{ steps.release-version.outputs.release-version-minor }}
            echo ${{ steps.release-version.outputs.release-version-patch }}
```

## Action Configuration

| Input Variable    | Description                                                           |                             |
| ----------------- | --------------------------------------------------------------------- | --------------------------- |
| python-version    | Python version to use for running the code                            | Optional                    |
| release-type      | Type of the release.                                                  | Required                    |
| release-version   | A release version to use. Overrides release-type                      | Optional                    |
| release-series    | A release series to use.                                              | Optional                    |
| versioning-scheme | The versioning scheme to use for the release. Either pep440 or semver | Optional. Default is pep440 |
| git-tag-prefix    | The prefix for the git tags                                           | Optional. Default is 'v'    |

## Output Arguments

| Output Variable            | Description                           |
| -------------------------- | ------------------------------------- |
| last-release-version       | The last release version              |
| last-release-version-major | The major version of the last release |
| last-release-version-minor | The minor version of the last release |
| last-release-version-patch | The patch version of the last release |
| release-version            | The determined version of the release |
| release-version-major      | The major version of the release      |
| release-version-minor      | The minor version of the release      |
| release-version-patch      | The patch version of the release      |
