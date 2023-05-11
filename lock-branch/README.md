# Lock Branch Action

GitHub Action to lock and unlock a branch of a GitHub repository.

## Examples

```yml
name: Lock and Unlock Branch

on:
  push:

jobs:
  lock:
    name: Lock/Unlock
    runs-on: ubuntu-latest
    steps:
      - name: lock <target> branch on <repository>
        uses: greenbone/actions/lock-branch@v2
        with:
          lock: "true"
          branch: <target>
          repository: <repository>
      - name: unlock <target> branch on <repository>
        uses: greenbone/actions/lock-branch@v2
        with:
          lock: "false"
          branch: <target>
          repository: <repository>
```

```yml
name: Lock and Unlock default Branch on current Repository

on:
  push:

jobs:
  lock:
    name: Lock/Unlock
    runs-on: ubuntu-latest
    steps:
      - name: lock default branch
        uses: greenbone/actions/lock-branch@v2
        with:
          lock: "true"
      - name: unlock default branch
        uses: greenbone/actions/lock-branch@v2
        with:
          lock: "false"
```

## Action Configuration

|Input Variable|Description| |
|--------------|-----------|-|
| github-token | Github user token, that is legitimated to set the lock. | Optional (default: `${{ github.token }}`) |
| lock | Lock or unlock (Options: `"true"`, `"false"`) | Optional (default is `"true"`) |
| repository | What repository branch should be locked? Defaults to the executing repository. | Optional (default is `${{ github.repository }}`) |
| branch | Branch that should be locked. | Optional (default is `"main"`) |
