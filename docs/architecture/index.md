# Architecture guide

Use this page to choose a reading path through llama.cpp and GGML architecture. The pages below are pinned to the project baseline unless they explicitly say they discuss newer upstream behavior.

> **Baseline:** `e3546c7948e3af463d0b401e6421d5a4c2faf565`  
> **Audience:** readers moving from an end-to-end overview to source-level implementation details  
> **Recommended first read:** [Guided inference atlas](../lifecycle/inference-atlas.md)

## Choose your path

<div class="grid cards" markdown>

-   :material-map-outline: **Understand the whole repository**

    Start with the [repository map](repository-map.md), then follow the [public API and minimal example](public-api-minimal-example.md) into model loading, context creation, and decode.

-   :material-file-cog-outline: **Understand GGUF and model loading**

    Read [GGUF file anatomy](../foundations/gguf-file-anatomy.md), [model tensor placement](../foundations/model-tensor-placement.md), and [model and GGUF loader Pass A](model-gguf-loader-pass-a.md).

-   :material-memory: **Understand memory and ownership**

    Begin with [memory lifetimes](../foundations/memory-lifetimes.md), then read [runtime context and memory Pass A](runtime-context-memory-pass-a.md), [context memory implementations](context-memory-implementations.md), and the [system ownership and execution map](system-ownership-and-execution-map.md).

-   :material-graph-outline: **Understand graphs and scheduling**

    Read [GGML graph construction and MoE](../ggml/graph-construction-and-moe.md), [backend scheduler Pass A](backend-scheduler-pass-a.md), and [backend scheduler execution](../lifecycle/backend-scheduler-execution.md).

-   :material-cpu-64-bit: **Understand CPU optional buffers**

    Start with the [CPU extra-buffer comparison](cpu-extra-buffer-comparison.md), then inspect the repack, AMX, KleidiAI, and SpacemiT pages. Finish with the [destruction harness](cpu-extra-buffer-destruction-harness.md) for executable lifetime evidence.

-   :material-expansion-card-variant: **Compare accelerator backends**

    Use the backend teardown pages to compare completion, queues or streams, buffer ownership, synchronization, and destruction across CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL.

</div>

## Core architecture

| Page | What it answers |
|---|---|
| [Repository map](repository-map.md) | Which directories and files own the public API, loader, graph builder, scheduler, backends, tools, and tests? |
| [Public API and minimal example](public-api-minimal-example.md) | How does a small application move from backend initialization to model loading, context creation, decode, and sampling? |
| [Model and GGUF loader Pass A](model-gguf-loader-pass-a.md) | Which source files parse metadata, create tensors, map or read weights, and assign them to devices? |
| [Runtime context and memory Pass A](runtime-context-memory-pass-a.md) | Which objects and allocations belong to `llama_context`, and how do they evolve during inference? |
| [Context memory implementations](context-memory-implementations.md) | How do KV and recurrent memory implementations allocate, update, and release persistent state? |
| [Backend scheduler Pass A](backend-scheduler-pass-a.md) | How are nodes assigned, split, copied, allocated, and dispatched across backends? |
| [System ownership and execution map](system-ownership-and-execution-map.md) | Which component owns each major object, buffer, mapping, queue, and graph resource? |

## Ownership and teardown

Read these pages when debugging leaks, use-after-free failures, synchronization assumptions, or destruction order.

| Page | Focus |
|---|---|
| [Model and context teardown order](model-context-teardown-order.md) | Persistent model state versus mutable context state and their required release order |
| [Scheduler core teardown](scheduler-teardown-core.md) | Scheduler-owned splits, copies, events, graph allocations, and backend dependencies |
| [Backend teardown audit method](backend-teardown-audit-method.md) | Reusable worksheet separating work completion from deleter independence |
| [Backend teardown comparison](backend-teardown-comparison.md) | Cross-backend summary of synchronization and ownership behavior |
| [CPU backend teardown](cpu-backend-teardown.md) | CPU wrapper, threadpool, extra buffers, and allocator lifetime |

## CPU optional buffers

These pages distinguish ordinary CPU storage from architecture-specific packed or accelerator-assisted representations.

| Page | Focus |
|---|---|
| [CPU repack lifetime](cpu-repack-extra-buffer-lifetime.md) | Static traits, packed upload, optional dispatch, and buffer independence |
| [CPU AMX lifetime](cpu-amx-extra-buffer-lifetime.md) | AMX allocation, tile permissions, packed representation, and disabled copy paths |
| [CPU KleidiAI lifetime](cpu-kleidiai-extra-buffer-lifetime.md) | KleidiAI packed layouts, callbacks, initialization, and portability questions |
| [CPU SpacemiT IME lifetime](cpu-spacemit-ime-extra-buffer-lifetime.md) | Worker pools, huge pages, device descriptors, and process-level state |
| [CPU extra-buffer comparison](cpu-extra-buffer-comparison.md) | Side-by-side ownership and teardown comparison |
| [CPU extra-buffer destruction harness](cpu-extra-buffer-destruction-harness.md) | Test design plus the first AVX2 CPU_REPACK ASan/LSan evidence |

## Accelerator backends

Use these pages to compare host-visible completion, command submission, persistent runtime objects, buffer deleters, and teardown.

| Backend | Page |
|---|---|
| CUDA | [CUDA backend teardown](cuda-backend-teardown.md) |
| Metal | [Metal backend teardown](metal-backend-teardown.md) |
| Vulkan | [Vulkan command lifetimes](vulkan-command-lifetime.md) and [Vulkan backend teardown](vulkan-backend-teardown.md) |
| SYCL | [SYCL backend teardown](sycl-backend-teardown.md) |
| RPC | [RPC backend teardown](rpc-backend-teardown.md) |
| CANN | [CANN backend teardown](cann-backend-teardown.md) |
| OpenCL | [OpenCL build and buffer lifetimes](opencl-build-and-buffer-lifetimes.md) |

## Suggested reading orders

### New to llama.cpp internals

1. [Guided inference atlas](../lifecycle/inference-atlas.md)
2. [Repository map](repository-map.md)
3. [Public API and minimal example](public-api-minimal-example.md)
4. [GGUF file anatomy](../foundations/gguf-file-anatomy.md)
5. [GGML graph construction and MoE](../ggml/graph-construction-and-moe.md)
6. [Backend scheduler execution](../lifecycle/backend-scheduler-execution.md)

### Investigating mmap, copies, or page faults

1. [GGUF file anatomy](../foundations/gguf-file-anatomy.md)
2. [Model tensor placement](../foundations/model-tensor-placement.md)
3. [Memory lifetimes](../foundations/memory-lifetimes.md)
4. [Model and GGUF loader Pass A](model-gguf-loader-pass-a.md)
5. [Generic copy fallback](../lifecycle/generic-copy-fallback.md)

### Investigating backend scheduling

1. [GGML graph construction and MoE](../ggml/graph-construction-and-moe.md)
2. [Backend scheduler Pass A](backend-scheduler-pass-a.md)
3. [Backend scheduler execution](../lifecycle/backend-scheduler-execution.md)
4. [Buffer compatibility](../lifecycle/buffer-compatibility.md)
5. [Backend teardown audit method](backend-teardown-audit-method.md)

### Investigating ownership or teardown

1. [Memory lifetimes](../foundations/memory-lifetimes.md)
2. [System ownership and execution map](system-ownership-and-execution-map.md)
3. [Model and context teardown order](model-context-teardown-order.md)
4. [Scheduler core teardown](scheduler-teardown-core.md)
5. [Backend teardown comparison](backend-teardown-comparison.md)

## Truth labels used throughout the site

- **Verified** — directly supported by pinned source, official specification, or executable evidence.
- **Interpretation** — a reasoned synthesis built from verified evidence.
- **Historical** — useful behavior or rationale tied to an older revision, PR, or design state.
- **Open question** — not yet established strongly enough to present as fact.

## Next page

For the most compact source-oriented overview, continue to the [repository map](repository-map.md).