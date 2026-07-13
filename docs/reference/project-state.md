# Project state

_Last updated: 2026-07-13 07:50 Africa/Cairo_

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
- Pass A pages for public API/minimal example, model/GGUF loading, runtime context/memory, and backend scheduler.
- Cross-subsystem system ownership and execution synthesis.
- Exact pinned map of seven concrete `llama_memory_i` implementations, their primary context implementations, architecture predicates, special factory branches, storage composition, update semantics, and sequence/state behavior.

## In progress

- Exact `llama_model` and `llama_context` member destruction ordering for retained mappings, buffers, scheduler, memory, graph results, outputs, and backends.
- Architecture-specific graph-builder downcasts to concrete memory-context types and exact state tensors read/written.
- Exact line-level source citations and generated source-link checking for the graph-construction chapter.
- Runtime evidence separating parsing, mapping/prefetch, faults, reads, aliases, uploads, memory updates, event waits, first-token access, KV/recurrent growth, activation peaks, and teardown.
- Concrete backend mapping for `cpy_tensor_async`, event wait/record, graph submission, and synchronization across CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL.

## Immediate next task

Trace exact declaration and destruction dependencies for `llama_model` and `llama_context`:

```text
member declaration order
→ C++ reverse destruction order
→ custom destructors and smart-pointer cleanup
→ queued backend work and synchronization prerequisites
→ scheduler/memory/output/backend lifetime dependencies
→ retained mappings and model buffers
→ safe application teardown order
```

Required deliverables:

1. declaration-order tables for model and context;
2. reverse destruction order and explicit synchronization boundaries;
3. borrowed versus owned members and external lifetime requirements;
4. failure and partial-construction cleanup;
5. CPU and accelerator teardown differences;
6. Verified, Interpretation, Historical, and Open question labels;
7. README, project-state, research-log, and detailed-note updates;
8. CI and Pages verification after publication.

## Latest publication verification

- Context-memory implementation page commit: `a47a8c344bc6850a507a69617d3d6fe52923a37e`.
- Navigation commit: `c6990a136c2b5aeda6c290397a4c0a74d3c2e528`.
- README/TODO commit: `288c5642852ec6ab04bc74f6160d8ad8f44ca3ea`.
- Connector-side source inspection confirmed seven concrete persistent implementations: ordinary KV, iSWA, DSA, DSV4, recurrent, hybrid, and hybrid-iSWA.
- Pinned `llama-arch.cpp` confirms exact recurrent and hybrid architecture sets; pinned `llama-model.cpp` confirms no-memory and specialized factory branches.
- GitHub Actions and Pages checks are performed after the final detailed-note commit; results or exact blockers are recorded below.
- Public site: `https://mohammed-alaa40123.github.io/How.to.llama.cpp/`.

## Known blockers and caveats

- **Local validation blocker:** no usable local checkout is available in this execution environment, so the full validation suite and `mkdocs build --strict` could not execute locally.
- **CI visibility blocker:** the connector workflow endpoint only reliably exposes pull-request-triggered results; an empty result is not evidence that push-triggered workflows passed or failed.
- **Pages verification blocker:** direct live-site verification may be limited by URL safety or DNS behavior; exact result is recorded after publication.
- Static link validation approximates Python-Markdown IDs; built-HTML validation is still required for plugin-generated anchors.
- Mapping, allocation, residency, validity, ownership, copy generation, and command completion are distinct states.
- Scheduler destination-copy allocation does not prove current-generation data validity.
- `llama_context` references, but does not own, `llama_model`.
- Attached thread pools are referenced resources and must outlive their use.
- Memory implementations and architecture mappings are revision-sensitive.
- `llama_kv_cache_dsv4` documents incomplete unified-mode support at the pinned revision.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, and memory ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
