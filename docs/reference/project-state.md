# Project state

_Last updated: 2026-07-13 20:51 Africa/Cairo_

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
- Revision-pinned file and symbol URLs derived from the exact indexed llama.cpp revision.

## Latest concrete findings

- `scripts/index_upstream.py` accepts `--source-url-base` and stores its normalized value in the generated summary.
- Indexed files receive `source_url`; symbol-location records receive pinned URLs ending in `#L<line>`.
- `scripts/update_upstream.sh` derives the blob prefix from `LLAMA_CPP_REV`, preventing silent source-link drift.
- Link enrichment copies records rather than mutating the extraction result.
- Tests cover URL normalization, absent-base behavior, line fragments, and non-mutation.
- The index remains regex based and therefore does not resolve preprocessing, dispatch, templates, or complete C++ semantics.

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

Regenerate the source inventory from the pinned checkout and use the new direct line links to finish the OpenCL teardown audit:

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

- Source-link implementation commit: `9ae07a9871474f3bc74043a8b1181940c4909a75`.
- Regression-test commit: `08bfff550c12aa9858a962949855bd85a5a2a011`.
- Pinned update-script commit: `ea6ef28a59b9fde358bcd7b7e45e2a5db1ba068c`.
- Source-index documentation commit: `1e52fb4030f05586e185d48d5089added45c6556`.
- Detailed note commit: `0d89af07dde6315a00bc2f69f0a6554ad808c097`.
- Research-log commit: `219118453b5d1c6201bfa37790ea1071c3791159`.
- Connector-side inspection verified the implementation, invocation, test cases, and documentation.
- Local clone of pinned llama.cpp still fails with `Could not resolve host: github.com`; source regeneration and full local project validation could not run.
- GitHub Actions and Pages verification for the final commit are pending the checks below.

## Known blockers and caveats

- **Pinned regeneration blocker:** the execution environment cannot resolve `github.com`, so the new index cannot be run against the pinned checkout here.
- **Large upstream file blocker:** the GitHub connector could not return the oversized pinned `ggml-opencl.cpp`, so the OpenCL teardown audit could not be completed honestly in this run.
- **Local validation blocker:** Python tests, strict MkDocs, and `check_site.sh` require a usable checkout and could not be run here.
- **CI visibility blocker:** inspect the final commit's workflow runs and statuses; record an empty result as unverified rather than failed.
- **Pages verification blocker:** verify the root and `reference/source-index/` route when direct live access is available.
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
