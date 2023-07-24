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
      - uses: greenbone/actions/mattermost-notify@v3
        with:
            MATTERMOST_WEBHOOK_URL: ${{ secrets.MATTERMOST_WEBHOOK_URL }}
            MATTERMOST_CHANNEL: ${{ secrets.MATTERMOST_CHANNEL }}
            highlight: USER1 USER2
```

## Action Configuration

|Input Variable|Description| |
|--------------|-----------|-|
| MATTERMOST_WEBHOOK_URL | Mattermost webhook url | Required |
| MATTERMOST_CHANNEL | Mattermost channel | Required |
| MATTERMOST_HIGHLIGHT | List of space separated users to highlight in the channel | Deprecated. Use highlight instead |
| highlight | List of space separated users to highlight in the channel | Optional |
| branch | Git branch to use in the message | Optional. Will be derived from the event if not set. |
| commit | Git commit to use in the message | Optional. Will be derived from the event if not set. |
| commit-message | Git commit message to use in the message | Optional. Will be derived from the event if commit is not set. Otherwise it will be derived from the git log. |
| repository | GitHub repository (org/repo) | Optional. Default is `${{ github.repository }}` |
| workflow | GitHub workflow ID to use in the message | Optional |
| workflow-name | GitHub workflow name to use in the message | Optional |
