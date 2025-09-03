# Sign Windows Binary

GitHub Action to sign a Windows binary.

## Example

```yml
name: Sign Windows Binary

on:
  workflow_dispatch:

jobs:
  sign-win-binary:
    name: Sign Windows Binary
    runs-on: windows-latest
    steps:
      - uses: greenbone/actions/sign-win-binary@v3.33.0
        with:
          file: "pathToFile"
          signing-certificate: "someCert.cer"
          signing-password: "somePassword"
          timestamp-url: "https://some.url"
```

## Action Configuration

| Input Variable               | Description                                                         |                                           |
|------------------------------|---------------------------------------------------------------------|-------------------------------------------|
| file                         | The file to sign with signtool.exe                                  |                                           |
| signing-certificate          | The certificate for signing the file                                | Base64 encoded                            |
| signing-certificate-hash-alg | The hash algorithm used for the signing-certificate                 | Optional: (Default is `"sha512"`)         |
| signing-password             | The password for the signing certificate                            |                                           |
| timestamp-url                | The url of the timestamp server                                     |                                           |
| timestamp-hash-alg           | The hash algorithm used for the timestamp server                    | Optional: (Default is `"sha512"`)         |
