# ORAS publish

Publish a single file to an OCI registry using ORAS, optionally signing the
published manifest digest with Cosign. The action is generic: callers prepare
package metadata, choose media types, and provide annotations.

## Example

```yaml
- uses: greenbone/actions/oras-publish@main
  id: publish
  with:
    artifact-file: dist/package.tar
    artifact-url: packages.example.com/team/package:1.2.3
    prevent-overwrite: 'true'
    registry-user: ${{ secrets.REGISTRY_USER }}
    registry-token: ${{ secrets.REGISTRY_TOKEN }}

- run: echo "$REFERENCE"
  env:
    REFERENCE: ${{ steps.publish.outputs.reference }}
```

## Inputs

| Input | Description | Default |
| --- | --- | --- |
| `artifact-file` | File to upload. Required. | |
| `artifact-url` | One `registry/repository:tag`, without a scheme. Required. | |
| `artifact-folder` | Working directory; relative paths are resolved here. | `.` |
| `artifact-type` | Type of the complete OCI artifact. | ORAS default |
| `media-type` | Type of the file payload. | `application/octet-stream` |
| `annotations` | Manifest annotations, one `key=value` per line. | Empty |
| `annotation-file` | ORAS JSON annotation file, for values containing newlines or file-specific annotations. | Empty |
| `export-manifest` | Path to write the published OCI manifest; parent directory must exist. | Empty |
| `registry-user` | Registry username. Required. | |
| `registry-token` | Registry password or token. Required. | |
| `prevent-overwrite` | Reject an existing destination tag before upload. | `false` |
| `oras-version` | ORAS version to download. Update together with `oras-sha256`. | `1.3.1` |
| `oras-sha256` | Expected SHA-256 of the Linux amd64 archive. | Pinned checksum for `1.3.1` in `action.yml` |
| `sign` | Enable Cosign signing explicitly. | `false` |
| `cosign-key` | Private key; omit for keyless signing. | Empty |
| `cosign-password` | Private key password, which may be empty. | Empty |
| `cosign-tlog-upload` | Upload signature to the transparency log. | `true` |
| `cosign-version` | Cosign version installed when signing. | `v2.5.2` |

Annotations are passed as data, without shell evaluation. Blank lines are ignored;
values may contain spaces and equals signs. Use an
[ORAS annotation file](https://oras.land/docs/commands/oras_push/) for multiline
values. Avoid defining the same annotation in both inputs.

## Signing

For key-based signing, supply `sign: 'true'`, `cosign-key`, and optionally
`cosign-password`. To match the old action's transparency-log behavior, also set
`cosign-tlog-upload: 'false'`.

For keyless signing, set `sign: 'true'`, omit the key, and grant the calling job
`id-token: write`. The default uploads the signature to the transparency log.
Signing targets the returned digest, not the mutable tag. If signing fails, the
action fails, but the uploaded artifact remains in the registry.

## Outputs and behavior

- `digest`: OCI manifest digest, for example `sha256:…`.
- `reference`: immutable `registry/repository@sha256:…` reference.

Outputs are emitted after upload and any requested signing succeed. An optional
exported manifest remains a local file; this action does not upload it as a
GitHub Actions artifact.

This action supports Linux amd64 runners with Bash, curl, tar, jq, and GNU
coreutils. It downloads ORAS directly from the official GitHub release, verifies
the archive against `oras-sha256`, and adds the installed binary to `PATH`.
Installation uses the runner's temporary directory and does not require sudo.
When changing `oras-version`, also supply the matching checksum from that
release's `oras_VERSION_checksums.txt` asset.

It uses
HTTPS and a temporary authentication directory shared by ORAS and Cosign, removed
when the publishing script exits. Existing Docker login configuration is untouched.
It uploads one unchanged file and records its basename as the artifact title.

By default, existing registry tags may be replaced, subject to registry policy.
Set `prevent-overwrite: 'true'` to check the destination after login and fail if
its tag already exists, even if it points to identical content. No push, signing,
or outputs occur in that case. Only an explicit missing manifest/repository
response permits upload; authentication, network, and unrecognized lookup errors
abort publication. The lookup uses the same temporary credentials as the upload.

This is a client-side check, not an atomic create-only operation: another writer
can create the tag between the check and push. Configure registry tag immutability
for guaranteed protection against concurrent overwrites. Version selection,
release records, and promotion belong to the caller.

## Migrating from push-and-sign-artifact

The old action remains unchanged. `artifact-file`, `artifact-url`,
`artifact-folder`, `registry-user`, and `registry-token` retain their roles.
The working directory now defaults to the workspace rather than `/tmp`.
`registry-domain` is unnecessary: the login host comes from `artifact-url`.
Signing requires explicit `sign: 'true'`; supplying a key alone does not enable it.
ORAS installation uses a direct download verified with SHA-256 instead of MD5,
without runner-name detection. Cosign still uses its installer action.
This is not a drop-in replacement.

## Validation

```sh
shellcheck oras-publish/publish.sh
python3 -B -m unittest discover -s oras-publish/tests -v
```

The tests substitute ORAS and Cosign to exercise arguments, failure propagation,
signing selection, outputs, and credential cleanup without publishing anything.
