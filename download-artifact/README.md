# Greenbone Download Artifact Action

GitHub Action to download artifacts of a workflow run.

For finding a corresponding workflow run currently only workflow runs with
an event of `schedule` and `workflow_dispatch` are considered. The action
loads workflow runs with these events and downloads the artifact(s) from the
newest run.

To use this action you need to add the following code to your workflow file
(for example `.github/workflows/artifacts.yml`):

```yml
name: Download Artifacts

on:
  pull_request:

jobs:
  download-artifacts:
    name: Download Artifacts
    runs-on: ubuntu-latest
    steps:
      - name: Download All Artifacts
        uses: greenbone/actions/download-artifact@v1
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          repository: "foo/bar"
          workflow: deploy.yml
      - name: Download Single Artifact
        uses: greenbone/actions/download-artifact@v1
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          repository: "foo/bar"
          workflow: deploy.yml
          name: artifact-a
      - name: Ignore non-existing Artifact
        uses: greenbone/actions/download-artifact@v1
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          repository: "foo/bar"
          workflow: deploy.yml
          name: artifact-b
          allow-not-found: true
```

## Action Configuration

| Input Variable  | Description                                                                                |                                  |
| --------------- | ------------------------------------------------------------------------------------------ | -------------------------------- |
| token           | Token required to create the backport pull request                                         | Required                         |
| repository      | Repository of the workflow to trigger                                                      | Required                         |
| workflow        | Workflow to trigger. Either a workflow ID or file name, for example `ci.yml`.              | Required                         |
| branch          | The git branch for the workflow.                                                           | Default: `main`                  |
| name            | Name of the artifact to be downloaded. If not set all artifacts will be downloaded.        | Optional                         |
| allow-not-found | Set to `true` to not fail if workflow or artifact can not be found.                        | Optional                         |
| path            | Destination path for the to be downloaded artifact of parent directory if name is not set. | Default: `.` (Current directory) |

The name input parameter mimics the [actions/download-artifact@v3](https://github.com/actions/download-artifact/tree/v3#download-all-artifacts)
behavior:

If the `name` input parameter is not provided, all artifacts will be downloaded.
To differentiate between downloaded artifacts, a directory denoted by the
artifacts name will be created for each individual artifact. Example, if there
are two artifacts `artifact-a` and `artifact-b`, and the `path` input parameter
is `tmp/artifacts/`, the directory structure will look like this:

```
  tmp/artifacts/
      artifact-a/
          ... contents of artifact-a
      artifact-b/
          ... contents of artifact-b
```

If the `name` input parameter is provided, its content will be directly put into
`path`. If the artifact `artifact-a` will be downloaded and the `path` input
parameter is `tmp`, the directory structure will look like this:

```
  tmp/
    ... contents of artifact-a
```
