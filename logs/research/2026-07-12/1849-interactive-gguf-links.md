# Interactive GGUF and model-loading links

- Run time: 2026-07-12 18:49 Africa/Cairo
- Scope: connect the interactive GGUF/graph view to the canonical GGUF anatomy and tensor-placement chapters
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Updated `docs/assets/interactive/llama-foundations-explorer.html` so the GGUF/graph tab exposes direct canonical-documentation links for:

- `docs/foundations/gguf-file-anatomy.md`;
- `docs/foundations/model-tensor-placement.md`.

The links use the explorer's existing documentation-root convention and `target="_top"`, so navigation escapes the iframe and opens the normal MkDocs page.

## Verified

- The GGUF container card links to `../../foundations/gguf-file-anatomy/`.
- The tensor registration and placement card links to `../../foundations/model-tensor-placement/`.
- Both links open in the top-level browsing context.
- The six existing explorer views, pinned source baseline, source links, Context links, and JavaScript initialization remain present.

## Interpretation

- The explorer now provides a progressive path from a compact conceptual card to the two source-pinned loading chapters: physical file anatomy first, then runtime placement and transfer.
- Keeping these as separate destinations avoids conflating GGUF's on-disk representation with backend storage and execution residency.

## Historical

- This is the second canonical-documentation integration in the explorer, after the `llama_context` links.

## Open questions

- Move the two hard-coded GGUF page paths into shared versioned metadata together with object-page links.
- Add CI checks that parse interactive HTML and verify canonical local routes against MkDocs navigation.
- Link the graph-construction cards after the canonical GGML graph chapter is published.

## Sources inspected

- Current repository README, project state, research log, research ledger, and latest detailed note.
- Current interactive explorer and the two canonical model-loading chapters.
- No new external source was introduced; the research ledger is unchanged.

## Validation

- Re-fetched the changed explorer from `main` and confirmed both routes and the pinned baseline.
- Local checkout and strict MkDocs validation remain blocked because the execution container cannot resolve `github.com`.
- CI and Pages checks are performed after durable context updates; exact results are recorded in project state.

## Next priority

Create the canonical GGML graph-construction chapter, then link its graph-construction and graph-expansion cards from the same explorer tab.