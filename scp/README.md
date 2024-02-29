# Scp files/folder

- Copy files/folder from/to a remote host.

#### Use Case

```yaml
jobs:
    name: Scp folder
    runs-on: ubuntu-latest
    steps:
      - name: Pull /var/log from remote host
        uses: greenbone/actions/scp@v3
        with:
          local-path: "/tmp"
          remote-path: "/var/log"
          known-hosts: "known hosts string"
          ssh-host: "remote server DNS"
          ssh-private-key: "private key string"
```

## Action Input

| Input Variable  | Description                                                  |          |
|-----------------|--------------------------------------------------------------|----------|
| mode            | Push or pull files/folder from remote host. Default is pull. | Optional |
| local-path      | Local files/folder path.                                     | Required |
| remote-path     | Remote files/folder path.                                    | Required |
| known-hosts     | SSH known hosts string.                                      | Required |
| ssh-user        | SSH login user. Default is root.                             | Optional |
| ssh-host        | SSH remote host IP/DNS.                                      | Required |
| ssh-private-key | SSH private key string.                                      | Required |
| ssh-tmp         | SSH private key storage folder path. Default is /tmp/ssh.    | Optional |
