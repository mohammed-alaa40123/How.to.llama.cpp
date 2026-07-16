#!/usr/bin/env bash
set -euo pipefail

MERMAID_VERSION="${MERMAID_VERSION:-11.16.0}"
MERMAID_URL="https://cdn.jsdelivr.net/npm/mermaid@${MERMAID_VERSION}/dist/mermaid.min.js"
OUTPUT_PATH="${1:-docs/assets/javascripts/vendor/mermaid.min.js}"
TEMP_PATH="${OUTPUT_PATH}.tmp"

mkdir -p "$(dirname "$OUTPUT_PATH")"
trap 'rm -f "$TEMP_PATH"' EXIT

curl \
  --fail \
  --location \
  --retry 3 \
  --retry-all-errors \
  --silent \
  --show-error \
  "$MERMAID_URL" \
  --output "$TEMP_PATH"

test -s "$TEMP_PATH"
grep -q 'mermaid' "$TEMP_PATH"

mv "$TEMP_PATH" "$OUTPUT_PATH"
trap - EXIT

printf 'Prepared Mermaid %s at %s\n' "$MERMAID_VERSION" "$OUTPUT_PATH"
