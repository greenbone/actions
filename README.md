![Greenbone Logo](https://www.greenbone.net/wp-content/uploads/gb_new-logo_horizontal_rgb_small.png)

# Greenbone GitHub Actions

Repository that contains a collection of GitHub Actions for Greenbone projects

## Language specific Actions

We offer several actions for linting, formatting, building and testing packages/modules/projects in different programming languages

### Python

* [Install python, poetry and the project](https://github.com/greenbone/actions/tree/v2/poetry)
* [Install python, poetry, project and run coverage to create a code coverage report](https://github.com/greenbone/actions/tree/v2/coverage-python)
* [Install python, poetry, project and run linter](https://github.com/greenbone/actions/tree/v2/lint-python)
* [Install python, poetry, project and and run mypy type checker](https://github.com/greenbone/actions/tree/v2/mypy-python)
* [Install python, poetry, build python package and upload it to PyPI](https://github.com/greenbone/actions/tree/v2/pypi-upload)
* [Setup python and pontos](https://github.com/greenbone/actions/tree/v2/setup-pontos)

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

## Language independent Actions
### Branch protection

* [Lock and unlock a branch in a GitHub repository](https://github.com/greenbone/actions/tree/v2/lock-branch)
* [Allow and disallow admin users bypassing protection rules](https://github.com/greenbone/actions/tree/v2/admin-bypass)

### Other useful actions

* [Release a project in C, GoLang, JavaScript or Python](https://github.com/greenbone/actions/tree/v2/release)
* [Create and upload signatures for GitHub release files](https://github.com/greenbone/actions/tree/v2/sign-release-files)
* [Report usage of conventional commits in a Pull Request](https://github.com/greenbone/actions/tree/v2/conventional-commits)
* [Check for consistent versioning in a project](https://github.com/greenbone/actions/tree/v2/check-version)
* [Backport Pull Requests to other additional branches](https://github.com/greenbone/actions/tree/v2/backport-pull-request)
* [Workflow notifications in Mattermost channels](https://github.com/greenbone/actions/tree/v2/mattermost-notify)
* [Trigger Workflow Runs](https://github.com/greenbone/actions/tree/v2/trigger-workflow)
* [Download Workflow Artifacts from a different workflow or even repository](https://github.com/greenbone/actions/tree/v2/trigger-workflow)

Update license header supporting many different filetypes

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

For any question on the usage of the Greenbone actions please use the
[Greenbone Community Forum](https://forum.greenbone.net/). If you
found a problem with the software, please
[create an issue](https://github.com/greenbone/actions/issues)
on GitHub.

## Maintainer

This project is maintained by [Greenbone AG](https://www.greenbone.net/).

## License

Copyright (C) 2020-2023 [Greenbone AG](https://www.greenbone.net/)

Licensed under the [GNU General Public License v3.0 or later](LICENSE).
