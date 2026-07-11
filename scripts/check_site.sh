#!/usr/bin/env bash
set -euo pipefail
URL="${1:-https://mohammed-alaa40123.github.io/How.to.llama.cpp/}"
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT
status="$(curl --location --silent --show-error --output "$TMP" --write-out '%{http_code}' "$URL")"
if [[ "$status" != "200" ]]; then
  printf 'site check failed: %s returned HTTP %s\n' "$URL" "$status" >&2
  exit 1
fi
if ! grep -q 'How.to.llama.cpp' "$TMP"; then
  printf 'site check failed: expected project title not found at %s\n' "$URL" >&2
  exit 1
fi
printf 'site check passed: %s\n' "$URL"
