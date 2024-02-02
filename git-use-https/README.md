# Use HTTPS for Git data transfer

GitHub Action to use Git over HTTPS with OAuth instead of SSH to transfer data to GitHub. This fixes cloning private GitHub repositories, when unable to use `actions/checkout`.

#### Use Case

```yaml
jobs:
  build:
    name: Build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: "Use HTTPS for GitHub data transfer"
        uses: greenbone/actions/git-use-https@v3
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
      - name: Setup Poetry with private GitHub repository as dependency
        uses: greenbone/actions/poetry@v3
```

## Action Configuration

| Input Variable          | Description                                                                     |          |
| ----------------------- | ------------------------------------------------------------------------------- | -------- |
| token                   | OAuth 2.0 token to use for authentication                                       | Required |
