# Project state

_Last updated: 2026-07-12 14:55 Africa/Cairo_

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
- Large interactive foundations explorer with six tabs:
  - system layers;
  - end-to-end code path;
  - memory lifecycle;
  - GGUF and graph construction;
  - execution and synchronization;
  - file-by-file subsystem map.
- Hover summaries and clickable detail panels with representative symbols, ownership, synchronization, and pinned source links.
- Foundations page and homepage integration.
- Expanded implementation roadmap with four passes: file inventory, subsystem grouping, cross-file composition, and complete workflow reconstruction.

## In progress

- Deep GGUF format and model-loader chapter, including the canonical upstream figure with verified attribution.
- Detailed `llama_context` construction, ownership, mutation, synchronization, and lifetime map.
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

After GGUF, build the canonical `llama_context` object page and then the GGML graph-construction chapter.

## Latest publication verification

- Latest documentation commit for this increment must be re-read after durable context updates.
- Connected combined-status and commit-workflow interfaces historically omit push-triggered run conclusions; absence of entries is not proof of success or failure.
- The public site is enabled at `https://mohammed-alaa40123.github.io/How.to.llama.cpp/`.
- Browser fetch of the Pages root returned a cache-miss error in this run.
- The new foundations path could not yet be verified through the browser fetcher; recheck after deployment.

## Known blockers and caveats

- The connected commit-status interface may omit push-triggered workflow conclusions.
- The connected workflow-run query is limited and may return no associated runs.
- The browser fetcher currently returns a cache-miss error for the Pages root; this is a verification-tool limitation, not evidence that the site failed.
- The exact "famous GGUF picture" has not yet been identified from a reliable upstream path. Do not copy an image until source, revision, and attribution/license are verified.
- The interactive explorer currently uses curated JavaScript data rather than generated versioned JSON.
- Some linked paths represent source areas rather than exact symbol definitions; detailed pages must refine them.
- Regex indexing cannot resolve macros, virtual dispatch, function pointers, generated code, or backend registration reliably.
- A conceptual layer stack is not a universal execution order for every model architecture or backend combination.
- "Layer-by-layer loading and freeing" must not be stated as a universal llama.cpp policy: mmap demand paging, OS reclaim, backend placement, graph allocation, and scheduler copies have different lifetimes.
- APIs named `async` do not prove host-visible overlap.
- CPU_Mapped addressability does not imply physical residency or fault-free access.
- Accelerator unified/shared/system memory does not by itself imply GGML host visibility, command completion, or safe reuse.

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
