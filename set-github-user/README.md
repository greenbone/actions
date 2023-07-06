# Setup GitHub User in a Repository

GitHub Action to setup the user for a repository. Can be used to push content
to GitHub.

## Example

```yml
name: Setup GitHub User

on:
  pull_request:

jobs:
  setup-pontos:
    name: Setup
    runs-on: ubuntu-latest
    steps:
        - uses: greenbone/actions/setup-github-user@v2
          with:
            user: ${{ vars.user }}
            mail: ${{ vars.mail }}
            token: ${{ secrets.TOKEN }}

```

## Action Configuration

|Input Variable|Description| |
|--------------|-----------|-|
| user | GitHub user name on behalf of whom the actions will be executed. | Optional (default: `github-actions`) |
| mail | Mail address for the given GitHub user. | Optional (default: `github-actions@github.com`) |
| token | The GitHub user's token (PAT) | Optional (default: `${{ github.token }}`) |
| repository | GitHub repository to use | Optional (default: `${{ github.repository }}`) |
