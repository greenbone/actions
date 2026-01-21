# Mattermost notify

Sends workflow status messages to a Mattermost channel.

## Examples

### Usage with job needs

```yml
name: Some Workflow

on:
  pull_request:

  jobs:
    do-something:
    runs-on: ubuntu-latest
    steps:
      - name: Do Something
        run: |
          echo "I am doing something"

  notify:
    needs: do-something
    runs-on: ubuntu-latest
    steps:
      - uses: greenbone/actions/mattermost-notify@v3
        with:
            url: ${{ secrets.MATTERMOST_WEBHOOK_URL }}
            channel: ${{ secrets.MATTERMOST_CHANNEL }}
            highlight: USER1 USER2

```

### Usage with workflow_run event

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
            url: ${{ secrets.MATTERMOST_WEBHOOK_URL }}
            channel: ${{ secrets.MATTERMOST_CHANNEL }}
            highlight: USER1 USER2
```


## Action Configuration

|Input Variable|Description| |
|--------------|-----------|-|
| url | Mattermost webhook url | Required. |
| channel | Mattermost channel to post message in. | Required. |
| highlight | List of space separated users to highlight in the channel | Optional. |
| branch | Git branch to use in the message | Optional. Default is `${{ github.ref_name }}`. Will be derived from the event if empty. |
| commit | Git commit to use in the message | Optional. Default is `${{ github.sha }}`. Will be derived from the event if empty. |
| message | Enter a markdown formatted text message. Note: Setting a string in this argument ignores all other arguments. | Optional. |
| shortline | If set to "true", the message will be sent as a short line | Optional. |
| commit-message | Git commit message to use in the message | Deprecated. Connected commit message to commit will be used |
| repository | GitHub repository (org/repo) | Optional. Default is `${{ github.repository }}`. |
| status | Specifies the notification status. Options success or failure. Default is automatic detected by `GITHUB_EVENT_PATH` json. | Optional. |
| skip-installation-on | Skip mn-notify installation on selected runner. Default is self-hosted-generic. | Optional. |
| workflow | GitHub workflow ID to use in the message | Optional. Default is `${{ github.run_id }}`. |
| workflow-name | GitHub workflow name to use in the message | Optional. Default is `${{ github.workflow }}` |
| product | Product name (asset, lookout, detect, management-console, security-intelligence, enterprise-containers) | Optional. |
| stage | Deployment stage (dev, integration, testing, staging, production) | Optional. |
| version | Product or service version | Optional. |
| service | Service name for service-update notifications | Optional. |
| from-stage | Source stage for stage-transition notifications (e.g., testing) | Optional. |
| to-stage | Target stage for stage-transition notifications (e.g., staging) | Optional. |
| notification-type | Type of notification: deployment, service-update, stage-transition, release, hotfix. Optional and empty by default. | Optional. |
| changed-services | Comma-separated list of changed services | Optional. |
| MATTERMOST_WEBHOOK_URL | Mattermost webhook url | Deprecated. Use url instead. |
| MATTERMOST_CHANNEL | Mattermost channel | Deprecated. Use channel instead. |
| MATTERMOST_HIGHLIGHT | List of space separated users to highlight in the channel | Deprecated. Use highlight instead |
