# Release action

You can use the release action to release a project within a GitHub Action workflow.

## Supported Programming Languages

Currently supported programming languages:

* C/C++ (CMake)
* GoLang
* JavaScript
* Java
* Python
* TypeScript

## Supported Release types

Currently this action can create different types of releases.
Supported with the `release-type` argument are `major`, `minor`, `patch` and different type of `pre-releases`. Additionally you can also use `calendar` versioning.

| Type              | Old version    | New version    |
| ----------------- | -------------- | -------------- |
| major             | `1.x.x`        | `2.x.x`        |
| minor             | `x.1.x`        | `x.2.x`        |
| patch             | `x.x.1`        | `x.x.2`        |
| alpha             | `x.x.1`        | `x.x.2-a1`     |
| alpha             | `x.x.2-a1`     | `x.x.2-a2`     |
| alpha             | `x.x.2-alpha1` | `x.x.2-alpha2` |
| beta              | `x.x.1`        | `x.x.2-a1`     |
| beta              | `x.x.2-a1`     | `x.x.2-b1`     |
| release-candidate | `x.x.2-a3`     | `x.x.2-rc1`    |
| release-candidate | `x.x.2`        | `x.x.3-rc1`    |
| calendar          | `20.5.1`       | `23.2.0`       |
| calendar          | `23.2.1`       | `23.2.2`       |

You can alternatively set an explicit `release-version`. It will overwrite the `release-type` argument.

**NOTE:** The release will only be successful, if the release version has a valid schema.

## Input arguments

| Argument             | Description                                                                                                                                                                               | Required?                                        |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| conventional-commits | Deprecated                                                                                                                                                                                | Optional                                         |
| git-tag-prefix       | Set git tag prefix to the passed input. Default: 'v'                                                                                                                                      | Optional (default is `v`)                        |
| github-user          | Github user name on behalf of whom the actions will be executed.                                                                                                                          | Yes                                              |
| github-user-mail     | Mail address for the given github user.                                                                                                                                                   | Yes                                              |
| github-user-token    | Token with write rights required to create the release.                                                                                                                                   | Yes                                              |
| gpg-fingerprint      | GPG fingerprint, represented as a string. Required for signing assets of the release.                                                                                                     | Optional                                         |
| gpg-key              | GPG key, represented as a string. Required for signing assets of the release.                                                                                                             | Optional                                         |
| gpg-passphrase       | GPG passphrase, represented as a string. Required for signing assets of the release.                                                                                                      | Optional                                         |
| strategy             | Deprecated by `release-type`.                                                                                                                                                             | Optional                                         |
| python-version       | Python version used to create the release. (Only important for python projects)                                                                                                           | Optional (default `"3.10"` )                     |
| ref                  | This branch's/tag's HEAD will be candidate of the next release.                                                                                                                           | Optional (default: `main`)                       |
| release-type         | What type of release should be executed? Supported: `alpha`, `beta`, `calendar`, `major`, `minor`, `patch`, `release-candidate`                                                           | Optional (default: `patch`)                      |
| release-version      | Set an explicit version, that should be released.                                                                                                                                         | Optional                                         |
| release-series       | Allow to determine release versions for an older release series like '22.4'.                                                                                                              | Optional                                         | None |
| versioning-scheme    | What versioning scheme should be used for the release? Supported: `semver`, `pep440`                                                                                                      | Optional (default: `pep440` )                    |
| sign-release-files   | Create and upload release file signatures. Default is 'true'. Set to an other string then 'true' to disable the signatures.                                                               | Optional (default `"true"`)                      |
| update-project       | Update version in project files like `pyproject.toml`. Default is 'true'. Set to an other string then 'true' to disable updating project files.                                           | Optional (default `"true"`)                      |
| next-version         | Set an explicit version that should be used after the release. Leave empty for determining the next version automatically. Set to `'false'` for not updating the version after a release. |                                                  |
| github-pre-release   | Set to `'true'`` to enforce uploading the release to GitHub as a pre-release                                                                                                              |                                                  |
| repository           | GitHub repository (owner/name) to create the release for.                                                                                                                                 | Optional (default is `${{ github.repository }}`) |
| changelog            | A path to a changelog file. If not set a changelog will be generated.                                                                                                                     | Optional                                         |
| last-release-version | The last release version. If not set, it will be detected automatically.                                                                                                                  | Optional                                         |

## Output Arguments

| Output Variable      | Description                                                                                              |
| -------------------- | -------------------------------------------------------------------------------------------------------- |
| release-version      | Version of the release. Depending on the inputs it is calculated from the detected last release version. |
| last-release-version | Detected version of the previous release.                                                                |
| git-release-tag      | Git tag created for the release version                                                                  |
| next-version         | Version set after a successful release                                                                   |


## Examples

```yml
name: Release Project with CalVer

on:
  pull_request:
    types: [closed]
  workflow_dispatch:

jobs:
  release:
    name: Create a new release with pontos
    # If the event is a workflow_dispatch or the label 'make release' is set and PR is closed because of a merge
    if: (github.event_name == 'workflow_dispatch') || (contains( github.event.pull_request.labels.*.name, 'make release') && github.event.pull_request.merged == true)
    runs-on: "ubuntu-latest"
    steps:
      - name: Run release actions with release type
        uses: greenbone/actions/release@v3
        with:
          github-user: ${{ secrets.FOO_BAR }}
          github-user-mail: foo@bar.baz
          github-user-token: bar
          gpg-key: boo
          gpg-passphrase: foo
          gpg-fingerprint: baz
          release-type: "calendar"
```

```yml
name: Release Project

on:
  pull_request:
    types: [closed]
  workflow_dispatch:

jobs:
  release:
    name: Create a new release with pontos
    # If the event is a workflow_dispatch or the label 'make release' is set and PR is closed because of a merge
    if: (github.event_name == 'workflow_dispatch') || (contains( github.event.pull_request.labels.*.name, 'make release') && github.event.pull_request.merged == true)
    runs-on: "ubuntu-latest"
    steps:
      - name: Run release actions with release version
        uses: greenbone/actions/release@v3
        with:
          github-user: ${{ secrets.FOO_BAR }}
          github-user-mail: foo@bar.baz
          github-user-token: bar
          gpg-key: boo
          gpg-passphrase: foo
          gpg-fingerprint: baz
          release-version: 2.0.0a1
          ref: "main"
```

```yml
name: Release project and upload additional release files

on:
  pull_request:
    types: [closed]
  workflow_dispatch:

jobs:
  release:
    name: Create a new release with pontos
    # If the event is a workflow_dispatch or the label 'make release' is set and PR is closed because of a merge
    if: (github.event_name == 'workflow_dispatch') || (contains( github.event.pull_request.labels.*.name, 'make release') && github.event.pull_request.merged == true)
    runs-on: "ubuntu-latest"
    steps:
      - name: Run release actions with release version
        id: release
        uses: greenbone/actions/release@v3
        with:
          release-type: "patch"
          versioning-scheme: "semver"
          sign-release-files: "false"
      - name: Upload additional release files
        run: |
          gh release upload ${{ steps.release.outputs.git-release-tag }} some_files/*
      - name: Sign all release files
        uses: greenbone/actions/sign-release-files@v3
          with:
            gpg-key: ${{ secrets.GPG_KEY }}
            gpg-fingerprint: ${{ secrets.GPG_FINGERPRINT }}
            gpg-passphrase: ${{ secrets.GPG_PASSPHRASE }}
            release-version: ${{ steps.release.outputs.release-version }}
```
