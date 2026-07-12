# Project state

_Last updated: 2026-07-12 23:51 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream reference used for the graph/MoE chapter: `6b4dc2116a92c5c8f2782bfe51fabe5ee66fb5ef`
- Policy: baseline claims stay pinned; newer refs are documented separately and labelled.

## Active milestone

**Foundations deepening — interactive system map plus file-by-file subsystem synthesis**

Reconstruct llama.cpp from the source in two complementary directions:

1. a large clickable system map explaining layers, code paths, memory, GGUF, graph construction, execution, synchronization, and MoE variants;
2. file-by-file analysis followed by subsystem grouping and end-to-end composition.

## Completed

- MkDocs Material site, strict documentation CI, Pages deployment, website health check, source indexing, and README-first scheduled-run context.
- Minimal end-to-end path and initial model-loading trace.
- Pinned decode, graph-reuse, backend-scheduler, copy-ring, split-allocation, and synchronization documentation.
- CPU, CUDA, Metal, Vulkan, and SYCL execution/buffer/copy documentation plus shared compatibility matrix.
- Generic tensor-copy fallback and blocking copy decision tree.
- Accessible static scheduler SVG replacing a Mermaid renderer failure.
- Object-centred, searchable, and interactive documentation quality roadmap.
- Large interactive foundations explorer with system, code-path, memory, GGUF/graph, execution/synchronization, and file-map tabs.
- Canonical `llama_context` and `llama_model` object pages plus interactive routes.
- Canonical GGUF file-anatomy and model tensor-placement/data-transfer chapters plus explorer links.
- Canonical GGML graph-construction and MoE chapter plus graph, expansion, routing, and reuse explorer links.
- Canonical memory-lifetime atlas covering storage, mappings, page faults/page cache/RSS, model buffers, KV/recurrent/hybrid state, graph allocations, scheduler copies, staging, outputs, synchronization, teardown, and runtime measurement requirements.
- Interactive memory-lifetime overlay: all eight memory entries now expose owner, backing storage, validity/residency, synchronization, release/reclaim, and canonical atlas links.
- Expanded four-pass roadmap: file inventory, subsystem grouping, cross-file composition, and complete workflow reconstruction.

## In progress

- Automated validation for local routes and section anchors embedded in interactive assets.
- Exact line-level source citations and generated source-link checking for the graph-construction chapter.
- Runtime evidence separating parsing, mapping/prefetch, page faults, reads, aliases, uploads, event waits, first-token access, KV/recurrent growth, activation peaks, and teardown.
- File-by-file Pass A for public API/examples, model/GGUF loader, and runtime context.
- Architecture-specific graph-builder, prefill/decode, KV/recurrent, and MoE extensions to the explorer.
- Exact Metal shared/private buffer-level branches.

## Immediate next task

Add CI validation for canonical routes and section anchors embedded in interactive HTML and JavaScript assets:

```text
extract href values and generated page routes
  -> distinguish external links from local MkDocs routes
  -> verify referenced source files and documentation paths
  -> validate section anchors against Markdown headings or built HTML
  -> report the exact asset and broken route
  -> run in docs-ci before mkdocs build --strict
```

Required deliverables:

1. a bounded validation script or extension to the existing context validator;
2. coverage for the foundations explorer's object, GGUF, graph, MoE, and memory links;
3. clear errors naming the asset, route, and anchor;
4. workflow integration without weakening strict MkDocs validation;
5. tests or fixture checks for valid and invalid links;
6. Verified, Interpretation, Historical, and Open question sections in the detailed note.

## Latest publication verification

- Interactive memory overlay commit: `f848385b8e85e77fb3af2183140f6a92fab5c1ea`.
- Detailed note commit: `5545b20801303e68c9cfa977ffb637c90f9fff67`.
- README state commit: `63929c4f6be9c98c2eaf1d748eeb538029937a84`.
- Public site: `https://mohammed-alaa40123.github.io/How.to.llama.cpp/`.
- The available connector exposes commit status and a limited workflow endpoint, but may not expose push-triggered Actions runs; verification must be attempted and exact limitations retained below.

## Known blockers and caveats

- **CI blocker:** connector access does not currently provide a reliable repository-wide listing of push-triggered workflow runs, so Documentation CI, Pages deployment, and hourly context status may remain unverified.
- **Pages blocker:** live verification depends on browser/DNS access; failure to fetch is a verification blocker, not evidence of deployment failure.
- **Local validation blocker:** the execution container cannot resolve `github.com`, so no checkout is available for `mkdocs build --strict` or repository scripts.
- Interactive routes and anchors are still hand-authored and are not automatically checked against built MkDocs output.
- The official GGUF specification can evolve beyond the pinned implementation.
- Mmap host-pointer wrapping is conditional; “zero-copy model loading” is not a model-wide property.
- Mapping, allocation, residency, validity, ownership, and command completion are distinct states.
- Prefetch requests do not prove permanent physical residency.
- RSS is not a per-tensor residency oracle.
- Shared or unified memory does not itself prove host visibility, coherence, or command completion.
- Regex indexing cannot resolve macros, virtual dispatch, function pointers, generated code, or backend registration reliably.
- A conceptual layer stack is not a universal execution order for every architecture/backend combination.
- APIs named `async` do not prove host-visible overlap.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible hover/click behavior.
- Source-pinned end-to-end code workflow.
- Deep GGUF and model-loading chapters.
- Canonical `llama_context` and `llama_model` ownership/lifetime pages.
- GGML tensor/op/graph-construction and execution chapter.
- Memory ownership and synchronization atlas plus interactive overlay.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.