# Create ssh known hosts file

- Create ssh known hosts file.

#### Use Case

```yaml
jobs:
  ssh_known_hosts:
    name: Create ssh known hosts file
    runs-on:
      - self-hosted
      - self-hosted-generic
    steps:
      - name: Create ssh known hosts file
        uses: greenbone/actions/set_ssh_known_hosts@v1
        with:
          ssh_known_hosts: ${{ secrets.KEYS }
```

