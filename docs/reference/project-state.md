# Project state

_Last updated: 2026-07-12 10:52 Africa/Cairo_

This file is the compact checkpoint for scheduled and manual research runs. Read it after the root README and update it whenever a meaningful increment is completed.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Baseline role: reproducible initial documentation target
- Current-ref policy: index newer refs separately; do not silently rewrite baseline claims

## Active milestone

**Milestone 1 — One complete vertical slice**

Trace a minimal application from backend loading and model creation through context construction, graph build/reuse, scheduler allocation, backend execution, output retrieval, sampling, and the next-token loop.

## Completed

- MkDocs Material site scaffold and Pages workflow.
- Pinned-source evidence convention.
- Minimal-example top-level flow from backend loading to sampling.
- Initial model-load trace covering loader creation, architecture dispatch, device preparation, hyperparameters, vocabulary, statistics, and tensors.
- Repository map, GGML introduction, research ledger, and research log.
- Mermaid overview and clickable inference prototype.
- Upstream mirror and approximate source-index scripts.
- Hourly context-integrity workflow and mandatory README bootstrap protocol.
- Independent strict documentation CI, Pages enablement detection, deployment health checking, and interactive HTML asset.
- Pinned `llama_decode -> llama_context::decode -> process_ubatch` trace, including memory-batch preparation, graph reuse/rebuild, reserve-versus-allocation, CPU thread selection, and scheduler submission.
- Pinned scheduler trace covering backend assignment, split construction, destination-copy allocation, copy-slot events, fallback synchronization, MoE partial transfers, split submission, and output visibility.
- Static accessible SVG replacement for the backend-scheduler Mermaid sequence that failed under the deployed Mermaid 11 renderer.
- Pinned CPU-versus-CUDA backend comparison covering threadpool completion, CUDA stream submission, event semantics, synchronous buffer operations, and the difference between internal parallelism and scheduler-level asynchrony.
- Pinned branch-by-branch `ggml_backend_cuda_cpy_tensor_async()` trace covering eligibility checks, same-backend copies, same-device cross-backend copies, peer copies, source-stream events, destination waits, and every `false` fallback condition.
- Pinned Metal backend trace covering graph command-buffer submission, dispatch-worker encoding, asynchronous blit set/get/copy operations, event signal/wait command buffers, explicit synchronization, and persistent error handling.
- CUDA-versus-Metal capability table distinguishing stream/event and command-buffer/event semantics, discrete-memory and unified-memory caveats, and scheduler-visible completion boundaries.
- Pinned generic tensor-copy fallback trace covering two-backend synchronization, host-source/host-destination branches, destination-buffer direct copies, and full-tensor heap staging.
- CPU/mmap-to-CUDA, CUDA-host-to-CUDA, and CPU/mmap-to-Metal fallback paths with ownership, visibility, and synchronization-bubble analysis.
- Concrete CPU, CPU_Mapped, CUDA-device, CUDA-host, and Metal capability documentation for `is_host`, blocking set/get, direct copy, ownership, completion, and staging behavior.
- Source-buffer × destination-buffer matrix for representative CPU/mmap/CUDA/Metal pairs plus a runtime validation schema for page faults, synchronization bubbles, overlap, and temporary RSS.
- Pinned Vulkan capability boundary covering non-host-visible default buffers, dedicated host-buffer support, async/events flags, queues, timeline-semaphore-backed host synchronization, and internal graph hazard tracking.
- Complete pinned Vulkan transfer trace covering adaptive memory-property selection, mapped versus staging writes, UMA and staged reads, same-device and cross-device blocking copies, Vulkan host registration, conditional async set/get behavior, scheduler async-copy acceptance, and fence/deferred-copy completion.
- Vulkan rows in the buffer compatibility matrix, including CPU/mmap, registered host, same-device device, cross-device device, and host-buffer destinations.

## In progress

- GitHub Pages must be enabled in repository settings before deployment can run.
- Latest CI and live-site status must be verified after this documentation increment.
- Detailed `llama_context` construction and ownership map.
- Exact SYCL, RPC, CANN, and Android-compiled-backend buffer compatibility.
- Exact Metal shared/private buffer-level branches below the wrapper layer.
- Runtime evidence for Vulkan memory-type selection and transfer behavior on Android integrated GPUs.

## Immediate next task

Trace the pinned SYCL transfer and memory model:

```text
SYCL buffer type and allocation
  -> device, shared, host, and USM ownership
  -> set_tensor / get_tensor
  -> blocking cpy_tensor acceptance
  -> scheduler cpy_tensor_async acceptance
  -> queue and event dependencies
  -> return-time completion guarantee
```

Deliverables for that task:

1. host/shared/device allocation and visibility table;
2. exact blocking set/get branches;
3. direct-copy and scheduler async-copy acceptance matrix;
4. queue, event, and synchronization rules;
5. SYCL rows in `docs/lifecycle/buffer-compatibility.md`;
6. runtime instrumentation points for Intel and non-Intel SYCL implementations.

## Known blockers and caveats

- Pages deployment remains intentionally skipped until **Settings -> Pages -> Source: GitHub Actions** is enabled.
- GitHub status APIs may not expose all check-run conclusions through the connected repository interface; workflow files retain durable checks, and unresolved verification remains a TODO.
- The execution environment has no local repository checkout and cannot resolve `github.com`, so strict MkDocs validation is delegated to GitHub Actions; connector-side source and publication checks remain available.
- Regex-based indexing cannot resolve virtual dispatch, macros, function pointers, generated code, or backend registration reliably.
- Graph reuse compatibility is distributed across graph-input implementations; the base implementation rejects reuse unless a specialized check exists.
- Scheduler APIs named `async` do not guarantee overlap: the pinned CPU backend blocks in `ggml_graph_compute`, while CUDA, Metal, and Vulkan advertise asynchronous execution paths.
- CPU threadpool parallelism is internal to a blocking graph call and is not scheduler-level asynchronous submission.
- CUDA ordinary buffer operations may call asynchronous CUDA primitives and then immediately synchronize; the primitive name alone does not prove host-visible asynchrony.
- The pinned CUDA async-copy callback accepts only CUDA backend objects with CUDA device buffers whose backend and buffer devices agree; CPU/mmap and CUDA host buffers return `false`.
- Cross-device CUDA copies require peer-copy support; `GGML_CUDA_NO_PEER_COPY` forces the generic fallback.
- A successful accelerator async-copy callback means the copy and dependencies were queued, not that bytes are host-visible.
- Rejected async copies synchronize both source and destination backends before blocking copy, potentially eliminating overlap on both sides.
- If neither buffer is host-visible and the destination buffer rejects direct `cpy_tensor`, the generic fallback allocates a full-tensor host buffer, performs blocking get and set operations, then frees it.
- CPU and CPU_Mapped report host visibility and use direct `memcpy()`, but CPU_Mapped does not imply physical residency or fault-free access.
- CUDA device set/get/direct-copy functions synchronize before returning and therefore expose blocking buffer semantics.
- CPU/mmap host-source paths avoid generic heap allocation but may still incur mmap page faults and a blocking accelerator transfer.
- Metal shared or unified memory does not imply command completion, safe reuse, or immediate host visibility.
- Vulkan's ordinary buffer may be internally mapped while still reporting `is_host == false`; GGML host visibility and Vulkan memory flags are different contracts.
- Vulkan registered host buffers enable queued host-to-device scheduler copies; ordinary CPU and mmap pointers do not.
- Vulkan backend async set/get callbacks synchronize when they must use the backend's coherent sync-staging buffer for an unregistered host pointer.
- Cross-device Vulkan blocking copies are host-mediated and complete synchronously; the scheduler async callback rejects them.
- Vulkan internal graph hazard tracking and cross-backend scheduler ordering solve different synchronization problems.
- Copy tensors are scheduler-owned temporary execution storage, not persistent model-owned duplicates.
- The pinned MoE partial-copy path optimizes transfer volume but is not a long-lived expert-cache policy.
- Backend behavior varies by build configuration, memory heaps, drivers, and device capabilities.
- Current upstream may differ materially from the pinned baseline; version labels are mandatory.
- Full runtime validation requires representative CPU and accelerator builds, traces, and models.

## Definition of done for the current milestone

- A beginner-readable end-to-end page.
- A source-level call chain from API to kernel execution and back.
- Separate prompt-processing and token-generation descriptions.
- Memory-owner and concurrency annotations.
- Mermaid sequence and architecture figures.
- Interactive nodes linked to exact source evidence.
- Open questions recorded rather than guessed.
