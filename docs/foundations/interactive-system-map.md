# Interactive llama.cpp system map

> **Source baseline:** llama.cpp commit [`e3546c7948e3af463d0b401e6421d5a4c2faf565`](https://github.com/ggml-org/llama.cpp/commit/e3546c7948e3af463d0b401e6421d5a4c2faf565)

This page is the new foundations entry point. It connects the public API, GGUF loading, model and context objects, GGML graph construction, backend scheduling, memory ownership, execution, synchronization, outputs, and sampling.

Use the tabs inside the figure to switch among:

- system layers;
- the end-to-end code path;
- the memory lifecycle;
- GGUF and graph construction;
- execution and synchronization;
- file-by-file source groups.

Hover over a layer for a one-sentence summary. Click it to inspect representative symbols, ownership, synchronization, and pinned source areas.

<div class="workflow-frame foundations-frame">
<iframe src="../../assets/interactive/llama-foundations-explorer.html" title="Interactive llama.cpp foundations and architecture explorer" loading="eager"></iframe>
</div>

## How to read the explorer

### Verified

- The public API enters model loading, context construction, decode, graph allocation, scheduler execution, output retrieval, and sampling through the source areas linked in the explorer.
- GGML operation calls create tensors that describe lazy graph nodes; graph expansion later records dependencies in a `ggml_cgraph`.
- Scheduler allocation and execution are separate phases: assignment, split construction, copy storage, and graph allocation happen before per-split copy and compute submission.
- mmap-backed model weights are file-backed virtual mappings. Addressability does not prove physical residency, and first access may page-fault data into RAM.
- Backend synchronization semantics differ: CPU graph compute may block, while accelerator backends can queue work and require later events or synchronization.

### Interpretation

- The layer stack is a conceptual map, not a claim that every architecture executes one strictly linear sequence.
- "Layer-by-layer loading and freeing" is not a universal llama.cpp policy. mmap demand paging, backend placement, graph allocation, scheduler copies, and OS reclaim create several overlapping lifetimes.
- The file groups are a research organization scheme. Runtime behavior crosses files through interfaces, callbacks, function pointers, architecture dispatch, and backend registration.

### Historical

- This explorer describes the pinned baseline. Newer source layouts, scheduler paths, memory objects, or backend capabilities must be compared explicitly rather than folded into this map silently.

### Open questions

- Which exact upstream image should be mirrored or linked as the canonical "famous GGUF picture," and what license/attribution text should accompany it?
- Which architecture-specific builder files and graph-input classes should become clickable sublayers first?
- Which nodes should load generated caller/callee data instead of curated representative paths?
- Which memory diagrams should gain runtime overlays for page faults, RSS, device transfers, and queue waits?

## Next foundations pages

1. Deep GGUF format and model-loader walkthrough.
2. Canonical `llama_context` ownership and lifetime map.
3. GGML tensor and `ggml_cgraph` construction, operation insertion, and graph expansion.
4. Memory lifecycle: mmap, page cache, model buffers, context state, KV/recurrent memory, activations, workspaces, copies, and teardown.
5. Execution lifecycle: scheduler splits, backend copies, CPU threads, accelerator queues, events, and host-visible completion.
