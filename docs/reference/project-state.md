# Project state

_Last updated: 2026-07-12 17:50 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Policy: baseline claims stay pinned; newer refs are documented separately.

## Active milestone

**Foundations deepening — interactive system map plus file-by-file subsystem synthesis**

Return to the foundations and reconstruct llama.cpp from the pinned source in two complementary directions:

1. a large clickable system map that explains layers, code paths, memory, GGUF, graph construction, execution, and synchronization;
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
- Canonical GGUF file-anatomy chapter covering format structure, split indexing, loader entry, mmap/page-fault distinctions, ownership, and truth labels.
- Canonical model tensor-placement and data-transfer chapter covering device assignment, per-tensor buffer selection, mapping initialization, host-pointer aliasing, explicit reads, synchronous/asynchronous uploads, progress, cancellation, validation, trimming, and ownership.
- Expanded implementation roadmap with four passes: file inventory, subsystem grouping, cross-file composition, and complete workflow reconstruction.

## In progress

- Linking the interactive GGUF/graph tab to both canonical model-loading chapters.
- GGML op insertion, tensor-as-node semantics, graph expansion, activation allocation, reuse, and execution.
- Memory atlas and interactive runtime overlays for mmap/page faults, RAM/RSS, backend copies, KV/recurrent state, and workspaces.
- Runtime evidence separating parsing, mapping/prefetch, page faults, direct reads, alias bytes, upload bytes, event waits, and first-token access.
- File-by-file Pass A for public API/examples, model/GGUF loader, and runtime context.
- Architecture-specific graph-builder, prefill/decode, KV/recurrent, and MoE extensions to the explorer.
- Exact Metal shared/private buffer-level branches.

## Immediate next task

Create the GGML graph-construction chapter and connect the GGUF explorer tab:

```text
architecture graph builder
  -> GGML op calls create output tensors
  -> source tensors define graph edges
  -> graph expansion discovers dependencies
  -> insertion and visit ordering
  -> views and aliases
  -> scheduler backend assignment
  -> activation/workspace allocation
  -> reuse compatibility checks
  -> execution and synchronization
```

Required deliverables:

1. exact pinned graph-builder and `ggml_build_forward_expand()` call chain;
2. explanation of tensors as lazy operation nodes rather than immediately executed values;
3. source-edge and topological-order diagrams;
4. allocation versus execution lifetime table;
5. graph-reuse boundaries across prefill/decode and architecture variants;
6. links from the interactive GGUF/graph tab to the GGUF and model-placement chapters.

The next canonical object page remains `llama_model`.

## Latest publication verification

- Model-placement chapter commit: `b61658e995acee3e4608c429b5aa16c70899409c`.
- Navigation update commit: `7d44f4db0780bf165d340721b65dbbe6aedc743f`.
- README milestone commit: `047730e9dce75f0f6c788c1f9144d7f924ecc75b`.
- Detailed-note commit checked for publication state: `3fe43f6f5cb8ae14132047357cb1679395fb7a10`.
- The combined-status endpoint returned no status records for that commit.
- The available commit-workflow endpoint returned no runs; it is documented to expose only pull-request-associated runs, so push-triggered Documentation CI, Pages, and hourly context checks remain unverified.
- Public site: `https://mohammed-alaa40123.github.io/How.to.llama.cpp/`.
- Site-specific searches returned no indexed results for either the project title or the new model-placement page.
- Direct opens of both the site root and new page were rejected by the browser safety layer because neither URL came from a prior search result.

## Known blockers and caveats

- **CI blocker:** the connector exposes no combined statuses and its workflow-run action filters to pull-request-triggered runs, so the latest push workflows cannot be confirmed or inspected for failures.
- **Pages blocker:** search returned no indexed site result, and direct open is disallowed for URLs not returned by search; therefore HTTP status and rendered content cannot be verified in this environment.
- **Local validation blocker:** prior runs could not obtain a checkout because the execution container failed DNS resolution for GitHub hosts; no new local checkout became available in this run.
- The official GGUF specification can evolve beyond the pinned llama.cpp implementation.
- Mmap host-pointer wrapping is conditional; “zero-copy model loading” is not a model-wide property under partial offload or incompatible buffer types.
- Prefetch requests do not prove permanent physical residency.
- Async upload requires a non-mmap, non-validation path plus device async, host-buffer, and event capabilities.
- CPU_Mapped addressability does not imply physical residency or fault-free access.
- Accelerator unified/shared/system memory does not by itself imply GGML host visibility, command completion, or safe reuse.
- Regex indexing cannot resolve macros, virtual dispatch, function pointers, generated code, or backend registration reliably.
- A conceptual layer stack is not a universal execution order for every model architecture or backend combination.
- APIs named `async` do not prove host-visible overlap.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible hover/click behavior.
- Source-pinned end-to-end code workflow.
- Deep GGUF and model-loading chapters.
- Canonical `llama_context` ownership/lifetime page.
- GGML tensor/op/graph-construction and execution chapter.
- Memory ownership and synchronization atlas.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
