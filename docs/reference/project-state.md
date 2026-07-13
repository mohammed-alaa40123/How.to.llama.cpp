# Project state

_Last updated: 2026-07-14 01:52 Africa/Cairo_

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
- Guided end-to-end inference atlas with a clickable pipeline, stage/lifetime table, and audience-specific reading paths.

## Latest concrete findings

- The new atlas gives one stable entry route across GGUF, loading, model/context, graph construction, scheduler execution, backend completion, persistent memory, sampling, decode reuse, and teardown.
- Mermaid click targets are resolved from the rendered route rather than the Markdown source directory; the initial targets were corrected after repository read-back.
- A linear learning map must not imply linear runtime execution: mappings/uploads, graph splits, asynchronous queues, copy generations, and persistent state cross the simplified stage boundaries.
- Backend-before-scheduler safety still requires two independent proofs: queued commands have completed, and later scheduler deleters retain valid state without using the deleted backend context.
- Ordinary CPU is verified safe because execution is synchronous and scheduler events are unsupported.
- Metal and Vulkan explicitly synchronize during backend cleanup and retain independent scheduler-resource deleter state for the audited ordinary paths.
- CUDA and SYCL ordinary scheduler events and buffers are structurally independent, but complete stream/queue completion remains conditional.
- RPC client buffers retain transport and remote handles, but graph submission has no server completion response and RPC synchronize is a no-op.
- CANN performs device-wide synchronization, but reset precedes later context and scheduler destructor calls.
- OpenCL remains unclassified beyond build composition and initial `cl_mem` ownership.

## In progress

- Regeneration of the pinned source inventory with line-aware records and pinned source links.
- Exact OpenCL backend/context teardown, queue completion, scheduler events/buffers, and program/kernel/context release order.
- Optional CPU extra-buffer teardown audit.
- Shared generated metadata for the static inference atlas and interactive workflow.
- Runtime overlays for page faults, scheduler copies, event waits, KV/recurrent growth, and backend queues.
- CANN reset semantics and multi-context runtime validation.
- RPC remote synchronization/completion protocol and shared-socket concurrency.
- CUDA concurrent-stream synchronization coverage.
- SYCL all-queue completion coverage and implicit destructor semantics.
- Vulkan performance-query-pool ownership and process-exit device teardown.
- Architecture-specific graph-builder downcasts and exact state tensors.

## Immediate next task

Finish the OpenCL teardown audit when the complete pinned oversized translation unit is searchable:

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

- Atlas page commit: `22a99967c7734eefb5251e853743025ed089d357`.
- Navigation commit: `549e5498408ec60c0f2248af6471dcfc7c7e3bfc`.
- README/TODO commit: `4af2aebf264878b2216b58514c78ce706c7f2879`.
- Detailed note commit: `77957ee8d03a41fc1cd3316079bb4ffca096e077`.
- Research-log commit: `910b3ae3608b42d4242048d7048567d43b7a1249`.
- Mermaid-route correction commit: `d41ca9ab43a94cc738319bf775cce4c3e1d3c377`.
- Repository read-back confirmed the atlas, truth labels, reading paths, and corrected Mermaid targets are present on `main`.
- The research ledger was unchanged because no new external source was introduced.
- Full local validation could not run because the execution environment still cannot resolve GitHub and has no usable checkout.
- Combined status for `910b3ae3608b42d4242048d7048567d43b7a1249` returned no status records.
- Commit-scoped workflow lookup returned `workflow_runs: []`; Documentation CI, Pages deployment, and hourly-context validation are unverified, not confirmed failed.
- Direct opening of the Pages root and `lifecycle/inference-atlas/` route was rejected by the safe-URL gate, so HTTP status and rendered content are unverified.

## Known blockers and caveats

- **Pinned regeneration blocker:** the execution environment cannot resolve `github.com`, so the new index cannot be run against the pinned checkout here.
- **Large upstream file blocker:** the pinned OpenCL blob is retrievable only as a truncated connector response; the hidden remainder is not searchable through the exposed resource, so the exact destructor chain remains blocked.
- **Local validation blocker:** the full Python tests, strict MkDocs build, and `check_site.sh` require a usable checkout and could not be run here.
- **CI visibility blocker:** combined status is empty and the available commit workflow endpoint returned no runs for the checked commit.
- **Pages verification blocker:** the safe-URL gate rejected direct access to the root and new atlas route.
- **Mermaid validation caveat:** source-relative Markdown links and browser-resolved Mermaid click URLs use different bases; built-site validation should cover both.
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
