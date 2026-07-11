#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUN_NAME="${1:-manual-run}"
README="$ROOT/README.md"
STATE="$ROOT/docs/reference/project-state.md"
RESEARCH_LOG="$ROOT/docs/reference/research-log.md"
LEDGER="$ROOT/docs/reference/research-ledger.md"
OUT="${RUN_CONTEXT_OUT:-$ROOT/.run-context/latest.md}"

required=("$README" "$STATE" "$RESEARCH_LOG" "$LEDGER")
for path in "${required[@]}"; do
    if [[ ! -r "$path" ]]; then
        printf 'scheduled-run bootstrap: required context file is missing or unreadable: %s\n' "$path" >&2
        exit 1
    fi
done

if ! grep -q '<!-- SCHEDULED-RUN-INSTRUCTIONS:START -->' "$README"; then
    printf 'scheduled-run bootstrap: README startup protocol marker is missing\n' >&2
    exit 1
fi

mkdir -p "$(dirname "$OUT")"
LATEST_DETAIL="$(find "$ROOT/logs/research" -type f -name '*.md' 2>/dev/null | sort | tail -n 1 || true)"

{
    printf '# Scheduled run context\n\n'
    printf -- '- Run: `%s`\n' "$RUN_NAME"
    printf -- '- Started (UTC): `%s`\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
    printf -- '- Repository root: `%s`\n\n' "$ROOT"

    printf '## Canonical README\n\n'
    cat "$README"

    printf '\n\n## Current project state\n\n'
    cat "$STATE"

    printf '\n\n## Recent canonical research log\n\n'
    tail -n 240 "$RESEARCH_LOG"

    printf '\n\n## Research ledger header and recent entries\n\n'
    tail -n 200 "$LEDGER"

    if [[ -n "$LATEST_DETAIL" ]]; then
        printf '\n\n## Latest detailed research note\n\n'
        printf 'Source: `%s`\n\n' "${LATEST_DETAIL#$ROOT/}"
        tail -n 240 "$LATEST_DETAIL"
    fi
} > "$OUT"

printf 'Scheduled-run context loaded successfully.\n'
printf 'Run name: %s\n' "$RUN_NAME"
printf 'README SHA-256: %s\n' "$(sha256sum "$README" | awk '{print $1}')"
printf 'Context bundle: %s\n' "$OUT"
printf 'Next task summary:\n'
awk '/^## Immediate next task/{flag=1; next} /^## /{if(flag) exit} flag' "$STATE" | sed -n '1,40p'
