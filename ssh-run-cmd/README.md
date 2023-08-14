# SSH run cmd

- Action to run a bash cmd string on a remote host.

#### Use Case

```yaml
jobs:
    name: Run cmd over ssh
    runs-on: ubuntu-latest
    steps:
      - name: Run cmd
        uses: greenbone/actions/ssh-run-cmd@v3
        with:
          cmd: "ls -lh"
          known-hosts: "known hosts string"
          ssh-remote-host: "remote server DNS"
          ssh-private-key: "private key string"
```

## Action Input

| Input Variable  | Description                                             |          |
|-----------------|---------------------------------------------------------|----------|
| cmd             | Bash cmd string. Single quotes are not allowed.         | Required |
| known-hosts     | SSH known hosts string.                                 | Required |
| ssh-user        | SSH login user. Default: root.                          | Optional |
| ssh-remote-host | SSH remote host IP/DNS.                                 | Required |
| ssh-private-key | SSH private key string.                                 | Required |
| ssh-tmp         | SSH private key storage folder path. Default: /tmp/ssh. | Optional |
