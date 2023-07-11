# Create ssh known hosts file

- Create ssh known hosts file.

#### Use Case

```yaml
jobs:
  ssh-known-hosts:
    name: Create ssh known hosts file
    runs-on:
      - self-hosted
      - self-hosted-generic
    steps:
      - name: Create ssh known hosts file
        uses: greenbone/actions/ssh-known-hosts@v3
        with:
          known_hosts: ${{ secrets.KEYS }}
```

