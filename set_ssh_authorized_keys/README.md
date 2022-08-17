# Create ssh authorized keys file

- Create ssh authorized keys file.

#### Use Case

```yaml
jobs:
  ssh_authorized_key:
    name: Create ssh authorized keys file
    runs-on:
      - self-hosted
      - self-hosted-generic
    steps:
      - name: Create ssh authorized keys file
        uses: greenbone/actions/set_ssh_authorized_keys@v1
        with:
          ssh_authorized_key: ${{ secrets.KEYS }
```

