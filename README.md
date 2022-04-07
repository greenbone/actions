# Greenbone GitHub Actions

GitHub Action for Greenbone projects

## Usage

```yml
- name: Install python and poetry and the project
  uses: greenbone/actions/poetry@v1
  with:
    version: 3.9

- name: Install python, poetry, project and run coverage
  uses: greenbone/actions/coverage-python@v1
  with:
    version: 3.9

- name: Run coverage for javascript
  uses: greenbone/actions/coverage-js@v1

- name: Install python, poetry, project and run lint
  uses: greenbone/actions/lint-python@v1
  with:
    version: 3.9

- name: upload documentation coverage to codecov.io for C Lang repository
  uses: greenbone/actions/doc-coverage-clang@v1

- name: Create a tag string for using with docker build-push-action
  uses: greenbone/actions/container-image-tags@v1

- name: Run release actions
  uses: greenbone/actions/release@v1
  with:
    github-user: ${{ secrets.GREENBONE_BOT }}
    github-user-mail: foo@bar.baz
    github-user-token: bar
    gpg-key: boo
    gpg-passphrase: foo
    gpg-fingerprint: baz
    conventional-commits: false
    strategy: calendar

- name: Run update header
  uses: greenbone/actions/update-header@v1
  with:
    github-user: ${{ secrets.GREENBONE_BOT }}
    github-user-mail: foo@bar.baz
    github-user-token: bar
    directories: foo tests
    target: main

- name: Create a sha256sums file for the foo directory
  uses: greenbone/actions/hashsums@v1
  with:
    directory: ./foo

- name: Create a GPG signature
  uses: greenbone/actions/signature@v1
  with:
    gpg-key: ${{ secrets.GPG_KEY }}
    gpg-passphrase: ${{ secrets.GPG_PASSPHRASE }}
    gpg-fingerprint: ${{ secrets.GPG_FINGERPRINT }}
    file: ./foo/bar
```
