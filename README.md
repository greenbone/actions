# Greenbone GitHub Actions

GitHub Actions for Greenbone projects

## Usage

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

### Others

```yml
- name: upload documentation coverage to codecov.io for C Lang repository
  uses: greenbone/actions/doc-coverage-clang@v2

- name: Run release actions
  uses: greenbone/actions/release@v2
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
  uses: greenbone/actions/update-header@v2
  with:
    github-user: ${{ secrets.FOO_BAR }}
    github-user-mail: foo@bar.baz
    github-user-token: bar
    directories: foo tests
    target: main

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
