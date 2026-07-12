# Project state

_Last updated: 2026-07-12 12:52 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Policy: baseline claims stay pinned; newer refs are documented separately.

## Active milestone

**Milestone 1 — One complete vertical slice**

Trace a minimal application from backend loading and model creation through context construction, graph build/reuse, scheduler allocation, backend execution, output retrieval, sampling, and the next-token loop.

## Completed

- MkDocs Material site, strict documentation CI, Pages deployment, website health check, source indexing, and README-first scheduled-run context.
- Minimal end-to-end path and initial model-loading trace.
- Pinned decode, graph-reuse, backend-scheduler, copy-ring, split-allocation, and synchronization documentation.
- CPU versus CUDA execution semantics and branch-by-branch CUDA asynchronous-copy analysis.
- Metal command-buffer, blit, event, synchronization, and completion analysis.
- Generic tensor-copy fallback and blocking copy decision tree.
- CPU, CPU_Mapped, CUDA, Metal, Vulkan, and SYCL buffer capability documentation.
- Vulkan allocation, transfer, registered-host, scheduler-copy, and fence semantics.
- SYCL allocation, system-USM, host-buffer, blocking set/get, Level Zero/peer/host-forward copy, async set/get, and disabled scheduler callback semantics.
- Shared buffer compatibility matrix now includes exact pinned SYCL rows and distinguishes generic emergency staging from SYCL mmap/PVC and host-forward staging.
- Accessible static scheduler SVG replacing a deployed Mermaid renderer failure.

## In progress

- Detailed `llama_context` construction, ownership, and lifetime map.
- Exact Metal shared/private buffer-level branches.
- RPC, CANN, OpenCL, and Android-compiled backend compatibility.
- Runtime evidence for page faults, queue/fence waits, temporary RSS, and copy/compute overlap.
- Historical comparison of later scheduler and backend changes.

## Immediate next task

Identify the first later llama.cpp revision that registers or replaces SYCL scheduler tensor-copy asynchrony:

```text
pinned interface: cpy_tensor_async = NULL
  -> search later commits and PRs
  -> identify first semantic change
  -> compare accepted source/destination pairs
  -> compare queue/event dependency construction
  -> compare host-return and safe-reuse boundaries
```

Deliver one reviewable pinned-versus-later comparison with exact refs, truth labels, and implications for the shared compatibility matrix.

## Latest publication verification

- Latest documentation commit checked: `93e1243a8181c42b0e441839be58b51d084bde48`.
- Connected combined-status response contained no status entries.
- Connected commit-workflow query returned an empty run list because that interface exposes only a limited subset of runs; it did not prove success or failure for push-triggered Documentation CI or Pages deployment.
- The public site is known to be enabled at `https://mohammed-alaa40123.github.io/How.to.llama.cpp/`.
- Automated browser verification could not fetch the root page in this run: the fetcher returned a cache-miss error, and search had not indexed the site or newly changed page.
- The execution container also could not resolve `github.com`, so local clone, strict MkDocs build, and direct `curl` verification were unavailable.
- These are verification-tooling blockers, not evidence that the site or CI failed. Recheck the Actions UI and public site on the next run.

## Known blockers and caveats

- The connected commit-status interface may omit push-triggered workflow conclusions.
- The execution container currently cannot resolve `github.com`; GitHub Actions remains the authoritative strict-build environment.
- Regex indexing cannot resolve macros, virtual dispatch, function pointers, generated code, or backend registration reliably.
- APIs named `async` do not prove host-visible overlap.
- Rejected scheduler async copies synchronize both source and destination before blocking fallback.
- Generic and backend-specific staging allocations are distinct and require separate instrumentation.
- CPU_Mapped addressability does not imply physical residency or fault-free access.
- Accelerator unified/shared/system memory does not by itself imply GGML host visibility, command completion, or safe reuse.
- Backend behavior depends on build configuration, runtime, driver, memory heaps, and device capabilities.

## Definition of done for Milestone 1

- Beginner-readable end-to-end explanation.
- Source-level API-to-kernel-and-back call chain.
- Separate prefill and token-generation descriptions.
- Memory-owner and concurrency annotations.
- Backend-specific execution and copy semantics.
- Source-pinned diagrams and interactive nodes.
- Historical changes and open questions labelled rather than guessed.
