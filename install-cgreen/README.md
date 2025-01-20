# Install the cgreen testing framework

GitHub Action to install the [cgreen](https://github.com/cgreen-devs/cgreen)
testing framework into the current runner. The cgreen testing framework is
intended for C and C++.

## Use Case

```yaml
jobs:
  test:
    name: Run Unit Tests
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: "Instal cgreen"
        uses: greenbone/actions/install-cgreen@v3
```

## Action Configuration

| Input Variable | Description                                          | Default                                                            |
| ---------------| -----------------------------------------------------| ------------------------------------------------------------------ |
| version        | cgreen release version to use                        | `1.6.2`                                                            |
| hash           | SHA256 hash of the downloaded cgreen release tarball | `fe6be434cbe280330420106bd5d667f1bc84ae9468960053100dbf17071036b9` |
