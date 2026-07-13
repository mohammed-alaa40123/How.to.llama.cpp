# Project state

_Last updated: 2026-07-14 02:49 Africa/Cairo_

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
- Generic scheduler plus ordinary CPU, CUDA, Metal, Vulkan, SYCL, RPC, and CANN teardown audits.
- Cross-backend teardown comparison matrix separating command completion from scheduler-resource independence.
- Reusable backend teardown audit method with a ten-step worksheet, classification vocabulary, and minimum runtime test matrix.
- Pinned OpenCL build composition, kernel deployment, official platform scope, and initial `cl_mem` RAII ownership map.
- Line-aware generated source indexing with pinned file and symbol links.
- Guided end-to-end inference atlas with clickable reading paths.

## Latest concrete findings

- Backend teardown requires two independent proofs: queued commands reached a host-visible completion boundary, and later scheduler deleters retain valid state without the deleted backend context.
- The reusable audit method now makes entry points, queue coverage, context ownership, scheduler events/buffers, registry lifetime, reverse destruction, optional paths, and runtime tests explicit.
- A backend result must name its resource scope; ordinary buffers do not automatically cover graph capture, profiling, communication, extra buffers, or vendor binary paths.
- The project classification vocabulary now distinguishes verified safe, completion conditional, lifetime conditional, remote completion conditional, and open-question states.
- OpenCL remains unclassified beyond build composition and initial `cl_mem` ownership.

## In progress

- Regeneration of the pinned source inventory with line-aware records and pinned source links.
- Exact OpenCL backend/context teardown, queue completion, scheduler events/buffers, and program/kernel/context release order.
- Optional CPU extra-buffer teardown audit.
- Shared generated metadata for the static inference atlas and interactive workflow.
- Runtime overlays for page faults, scheduler copies, event waits, KV/recurrent growth, and backend queues.
- CANN reset semantics, RPC completion, CUDA all-stream coverage, SYCL all-queue coverage, and Vulkan query-pool ownership.

## Immediate next task

Apply the new audit method to the complete pinned OpenCL backend:

```text
backend free entry
→ submission and queue model
→ host-visible completion boundary
→ scheduler event/buffer deleter independence
→ program/kernel/context release
→ optional binary-library lifetime
→ bounded teardown classification
```

Then audit optional CPU extra-buffer deleters independently.

## Publication and verification state

- Work is on branch `automation/backend-teardown-audit-method`.
- Added `docs/architecture/backend-teardown-audit-method.md` and linked it before the comparison page.
- Added detailed note `logs/research/2026-07-14/0249-backend-teardown-audit-method.md`.
- Updated the research log; the research ledger was unchanged because no external source changed.
- Full local validation could not run because the execution environment could not resolve `github.com` and has no checkout.
- CI and Pages verification must be completed against the branch/PR and recorded below when visible.

## Known blockers and caveats

- **Pinned regeneration blocker:** local GitHub DNS resolution failed, so the source index could not be regenerated here.
- **Large upstream file blocker:** the connector still exposes the pinned OpenCL blob as truncated output and exact hidden symbols remain difficult to search.
- **Local validation blocker:** Python tests, strict MkDocs build, and `check_site.sh` require a usable checkout.
- **CI visibility caveat:** commit-scoped checks must be inspected after the branch is published as a PR.
- **Pages caveat:** branch content will not appear on the public site until merged and deployed.
- Mapping, allocation, residency, validity, command completion, ownership, reset, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, memory, and teardown ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
