# Project state

_Last updated: 2026-07-12 01:54 Africa/Cairo_

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
- Mermaid overview and clickable 23-stage inference prototype.
- Upstream mirror and approximate source-index scripts.
- Hourly context-integrity workflow and mandatory README bootstrap protocol.
- Independent strict documentation CI, Pages enablement detection, deployment health checking, and the missing interactive HTML asset.

## In progress

- GitHub Pages must be enabled in repository settings before deployment can run.
- Latest CI and live-site status must be verified after the repair commit completes.
- Detailed `llama_context` construction and ownership map.
- Scheduler reservation for prompt processing versus token generation.
- `process_ubatch()` graph reuse/build/allocate path.
- `ggml_backend_sched_graph_compute_async()` split, copy, event, and compute ordering.

## Immediate next task

Trace and document this path at the pinned revision:

```text
llama_decode
  -> llama_context::decode
  -> process_ubatch
  -> model.build_graph / graph reuse
  -> scheduler allocation
  -> graph_compute
  -> ggml_backend_sched_graph_compute_async
  -> backend split execution
```

Deliverables for that task:

1. exact source locations and functions;
2. a sequence diagram;
3. graph reuse conditions and invalidation notes;
4. scheduler reserve/allocation distinction;
5. thread/backend and synchronization annotations;
6. updates to the interactive workflow nodes;
7. a concise research-log entry.

## Known blockers and caveats

- The GitHub connector available to this run does not expose push-triggered Actions run listings or Pages settings, so repository-side workflows perform the durable checks.
- Pages deployment remains intentionally skipped until **Settings → Pages → Source: GitHub Actions** is enabled.
- Regex-based indexing cannot resolve virtual dispatch, macros, function pointers, generated code, or backend registration reliably.
- Backend behavior varies by build configuration and device capabilities.
- Current upstream may differ materially from the pinned baseline; version labels are mandatory.
- Full runtime validation will require representative CPU and accelerator builds, traces, and models.

## Definition of done for the current milestone

- A beginner-readable end-to-end page.
- A source-level call chain from API to kernel execution and back.
- Separate prompt-processing and token-generation descriptions.
- Memory-owner and concurrency annotations.
- Mermaid sequence and architecture figures.
- Interactive nodes linked to exact source evidence.
- Open questions recorded rather than guessed.
