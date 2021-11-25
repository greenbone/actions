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
```
