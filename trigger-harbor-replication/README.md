# Trigger Harbor Replication Policy

An action to trigger a harbor replication policy.

## Example

```yml
name: Trigger harbor replication

on:
  push:

jobs:
  build:
    runs-on: "ubuntu-latest"
    steps:
      - uses: greenbone/actions/trigger-harbor-replication@v3
        with:
          registry: ${{ vars.HARBOR_REGISTRY }}
          user: ${{ secret.HARBOR_USER }}
          token: ${{ secret.HARBOR_TOKEN }}
```

## Inputs

| Name     | Description                                        |                          |
| -------- | -------------------------------------------------- | ------------------------ |
| registry | The URL of the Harbor registry (without https://)  | Required                 |
| token    | The token to authenticate with the Harbor registry | Required                 |
| user     | The user to authenticate with the Harbor registry  | Required                 |
| policy   | The ID of the policy to trigger                    | Optional (default: "1"). |
