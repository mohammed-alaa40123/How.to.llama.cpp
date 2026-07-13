# Project state

_Last updated: 2026-07-13 05:52 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream reference used for the graph/MoE chapter: `6b4dc2116a92c5c8f2782bfe51fabe5ee66fb5ef`
- Policy: baseline claims stay pinned; newer refs are documented separately and labelled.

## Active milestone

**Foundations deepening — interactive system map plus file-by-file subsystem synthesis**

Reconstruct llama.cpp from the source through a clickable system map and file-by-file analysis followed by subsystem grouping and end-to-end composition.

## Completed

- MkDocs Material site, strict documentation CI, Pages deployment, website health check, source indexing, and README-first scheduled-run context.
- Pinned decode, graph-reuse, backend-scheduler, copy-ring, split-allocation, synchronization, and CPU/accelerator backend documentation.
- Canonical `llama_context`, `llama_model`, GGUF anatomy, model placement, graph construction/MoE, and memory-lifetime pages.
- Large six-tab interactive foundations explorer with canonical object, graph, GGUF/model-loading, and memory routes.
- Static interactive-link validator, fixture tests, and Documentation CI integration.
- Four-pass roadmap: file inventory, subsystem grouping, cross-file composition, and workflow reconstruction.
- File-by-file Pass A public API/minimal-example inventory.
- File-by-file Pass A model/GGUF loader inventory.
- File-by-file Pass A runtime-context and memory inventory.
- Cross-subsystem system ownership and execution synthesis connecting loader publication, persistent model storage, context-owned mutable state, polymorphic memory, graph build/reuse, scheduler execution, output visibility, and teardown.

## In progress

- File-by-file Pass A for backend scheduler internals: assignment, splits, dependency copies, copy-ring validity, events, asynchronous submission, reuse, fallback synchronization, and teardown.
- Enumerate every concrete `llama_memory_i` implementation and map model architectures to KV, recurrent, hybrid, iSWA, and specialized caches.
- Exact `llama_model` and `llama_context` member destruction ordering for retained mappings, buffers, scheduler, memory, graph results, outputs, and backends.
- Exact line-level source citations and generated source-link checking for the graph-construction chapter.
- Runtime evidence separating parsing, mapping/prefetch, faults, reads, aliases, uploads, memory updates, event waits, first-token access, KV/recurrent growth, activation peaks, and teardown.

## Immediate next task

Create one bounded backend-scheduler Pass A page connecting:

```text
ggml_build_forward_expand()
→ scheduler backend assignment
→ graph splitting
→ cross-backend dependency discovery
→ copy-ring destination allocation
→ event or synchronized copy readiness
→ asynchronous backend submission
→ graph-allocation reuse
→ synchronization and teardown
```

Required deliverables:

1. file and symbol inventory centered on `ggml/src/ggml-backend.cpp` and scheduler APIs;
2. exact ownership and validity rules for split graphs, copied tensors, events, and reusable destinations;
3. allocation-time and execution-time call chains;
4. CPU-only, CPU/GPU, multi-backend, event-capable, and fallback-copy variants;
5. Verified, Interpretation, Historical, and Open question labels;
6. README, project-state, research-log, and detailed-note updates;
7. CI and Pages verification after publication.

## Latest publication verification

- System synthesis page commit: `14c3740246152b7a2db7ce50a37fdfe730c585e1`.
- README update commit: `38abb70284f5c7abb1439f07036121aaa93c7bfc`.
- Navigation update commit: `ee5b33db2310b83d52d9955304853758455c36ea`.
- Research-log update commit: `e4e44c311afc0cb19f2cc05a56d79bbfed29154a`.
- Connector-side re-fetch confirmed the published page, pinned baseline, ownership diagram, construction/decode paths, scheduler boundary, memory-state distinctions, teardown order, truth labels, and source links.
- Commit-workflow lookup for `e4e44c311afc0cb19f2cc05a56d79bbfed29154a` returned `workflow_runs: []`; the endpoint filters to pull-request-triggered runs and cannot verify push workflows.
- Direct browser opening of the Pages root and `architecture/system-ownership-and-execution-map/` was rejected by the safe-URL gate because those URLs were absent from prior search results.
- Public site: `https://mohammed-alaa40123.github.io/How.to.llama.cpp/`.

## Known blockers and caveats

- **Local validation blocker:** no local repository checkout is available in this execution environment, so the full validation suite and `mkdocs build --strict` could not be executed locally.
- **CI visibility blocker:** the available commit-workflow endpoint returned no runs and only exposes pull-request-triggered results reliably; Documentation CI, Pages, and hourly-context workflows are unverified rather than confirmed failed.
- **Pages verification blocker:** direct opening of the root and new page was rejected by the safe-URL gate. HTTP status and rendered content remain unverified.
- Static link validation approximates Python-Markdown IDs; built-HTML validation is still required for plugin-generated anchors.
- Mapping, allocation, residency, validity, ownership, and command completion are distinct states.
- Mmap host-pointer wrapping is conditional; model pages and context-owned KV/recurrent memory are separate lifetimes.
- Shared/unified memory does not prove coherence or queue completion.
- `async` APIs indicate submission semantics, not immediate host visibility.
- `llama_context` references, but does not own, `llama_model`.
- Attached thread pools are referenced resources and must outlive their use.
- Memory implementations and architecture mappings are revision-sensitive.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, and memory ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
