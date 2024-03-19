# Greenbone Conventional Commits Action

GitHub Action to check for conventional commits to add labels to a PR based on a given configuration.

It reads the changelog.toml as well as a given configuration.toml for labels.

The configuration.toml must contain a list of `labels` that contain a `name` and an optional `priority` field.
`name` is a string that will be the label on a pr, while priority must be a number. The priority field is used when `only_highest_priority` is set to `true`. In that case only the label with the highest `priority` will bet set. If there are labels with the same priority it is considered undefined behavior and the label may vary per run.

Additionally the configuration.toml must have a list  of `groups` containing elements with a `group` and a `label` field. The `group` field must be defined within the `changelog.toml` within `commit_types`.

To control if all found labels or just one label based on the highest priority number will be added to a PR you can set the `only_highest_priority` field to either `true` or `false`.

To exclude PR from auto labeling there is the possibility to set a `disable_on` label. When `disable_on` is configured and a PR contains the specified label the PR will be skipped.


## Examples

As an example we define a configuration for labels as `release_tag.toml`:

```toml
# disables labeling when a PR contains the following label
disable_on = "no_release"

# the name functions as a key and should be unique.
# The priority is used when only_highest_priority is set to true
labels = [
  { name = "patch_release", priority = 1 },
  { name = "minor_release", priority = 2 },
  { name = "major_release", priority = 3 },
]

# group within groups must be defined in `changelog.toml`
# label within groups must be defined in `labels`
groups = [
  { group = "Added", label = "minor_release" },
  { group = "Changed", label = "major_release" },
  { group = "Removed", label = "major_release" },
  { group = "Bug Fix", label = "patch_release" },
]

# when set to false all unique labels will be set
# otherwise only one label with the highest priority
# will be set
only_highest_priority = true
```


```yml
name: Labeler

on:
  pull_request:

permissions:
  pull-requests: write
  contents: read

jobs:
  label:
    runs-on: ubuntu-latest
    steps:
        - uses: greenbone/actions/pr-conventional-commit-labeler@main
          with:
            configuration_toml: release_tag.toml
```


## Action Configuration

|Input Variable|Description| |
|--------------|-----------|-|
| token | GitHub token to add lebels to the pull request comments. | Optional (default is [`${{ github.token }}`](https://docs.github.com/en/actions/learn-github-actions/contexts#github-context)) |
| python-version | Python version to use for running the action. | Optional (default is `3.10`) |
| poetry-version | Poetry version to use for running the action. | Optional (default is latest) |
| cache-poetry-installation | Cache poetry and its dependencies. | Optional (default is `"true"`) |
| configuration_toml| Name of the configuration file, must be in root | Required  |
| pr | Number of the Pull Request (PR) | Optional (default is ${{ github.event.pull_request.number }} |
