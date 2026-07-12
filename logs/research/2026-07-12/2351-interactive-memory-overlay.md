# Interactive memory-lifetime overlay

- Run time: 2026-07-12 23:51 Africa/Cairo
- Scope: connect every memory-lifecycle explorer entry to the canonical atlas and expose ownership/lifetime fields
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Updated `docs/assets/interactive/llama-foundations-explorer.html` so the Memory lifecycle tab is now a selectable, keyboard-focusable atlas rather than a static card grid.

Each of the eight entries shows:

- owner;
- backing storage;
- validity or physical-residency condition;
- synchronization boundary;
- release or reclaim condition;
- a top-level link to the matching section of `docs/foundations/memory-lifetimes.md`.

The entries cover GGUF storage, mappings, page faults/page cache, model buffers, context sequence state, scheduler copies/staging, graph activations/workspaces, and outputs/teardown.

## Verified

- Every existing memory-lifecycle concept now has a canonical atlas route.
- The overlay explicitly separates logical ownership, virtual mapping, physical residency, backend-copy validity, and command completion.
- Memory selection uses native buttons, visible focus/hover state, `aria-pressed`, and an `aria-live` detail panel.
- Canonical links use `target="_top"`, preserving normal MkDocs navigation outside the iframe.
- The explorer remains pinned to llama.cpp revision `e3546c7948e3af463d0b401e6421d5a4c2faf565`.

## Interpretation

- A compact five-field overlay is a useful minimum model for explaining memory resources across CPU-only, mapped, and accelerator paths.
- The most important correction is that ownership, addressability, physical residency, byte validity, queue completion, and release eligibility are not interchangeable states.

## Historical

- The previous Memory lifecycle tab rendered eight static summaries without selectable details or canonical links.
- This increment closes the first unfinished item in the living README TODO list after publication of the canonical memory atlas.

## Open questions

- Generate explorer records and anchors from versioned metadata rather than hand-authored JavaScript.
- Validate all local routes and anchors against built MkDocs output in CI.
- Add runtime overlays for RSS/PSS, file faults, storage reads, device allocations, copy events, and queue waits.
- Map every architecture to its concrete KV, recurrent, or hybrid `llama_memory_i` implementation.

## Sources inspected

- Complete repository `README.md`.
- `docs/reference/project-state.md`.
- `docs/reference/research-log.md`.
- `docs/reference/research-ledger.md`.
- Latest detailed note: `logs/research/2026-07-12/2250-memory-lifetime-atlas.md`.
- `docs/foundations/memory-lifetimes.md`.
- Existing interactive explorer implementation.

No new external source was introduced, so `docs/reference/research-ledger.md` remains unchanged.

## Validation

- Repository-side explorer replacement succeeded.
- Static re-fetch is used to confirm all eight records, atlas anchors, five detail fields, accessibility attributes, and pinned baseline.
- Local `mkdocs build --strict` remains subject to the existing checkout/DNS blocker.
- CI and Pages verification are attempted after durable context updates; exact access limitations are retained in README and project state.

## Next priority

Add automated validation for local routes and anchors embedded in interactive HTML/JavaScript, then begin file-by-file Pass A for public API/examples and model/GGUF loader files.