# Implementation and research roadmap

The project is organized as research milestones rather than a fixed chapter-writing sequence. Each milestone must leave behind source notes, diagrams, references, and unresolved questions.

## Milestone 0 — Reproducible research infrastructure

**Deliverables**

- Pin a baseline commit while retaining a mirror of all upstream refs.
- Export branch, tag, and commit metadata.
- Inventory all text source files, approximate symbols, includes, hashes, and line counts.
- Define truth labels and citation rules.
- Deploy MkDocs Material to GitHub Pages.

**Validation**

- The index can be regenerated in CI.
- Every implementation page declares its source revision.
- A broken pinned source link fails CI in a future link-check workflow.

## Milestone 1 — One complete vertical slice

Trace a minimal program from startup to one generated token:

1. backend discovery;
2. model parameters;
3. GGUF parsing and model architecture creation;
4. tensor loading and placement;
5. prompt tokenization;
6. `llama_context` construction;
7. batch preparation;
8. prefill/decode;
9. graph build or reuse;
10. backend split, allocation, copies, and compute;
11. output transfer;
12. sampling and the next-token loop;
13. teardown.

Produce a short page, a detailed sequence, and the first interactive workflow.

## Milestone 2 — Repository atlas

Map each major tree and its responsibility:

- public API and core runtime;
- GGML core, allocator, scheduler, and backend interfaces;
- CPU kernels and thread pool;
- CUDA, Metal, Vulkan, SYCL, OpenCL, RPC, and other backends;
- model converters and GGUF tools;
- examples, tools, tests, scripts, and CI;
- architecture-specific model implementations.

For every directory, record ownership boundaries, common entry points, and cross-directory dependencies.

## Milestone 3 — GGML foundations

Explain tensors, shapes/strides, views, operations, graph construction, graph planning, allocation, backend buffers, execution, quantized types, and why GGML is not simply “a graph executor.”

Figures:

- tensor metadata versus tensor storage;
- operation node and source tensors;
- graph construction versus execution;
- backend buffer ownership and placement;
- graph allocator lifetime.

## Milestone 4 — Model and GGUF lifecycle

Deep-trace:

- GGUF header, metadata, tensor descriptors, alignment, and data region;
- split GGUF files;
- architecture dispatch;
- hyperparameters and vocabulary;
- tensor name mapping;
- mmap versus explicit reads;
- device and buffer-type selection;
- quantized tensor storage;
- load-time progress and cancellation.

## Milestone 5 — Memory atlas

Separate all memory categories:

- model weight mappings and backend buffers;
- OS page cache, virtual mappings, page faults, RSS, and clean-page reclaim;
- context and graph metadata;
- KV/recurrent/hybrid memory;
- compute and graph-allocation buffers;
- outputs, logits, embeddings, staging, and copy tensors;
- device-local memory and host-pinned buffers;
- transient workspace and thread scratch buffers.

Every category must state owner, allocator, lifetime, visibility, mutability, and reclaim behavior.

## Milestone 6 — Scheduling, process, and concurrency

Trace:

- process-level startup and dynamic backend loading;
- context-level scheduler creation and reservation;
- graph backend assignment and split creation;
- cross-backend copies and events;
- pipeline parallelism;
- CPU thread-pool lifecycle, barriers, atomics, and work partitioning;
- asynchronous backend queues and synchronization;
- graph reuse and topology matching;
- batching, micro-batching, and multiple sequences.

## Milestone 7 — Backend encyclopedia

Use one template for every backend:

1. build and registration;
2. device discovery;
3. buffer types;
4. supported operations;
5. graph compute entry point;
6. command queues/streams and events;
7. copies and synchronization;
8. kernel organization;
9. memory constraints;
10. profiling/debugging;
11. known limitations and active PRs.

## Milestone 8 — Model architecture and MoE deep dives

Explain the model-class interface, architecture-specific graph builders, attention variants, dense FFNs, MoE routing, `MUL_MAT_ID`, expert tensor layouts, selected-expert copies, recurrent models, multimodal paths, and speculative decoding.

## Milestone 9 — Full interactive inference animation

Build a data-driven visualizer with synchronized lanes:

- application/API;
- model/context objects;
- GGML graph;
- scheduler;
- memory/OS;
- CPU threads;
- GPU queues;
- outputs/sampler.

Each node opens:

- a plain-language explanation;
- exact functions and files;
- inputs/outputs and state mutations;
- memory ownership;
- thread/backend context;
- source links;
- relevant PRs/discussions;
- diagrams and runtime traces.

The animation must support prefill, single-token decode, CPU-only, GPU offload, multi-backend, and MoE variants rather than presenting one path as universal.

## Milestone 10 — Object-centred and searchable documentation

Treat runtime objects and source symbols as first-class entry points, not only files and chapters. Build canonical pages for `llama_model`, `llama_context`, `llama_batch`, `ggml_tensor`, `ggml_cgraph`, `ggml_backend_sched`, backend buffers, GGUF loaders, and KV/recurrent memory.

Connect those pages to a clickable source explorer, synchronized diagrams, memory and execution visualizers, backend/version comparisons, prerequisites, related topics, and next-step navigation.

The complete quality contract, review rubric, and first implementation slices live in [Documentation quality and interaction roadmap](reference/documentation-quality-roadmap.md).

## Ongoing research tracks

- Official docs, source comments, tests, examples, and benchmarks.
- Pull requests and discussions explaining design rationale.
- Papers evaluating llama.cpp, GGML, quantization, and heterogeneous execution.
- Conference talks, maintainer interviews, videos, blogs, and technical social posts.
- Runtime validation with logs, profilers, page-fault counters, memory maps, and backend traces.
- Periodic live-site reviews covering discoverability, source traceability, ownership clarity, accessibility, cross-links, and interaction quality.
