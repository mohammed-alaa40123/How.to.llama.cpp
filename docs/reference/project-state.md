# Project state

_Last updated: 2026-07-16 09:51 Africa/Cairo_

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

- The deterministic CPU_REPACK generator now emits a complete two-graph candidate test instead of returning status 2.
- The generated reference and tested graphs use the same Q4_0 `[32, 8]` weight bytes and F32 `[32, 1]` activation values.
- Only the tested weight is explicitly allocated from `ggml_backend_cpu_repack_buffer_type()`; activation and output are allocated through an ordinary CPU graph allocator.
- The candidate asserts exact repack buffer identity, non-null repack traits, and `ggml_backend_supports_op()` before execution.
- Both graphs are computed, outputs are read back, and normalized mean squared error must be `<= 1e-7`.
- The tested CPU backend wrapper is freed before the retained repack buffer.
- Seven focused Python tests passed and now forbid the former `INCOMPLETE`/`return 2` boundary.

### Interpretation

- The generator-level implementation gap is closed, but this is not runtime lifetime proof until the candidate compiles and runs against the pinned llama.cpp tree.
- Exact path proof remains necessary because numerically correct output alone could come from ordinary CPU fallback.
- The next authoritative evidence must combine compiler validation, AVX2 confirmation, successful CPU_REPACK admission, repeated execution, and ASan/LSan.

### Historical

- Prior runs selected the dedicated executable, minimal Q4_0 `[32, 8]` × F32 `[32, 1]` AVX2 case, two-graph topology, identical quantized inputs, `1e-7` NMSE contract, and address-based per-tensor allocation API.
- This run combines those decisions into a complete generated C++ body.

### Open questions

- Whether the exact pinned compiler accepts every generated API spelling and graph-overhead sizing choice.
- Whether the graph allocator preserves the externally allocated repack weight exactly as expected at runtime.
- Whether GitHub-hosted Ubuntu exposes AVX2 consistently enough for authoritative sanitizer coverage.
- Whether repetition should occur inside the test executable or through repeated CTest invocations.

## Immediate next task

```text
materialize generated patch in pinned llama.cpp tree
  → compile dedicated test target
  → correct any pinned-API mismatch
  → prove AVX2 and CPU_REPACK admission
  → execute repeatedly under ASan/LSan
  → fail on skip when AVX2 is present
  → preserve backend-wrapper-before-buffer teardown
```

## In progress

- Pinned-tree compilation and sanitizer CI for the first CPU repack lifetime fixture.
- Manual/upstream submission of the reviewed 46-release OpenCL ownership correction; GitHub App write access to upstream is blocked.
- Source-index regeneration with pinned line-aware symbol inventory.
- Hardware-specific lifetime extensions for KleidiAI, AMX, and SpacemiT.
- Runtime overlays for mmap/page faults, scheduler copies, events, KV/recurrent growth, and backend queues.

## Publication and validation state

- Work is published in PR #1 from branch `automation/backend-teardown-audit-method`.
- Added detailed note `logs/research/2026-07-16/0951-cpu-repack-complete-generated-fixture.md`.
- Updated the generator, focused tests, README living TODOs, this project checkpoint, and the concise research log.
- Research ledger unchanged: this increment used the already-recorded pinned llama.cpp primary source.
- Final-head workflow results must be checked after all context commits.

## Known blockers and caveats

- **Runtime proof:** the complete generated source has not yet been compiled or executed against the pinned tree.
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
