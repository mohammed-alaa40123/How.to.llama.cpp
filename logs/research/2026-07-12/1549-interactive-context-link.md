# Interactive Context node to canonical object page

- Run time: 2026-07-12 15:49 Africa/Cairo
- Scope: connect the interactive foundations explorer to the canonical `llama_context` documentation page
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Verified

- The explorer now carries one explicit pinned metadata object for the upstream baseline, source root, and documentation root.
- The **llama_context runtime** system-layer node exposes a canonical documentation link to `objects/llama-context/`.
- The **Construct context** end-to-end workflow step exposes the same canonical documentation link.
- Canonical documentation links use `target="_top"`, so they navigate the full MkDocs page instead of trapping the destination inside the explorer iframe.
- Pinned source links continue to resolve from the shared baseline source root.
- The explorer retains six views: system layers, end-to-end workflow, memory lifecycle, GGUF/graph, synchronization, and file groups.

## Interpretation

- Object-page links are most useful at both the conceptual system-layer entry point and the concrete workflow step where construction occurs.
- A small metadata object is an incremental improvement over duplicated URL literals, but generated versioned JSON remains the maintainable long-term design.

## Historical

- The previous explorer showed only pinned upstream source areas. This increment introduces the first interactive bridge from a system object to a canonical local documentation page.

## Open questions

- Whether local object/page metadata should move to a generated JSON bundle shared by MkDocs pages, source maps, and all interactive assets.
- Which object should be linked next: `llama_model`, scheduler, `ggml_cgraph`, or memory modules.
- Whether CI should parse interactive JavaScript and verify every local canonical-page path.

## Artifact

Updated `docs/assets/interactive/llama-foundations-explorer.html`:

- added shared baseline/source/docs metadata;
- linked the Context layer to `docs/objects/llama-context.md` through the deployed page route;
- linked workflow step 4 to the same page;
- retained source-pinned details and evidence labeling;
- simplified duplicated rendering logic into reusable source and page-link helpers.

## Sources

No new external source was introduced. Existing pinned llama.cpp source and the canonical local object page were reused, so the research ledger did not change.

## Validation

- Connector write succeeded at commit `b32b8efcbc2ac5c5d976b20d0977be3ba1447e14`.
- Static review confirms balanced HTML/script structure, all referenced element IDs, six tab targets, and both canonical Context links.
- Full local MkDocs validation was unavailable because the execution container could not resolve GitHub for a checkout.

## Next priority

Deepen the GGUF foundations/model-loader chapter with the official specification, pinned loader call chain, split-file and alignment behavior, memory ownership, mmap/page-fault implications, and verified figure attribution.
