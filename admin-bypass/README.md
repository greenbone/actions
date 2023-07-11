# Admin bypass Action

GitHub Action that allows or disallows repository admins to bypass branch
protection rules.

## Examples

```yml
name: Bypass Branch Protection

on:
  push:

jobs:
  lock:
    name: Bypass Protection
    runs-on: ubuntu-latest
    steps:
      - name: allow admin users bypassing protection on <target> branch on <repository>
        uses: greenbone/actions/admin-bypass@v3
        with:
          allow: "true"
          branch: <target>
          repository: <repository>
      - name: disable bypassing protection on <target> branch on <repository> for admin users
        uses: greenbone/actions/admin-bypass@v3
        with:
          allow: "false"
          branch: <target>
          repository: <repository>
```

## Action Configuration

|Input Variable|Description| |
|--------------|-----------|-|
| github-token | Github user token, that is legitimated to bypass branch protection. | Optional (default: `${{ github.token }}`) |
| allow | Allow or not? (Options: `"true"`, `"false"`)? | Optional (default is `"false"`) |
| repository | What repository branch should be able to be bypassed by admins? Defaults to the executing repository. | Optional (default is `${{ github.repository }}` |
| branch | Target branch for the bypass. | Optional (default is `"main"`) |
