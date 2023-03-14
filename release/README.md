# Release action

You can use the release action to release a project within a GitHub Action workflow.

## Supported Programming Languages

Currently supported programming languages:
* C/C++ (CMake)
* GoLang
* JavaScript
* Python
* TypeScript

## Supported Release types

Currently this action can create different types of releases.
Supported with the `release-type` argument are `major`, `minor`, `patch` and different type of `pre-releases`. Additionally you can also use `calendar` versioning.

| Type              | Old version      | New version      |
|-------------------|------------------|------------------|
| major             |      `1.x.x`     |      `2.x.x`     |
| minor             |      `x.1.x`     |      `x.2.x`     |
| patch             |      `x.x.1`     |      `x.x.2`     |
| alpha             |      `x.x.1`     |   `x.x.2-a1`     |
| alpha             |   `x.x.2-a1`     |   `x.x.2-a2`     |
| alpha             |   `x.x.2-alpha1` |   `x.x.2-alpha2` |
| beta              |      `x.x.1`     |   `x.x.2-a1`     |
| beta              |   `x.x.2-a1`     |   `x.x.2-b1`     |
| release-candidate |   `x.x.2-a3`     |  `x.x.2-rc1`     |
| release-candidate |      `x.x.2`     |  `x.x.3-rc1`     |
| calendar          |     `20.5.1`     |     `23.2.0`     |
| calendar          |     `23.2.1`     |     `23.2.2`     |

You can alternatively set an explicit `release-version`. It will overwrite the `release-type` argument.

**NOTE:** The release will only be successful, if the release version has a valid schema.

## Input arguments

| Argument             | Description                                                                                                                     | Required? | Default               |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------|-----------|-----------------------|
| conventional-commits | Deprecated                                                                                                                      | No        | None                  |
| github-user          | Github user name on behalf of whom the actions will be executed.                                                                | Yes       | None                  |
| github-user-mail     | Mail address for the given github user.                                                                                         | Yes       | None                  |
| github-user-token    | Token with write rights required to create the release.                                                                         | Yes       | None                  |
| gpg-fingerprint      | GPG fingerprint, represented as a string. Required for signing assets of the release.                                           | No        | None                  |
| gpg-key              | GPG key, represented as a string. Required for signing assets of the release.                                                   | No        | None                  |
| gpg-passphrase       | GPG passphrase, represented as a string. Required for signing assets of the release.                                            | No        | None                  |
| strategy             | Deprecated by `release-type`.                                                                                                   | No        | None                  |
| python-version       | Python version used to create the release. (Only important for python projects)                                                 | No        | `"3.10"`              |
| ref                  | This branch's/tag's HEAD will be candidate of the next release.                                                                 | No        | `""` (default branch) |
| release-type         | What type of release should be executed? Supported: `alpha`, `beta`, `calendar`, `major`, `minor`, `patch`, `release-candidate` | No        | `patch`               |
| release-version      | Set an explicit version, that should be released.                                                                               | No        | None                  |
| versioning-scheme    | What versioning scheme should be used for the release? Supported: `semantic`, `pep440`                                          | No        | `pep440`              |


## Examples

```yml
- name: Run release actions with release type
  uses: greenbone/actions/release@v2
  with:
    github-user: ${{ secrets.FOO_BAR }}
    github-user-mail: foo@bar.baz
    github-user-token: bar
    gpg-key: boo
    gpg-passphrase: foo
    gpg-fingerprint: baz
    release-type: minor
```

```yml
- name: Run release actions with release version
  uses: greenbone/actions/release@v2
  with:
    github-user: ${{ secrets.FOO_BAR }}
    github-user-mail: foo@bar.baz
    github-user-token: bar
    gpg-key: boo
    gpg-passphrase: foo
    gpg-fingerprint: baz
    release-version: 2.0.0a1
    ref: main
```