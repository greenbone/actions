# Mattermost notify

Sends workflow status messages to a Mattermost channel.

## Example

- Create a yml file under /.github/workflows.
- Add under "workflows:" the workflows you want to receive a status message about.

```yaml
name: CI notify

on:
  workflow_run:
    # Workflows need to be added here!
    workflows:
      - test-notify
      - test-notify-ok
    types:
      - completed

jobs:
  notify:
    name: Mattermost notify
    runs-on:
      - self-hosted
      - self-hosted-generic
    steps:
      - uses: greenbone/actions/mattermost-notify@v1
        with:
            MATTERMOST_WEBHOOK_URL: ${{ secrets.MATTERMOST_WEBHOOK_URL }}
            MATTERMOST_CHANNEL: ${{ secrets.MATTERMOST_CHANNEL }}
            MATTERMOST_HIGHLIGHT: USER1 USER2
```

## Action Configuration

|Input Variable|Description| |
|--------------|-----------|-|
| MATTERMOST_WEBHOOK_URL | Mattermost webhook url | Required |
| MATTERMOST_CHANNEL | Mattermost channel | Required |
| MATTERMOST_HIGHLIGHT | List of space separated users to highlight in the channel | Optional |
