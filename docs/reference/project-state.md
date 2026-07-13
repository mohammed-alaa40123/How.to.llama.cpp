# Project state

_Last updated: 2026-07-13 06:49 Africa/Cairo_

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
- File-by-file Pass A backend-scheduler inventory covering assignment, splits, copy-ring resources, destination validity, events, fallback synchronization, asynchronous submission, reuse, and teardown.
- Cross-subsystem system ownership and execution synthesis connecting loader publication, persistent model storage, context-owned mutable state, polymorphic memory, graph build/reuse, scheduler execution, output visibility, and teardown.

## In progress

- Enumerate every concrete `llama_memory_i` implementation and map model architectures to KV, recurrent, hybrid, iSWA, and specialized caches.
- Exact `llama_model` and `llama_context` member destruction ordering for retained mappings, buffers, scheduler, memory, graph results, outputs, and backends.
- Exact line-level source citations and generated source-link checking for the graph-construction chapter.
- Runtime evidence separating parsing, mapping/prefetch, faults, reads, aliases, uploads, memory updates, event waits, first-token access, KV/recurrent growth, activation peaks, and teardown.
- Concrete backend mapping for `cpy_tensor_async`, event wait/record, graph submission, and synchronization across CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL.

## Immediate next task

Enumerate concrete context-memory implementations and architecture mappings at the pinned revision:

```text
llama_model::create_memory()
→ architecture-specific factory decision
→ llama_memory_i implementation
→ KV, recurrent, hybrid, iSWA, or specialized storage
→ per-batch memory context
→ update graph or direct mutation
→ sequence operations, state I/O, reset, and teardown
```

Required deliverables:

1. exact list of concrete `llama_memory_i` and `llama_memory_context_i` implementations;
2. architecture-to-memory mapping with pinned factory call sites;
3. storage ownership, allocation, update, synchronization, and sequence semantics;
4. ordinary KV, recurrent, hybrid, iSWA, and specialized differences;
5. Verified, Interpretation, Historical, and Open question labels;
6. README, project-state, research-log, and detailed-note updates;
7. CI and Pages verification after publication.

## Latest publication verification

- Backend scheduler Pass A page commit: `192b2ca503015d1d06ef2913caa1b69cadfaf206`.
- Navigation commit: `28429273f20901c2adafe1b40f41961d663a6c81`.
- Connector-side source inspection confirmed scheduler structures, backend assignment passes, split/copy metadata, copy slots, and event ownership at the pinned revision.
- CI and Pages verification for the final increment remain to be checked after all state commits are published.
- Public site: `https://mohammed-alaa40123.github.io/How.to.llama.cpp/`.

## Known blockers and caveats

- **Local validation blocker:** no local repository checkout is available in this execution environment, so the full validation suite and `mkdocs build --strict` could not be executed locally.
- **CI visibility blocker:** the available commit-workflow endpoint only exposes pull-request-triggered results reliably; push-triggered Documentation CI, Pages, and hourly-context workflows may remain unverified.
- **Pages verification blocker:** direct opening may be rejected by the safe-URL gate or fail if the environment cannot resolve GitHub Pages. Record the exact observed result for this increment.
- Static link validation approximates Python-Markdown IDs; built-HTML validation is still required for plugin-generated anchors.
- Mapping, allocation, residency, validity, ownership, copy generation, and command completion are distinct states.
- Scheduler destination-copy allocation does not prove current-generation data validity.
- Mmap host-pointer wrapping is conditional; model pages and context-owned KV/recurrent memory are separate lifetimes.
- Shared/unified memory does not prove coherence or queue completion.
- `async` APIs indicate submission semantics, not immediate host visibility.
- `llama_context` references, but does not own, `llama_model`.
- Attached thread pools are referenced resources and must outlive their use.
- Memory implementations and architecture mappings are revision-sensitive.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, and memory ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
