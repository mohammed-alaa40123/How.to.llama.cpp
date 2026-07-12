# Project state

_Last updated: 2026-07-12 15:49 Africa/Cairo_

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
- Canonical `llama_context` object page covering creation, ownership, lifetime, memory, mutation, call chain, synchronization, teardown, source map, backend/version differences, and truth labels.
- Interactive **llama_context runtime** layer and **Construct context** workflow step now link to the canonical object page through shared pinned metadata.
- Expanded implementation roadmap with four passes: file inventory, subsystem grouping, cross-file composition, and complete workflow reconstruction.

## In progress

- Deep GGUF format and model-loader chapter, including the canonical upstream figure with verified attribution.
- Generated versioned metadata shared by interactive nodes, object pages, and source maps.
- GGML op insertion, tensor-as-node semantics, graph expansion, activation allocation, reuse, and execution.
- Memory atlas and interactive runtime overlays for mmap/page faults, RAM/RSS, backend copies, KV/recurrent state, and workspaces.
- File-by-file Pass A for public API/examples, model/GGUF loader, and runtime context.
- Architecture-specific graph-builder, prefill/decode, KV/recurrent, and MoE extensions to the explorer.
- Exact Metal shared/private buffer-level branches.
- Runtime evidence for page faults, queue/fence waits, temporary RSS, and copy/compute overlap.

## Immediate next task

Deepen the GGUF foundations chapter and connect it to the explorer:

```text
GGUF header and version
  -> metadata key/value entries
  -> architecture and hyperparameters
  -> tokenizer/vocabulary metadata
  -> tensor descriptors, types, shapes, offsets, alignment
  -> tensor data region and split files
  -> llama_model_loader construction
  -> tensor metadata creation
  -> mmap versus explicit read/upload
  -> model and backend buffer ownership
```

Required deliverables:

1. official GGUF specification summary;
2. exact pinned model-loader call chain and file map;
3. canonical upstream figure only after verifying its exact source and attribution requirements;
4. memory ownership and page-fault explanation;
5. links from the interactive GGUF tab to the detailed page;
6. Verified, Interpretation, Historical, and Open question sections.

After GGUF, build the GGML graph-construction chapter. The `llama_context` object-page and interactive-link requirements are complete; the next object page is `llama_model`.

## Latest publication verification

- Interactive link implementation commit: `b32b8efcbc2ac5c5d976b20d0977be3ba1447e14`.
- Detailed research note commit: `63897de51dcb95541b52e47c2d668092a419e8d8`.
- Connected commit-workflow lookup is limited and cannot reliably establish all push-triggered Documentation CI or Pages conclusions.
- The public site is configured at `https://mohammed-alaa40123.github.io/How.to.llama.cpp/`.
- Live HTTP/content verification remains required after the final state commits.

## Known blockers and caveats

- The execution container could not resolve `github.com`, preventing a local checkout and local `mkdocs build --strict`.
- The connected workflow-run query may omit push-triggered runs.
- Browser or search fetchers may temporarily miss a newly deployed Pages revision; that is not by itself evidence of deployment failure.
- The exact canonical GGUF image has not yet been identified from a reliable upstream path. Do not copy an image until source, revision, and attribution/license are verified.
- The interactive explorer now centralizes baseline/source/docs roots in one JavaScript metadata object, but does not yet consume generated versioned JSON.
- Regex indexing cannot resolve macros, virtual dispatch, function pointers, generated code, or backend registration reliably.
- A conceptual layer stack is not a universal execution order for every model architecture or backend combination.
- "Layer-by-layer loading and freeing" must not be stated as a universal llama.cpp policy.
- APIs named `async` do not prove host-visible overlap.
- CPU_Mapped addressability does not imply physical residency or fault-free access.
- Accelerator unified/shared/system memory does not by itself imply GGML host visibility, command completion, or safe reuse.
- The `llama_context` page infers external serialization for concurrent mutation; a future pass should locate an explicit public thread-safety contract or preserve this as an open question.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible hover/click behavior.
- Source-pinned end-to-end code workflow.
- Deep GGUF and model-loading chapter.
- Canonical `llama_context` ownership/lifetime page.
- GGML tensor/op/graph-construction and execution chapter.
- Memory ownership and synchronization atlas.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
