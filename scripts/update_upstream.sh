#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MIRROR="$ROOT/.upstream/llama.cpp.git"
WORKTREE="$ROOT/.upstream/worktree"
REV="${LLAMA_CPP_REV:-e3546c7948e3af463d0b401e6421d5a4c2faf565}"
mkdir -p "$ROOT/.upstream" "$ROOT/data/generated"
if [[ ! -d "$MIRROR" ]]; then
  git clone --mirror https://github.com/ggml-org/llama.cpp.git "$MIRROR"
else
  git -C "$MIRROR" remote update --prune
fi
rm -rf "$WORKTREE"
git clone --no-checkout "$MIRROR" "$WORKTREE"
git -C "$WORKTREE" checkout --detach "$REV"
git -C "$MIRROR" for-each-ref --format='%(refname),%(objectname),%(creatordate:iso8601)' refs/heads refs/tags > "$ROOT/data/generated/upstream-refs.csv"
python3 "$ROOT/scripts/index_upstream.py" "$WORKTREE" --out "$ROOT/data/generated/source-index.json" --markdown "$ROOT/docs/reference/generated-source-inventory.md"
printf 'Pinned llama.cpp at %s\n' "$REV"
