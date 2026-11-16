#!/bin/bash
# SPDX-FileCopyrightText: 2026 Greenbone AG
# SPDX-License-Identifier: GPL-3.0-or-later
set -euo pipefail

: "${ARTIFACT_FILE:?artifact-file is required}"
: "${ARTIFACT_URL:?artifact-url is required}"
: "${REGISTRY_USER:?registry-user is required}"
: "${REGISTRY_TOKEN:?registry-token is required}"
: "${MEDIA_TYPE:?media-type is required}"

# Require one tagged destination; derive the login host from it.
if [[ $ARTIFACT_URL == *://* || $ARTIFACT_URL != */* ||
      $ARTIFACT_URL == *@* || $ARTIFACT_URL == *,* ||
      $ARTIFACT_URL =~ [[:space:]] ||
      ! ${ARTIFACT_URL##*/} =~ ^[^:]+:[a-zA-Z0-9_][a-zA-Z0-9_.-]{0,127}$ ]]; then
  echo 'artifact-url must be a single registry/repository:tag' >&2
  exit 1
fi
PREVENT_OVERWRITE=${PREVENT_OVERWRITE:-false}
case "$PREVENT_OVERWRITE" in true|false) ;; *) echo 'prevent-overwrite must be true or false' >&2; exit 1 ;; esac
case "$SIGN" in true|false) ;; *) echo 'sign must be true or false' >&2; exit 1 ;; esac
case "$COSIGN_TLOG_UPLOAD" in true|false) ;; *) echo 'cosign-tlog-upload must be true or false' >&2; exit 1 ;; esac

file=$(realpath -e -- "$ARTIFACT_FILE")
[[ -f $file ]] || { echo 'artifact-file must be a regular file' >&2; exit 1; }
args=(push --image-spec v1.1 --format json)
if [[ -n $ARTIFACT_TYPE ]]; then
  args+=(--artifact-type "$ARTIFACT_TYPE")
fi
if [[ -n $ANNOTATION_FILE ]]; then
  args+=(--annotation-file "$(realpath -e -- "$ANNOTATION_FILE")")
fi
if [[ -n $EXPORT_MANIFEST ]]; then
  args+=(--export-manifest "$(realpath -m -- "$EXPORT_MANIFEST")")
fi
while IFS= read -r annotation || [[ -n $annotation ]]; do
  annotation=${annotation%$'\r'}
  [[ -n $annotation ]] || continue
  if [[ $annotation != *=* || $annotation == =* ]]; then
    echo 'Each annotation must be key=value' >&2
    exit 1
  fi
  args+=(--annotation "$annotation")
done <<< "$ANNOTATIONS"

# ORAS and Cosign share an isolated Docker-compatible authentication file.
export DOCKER_CONFIG
DOCKER_CONFIG=$(mktemp -d "$RUNNER_TEMP/oras-publish.XXXXXX")
trap 'rm -rf -- "$DOCKER_CONFIG"' EXIT
printf '%s' "$REGISTRY_TOKEN" | oras login "${ARTIFACT_URL%%/*}" \
  --username "$REGISTRY_USER" --password-stdin \
  --registry-config "$DOCKER_CONFIG/config.json"
unset REGISTRY_TOKEN

# ORAS has no atomic create-only push. This check rejects existing tags, but
# registry immutability is required to protect against concurrent writers.
if [[ $PREVENT_OVERWRITE == true ]]; then
  lookup_error="$DOCKER_CONFIG/lookup-error"
  if oras manifest fetch --descriptor --registry-config "$DOCKER_CONFIG/config.json" \
      -- "$ARTIFACT_URL" > /dev/null 2> "$lookup_error"; then
    echo 'Destination tag already exists; refusing to overwrite (prevent-overwrite=true).' >&2
    exit 1
  else
    lookup_status=$?
  fi
  # Only explicit missing-manifest/repository responses permit an upload.
  # Never treat authentication, transport, or unrecognized failures as absence.
  error=$(<"$lookup_error")
  if [[ $error != "Error: $ARTIFACT_URL: not found" ]] &&
      ! grep -Eq '(^|: )(MANIFEST_UNKNOWN|NAME_UNKNOWN):' "$lookup_error"; then
    echo 'Unable to check destination tag; publication aborted.' >&2
    exit "$lookup_status"
  fi
fi

# Upload from beside the file so absolute paths and spaces work without
# recording the runner's directory structure in the artifact title.
cd -- "$(dirname -- "$file")"
result=$(oras "${args[@]}" --registry-config "$DOCKER_CONFIG/config.json" \
  -- "$ARTIFACT_URL" "${file##*/}:$MEDIA_TYPE")
digest=$(jq -er '.digest | select(type == "string")' <<< "$result")
[[ $digest =~ ^sha256:[0-9a-f]{64}$ ]] || { echo 'Invalid manifest digest returned by ORAS' >&2; exit 1; }
reference="${ARTIFACT_URL%:*}@$digest"

if [[ $SIGN == true ]]; then
  signing_args=(--yes "--tlog-upload=$COSIGN_TLOG_UPLOAD")
  if [[ -n $COSIGN_KEY ]]; then
    signing_args+=(--key env://COSIGN_KEY)
  fi
  cosign sign "${signing_args[@]}" "$reference"
fi

printf 'digest=%s\nreference=%s\n' "$digest" "$reference" >> "$GITHUB_OUTPUT"
