![Greenbone Logo](https://www.greenbone.net/wp-content/uploads/gb_new-logo_horizontal_rgb_small.png)

# Greenbone GitHub Actions

Repository that contains a collection of GitHub Actions for Greenbone projects

## Language specific CI actions

We offer several actions for linting, formatting, building and testing packages/modules/projects in different programming languages

### Python

```yml
- name: Install python and poetry and the project
  uses: greenbone/actions/poetry@v2
  with:
    version: 3.9

- name: Install python, poetry, project and run coverage
  uses: greenbone/actions/coverage-python@v2
  with:
    version: 3.9

- name: Install python, poetry, project and run lint
  uses: greenbone/actions/lint-python@v2
  with:
    version: 3.9
```

### JavaScript

```yml
- name: Install JavaScript and the project [npm]
  uses: greenbone/actions/install-npm@v2
  with:
    version: 3.9
    token: ${{ secrets.FOO_BAR }}
- name: Install and check Lint and Format in JavaScript Projects [npm]
  uses: greenbone/actions/lint-npm@v2
  with:
    version: 3.9
    token: ${{ secrets.FOO_BAR }}
- name: Install, Build and Test JavaScript Projects [npm]
  uses: greenbone/actions/test-npm@v2
  with:
    version: 3.9
    token: ${{ secrets.FOO_BAR }}
- name: Run coverage for javascript
  uses: greenbone/actions/coverage-js@v2
```

### GoLang

```yml
- name: Check Lint and Format in GoLang Projects
  uses: greenbone/actions/lint-golang@v2
  with:
    version: 3.9
    generate: go generate # mocks, docs, etc
    golangci-lint: v1.50 # specify golangci-lint version
```

### CLang

```yml
- name: upload documentation coverage to codecov.io for C Lang repository
  uses: greenbone/actions/doc-coverage-clang@v2
```

## Branch protection

```yml
- name: lock <target> branch on <repository>
  uses: greenbone/actions/lock-branch@v2
  with:
    lock: "true"
    github-token: ${{ token }}
    branch: <target>
    repository: <repository>
- name: unlock <target> branch on <repository>
  uses: greenbone/actions/lock-branch@v2
  with:
    lock: "false"
    github-token: ${{ token }}
    branch: <target>
    repository: <repository>
- name: allow admin bypassing protection on <target> branch on <repository>
  uses: greenbone/actions/admin-bypass@v2
  with:
    allow: "true"
    github-token: ${{ token }}
    branch: <target>
    repository: <repository>
- name: disable admin bypassing protection on <target> branch on <repository>
  uses: greenbone/actions/admin-bypass@v2
  with:
    allow: "false"
    github-token: ${{ token }}
    branch: <target>
    repository: <repository>
```

## Other useful actions


Release a project in C or JavaScript

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
    conventional-commits: false
    strategy: calendar
```

Release a Python project

```yml
- name: Release with release action
  uses: greenbone/actions/release-python@v2
  with:
    version: 3.9 # python version
    conventional-commits: true
    github-user: ${{ secrets.FOO_BAR }}
    github-user-mail: foo@bar.baz
    github-user-token: bar
    gpg-key: boo
    gpg-passphrase: foo
    gpg-fingerprint: baz
    strategy: calendar
```

Update licence header supporting many different filetypes

```yml
- name: Run update header
  uses: greenbone/actions/update-header@v2
  with:
    github-user: ${{ secrets.FOO_BAR }}
    github-user-mail: foo@bar.baz
    github-user-token: bar
    directories: foo tests
    target: main
```

SHA256 file or GPG signature generation

```yml
- name: Create a sha256sums file for the foo directory
  uses: greenbone/actions/hashsums@v2
  with:
    directory: ./foo

- name: Create a GPG signature
  uses: greenbone/actions/signature@v2
  with:
    gpg-key: ${{ secrets.FOO_BAR }}
    gpg-passphrase: ${{ secrets.FOO_BAZ }}
    gpg-fingerprint: ${{ secrets.BAR_BAZ }}
    file: ./foo/bar
```

## Support

For any question on the usage of python-gvm please use the
[Greenbone Community Forum](https://forum.greenbone.net/). If you
found a problem with the software, please
[create an issue](https://github.com/greenbone/actions/issues)
on GitHub.

## Maintainer

This project is maintained by [Greenbone Networks GmbH](https://www.greenbone.net/).

## License

Copyright (C) 2020-2022 [Greenbone Networks GmbH](https://www.greenbone.net/)

Licensed under the [GNU General Public License v3.0 or later](LICENSE).
