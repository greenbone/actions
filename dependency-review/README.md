dependency-review-action

This action scans your pull requests for dependency changes, and will raise an error if any vulnerabilities or invalid licenses are being introduced. The action is supported by an API endpoint that diffs the dependencies between any two revisions on your default branch.

The action is available for all public repositories, as well as private repositories that have GitHub Advanced Security licensed.

You can use the dependency review action within a GitHub Action workflow.

More information availabe in [dependency-review](https://github.com/actions/dependency-review-action)

#### Example using as a Workflow

```yaml
name: 'Dependency Review'
on: [pull_request]

permissions:
  contents: read

jobs:
  dependency-review:
    runs-on: ubuntu-latest
    steps:
      - name: 'Checkout Repository'
        uses: greenbone/actions/dependency-review@v2
      - name: 'Dependency Review'
        uses: greenbone/actions/dependency-review@v2
```
