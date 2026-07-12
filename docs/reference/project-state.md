# Project state

_Last updated: 2026-07-12 13:52 Africa/Cairo_

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
- Published object-centred, searchable, and interactive documentation quality roadmap with a page contract, live-site review rubric, and bounded first implementation slices.
- Added website-quality review to the durable scheduling plan and navigation.

## In progress

- Detailed `llama_context` construction, ownership, and lifetime map.
- Exact Metal shared/private buffer-level branches.
- RPC, CANN, OpenCL, and Android-compiled backend compatibility.
- Runtime evidence for page faults, queue/fence waits, temporary RSS, and copy/compute overlap.
- Historical comparison of later scheduler and backend changes.
- Object and symbol navigation, source-linked interactive nodes, and memory visualizers.

## Immediate next task

Create the canonical `llama_context` object page using the new documentation quality contract:

```text
public creation API and constructor path
  -> owned and referenced subsystems
  -> scheduler, memory, output, sampler-facing state
  -> decode/prefill mutation points
  -> thread and synchronization boundaries
  -> teardown order
  -> exact pinned source map
```

Deliver one reviewable object page with prerequisites, five-minute explanation, ownership/lifetime table, call chain, memory and concurrency notes, related pages, truth labels, and open questions.

The historical SYCL comparison remains high priority, but the available source index did not expose a reliable first later revision in this run; do not claim one without an exact commit or PR.

## Latest publication verification

- Latest documentation commit checked: `b49b7f08cd59edd00c973f6cce52e085192259e9`.
- Connected combined-status response contained no status entries.
- Connected commit-workflow query returned an empty run list because that interface exposes only a limited subset of runs; it did not prove success or failure for push-triggered Documentation CI or Pages deployment.
- The public site is enabled at `https://mohammed-alaa40123.github.io/How.to.llama.cpp/`.
- Automated browser verification could not fetch the root page in this run: the fetcher returned a cache-miss error.
- Search did not yet index the site or the newly added documentation-quality page.
- These are verification-tooling blockers, not evidence that the site or CI failed. Recheck the Actions UI and public site on the next run.

## Known blockers and caveats

- The connected commit-status interface may omit push-triggered workflow conclusions.
- The connected workflow-run query is limited and returned no associated runs for the latest commit.
- The browser fetcher currently returns a cache-miss error for the Pages root, and search indexing is unavailable for the site.
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
