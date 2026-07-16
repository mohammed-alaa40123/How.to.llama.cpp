# Project state

_Last updated: 2026-07-16 06:49 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream OpenCL revision audited: `505b1ed15ca80e2a19f12ff4ac365e40fb374053`
- Policy: baseline claims stay pinned; newer refs are documented separately and labelled.

## Active milestone

**Foundations deepening — source-backed lifetime regressions for optional CPU buffers**

## Completed foundations

- Canonical GGUF, model placement, `llama_model`, `llama_context`, graph/MoE, scheduler, memory-lifetime, backend, and inference-atlas pages.
- Source indexing, strict documentation CI, Pages deployment workflow, health checks, and durable run context.
- Generic scheduler plus CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL teardown audits.
- CPU repack, AMX, KleidiAI, and SpacemiT extra-buffer ownership comparison and destruction-harness specification.
- Complete pinned/current OpenCL event-ownership audit, generated 46-release correction, synchronous tensor-set contract analysis, and upstream proposal staging.

## Latest concrete findings

### Verified

- Added `scripts/generate_cpu_repack_lifetime_fixture.py`, which deterministically emits a revision-scoped candidate patch for the dedicated CPU_REPACK lifetime test and CMake target.
- The generated skeleton encodes Q4_0 `[32, 8]` × F32 `[32, 1]`, AVX2 gating, exact repack-buffer lookup, mandatory buffer/trait/admission proof, and backend-before-buffer teardown order.
- Added focused unit tests for deterministic output, pinned revision, minimal dimensions, CMake registration, path-proof tokens, teardown ordering, and false-success prevention.
- The generated skeleton intentionally exits with status 2 after setup; it cannot be reported as successful lifetime evidence before pinned-tree graph/allocation integration and sanitizer execution.
- Pinned `tests/CMakeLists.txt` uses `llama_build_and_test()` for test targets, and the repack buffer type is declared in internal `ggml/src/ggml-cpu/repack.h`.

### Interpretation

- The generator is a safe intermediate artifact: structural CI can freeze the intended fixture contract without pretending an uncompiled C++ skeleton proves lifetime correctness.
- A successful Python test run validates patch shape only. Runtime evidence still requires compiling against the pinned tree, proving actual CPU_REPACK admission, comparing numerical output, and running repeated ASan/LSan teardown.

### Historical

- The prior run selected the smallest admitted AVX2 case and resolved the dedicated integration point.
- This run materializes those decisions into deterministic candidate patch output.

### Open questions

- Which exact pinned no-allocation graph and buffer-allocation sequence best permits the repack buffer to outlive the tested backend wrapper?
- Which existing Q4_0 comparison tolerance should be reused verbatim?
- Whether GitHub-hosted Ubuntu exposes AVX2 consistently enough for authoritative sanitizer coverage.

## Immediate next task

```text
Complete the generated CPU_REPACK fixture
  → construct identical reference and repack no-alloc MUL_MAT graphs
  → allocate only the tested weight from CPU_REPACK
  → upload deterministic identical Q4_0/F32 inputs
  → assert buffer identity, non-null traits, and supports_op
  → compare F32 outputs with the pinned Q4_0 tolerance
  → free tested CPU backend wrapper before retained repack buffer
  → repeat under ASan/LSan
  → add an AVX2-confirmed CI invocation
```

## In progress

- First CPU repack lifetime fixture implementation and sanitizer CI.
- Manual/upstream submission of the reviewed 46-release OpenCL ownership correction; GitHub App write access to upstream is blocked.
- Source-index regeneration with pinned line-aware symbol inventory.
- Hardware-specific lifetime extensions for KleidiAI, AMX, and SpacemiT.
- Runtime overlays for mmap/page faults, scheduler copies, events, KV/recurrent growth, and backend queues.

## Publication and validation state

- Work is published in PR #1 from branch `automation/backend-teardown-audit-method`.
- Added generator `scripts/generate_cpu_repack_lifetime_fixture.py`, focused tests, and detailed note `logs/research/2026-07-16/0649-cpu-repack-fixture-generator.md`.
- Updated README living TODOs, this project checkpoint, and the concise research log.
- Research ledger unchanged: this increment used the already-recorded pinned llama.cpp primary source.
- Local pinned-tree C++ compilation remains unavailable; GitHub-hosted documentation CI validates the generator and Python tests only.
- Final-head workflow results must be checked after all context commits.

## Known blockers and caveats

- **Runtime proof:** the generated source is intentionally incomplete and exits nonzero until graph/allocation integration is implemented.
- **Hardware gate:** successful skip on a non-AVX2 runner does not validate repack lifetime ordering.
- **Path proof:** correct numerical output alone is insufficient because ordinary CPU fallback can produce the same answer.
- **Sanitizer scope:** process-static dispatch metadata should be documented separately, not hidden with broad leak suppression.
- **Upstream permission:** direct issue/PR creation in `ggml-org/llama.cpp` is blocked for the connected GitHub App.
- **Pages verification:** branch-added content cannot deploy until PR #1 merges; independent live response verification is still required.
- Mapping, allocation, residency, representation validity, command completion, event ownership, reset, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map and source-pinned end-to-end workflow.
- Deep GGUF/model-loading, model/context, graph, scheduler, memory, and teardown documentation.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays and executable lifetime regressions where source reasoning alone is insufficient.
