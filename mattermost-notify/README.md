# Mattermost notify

- Send a Mattermost message into a channel

## Examples

#### Use Case

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
            WORKFLOW_NAME: ${{ github.event.workflow_run.name }}
            REPOSITORY_NAME: ${{ github.event.workflow_run.head_repository.full_name }}
            CONCLUSION: ${{ github.event.workflow_run.conclusion }}
            BRANCH: ${{ github.event.workflow_run.head_branch }}
            WORKFLOW_URL: ${{ github.event.workflow_run.html_url }}
            REPOSITORY_URL: ${{ github.event.workflow_run.head_repository.html_url }}
            MATTERMOST_WEBHOOK_URL: ${{ secrets.MATTERMOST_WEBHOOK_URL }}
            MATTERMOST_CHANNEL: ${{ secrets.MATTERMOST_CHANNEL }}
```
