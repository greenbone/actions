#!/usr/bin/env bash
set -euo pipefail
if [[ "$(uname -s)/$(uname -m)" != Linux/x86_64 ]]; then
  echo '::error::workflow-lint supports only Linux x86_64 runners' >&2
  exit 1
fi
version=1.7.12
archive="actionlint_${version}_linux_amd64.tar.gz"
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
curl --fail --silent --show-error --location --proto '=https' --proto-redir '=https' \
  "https://github.com/rhysd/actionlint/releases/download/v${version}/${archive}" -o "$tmp/$archive"
(cd "$tmp" && sha256sum -c "$ACTION_PATH/checksums.txt")
tar -xzf "$tmp/$archive" -C "$tmp" actionlint
for tool in "$SHELLCHECK" "$PYFLAKES"; do
  if [[ -n "$tool" ]] && ! command -v "$tool" >/dev/null; then
    echo "::warning::Optional executable '$tool' unavailable; its checks will not run"
  fi
done
cd "$GITHUB_WORKSPACE"
"$tmp/actionlint" -shellcheck "$SHELLCHECK" -pyflakes "$PYFLAKES"
