# Project state

_Last updated: 2026-07-13 11:49 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream reference used for the graph/MoE chapter: `6b4dc2116a92c5c8f2782bfe51fabe5ee66fb5ef`
- Policy: baseline claims stay pinned; newer refs are documented separately and labelled.

## Active milestone

**Foundations deepening — interactive system map plus file-by-file subsystem synthesis**

## Completed

- MkDocs Material site, strict documentation CI, Pages deployment, health checks, source indexing, and durable run context.
- Canonical GGUF, model placement, model/context, graph/MoE, scheduler, memory-lifetime, and system-ownership pages.
- Pass A pages for public API, model/GGUF loading, runtime context/memory, scheduler, and concrete context-memory implementations.
- Exact pinned declaration and reverse-destruction map for `llama_model` and `llama_context`.
- Exact pinned generic scheduler teardown path.
- Ordinary pinned CPU backend teardown classification.
- Pinned CUDA backend teardown dependency audit and conditional safety classification.

## Latest concrete findings

- `ggml_backend_cuda_free()` deletes the CUDA context and then the backend wrapper.
- The CUDA context destructor waits for active graph capture to end, then destroys its copy event, created streams, and cuBLAS handles; it does not explicitly synchronize queued work first.
- CUDA graph compute is asynchronous and returns after enqueueing kernels or launching a CUDA graph.
- `ggml_backend_cuda_synchronize()` synchronizes the current context stream.
- Scheduler CUDA events own their own `cudaEvent_t` and are freed through the static CUDA device interface without accessing the deleted backend context.
- Scheduler CUDA buffers own a device id and pointer and reach `cudaFree` through their own buffer context; CUDA buffer types are static per-device registry objects.
- Context-owned pools, concurrent events, and CUDA graph objects unwind after the destructor body, after the explicit stream-destruction loop.
- Backend-before-scheduler destruction is therefore structurally independent for ordinary CUDA scheduler events and buffers, but queued-work completion remains conditional on CUDA-family runtime destruction semantics.

## In progress

- Metal teardown audit: command queues/buffers, events/fences, Objective-C ownership, synchronization, and buffer lifetime.
- Remaining concrete backend teardown audits for Vulkan, SYCL, RPC, CANN, and OpenCL.
- Optional CPU extra-buffer teardown audit.
- Architecture-specific graph-builder downcasts and exact state tensors.
- Runtime evidence for synchronization, event waits, page faults, memory updates, and teardown.

## Immediate next task

Trace Metal teardown dependencies:

```text
Metal backend wrapper free
→ command-buffer and queue completion
→ event/fence destruction
→ shared/private buffer release
→ Objective-C/autorelease ownership
→ scheduler event and buffer lifetime
→ classify backend-before-scheduler ordering
```

Required deliverables:

1. exact Metal backend/context free chain;
2. command queue, command buffer, event, and fence synchronization behavior;
3. buffer and buffer-type ownership;
4. queued-work requirements during Objective-C resource release;
5. safety classification for the pinned context member order;
6. truth labels and durable context updates.

## Publication and verification state

- New page: `docs/architecture/cuda-backend-teardown.md`.
- Page commit: `b7b8eb2cea00eccf5f4a7984d9639d5d1877ef48`.
- Navigation commit: `733afe97c96798043a65d84871c128df40711752`.
- Detailed-note commit: `d12b7772860934e4bb2a1445c085be01d63b077f`.
- Research-log commit: `4016a5253e402edc8405d0395ec1e81804e2f36c`.
- README/TODO commit: `5f50f3ccc623537187cf2631a8a655fbc8c3d186`.
- Connector-side source inspection confirmed the pinned CUDA free path, context-destructor order, async interface, explicit synchronize callback, static device/buffer-type lifetime, scheduler event deleter, and buffer `cudaFree` path.
- Workflow lookup for `5f50f3ccc623537187cf2631a8a655fbc8c3d186` returned `workflow_runs: []`; Documentation CI, Pages deployment, and hourly-context validation are unverified rather than confirmed failed.
- Site-specific searches for the project root and `architecture/cuda-backend-teardown/` returned no indexed result, so live HTTP status and rendered content could not be verified through the available web tooling.
- No new external secondary source passed the verification bar; the research ledger remains unchanged.

## Known blockers and caveats

- **Local validation blocker:** the execution environment cannot resolve `github.com` and has no usable checkout, so repository validation commands cannot run locally.
- **CI visibility blocker:** the commit workflow lookup returned an empty run list and the available connector does not expose push-triggered runs for this commit.
- **Pages verification blocker:** site-specific search returned no indexed root or CUDA teardown route; live HTTP status and expected rendered content remain unverified.
- The CUDA classification proves object-path independence, not universal queued-work completion safety across CUDA, HIP, and MUSA runtimes.
- `ggml_backend_cuda_synchronize()` appears to synchronize the current stream only; concurrent-stream coverage requires further verification.
- Mapping, allocation, physical residency, data validity, queued completion, ownership, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, memory, and teardown ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
