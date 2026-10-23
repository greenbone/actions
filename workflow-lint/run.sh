#!/usr/bin/env bash
set -euo pipefail
if [[ "$(uname -s)/$(uname -m)" != Linux/x86_64 ]]; then
  echo '::error::workflow-lint supports only Linux x86_64 runners' >&2
  exit 1
fi
version=1.7.12
archive="actionlint_${version}_linux_amd64.tar.gz"
tmp=$(mktemp -d)
cleanup() {
  echo '::remove-matcher owner=actionlint::'
  rm -rf "$tmp"
}
trap cleanup EXIT
curl --fail --silent --show-error --location --proto '=https' --proto-redir '=https' \
  "https://github.com/rhysd/actionlint/releases/download/v${version}/${archive}" -o "$tmp/$archive"
(cd "$tmp" && sha256sum -c "$ACTION_PATH/checksums.txt")
tar -xzf "$tmp/$archive" -C "$tmp" actionlint
for tool in "$SHELLCHECK" "$PYFLAKES"; do
  if [[ -n "$tool" ]] && ! command -v "$tool" >/dev/null; then
    safe_tool=${tool//'%'/'%25'}
    safe_tool=${safe_tool//$'\r'/'%0D'}
    safe_tool=${safe_tool//$'\n'/'%0A'}
    echo "::warning::Optional executable '$safe_tool' unavailable; its checks will not run"
  fi
done
cd "$GITHUB_WORKSPACE"
echo "::add-matcher::$ACTION_PATH/actionlint-matcher.json"
status=0
"$tmp/actionlint" -no-color -shellcheck "$SHELLCHECK" -pyflakes "$PYFLAKES" > "$tmp/diagnostics" 2>&1 || status=$?
# Disable command parsing for untrusted diagnostics; matchers still see lines.
stop_token=$(cat /proc/sys/kernel/random/uuid)
echo "::stop-commands::$stop_token"
cat "$tmp/diagnostics"
echo "::$stop_token::"
python3 "$ACTION_PATH/report.py" "$tmp/diagnostics" "$status" || echo '::warning::Workflow lint reporting failed'
exit "$status"
