# Project state

_Last updated: 2026-07-12 04:51 Africa/Cairo_

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
- Pinned CPU-versus-CUDA backend comparison covering threadpool completion, CUDA stream submission, event semantics, synchronous buffer operations, and the difference between internal parallelism and scheduler-level asynchrony.

## In progress

- GitHub Pages must be enabled in repository settings before deployment can run.
- Latest CI and live-site status must be verified after this documentation increment.
- Detailed `llama_context` construction and ownership map.
- Exact branch-by-branch behavior of `ggml_backend_cuda_cpy_tensor_async()`.
- Metal or Vulkan comparison against the CUDA stream/event model.

## Immediate next task

Trace the pinned CUDA copy callback and compare one second accelerator backend:

```text
ggml_backend_cuda_cpy_tensor_async
  -> accepted source/destination buffer combinations
  -> device-to-device or peer transfer primitive
  -> false return and scheduler fallback

Metal or Vulkan
  -> graph submission primitive
  -> copy primitive
  -> event/semaphore ordering
  -> host synchronization boundary
```

Deliverables for that task:

1. exact CUDA copy branches and return conditions;
2. one Metal or Vulkan backend source map;
3. host, same-device, and peer-device transfer table;
4. device-side versus host-side wait semantics;
5. build-configuration caveats;
6. update to the backend comparison page and interactive workflow;
7. concise research-log entry.

## Known blockers and caveats

- Pages deployment remains intentionally skipped until **Settings -> Pages -> Source: GitHub Actions** is enabled.
- GitHub status APIs may not expose all check-run conclusions through the connected repository interface; workflow files retain durable checks, and unresolved verification remains a TODO.
- The execution environment currently cannot resolve `github.com`, so local cloning and strict MkDocs validation cannot run here.
- Regex-based indexing cannot resolve virtual dispatch, macros, function pointers, generated code, or backend registration reliably.
- Graph reuse compatibility is distributed across graph-input implementations; the base implementation rejects reuse unless a specialized check exists.
- Scheduler APIs named `async` do not guarantee overlap: the pinned CPU backend blocks in `ggml_graph_compute`, while CUDA normally queues work on a stream.
- CPU threadpool parallelism is internal to a blocking graph call and is not scheduler-level asynchronous submission.
- CUDA ordinary buffer operations may call asynchronous CUDA primitives and then immediately synchronize; the primitive name alone does not prove host-visible asynchrony.
- Copy tensors are scheduler-owned temporary execution storage, not persistent model-owned duplicates.
- The pinned MoE partial-copy path optimizes transfer volume but is not a long-lived expert-cache policy.
- Backend behavior varies by build configuration and device capabilities.
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