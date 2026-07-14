# Project state

_Last updated: 2026-07-14 07:49 Africa/Cairo_

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
- Cross-backend teardown comparison matrix and reusable teardown audit method.
- Pinned OpenCL build composition and initial `cl_mem` ownership map.
- Line-aware generated source indexing with pinned file and symbol links.
- Guided end-to-end inference atlas with clickable reading paths.
- Bounded CPU repack, AMX, KleidiAI, and SpacemiT IME extra-buffer lifetime audits.
- Cross-implementation CPU optional-buffer comparison and portable destruction-test matrix.

## Latest concrete findings

- Repack and KleidiAI retain ordinary CPU allocation/free ownership while installing alternate packed layouts and static dispatch traits.
- AMX owns a dedicated aligned allocation through the buffer context; SpacemiT owns a dedicated Spine pool allocation through the buffer context.
- All four audited paths store process-static traits in `tensor->extra`, execute synchronously through CPU graph computation, and introduce no scheduler event or independent accelerator queue.
- Therefore the audited weight-buffer free paths do not require `ggml_backend_cpu_context`.
- Complete implementation shutdown remains path-specific: AMX retains allocator/tile-permission questions, while SpacemiT retains worker-local TCM and process-pool shutdown obligations.
- A portable test matrix now covers normal free, backend-free-before-buffer-free, unsupported transfer callbacks, threaded initialization, sanitizers, and memory-expansion measurement.

## In progress

- Regeneration of the pinned source inventory with line-aware records and pinned source links.
- Exact OpenCL backend/context teardown, queue completion, scheduler events/buffers, and program/kernel/context release order.
- CPU extra-buffer destruction regression tests under ASan/LSan/TSan and SpacemiT TCM/threadpool teardown tests on supported hardware.
- Shared generated metadata for the static inference atlas and interactive workflow.
- Runtime overlays for page faults, scheduler copies, event waits, KV/recurrent growth, and backend queues.
- CANN reset semantics, RPC completion, CUDA all-stream coverage, SYCL all-queue coverage, and Vulkan query-pool ownership.

## Immediate next task

Finish the OpenCL teardown audit when the complete pinned source is searchable. Otherwise implement the first portable CPU optional-buffer regression increment from the comparison matrix:

```text
create CPU backend
→ obtain admitted optional buffer type
→ allocate/populate supported tensor
→ run one supported operation
→ free CPU backend wrapper
→ free tensor metadata and buffer
→ repeat under ASan/LSan
```

## Publication and verification state

- Work is published in PR #1 from branch `automation/backend-teardown-audit-method`; current checked head before this state-only commit was `b47a582d69bc931abad752e23e0a712bf445ed14`, and the PR was open and mergeable.
- Added `docs/architecture/cpu-extra-buffer-comparison.md` and linked it after the four implementation-specific CPU pages.
- Added detailed note `logs/research/2026-07-14/0749-cpu-extra-buffer-comparison.md`.
- Updated README TODOs, project state, and research log; the research ledger is unchanged because no external source changed.
- Repository read-back confirmed the comparison table, ownership diagram, truth labels, portable destruction-test matrix, and detailed-audit links.
- A local clone attempt failed with `Could not resolve host: github.com`, so checkout-based Python tests, strict MkDocs build, and `check_site.sh` could not run.
- Documentation CI run `29307248750` completed with failure. The failing job was `build`, specifically step `Validate project context, interactive links, and scripts`; dependency installation and strict MkDocs build were skipped.
- The connector-decoded job log was truncated before the validator/test stderr, so the exact assertion could not be identified safely and no speculative patch was applied.
- Public search returned no indexed result for the site or new route. Direct opening of the Pages root and `architecture/cpu-extra-buffer-comparison/` was rejected by the web safe-URL gate; the new route is also branch-only until PR #1 merges.

## Known blockers and caveats

- **Pinned regeneration blocker:** no usable local pinned llama.cpp checkout is available, so the source index could not be regenerated here.
- **Large upstream file blocker:** the connector exposes the pinned OpenCL blob as truncated output and exact hidden symbols remain difficult to search.
- **Local validation blocker:** cloning failed with `Could not resolve host: github.com`; Python tests, strict MkDocs build, and `check_site.sh` require a usable checkout.
- **Current CI failure:** Documentation CI run `29307248750` failed at `Validate project context, interactive links, and scripts`; the decoded log was truncated before the exact error, and later dependency/build steps were skipped.
- **Pages verification blocker:** public search returned no indexed result and direct URL access was rejected by the safe-URL gate; the comparison page cannot deploy until PR #1 merges.
- **SpacemiT caveat:** buffer lifetime is distinct from thread-local TCM leases and process-level pool-manager lifetime.
- **Scope caveat:** optional CPU extra-buffer audits do not prove behavior for HBM or future implementations.
- Mapping, allocation, residency, validity, command completion, ownership, reset, thread-local leases, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, memory, and teardown ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
