# Project state

_Last updated: 2026-07-13 21:49 Africa/Cairo_

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
- Pinned OpenCL build composition, kernel deployment, official platform scope, and initial `cl_mem` RAII ownership map.
- Line-aware generated source indexing with untruncated symbol records, declaration kinds, 1-based lines, and regression tests.
- Revision-pinned file and symbol URLs derived from the exact indexed llama.cpp revision.

## Latest concrete findings

- Backend-before-scheduler safety requires two independent proofs: queued commands have completed, and later scheduler deleters retain valid state without using the deleted backend context.
- Ordinary CPU is verified safe because execution is synchronous and scheduler events are unsupported.
- Metal and Vulkan explicitly synchronize during backend cleanup and retain independent scheduler-resource deleter state for the audited ordinary paths.
- CUDA and SYCL ordinary scheduler events and buffers are structurally independent, but complete stream/queue completion remains conditional.
- RPC client buffers retain transport and remote handles, but graph submission has no server completion response and RPC synchronize is a no-op.
- CANN performs device-wide synchronization, but reset precedes later context and scheduler destructor calls.
- OpenCL remains unclassified beyond build composition and initial `cl_mem` ownership.
- The comparison page links each concise classification to its detailed evidence page and is now in the Architecture navigation.

## In progress

- Regeneration of the pinned source inventory with line-aware records and pinned source links.
- Exact OpenCL backend/context teardown, queue completion, scheduler events/buffers, and program/kernel/context release order.
- Optional CPU extra-buffer teardown audit.
- CANN reset semantics and multi-context runtime validation.
- RPC remote synchronization/completion protocol and shared-socket concurrency.
- CUDA concurrent-stream synchronization coverage.
- SYCL all-queue completion coverage and implicit destructor semantics.
- Vulkan performance-query-pool ownership and process-exit device teardown.
- Architecture-specific graph-builder downcasts and exact state tensors.
- Runtime evidence for synchronization, event waits, page faults, memory updates, and teardown.

## Immediate next task

Finish the OpenCL teardown audit when the pinned oversized translation unit is accessible:

```text
OpenCL backend/context free
→ queue completion and event waits
→ scheduler event and buffer ownership
→ program and kernel release
→ cl_mem and context release
→ optional binary-library handle lifetime
→ backend-before-scheduler classification
```

Then audit optional CPU extra-buffer deleters independently.

## Publication and verification state

- Backend comparison page commit: `963ff8b9523e9d484063c75bef0f3f89d0c54e80`.
- Navigation commit: `c831b301519fbb84a8b8657c82e49db9a83b554b`.
- Detailed note commit: `121ed3bafc3c1d0a0ba218d5a37af8fde395d0ba`.
- Research-log commit: `c9223bf0049919a334fc8b00c6b0113c16fb67d0`.
- Repository contents API confirmed creation of the new page and navigation update.
- Local clone of both repositories still fails with `Could not resolve host: github.com`; full local validation could not run.
- The pinned oversized `ggml-opencl.cpp` remains inaccessible through the connector, so the OpenCL classification was not guessed.
- CI and Pages verification results for the latest commit are recorded below when observable; absent results are treated as unverified rather than failed.

## Known blockers and caveats

- **Pinned regeneration blocker:** the execution environment cannot resolve `github.com`, so the new index cannot be run against the pinned checkout here.
- **Large upstream file blocker:** the GitHub connector returns no content for the oversized pinned `ggml-opencl.cpp`, so the exact OpenCL teardown audit remains blocked.
- **Local validation blocker:** the full Python tests, strict MkDocs build, and `check_site.sh` require a usable checkout and could not be run here.
- **CI visibility blocker:** commit status and workflow visibility may be empty even when Actions later run; record exact results rather than inferring failure.
- **Pages verification blocker:** if direct HTTP inspection is rejected or unavailable, root and route status remain unverified.
- **OpenCL completion caveat:** `cl_mem` ownership is verified, but command completion before release remains open.
- **CANN reset-order caveat:** device-wide completion is explicit, but the validity of later ACL destroy/free calls after `aclrtResetDevice()` is unverified.
- **RPC completion caveat:** graph compute has no completion response and RPC synchronize remains a no-op.
- **SYCL completion caveat:** backend free does not explicitly wait before destroying context-owned resources.
- **Vulkan query-pool caveat:** the optional performance query pool still needs a focused ownership audit.
- Mapping, allocation, residency, validity, command completion, ownership, reset, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, memory, and teardown ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
