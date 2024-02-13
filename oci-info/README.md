# OCI Info

GitHub Action to interacting with OCI (Open Container Initiative) registries.

## Example

```yml

name: oci-info
on:
  workflow_dispatch:
jobs:
  oci-info:
    name: list-tags
    runs-on: ubuntu-latest
    steps:
      - name: get tags
        id: tags
        uses: greenbone/actions/oci-info@v3
        with:
          repository: opensight-postgres
          namespace: greenbone
      - name: Print tags
        run: echo "${{ steps.tags.outputs.output }}"
```
## Action Configuration

| Input Variable            | Description                                                                                                    |          |
| ------------------------- | -------------------------------------------------------------------------------------------------------------- | -------- |
| command                   | Available commands are list-tags, compare-tag-annotation. Default is list-tags .                               | Optional |
| repository                | Repository name.                                                                                               | Required |
| namespace                 | Namespace for the registry.                                                                                    | Required |
| user                      | User for the registry login.                                                                                   | Optional |
| password                  | Password/token for the registry login.                                                                         | Optional |
| reg-domain                | Registry domain. Default is ghcr.io .                                                                          | Optional |
| reg-auth-domain           | Registry authentication domain. Default is ghcr.io .                                                           | Optional |
| reg-auth-service          | Registry authentication service. Default is ghcr.io .                                                          | Optional |
| tag                       | Tag to compare. Required if command is compare-tag-annotation.                                                 | Optional |
| architecture              | Annotation from architecture to compare. Default is amd64 .                                                    | Optional |
| compare-repository        | Compare repository name. Required if command is compare-tag-annotation.                                        | Optional |
| annotation                | Annotation to compare. Default is org.opencontainers.image.created .                                           | Optional |
| mode                      | Compare mode. Available commands are eq, lt and gt. Default is eq .                                            | Optional |
| compare-namespace         | Compare registry Namespace. Default is library .                                                               | Optional |
| compare-reg-domain        | Compare registry domain. Default is registry-1.docker.io .                                                     | Optional |
| compare-reg-auth-domain   | Compare registry authentication domain. Default is auth.docker.io .                                            | Optional |
| compare-reg-auth-service  | Compare registry authentication service. Default is registry.docker.io .                                       | Optional |
| compare-user              | User for the compare registry login.                                                                           | Optional |
| compare-password          | Password for the compare registry login.                                                                       | Optional |
| python-version            | Python version to use for running the action. Default is 3.11 .                                                | Optional |
| poetry-version            | Use a specific poetry version. By default the latest release is used.                                          | Optional |
| cache-poetry-installation | Cache poetry and its dependencies. Default is 'true'. Set to an other string then 'true' to disable the cache. | Optional |

## Action Output

| Output Variable | Description                 |
| --------------- | --------------------------- |
| output          | The oci-info stdout output. |
