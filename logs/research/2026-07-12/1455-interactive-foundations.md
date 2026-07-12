# Interactive foundations explorer and file-by-file plan

- Run time: 2026-07-12 14:55 Africa/Cairo
- Baseline: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: deepen foundations, add a large clickable system map, and reorganize the implementation plan around file-by-file analysis followed by subsystem synthesis

## Verified

- Added `docs/assets/interactive/llama-foundations-explorer.html` with six interactive tabs:
  - system layers;
  - end-to-end code path;
  - memory lifecycle;
  - GGUF and graph construction;
  - execution and synchronization;
  - file-by-file source groups.
- System-layer buttons provide hover/focus summaries and click-to-open detail panels.
- Detail panels expose representative symbols, pinned source areas, memory ownership, and synchronization notes.
- The end-to-end tab covers backend initialization, GGUF open, tensor storage, context construction, batch preparation, decode, graph build/reuse, graph allocation, split execution, synchronization, sampling, and teardown.
- The memory tab separates GGUF storage, virtual mappings, page faults/page cache, model tensor metadata, context state, backend copies/staging, temporary graph allocations, and teardown.
- The GGUF/graph tab explains metadata/tensor descriptors, tensor registration, lazy operation tensors, graph expansion, activations versus weights, and the non-universality of per-layer load/free behavior.
- The synchronization tab separates graph-input overwrite safety, copy-slot reuse, async-copy acceptance/fallback, split submission, event record, and host-visible completion.
- Added `docs/foundations/interactive-system-map.md` and linked it from Foundations, Interactive navigation, and the homepage.
- Expanded `docs/roadmap.md` with four explicit passes: per-file inventory, subsystem grouping, cross-file synthesis, and complete workflow reconstruction.

## Interpretation

- A layered map, code workflow, memory lifecycle, graph view, synchronization timeline, and file map must coexist because each answers a different class of systems question.
- File-by-file analysis should not end with function summaries. It must identify object lifetime, memory ownership, synchronization, and the cross-file interfaces that produce runtime behavior.
- The explorer is a curated teaching artifact today; versioned generated metadata should eventually become the shared source of truth for diagrams, object pages, and symbol pages.

## Historical

- The previous `inference-flow.html` remains a focused minimal decoder loop.
- The new explorer broadens foundations without replacing source-pinned lifecycle pages or backend-specific analysis.

## Open questions

- Exact authoritative source path, revision, license, and attribution for the requested canonical/famous GGUF image.
- Exact architecture-specific builder files and graph-input classes to expose as the next sublayers.
- Whether the explorer should evolve as static HTML plus JSON or as a larger client-side application.
- Which runtime metrics should be overlaid first: page faults, RSS, transfer bytes, queue waits, or split timing.

## Source ledger

- No new secondary source was introduced.
- Existing pinned llama.cpp source links and the already-ledgered official GGUF specification were reused.

## Validation

- Connector-side file creation and navigation updates succeeded.
- The browser fetcher returned a cache-miss error for the public Pages root, so deployment and rendering of the new path remain unverified through that tool.
- The interactive asset is self-contained HTML/CSS/JavaScript and uses keyboard-focusable buttons and iframe title text.
- Full `mkdocs build --strict` was not run locally in this environment.

## Next priority

Deepen the GGUF and model-loader foundations chapter, verify the canonical upstream figure and attribution, then connect the interactive GGUF tab to that detailed page. Follow with the canonical `llama_context` object page and the GGML graph-construction chapter.
