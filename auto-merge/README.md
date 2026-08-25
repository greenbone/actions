# Auto-merge Action

Action to enable auto-merge for a pull request.

## Example

```yml
name: Enable auto-merge

on:
  pull_request_target:
    types:
      - opened
      - reopened
      - synchronize
      - ready_for_review

jobs:
  auto-merge:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - name: Enable auto-merge
        uses: greenbone/actions/auto-merge@v3
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          mode: squash
```

## Action Configuration

| Input        | Description                                       | Default                                     |
| ------------ | ------------------------------------------------- | ------------------------------------------- |
| github-token | GitHub token used to enable auto-merge.           | `${{ github.token }}`                       |
| pr-url       | URL of the pull request to enable auto-merge for. | `${{ github.event.pull_request.html_url }}` |
| mode         | Merge mode: `merge`, `squash`, or `rebase`.       | `rebase`                                    |

`${{ github.event.pull_request.html_url }}` is the pull request URL from the triggering the job run.
