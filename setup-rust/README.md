# Setup Rust Action

Action to setup a rust environment.

## Example

```yml

name: Build with rust

on:
  push:


jobs:
  build:
  runs-on: ubuntu-latest
  steps:
    - name: Setup Rust
      uses: greenbone/actions/setup-rust@v3
    - name: Build
      run: |
        cargo build
```

## Action Configuration

| Input        | Description                                       |                                |
| ------------ | ------------------------------------------------- | ------------------------------ |
| rust-version | The rust version to setup, for example `nightly`. | Optional (default is `stable`) |
