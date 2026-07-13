# Project state

_Last updated: 2026-07-13 19:51 Africa/Cairo_

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
- Pinned OpenCL build composition, kernel deployment, official platform scope, and initial `cl_mem` RAII ownership map.
- Line-aware generated source indexing with untruncated symbol records, declaration kinds, 1-based lines, and regression tests.

## Latest concrete findings

- `scripts/index_upstream.py` now emits `symbol_locations` for each file while retaining the legacy compact `symbols` field.
- Symbol locations are source ordered and retain duplicate names, which preserves overload and conditional-branch navigation targets.
- Tests cover line calculation, ordering, scoped function names, and duplicate declarations.
- The index remains regex based and therefore does not resolve preprocessing, dispatch, templates, or complete C++ semantics.
- This removes the tooling blocker for locating teardown symbols inside very large translation units such as `ggml-opencl.cpp`.

## In progress

- Regeneration of the pinned source inventory with the new symbol-location schema.
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

Regenerate the source inventory from the pinned checkout and use `symbol_locations` to finish the OpenCL teardown audit:

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

- Script commit: `1f1a3bb1f8891448fc40c3899e264e0464ea7db2`.
- Test commit: `96750c555f81287516b5b69080f20dc8ca1a0855`.
- Source-index documentation commit: `06f4946f1b43eb9f258a66bb7a4e839a7523fdec`.
- README/TODO commit: `5d6505737c06e515a7cd1cb72f592a3f9630f930`.
- Detailed note commit: `ea6145c3940f0a4d25ffe3af4d5ce8eb19e563ce`.
- Research-log commit: `778635b940b0bcf866d9727eaf7fd8d065222b0f`.
- Connector-side inspection verified the implementation and test fixture structure.
- Local clone of pinned llama.cpp failed with `Could not resolve host: github.com`; source regeneration and local project validation could not run.
- GitHub Actions and Pages status for this increment are recorded below after final checks.

## Known blockers and caveats

- **Pinned regeneration blocker:** the execution environment cannot resolve `github.com`, so the new index could not be run against the pinned checkout in this run.
- **Local validation blocker:** Python tests, strict MkDocs, and `check_site.sh` require a usable checkout and could not be run here.
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
