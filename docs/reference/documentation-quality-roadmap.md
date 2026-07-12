# Documentation quality and interaction roadmap

This roadmap turns How.to.llama.cpp from a collection of source-guided articles into a navigable, object-centred reference and interactive textbook.

## Design objective

A reader should be able to begin with a question such as “what owns the KV cache?”, “what calls `llama_decode()`?”, or “when is a backend copy complete?” and reach the relevant object, call path, source lines, memory owner, synchronization boundary, and historical context without manually searching the repository.

## Priority 1 — Object-centred encyclopedia

Create canonical pages for major runtime objects rather than documenting only files:

- `llama_model`
- `llama_context`
- `llama_batch` and `llama_ubatch`
- `ggml_tensor`
- `ggml_cgraph`
- `ggml_backend_sched`
- `ggml_backend_buffer` and buffer types
- KV, recurrent, and hybrid memory objects
- GGUF contexts and model loaders

Each object page must answer:

1. What is it and why does it exist?
2. Who creates, owns, mutates, and destroys it?
3. What is its lifetime?
4. What memory does it own, reference, or map?
5. Which threads, queues, and backends access it?
6. Which functions call into it and which functions it calls?
7. Which invariants and synchronization rules protect it?
8. Which pinned source lines, PRs, tests, and traces support the explanation?

## Priority 2 — Clickable source explorer

Build a generated symbol index for important functions, objects, files, and subsystems. Every entry should expose:

- definition and pinned GitHub source link;
- direct callers and callees where statically recoverable;
- owning subsystem and related object pages;
- memory and synchronization annotations;
- related diagrams, tests, PRs, discussions, and research notes;
- explicit warnings where macros, function pointers, virtual dispatch, generated code, or backend registration make the graph incomplete.

The generated index is a navigation aid, not a compiler-grade call graph.

## Priority 3 — Diagram and source synchronization

Interactive diagrams should use stable node identifiers shared with documentation metadata. Clicking a node should reveal:

- plain-language explanation;
- exact functions and files;
- inputs, outputs, and state mutations;
- memory ownership;
- thread, queue, event, or barrier context;
- source links and historical references.

Initial synchronized traces:

1. GGUF loading and mmap page faults;
2. `llama_context` construction;
3. prefill and one-token decode;
4. graph build versus graph reuse;
5. scheduler split, copy-ring, events, compute, and synchronization;
6. KV/recurrent memory update;
7. CPU-only, GPU-offload, multi-backend, and MoE variants.

## Priority 4 — Memory and execution visualizers

Develop small, bounded visualizers rather than one monolithic animation:

- mmap → virtual mapping → page fault → page cache/RAM → reclaim;
- tensor metadata versus backing storage;
- model, context, KV, compute, output, and staging lifetimes;
- scheduler split and backend-copy timeline;
- CPU thread-pool work partitioning and barriers;
- GPU stream/queue/event ordering;
- KV-cache occupancy and sequence movement;
- MoE routing and selected-expert execution.

Every visualizer must state whether it is conceptual, source-derived, or runtime-measured.

## Priority 5 — Navigation contract

Every mature page should provide:

- prerequisites;
- a five-minute explanation;
- an end-to-end flow;
- pinned source map;
- memory and concurrency notes;
- backend/version differences;
- related objects and pages;
- next recommended page;
- Verified, Interpretation, Historical, and Open question sections.

Search should support important symbols such as `llama_decode`, `llama_context`, `ggml_tensor`, and `ggml_backend_sched`, not only prose titles.

## Priority 6 — Version and backend comparison

Add structured comparisons for:

- pinned baseline versus selected later upstream revisions;
- backend buffers, host visibility, copies, events, graph support, and completion semantics;
- changed call paths, ownership, and synchronization rules;
- removed, replaced, or renamed objects and functions.

Historical comparisons must identify exact commits or PRs and must never silently rewrite baseline claims.

## Review rubric

A website review should score each major section for:

1. discoverability;
2. source traceability;
3. object and ownership clarity;
4. memory and synchronization clarity;
5. diagram usefulness;
6. mobile readability and accessibility;
7. cross-link quality;
8. version clarity;
9. open-question visibility;
10. whether the page guides the reader to a sensible next step.

## First implementation slices

- [ ] Create the canonical `llama_context` object page and apply the page contract.
- [ ] Add reusable page metadata for prerequisites, related objects, source symbols, and next pages.
- [ ] Extend the source index with object and symbol landing pages.
- [ ] Make the existing inference workflow nodes link to source and object pages.
- [ ] Add an mmap/page-fault visualizer with conceptual and runtime-evidence modes.
- [ ] Add automated checks for missing truth labels, source maps, and navigation metadata on mature pages.

## Truth labels

### Verified

- The current site already contains a clickable inference workflow, source-pinned lifecycle pages, a source index, and backend-specific copy/memory documentation.
- The current generated source index is explicitly limited and cannot resolve all dispatch mechanisms.

### Interpretation

- Object-centred navigation and synchronized source/diagram metadata will reduce the largest current usability gap: readers must otherwise reconstruct ownership and cross-file relationships themselves.

### Historical

- The project began as a linear end-to-end source walkthrough; this roadmap preserves that path while adding object, symbol, memory, backend, and version entry points.

### Open question

- Which interaction layer should be implemented first using only static MkDocs assets, and which features require a generated data bundle or client-side application.
