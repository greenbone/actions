# Release action

You can use the release action to release a project within a GitHub Action workfl.
Currently supported programming languages:
* C
* GoLang
* JavaScript
* Python
* TypeScript

Currently this action can create `major`, `minor`, `patch` and `pre-releases`. Additionally you can use `calendar` versioning.

| Type              | Old version  | New version  |
|-------------------|--------------|--------------|
| major             |      `1.x.x` |      `2.x.x` |
| minor             |      `x.1.x` |      `x.2.x` |
| patch             |      `x.x.1` |      `x.x.2` |
| alpha             |      `x.x.1` |    `x.x.2a1` |
| alpha             |    `x.x.2a1` |    `x.x.2a2` |
| beta              |      `x.x.1` |    `x.x.2a1` |
| beta              |    `x.x.2a1` |    `x.x.2b1` |
| release-candidate |    `x.x.2a3` |   `x.x.2rc1` |
| release-candidate |      `x.x.2` |   `x.x.3rc1` |
| calendar          |     `20.5.1` |     `23.2.0` |
| calendar          |     `23.2.1` |     `23.2.2` |

## Example

```yml
- name: Run release actions
  uses: greenbone/actions/release@v2
  with:
    github-user: ${{ secrets.FOO_BAR }}
    github-user-mail: foo@bar.baz
    github-user-token: bar
    gpg-key: boo
    gpg-passphrase: foo
    gpg-fingerprint: baz
    strategy: calendar
    ref: main
```