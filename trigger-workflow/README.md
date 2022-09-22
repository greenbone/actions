# Greenbone Trigger Workflow Action

GitHub Action to trigger workflow runs.

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
        uses: greenbone/actions/trigger-workflow@v1
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          repository: "foo/bar"
          workflow: deploy.yml
```

The to be triggered workflow requires to react on the `workflow_dispatch` event.

## Action Configuration

| Input Variable | Description                                        |          |
| -------------- | -------------------------------------------------- | -------- |
| token          | Token required to create the backport pull request | Required |
