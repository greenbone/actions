# Release Type

GitHub Action to determine the release type and release reference

## Example

```yml
name: Determine Release Type

on:
  pull_request:
    type: [closed]
  workflow_dispatch:
      release-type:
        type: choice
        description: What kind of release do you want to do (pontos --release-type argument)?
        options:
          - patch
          - minor
          - major
          - release-candidate
          - alpha
          - beta

jobs:
  check:
    name: Determine Release Type and Ref
    runs-on: ubuntu-latest
    steps:
        - uses: greenbone/actions/release-type@v3
          id: release
          with:
            release-type-input: ${{ inputs.release-type }}
        - name: Print release type and ref
          run: |
            echo ${{ steps.release.outputs.release-type }}
            echo ${{ steps.release.outputs.release-ref }}
```

## Action Configuration

|Input Variable|Description| |
|--------------|-----------|-|
| release-type-input | Release type for workflow dispatch based manual release. If not set the release type will be derived from the pull request labels. | Optional |

## Output Arguments

|Output Variable|Description|
|---------------|-----------|
| release-type | Determined release type based on input and set pull requests labels |
| release-ref  | Determined release reference |
