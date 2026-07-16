# Project state

_Last updated: 2026-07-16 10:50 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream OpenCL revision audited: `505b1ed15ca80e2a19f12ff4ac365e40fb374053`
- Policy: baseline claims stay pinned; newer refs are documented separately and labelled.

## Active milestone

**Foundations deepening — executable lifetime regressions for optional CPU buffers**

## Completed foundations

- Canonical GGUF, model placement, `llama_model`, `llama_context`, graph/MoE, scheduler, memory-lifetime, backend, and inference-atlas pages.
- Source indexing, strict documentation CI, Pages deployment workflow, health checks, and durable run context.
- Generic scheduler plus CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL teardown audits.
- CPU repack, AMX, KleidiAI, and SpacemiT extra-buffer ownership comparison and destruction-harness specification.
- Complete pinned/current OpenCL event-ownership audit, generated 46-release correction, synchronous tensor-set contract analysis, and upstream proposal staging.

## Latest concrete findings

### Verified

- Added `.github/workflows/cpu-repack-lifetime-sanitizer.yml` as the first exact-revision compiler and sanitizer path for the generated CPU_REPACK fixture.
- The workflow verifies the pinned llama.cpp SHA before materializing the generated C++ source and CMake target.
- The hosted runner must expose AVX2; lack of AVX2 is a hard failure, not successful skipped evidence.
- The target is configured with AddressSanitizer, LeakSanitizer leak detection, and frame pointers, then compiled independently.
- The fixture must run in twenty separate processes, emit twenty exact CPU_REPACK success markers, and never emit `SKIP:`.
- CPU capability, generated fixture source, and sanitizer output are uploaded as retained evidence.
- The first workflow appeared as run `29481384561` and was queued at the initial status check.

### Interpretation

- The CI implementation boundary is now closed, but runtime lifetime proof still requires a passing first run.
- Separate process invocations exercise initialization and process teardown repeatedly and avoid hiding process-static lifetime behavior inside one test process.
- The first run should be treated as compiler/runtime discovery evidence; any pinned API or allocation mismatch must be corrected rather than worked around with a skip.

### Historical

- Prior runs selected and generated the complete two-graph Q4_0 `[32, 8]` × F32 `[32, 1]` fixture with identical inputs, `1e-7` NMSE, exact path proof, and backend-wrapper-before-buffer teardown.
- This run moves that candidate into an exact pinned-tree AVX2-confirmed ASan/LSan workflow.

### Open questions

- Whether the generated source compiles unchanged against the pinned revision.
- Whether `ubuntu-latest` consistently exposes AVX2.
- Whether the graph allocator preserves the externally allocated repack weight at runtime.
- Whether LSan reports process-static CPU dispatch allocations that require narrow documentation rather than broad suppression.

## Immediate next task

```text
inspect first CPU_REPACK sanitizer run
  → fetch failed job logs if compilation or execution fails
  → correct exact pinned API/CMake/runtime issues
  → rerun until AVX2-confirmed twenty-process ASan/LSan evidence passes
  → preserve artifact identity and concrete NMSE results
  → update the destruction-harness page with executable evidence
```

## In progress

- First pinned-tree compile and sanitizer CI run for the CPU repack lifetime fixture.
- Manual/upstream submission of the reviewed 46-release OpenCL ownership correction; GitHub App write access to upstream is blocked.
- Source-index regeneration with pinned line-aware symbol inventory.
- Hardware-specific lifetime extensions for KleidiAI, AMX, and SpacemiT.
- Runtime overlays for mmap/page faults, scheduler copies, events, KV/recurrent growth, and backend queues.

## Publication and validation state

- Work is published in PR #1 from branch `automation/backend-teardown-audit-method`.
- Added workflow `.github/workflows/cpu-repack-lifetime-sanitizer.yml`.
- Added detailed note `logs/research/2026-07-16/1050-cpu-repack-pinned-sanitizer-workflow.md`.
- Updated README living TODOs, this project checkpoint, and the concise research log.
- Research ledger unchanged: this increment used the already-recorded pinned llama.cpp primary source.
- First CPU_REPACK workflow run: `29481384561`, queued at initial verification.
- Final-head workflow results must be checked after all context commits.

## Known blockers and caveats

- **Runtime proof:** no passing sanitizer execution exists until run `29481384561` or a corrected successor completes.
- **Hardware gate:** the new workflow intentionally fails when AVX2 is unavailable; a skip is not lifetime evidence.
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
