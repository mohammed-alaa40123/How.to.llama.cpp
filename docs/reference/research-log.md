# Research log

This is the concise chronological ledger. Detailed notes live under `logs/research/`.

## 2026-07-12 — Baseline, decode, scheduler, and backends

**Verified**

- Baseline pinned to `e3546c7948e3af463d0b401e6421d5a4c2faf565`.
- The minimal path loads backends/model, tokenizes, creates a context, decodes, samples, and feeds the next token back.
- Decode delegates to `llama_context::decode()`; graph reuse requires specialized compatibility checks.
- Scheduler allocation assigns backends, creates splits and copy-ring destinations, and execution uses events plus synchronized fallback copies.
- CPU, CUDA, Metal, Vulkan, and SYCL execution/buffer/copy semantics are documented.

**Interpretation**

- Reuse preserves compatible topology/allocation, not token values or outputs.
- CPU-mapped addressability does not prove physical residency.

## 2026-07-12 — Documentation architecture and core objects

**Verified**

- Added the documentation-quality roadmap and foundations explorer.
- Published canonical `llama_context` and `llama_model` pages.
- The context stores a non-owning model reference while owning mutable runtime state, scheduler resources, outputs, and memory modules.
- `llama_model` owns architecture/vocabulary state, persistent tensors, buffers, retained mappings, and architecture-specific graph dispatch.

## 2026-07-12 — GGUF, placement, graphs, MoE, and memory

**Verified**

- Published canonical GGUF anatomy, tensor-placement, graph/MoE, and memory-lifetime chapters.
- GGUF stores tensors and metadata, not an executable graph; architecture code rebuilds GGML operations over loaded tensors.
- Population paths include mapped alias, mapped copy/upload, direct read, asynchronous staging, and synchronous fallback.
- Mapping, allocation, residency, validity, command completion, and ownership are distinct states.

**Interpretation**

- `weights_map` joins physical GGUF layout to backend-aware tensor construction.
- Cache-aware routing should generally bias selection scores before top-k when expert weights should remain based on original probabilities.

## 2026-07-13 — Pass A, subsystem synthesis, and teardown audits

**Verified**

- Published Pass A pages for public API/minimal example, model/GGUF loader, runtime context/memory, backend scheduler, and concrete context-memory implementations.
- Published the cross-subsystem ownership/execution map.
- The pinned tree contains ordinary KV, iSWA, DSA, DSV4, recurrent, hybrid, and hybrid-iSWA persistent memory implementations.
- Scheduler copy allocation, current-generation validity, and previous-consumer completion are separate states.
- Published model/context, generic scheduler, CPU, CUDA, Metal, Vulkan, SYCL, RPC, and CANN teardown audits.
- Published the pinned OpenCL build, kernel deployment, platform scope, and initial `cl_mem` ownership map.

**Interpretation**

- The loader is a transactional publisher, `llama_context` is a mutable session around a borrowed model, and the scheduler is an execution planner.
- Backend-before-scheduler safety depends on resource-deleter independence and queued-work completion.

## 2026-07-13 19:51–21:49 — Source navigation and teardown comparison

**Verified**

- `scripts/index_upstream.py` emits source-ordered `symbol_locations` with approximate kind, exact 1-based lines, and revision-pinned links.
- Added a pinned teardown matrix for CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and the initial OpenCL gap.

## 2026-07-14 01:52–08:49 — Inference atlas and CPU optional buffers

**Verified**

- Added a clickable inference pipeline and reusable ten-step teardown worksheet.
- Audited CPU repack, AMX, KleidiAI, and SpacemiT IME extra-buffer ownership and synchronous execution.
- Added a cross-implementation comparison, portable destruction-test matrix, and implementation-ready admitted `MUL_MAT` fixture.

**Interpretation**

- A tiny deterministic graph is stronger than a full model for lifetime-ordering tests because admission, fallback placement, owners, and destruction order remain visible.

## 2026-07-14 09:49–12:50 — CI observability and source-line repair

**Verified**

- Split Documentation CI into named validators and isolated unit suites before full discovery.
- Replaced newline-crossing whitespace matches that shifted type/function records to preceding lines.
- Added regression coverage and passed complete CI.

## 2026-07-14 13:51–23:51 — Bounded C++ syntax and telemetry

**Verified**

- Added exact-line support for same-line attributes, trailing returns, bounded `requires`, qualified operators, constructors/destructors, parenthesized initializer lists, and delegating constructors.
- Added negative tests and per-file/aggregate telemetry for braced and multiline constructor initializers.
- Added constructor function-try-block telemetry while keeping those forms out of navigation.

**Interpretation**

- These are bounded navigation features, not claims to parse full C++ grammar.
- Measurable false-negative telemetry prioritizes scanner work without weakening link accuracy.

## 2026-07-15 02:51–04:49 — OpenCL lifecycle extraction

**Verified**

- Added an exact-line extractor for selected OpenCL completion, wait, release, creation, and retention calls.
- Masked comments and quoted literals while preserving offsets and lines.
- Added bounded original-source context and focused regression coverage.
- Full discovery exposed and fixed a `try : member(...) {` false ordinary-function record.

**Interpretation**

- The extractor is a review inventory, not proof of ownership or safe release ordering.

## 2026-07-15 05:51 — GitHub-hosted pinned OpenCL report generation

**Verified**

- Added `.github/workflows/opencl-lifecycle-report.yml` to fetch the exact pinned source, generate the report, validate it, and upload a 30-day artifact.
- This replaced the local DNS/source-recovery blocker with a repository-owned evidence path.

## 2026-07-15 06:49 — First complete OpenCL lifecycle classification

**Verified**

- The first complete report contained 556 selected calls: 343 memory releases, 121 program releases, 51 waits, 23 kernel releases, 11 finishes, 6 event releases, and 1 flush.
- Shared `free()` calls `clFinish(queue)` before final-reference pooled-view cleanup.
- Cross-device synchronization publishes marker events with `clFlush()`, then enqueues a dependent destination barrier.

**Interpretation**

- OpenCL teardown became conditional with verified local completion evidence; queue/context ownership was still unresolved.

## 2026-07-15 07:52 — Queue/context ownership-call inventory

**Verified**

- Expanded the report to 558 calls by adding direct context/queue creation and retention APIs.
- One `clCreateContext()` assigns to `shared_context`; one `clCreateCommandQueue()` assigns to `backend_ctx->queue`.
- No direct context/queue retain or release call appears.

**Open questions**

- Locate declarations and final ownership, verify scheduler-resource independence, classify retention-only release groups, and resolve Adreno library lifetime.

## 2026-07-15 08:50–09:10 — Source-bearing artifact and process-lifetime ownership

**Verified**

- Updated the report workflow to verify the exact checkout revision and preserve the complete pinned `ggml-opencl.cpp`, generated JSON report, and a SHA-256 manifest in one artifact.
- Workflow run `29392658206` succeeded; artifact `8333854723` expires on 2026-08-14.
- The downloaded source and report hashes matched the manifest.
- Device registration creates one `shared_context` and copies it into every supported device context.
- Device contexts are stored in static `g_ggml_backend_opencl_dev_ctxs`; the source explicitly states the devices and contexts live as long as the process.
- `ggml_cl_init()` lazily creates one `ggml_backend_opencl_context` per device, stores it in `dev_ctx->backend_ctx`, copies the shared context, and creates one queue.
- Backend wrappers increment `ref_count`; wrapper free calls `clFinish(queue)` and decrements it but does not delete the per-device context or release queue/context handles.
- On the final wrapper reference, pooled KV/dequant image and sub-buffer views are released.
- OpenCL backend events are unsupported and event callbacks are null; no scheduler-owned OpenCL event deleter outlives the wrapper.
- Buffer deleters own buffer-local `cl_mem` references and do not require the destroyed wrapper.

**Interpretation**

- Pinned OpenCL backend-wrapper destruction is structurally supported because work is completed and the real OpenCL owner persists in process-lifetime state.
- Deterministic process-exit cleanup is omitted: no explicit command-queue/context release or per-device backend-context deletion path exists in the pinned translation unit.
- The stronger classification is **backend-wrapper order supported; deterministic process-exit release omitted**.

**Historical**

- Earlier three-line report windows located creation but could not expose declaration or owner lifetimes. Preserving the exact source closed that gap.

**Open questions**

- Resolve optional Adreno dynamic-library handle and kernel-destruction ordering.
- Classify enqueue-then-release groups relying only on OpenCL object-retention semantics.
- Determine whether repeated registration or shared-library unload is supported.
- Fix the artifact checksum manifest to use basenames for direct `sha256sum -c` after download.
