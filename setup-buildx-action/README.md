# Greenbone Setup Buildx Action

- Buildx is pre-installed in the self hosted environment. The Buildx container is CA incompatible with our caching system.

## Use Case

```yaml
jobs:
  self-hosted:
    name: Setup Buildx Action
    runs-on: ubuntu-latest
    steps:
      - uses: greenbone/actions/setup-buildx-action@v3
```

## Action Configuration

| Input Variable          | Description                                                           |          |
| ----------------------- | ----------------------------------------------------------------------| -------- |
| skip-installation-on    | Skip installation on selected runner. Default is self-hosted-generic. | Optional |
