# Sign Windows Binary

GitHub Action to sign a Windows binary.

## Example

```yml
name: Sign Windows Binary

on:
  release:
    types: [published]

jobs:
  sign:
    name: Sign Windows Binary
    runs-on: windows-latest
    steps:
        - uses: greenbone/actions/sign-win-binary@v1
          with:
```

## Action Configuration

| Input Variable    | Description                                                                              |                                                  |
| ----------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------ |
|                   |                                                                                          |                                                  |
