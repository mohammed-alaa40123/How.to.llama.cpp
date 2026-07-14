# Project state

_Last updated: 2026-07-14 10:52 Africa/Cairo_

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
- Implementation-ready CPU optional-buffer destruction-harness specification with admission, correctness, lifetime-ordering, and sanitizer assertions.
- Documentation CI validation commands split into named steps with verbose unittest output.
- Python unit tests split into source-index and interactive-link suites, followed by a full discovery guard.

## Latest concrete findings

- Documentation CI run `29312885959` completed with failure in the aggregate Python unit-test step.
- Durable project-context validation and interactive-link validation both passed.
- Shell syntax, Python compilation, asset checks, dependency installation, and strict MkDocs building were skipped after the unit-test failure.
- The available decoded job log remained truncated before the failing unittest name and traceback.
- The workflow now executes `tests.test_index_upstream` and `tests.test_validate_interactive_links` as separate named steps, then runs full test discovery as a coverage guard.

## In progress

- Exact identification and repair of the isolated Documentation CI unit-test failure.
- Regeneration of the pinned source inventory with line-aware records and pinned source links.
- Exact OpenCL backend/context teardown, queue completion, scheduler events/buffers, and program/kernel/context release order.
- Implementation of the first CPU repack backend-free-before-buffer-free test fixture under ASan/LSan.
- CPU extra-buffer destruction tests for KleidiAI, AMX, and SpacemiT plus TSan and hardware-specific cleanup coverage.
- Shared generated metadata for the static inference atlas and interactive workflow.
- Runtime overlays for page faults, scheduler copies, event waits, KV/recurrent growth, and backend queues.
- CANN reset semantics, RPC completion, CUDA all-stream coverage, SYCL all-queue coverage, and Vulkan query-pool ownership.

## Immediate next task

Inspect the Documentation CI run created by the suite-isolation workflow and patch the exact failing test or implementation. Once the unit tests pass, continue through shell, compilation, asset, dependency, and strict MkDocs validation, then resume the portable CPU repack lifetime fixture:

```text
create CPU backend
→ select the admitted repack buffer type
→ allocate/populate a supported quantized weight tensor
→ run one deterministic supported MUL_MAT
→ compare against an ordinary CPU reference
→ free CPU backend wrapper
→ free graph/tensor metadata and repack buffer
→ repeat under ASan/LSan
```

## Publication and verification state

- Work is published in PR #1 from branch `automation/backend-teardown-audit-method`; the PR remains open and mergeable.
- Documentation CI run `29312885959` identified Python unit tests as the failing subsystem while both context validators passed.
- Updated `.github/workflows/docs-ci.yml` to isolate the two current test modules and retain full discovery coverage.
- Added detailed note `logs/research/2026-07-14/1052-unit-test-suite-isolation.md`.
- Local cloning again failed with `Could not resolve host: github.com`, so checkout-based test reproduction, strict MkDocs build, and `check_site.sh` remain unavailable.
- The public Pages route for branch-only artifacts cannot deploy until PR #1 merges; live verification remains pending.

## Known blockers and caveats

- **Current CI diagnosis:** the failing subsystem is Python unit tests, but the prior aggregate step and truncated log did not expose the exact module or traceback. The new suite-isolation run must complete before a precise fix can be applied.
- **Pinned regeneration blocker:** no usable local pinned llama.cpp checkout is available, so the source index could not be regenerated here.
- **Large upstream file blocker:** the connector exposes the pinned OpenCL blob as truncated output and exact hidden symbols remain difficult to search.
- **Local validation blocker:** cloning failed with `Could not resolve host: github.com`; Python tests, strict MkDocs build, and `check_site.sh` require a usable checkout.
- **Pages verification blocker:** branch-only documentation cannot deploy until PR #1 merges; live HTTP and rendered-content checks remain pending.
- **Harness caveat:** a skipped hardware-gated path is not evidence that the lifetime ordering passed.
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
