# Greenbone Trigger Workflow Action

GitHub Action to trigger workflow runs.

## Example

To run this action you need to add the following code to your workflow file
(for example `.github/workflows/trigger.yml`):

```yml
name: Trigger Workflow

on:
  pull_request:

jobs:
  trigger:
    name: Trigger Workflow
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Workflow
        uses: greenbone/actions/trigger-workflow@v3
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          repository: "foo/bar"
          workflow: deploy.yml
```

The to be triggered workflow requires to react on the `workflow_dispatch` [event](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows).

## Action Configuration

| Input Variable | Description | |
| ---------------| ------------|-|
| token | Token required to create the backport pull request | Required |
| repository | Repository of the workflow to trigger | Required |
| workflow | Workflow to trigger. Either a workflow ID or file name, for example `"ci.yml"`. | Required |
| ref | The git reference for the workflow. The reference can be a branch or tag | Default: `"main"` |
| inputs | Inputs to pass to the workflow, must be a JSON string. All values must be strings (even if used as boolean or number). | Optional |
| wait-for-completion-timeout  | Maximum amount of time in seconds to wait to for workflow to finish. Set to empty string or false to not wait for the workflow. | Default: `3600` (1 hour) |
| wait-for-completion-interval | Time to wait between two polls to get run status in seconds. | Default: `60` (1 Minute) |
