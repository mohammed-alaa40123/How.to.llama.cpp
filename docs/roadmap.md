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

## Milestone 11 — File-by-file analysis and subsystem synthesis

Analyze the pinned repository file by file, then group files into subsystems and explain how their interfaces compose into end-to-end behavior.

### Pass A — File inventory

For every relevant source file, record:

1. purpose and directory role;
2. major structs, classes, functions, and callbacks;
3. public and internal entry points;
4. direct includes and important dependencies;
5. objects created, owned, referenced, mutated, and destroyed;
6. allocations, mappings, copies, and reclaim paths;
7. threads, queues, events, locks, barriers, and synchronization;
8. build flags and backend-specific branches;
9. callers/callees recoverable from source and tests;
10. unresolved dispatch through macros, function pointers, virtual methods, registration, or generated code.

### Pass B — Group files into subsystem bundles

Initial bundles:

- **Public API and applications:** `include/llama.h`, examples, CLI/server entry points.
- **Model and GGUF loading:** model loader, mmap/file helpers, architecture metadata, tensor naming, vocabulary.
- **Runtime context:** `llama_context`, batching, outputs, graph inputs, decode/prefill control.
- **Memory modules:** KV, recurrent, hybrid memory, sequence state, movement, update, and teardown.
- **GGML core:** tensor metadata, operations, graph expansion, planning, allocation, quantized types.
- **Scheduler and backend interface:** registration, buffer types, split construction, copy-ring storage, events, generic fallback.
- **CPU execution:** thread pools, barriers, graph planning, kernels, scratch/workspace.
- **Accelerator execution:** CUDA, Metal, Vulkan, SYCL, OpenCL, CANN, RPC, and platform-specific backends.
- **Model architectures:** transformer, MoE, recurrent, multimodal, speculative, and architecture-specific builders.
- **Tools and evidence:** converters, GGUF tools, tests, benchmarks, profiling, and CI.

### Pass C — Explain cross-file composition

For each subsystem bundle, produce:

- a five-minute explanation;
- a file relationship diagram;
- public entry → internal call chain;
- object ownership and lifetime map;
- memory and synchronization timeline;
- error/fallback paths;
- tests and runtime evidence;
- links into the interactive system map;
- exact boundaries where control crosses into another subsystem.

### Pass D — Reconstruct complete workflows

Use the subsystem bundles to build source-pinned workflows for:

- startup and backend discovery;
- GGUF open, metadata parse, tensor creation, mmap/read/upload;
- `llama_context` construction;
- prompt tokenization and prefill;
- one-token decode;
- graph build versus graph reuse;
- operation insertion into `ggml_cgraph`;
- scheduler assignment, split copies, compute, events, and synchronization;
- KV/recurrent memory update;
- logits, sampling, next-token loop;
- teardown and memory reclaim.

### Required quality bar

A file is not considered documented merely because its functions are listed. The final explanation must show how it participates in object lifetime, memory ownership, graph construction, execution, and synchronization with neighboring files.

## Ongoing research tracks

- Official docs, source comments, tests, examples, and benchmarks.
- Pull requests and discussions explaining design rationale.
- Papers evaluating llama.cpp, GGML, quantization, and heterogeneous execution.
- Conference talks, maintainer interviews, videos, blogs, and technical social posts.
- Runtime validation with logs, profilers, page-fault counters, memory maps, and backend traces.
- Periodic live-site reviews covering discoverability, source traceability, ownership clarity, accessibility, cross-links, and interaction quality.
