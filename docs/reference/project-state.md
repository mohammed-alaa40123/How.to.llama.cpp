# Project state

_Last updated: 2026-07-12 22:50 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream reference used for the graph/MoE chapter: `6b4dc2116a92c5c8f2782bfe51fabe5ee66fb5ef`
- Policy: baseline claims stay pinned; newer refs are documented separately and labelled.

## Active milestone

**Foundations deepening — interactive system map plus file-by-file subsystem synthesis**

Return to the foundations and reconstruct llama.cpp from the source in two complementary directions:

1. a large clickable system map that explains layers, code paths, memory, GGUF, graph construction, execution, synchronization, and MoE variants;
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
- Canonical `llama_context` object page and interactive links.
- Canonical `llama_model` object page and interactive Model object route.
- Canonical GGUF file-anatomy and model tensor-placement/data-transfer chapters plus explorer links.
- Canonical GGML graph-construction and MoE chapter plus graph, expansion, routing, and reuse explorer links.
- Canonical memory-lifetime atlas covering GGUF storage, virtual mappings, page faults/page cache/RSS, persistent model buffers, KV/recurrent/hybrid context state, graph metadata and activations, scheduler copies, staging, outputs, prefill/decode differences, synchronization, teardown, and runtime measurement requirements.
- Expanded implementation roadmap with four passes: file inventory, subsystem grouping, cross-file composition, and complete workflow reconstruction.

## In progress

- Interactive memory overlay and canonical links from every memory-lifecycle card.
- Adding exact line-level source citations and generated source-link checking to the graph-construction chapter.
- Runtime evidence separating parsing, mapping/prefetch, page faults, direct reads, alias bytes, upload bytes, event waits, first-token access, KV/recurrent growth, activation peaks, and teardown.
- File-by-file Pass A for public API/examples, model/GGUF loader, and runtime context.
- Architecture-specific graph-builder, prefill/decode, KV/recurrent, and MoE extensions to the explorer.
- Exact Metal shared/private buffer-level branches.

## Immediate next task

Connect the memory-lifecycle explorer cards to the canonical memory atlas and add a compact interactive ownership/lifetime overlay:

```text
GGUF storage
  -> mapping and page residency
  -> model buffer ownership
  -> context KV/recurrent ownership
  -> graph activation lifetime
  -> scheduler copy-ring and staging lifetime
  -> output visibility
  -> synchronization and teardown
```

Required deliverables:

1. canonical links from each existing memory card to the matching atlas section;
2. owner, backing storage, validity/residency, synchronization, and release fields in the detail panel;
3. explicit distinction between logical cache state, virtual mapping, OS residency, backend-copy validity, and command completion;
4. preserved keyboard/hover accessibility and top-level navigation;
5. Verified, Interpretation, Historical, and Open question sections in the detailed note.

## Latest publication verification

- Memory atlas creation commit: `5eafa682baf90e014ce6585faac9b816b5367f84`.
- Navigation update commit: `4142b3c515a68c047c4b2454825b99822e25db92`.
- README state update commit: `80d3618b7890682660e65d31635bd08e7fd8015c`.
- Public site: `https://mohammed-alaa40123.github.io/How.to.llama.cpp/`.
- The available connector exposes repository files but may not expose push-triggered workflow runs or Pages deployment checks; verification must be attempted and exact limitations retained below.

## Known blockers and caveats

- **CI blocker:** available connector access does not currently expose a reliable push-triggered workflow-run/check-run listing, so Documentation CI, Pages deployment, and hourly context status may remain unverified.
- **Pages blocker:** live site verification depends on browser/DNS access; failure to fetch must be recorded as a verification blocker rather than treated as deployment failure.
- **Local validation blocker:** no local authenticated checkout is available in the execution container, and earlier runs failed DNS resolution for `github.com`; therefore `mkdocs build --strict` may remain unavailable.
- Interactive local section anchors and routes are hand-authored and are not yet validated automatically against built MkDocs output.
- The official GGUF specification can evolve beyond the pinned llama.cpp implementation.
- Mmap host-pointer wrapping is conditional; “zero-copy model loading” is not a model-wide property under partial offload or incompatible buffer types.
- Mapping, allocation, residency, validity, and command completion are distinct states.
- Prefetch requests do not prove permanent physical residency.
- CPU_Mapped addressability does not imply physical residency or fault-free access.
- RSS is not a per-tensor residency oracle.
- Accelerator unified/shared/system memory does not by itself imply GGML host visibility, command completion, or safe reuse.
- Regex indexing cannot resolve macros, virtual dispatch, function pointers, generated code, or backend registration reliably.
- A conceptual layer stack is not a universal execution order for every model architecture or backend combination.
- APIs named `async` do not prove host-visible overlap.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible hover/click behavior.
- Source-pinned end-to-end code workflow.
- Deep GGUF and model-loading chapters.
- Canonical `llama_context` and `llama_model` ownership/lifetime pages.
- GGML tensor/op/graph-construction and execution chapter.
- Memory ownership and synchronization atlas.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.