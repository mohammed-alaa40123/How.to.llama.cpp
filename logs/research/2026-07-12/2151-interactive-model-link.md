# Interactive `llama_model` explorer link

- Run time: 2026-07-12 21:51 Africa/Cairo
- Scope: connect the existing Model object system-layer card to the canonical `llama_model` page
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Updated `docs/assets/interactive/llama-foundations-explorer.html` so the **Model object** layer includes:

```text
page: objects/llama-model/
```

The existing page-link renderer opens canonical documentation with `target="_top"`, so selecting the Model object layer and following the link exits the iframe and opens the normal MkDocs page.

## Verified

- The explorer metadata now assigns `objects/llama-model/` to the Model object layer.
- The shared renderer already emits top-level canonical-page navigation.
- The pinned source baseline and the other layer, workflow, GGUF, graph, MoE, memory, and synchronization entries were preserved.
- The completed integration removes the blocker recorded by the previous `llama_model` object-page run.

## Interpretation

- Direct object-page navigation makes the explorer useful as a progressive-disclosure interface: the layer card gives the concise role, while the canonical page provides creation, ownership, architecture dispatch, graph-factory behavior, sharing, and teardown details.
- Keeping the link on the Model object layer reinforces the distinction between persistent loaded-model state and context-owned mutable inference state.

## Historical

- This completes the object-level explorer pair: both `llama_model` and `llama_context` now have canonical routes.
- Routes remain hand-authored in the interactive asset; generated metadata and automatic route validation are future work.

## Open questions

- Add CI validation that every interactive canonical route resolves in the built MkDocs site.
- Replace curated JavaScript records with generated, versioned metadata shared by object pages and visualizers.
- Build the memory-lifetime chapter and attach the memory cards to canonical sections.

## Sources inspected

- Complete repository `README.md`.
- `docs/reference/project-state.md`.
- `docs/reference/research-log.md`.
- `docs/reference/research-ledger.md`.
- Latest prior detailed note: `logs/research/2026-07-12/2108-llama-model-object-page.md`.
- Current `docs/assets/interactive/llama-foundations-explorer.html`.
- Existing `docs/objects/llama-model.md` and explorer route-rendering behavior.

No external source changed, so `docs/reference/research-ledger.md` was intentionally unchanged.

## Validation

- Connector-side full-file replacement succeeded.
- Static re-fetch is required to confirm the route and preservation of the explorer structure.
- A local clone and `mkdocs build --strict` were blocked because the execution container could not resolve `github.com`.
- CI and Pages checks are attempted after the durable updates; exact connector or network limitations are recorded in project state and the README TODO list.

## Next priority

Build the canonical memory-lifetime chapter and interactive overlay spanning GGUF storage, mappings, page faults, model buffers, context memory, graph allocations, scheduler copies, outputs, synchronization, teardown, and OS reclaim.