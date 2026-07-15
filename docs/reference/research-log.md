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
- Published model/context, generic scheduler, CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and initial OpenCL teardown audits.

**Interpretation**

- The loader is a transactional publisher, `llama_context` is a mutable session around a borrowed model, and the scheduler is an execution planner.
- Backend-before-scheduler safety depends on resource-deleter independence and queued-work completion.

## 2026-07-13 19:51–21:49 — Source navigation and teardown comparison

**Verified**

- `scripts/index_upstream.py` emits source-ordered `symbol_locations` with approximate kind, exact 1-based lines, and revision-pinned links.
- Added a pinned teardown matrix for CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL.

## 2026-07-14 01:52–08:49 — Inference atlas and CPU optional buffers

**Verified**

- Added a clickable inference pipeline and reusable ten-step teardown worksheet.
- Audited CPU repack, AMX, KleidiAI, and SpacemiT IME extra-buffer ownership and synchronous execution.
- Added a cross-implementation comparison, portable destruction-test matrix, and implementation-ready admitted `MUL_MAT` fixture.

## 2026-07-14 09:49–12:50 — CI observability and source-line repair

**Verified**

- Split Documentation CI into named validators and isolated unit suites before full discovery.
- Replaced newline-crossing whitespace matches that shifted type/function records to preceding lines.
- Added regression coverage and passed complete CI.

## 2026-07-14 13:51–23:51 — Bounded C++ syntax and telemetry

**Verified**

- Added exact-line support for same-line attributes, trailing returns, bounded `requires`, qualified operators, constructors/destructors, parenthesized initializer lists, and delegating constructors.
- Added negative tests and telemetry for braced/multiline initializers and constructor function-try-blocks.

**Interpretation**

- These are bounded navigation features, not claims to parse full C++ grammar.

## 2026-07-15 02:51–05:51 — OpenCL lifecycle extraction and evidence workflow

**Verified**

- Added an exact-line extractor for selected OpenCL ownership, completion, wait, and release calls.
- Masked comments and quoted literals while preserving offsets and lines.
- Added bounded source context, focused tests, and a GitHub-hosted exact-pinned-source report artifact.
- Full discovery exposed and fixed a `try : member(...) {` false ordinary-function record.

**Interpretation**

- The extractor is a review inventory, not proof of ownership or safe release ordering.

## 2026-07-15 06:49–09:10 — Complete OpenCL ownership classification

**Verified**

- The complete report contained 558 selected direct calls after adding context/queue creation and retention APIs.
- Shared `free()` calls `clFinish(queue)` before final-reference pooled-view cleanup.
- One `clCreateContext()` creates `shared_context`; one `clCreateCommandQueue()` creates `backend_ctx->queue`; no direct retain or release exists for either handle.
- Static device contexts and lazily allocated per-device backend contexts live for the process.
- OpenCL backend scheduler events are unsupported; buffer deleters use buffer-local `cl_mem` handles.

**Interpretation**

- Backend-wrapper destruction is structurally supported, while deterministic process-exit release is omitted.

## 2026-07-15 09:51 — Adreno binary-library lifetime

**Verified**

- `ggml_cl_init()` loads the optional library into a block-local raw handle, retains only the exported lookup function, and never closes the handle.
- Successful and invalid-symbol loads both remain mapped until process teardown.

**Interpretation**

- The library is process-lifetime by leaked raw handle; close ordering is absent rather than prematurely unsafe.

## 2026-07-15 10:50 — Portable artifact verification

**Verified**

- The OpenCL evidence manifest now uses artifact-root basenames, passes `sha256sum -c` before upload, and guards the exact two filenames.

## 2026-07-15 11:51–12:49 — Transpose retention and callers

**Verified**

- `transpose_2d()` enqueues a transpose and same-queue copy before dropping the temporary sub-buffer reference.
- OpenCL command retention makes the nonblocking reference drop locally safe.
- All 53 pinned typed-wrapper call sites use the default `blocking=true`; `blocking=false` has zero pinned callers.

**Interpretation**

- The nonblocking branch is dormant capability in the baseline.

## 2026-07-15 13:52–15:52 — Event lifetime, pairing, and fatal errors

**Verified**

- Both Q4_0 conversion branches wait before releasing temporary `data_device` but omit `clReleaseEvent(evt)`.
- Paired all 51 direct `clWaitForEvents()` sites: five waited events are released and 46 local command events are waited without release or transfer.
- Pinned `CL_CHECK` logs non-success, asserts, enters `ggml_abort()`, and unconditionally calls `abort()`.

**Interpretation**

- The event leak is systematic and primarily scales with tensor conversion/readback and repeated initialization, not decode tokens.
- Successful-path releases can be inserted after waits without designing recoverable-error cleanup for the pinned code.

## 2026-07-15 16:51 — Simple waited-event regression

**Verified**

- Added a bounded lexical diagnostic for literal `clWaitForEvents(1, &identifier)` calls.
- The pinned workflow guards 50 simple identifier waits: 4 released in scope and 46 unmatched.

**Interpretation**

- The heuristic is a reproducible bounded regression, not general C++ ownership analysis.

## 2026-07-15 17:52–18:51 — Blocking-read wait classification

**Verified**

- Of the 46 unmatched waits, 22 are immediately followed by same-queue `clEnqueueReadBuffer(..., CL_TRUE, ...)` calls.
- The pinned queue is in-order, and a blocking read supplies the required host-visible completion.
- Added a separate machine-readable follow-up annotation and CI guard for the 22/24 split.

**Interpretation**

- The 22 explicit waits are redundant for completion, but their event references still require release.
- Ownership repair and synchronization removal remain separate patches.

## 2026-07-15 19:52 — Generated release-only event patch

**Verified**

- Added `scripts/apply_opencl_event_release_fix.py`, which inserts releases after all 46 audited unmatched simple waits using exact lines and identifiers.
- The workflow proves 46 inserted releases, 51 waits preserved, 50 simple waits released in scope, zero unmatched, and 52 total direct event releases.
- The baseline report and independent 22/24 synchronization split remain preserved.

**Interpretation**

- The repository now has a concrete behavior-preserving ownership correction artifact.

## 2026-07-15 20:51 — Remaining `set_tensor` wait groups

**Verified**

- Added `scripts/classify_opencl_set_tensor_waits.py` and focused tests.
- All remaining 24 non-blocking-read waits are inside `ggml_backend_opencl_buffer_set_tensor()`.
- Twenty-one waits are immediately followed by `clReleaseMemObject(data_device)`; three end nested lexical scopes; zero fall into `other`.
- OpenCL command retention means the 21 waits are not needed merely to keep the temporary input object alive.

**Interpretation**

- The 21 waits were not yet proven removable because synchronous tensor-set output readiness remained unresolved.

## 2026-07-15 21:52 — Pinned `set_tensor` wait-group CI contract

**Verified**

- Integrated `scripts/classify_opencl_set_tensor_waits.py` and its tests into the pinned OpenCL workflow trigger set.
- The workflow generates and uploads `opencl-set-tensor-wait-groups-e3546c7.json`.
- CI asserts exactly 24 records, 21 `temporary_upload_buffer_release`, 3 `nested_scope_exit`, all in `ggml_backend_opencl_buffer_set_tensor()`, and zero `other` records.

**Interpretation**

- The reviewed 21/3 grouping is a pinned evidence contract. Source drift or classifier regression must fail visibly and trigger re-audit.

## 2026-07-15 22:49 — OpenCL return-boundary expansion waits

**Verified**

- The three `nested_scope_exit` records are Q5_0, Q8_0, and Q5_K MoE scale/min expansion kernels.
- Each wait occurs immediately before effective return from its tensor-type branch.

**Interpretation**

- They are return-boundary completion waits: redundant for later same-queue consumers but potentially required by synchronous tensor-set return semantics.

## 2026-07-15 23:49 — Cross-backend tensor-set completion contract

**Verified**

- The generic `ggml_backend_tensor_set()` wrapper directly dispatches to `buf->iface.set_tensor(...)` and performs no extra synchronization.
- Pinned CUDA enqueues the host-to-device copy and synchronizes `cudaStreamPerThread` before returning.
- Pinned SYCL waits device queues and waits the submitted copy before returning; its mmap staging buffer is freed only after completion.
- Pinned OpenCL waits its conversion and expansion kernels before returning from ordinary tensor set.

**Interpretation**

- CUDA, SYCL, and OpenCL establish a strong de facto synchronous tensor-set contract in the pinned baseline, although the public header does not state it normatively.
- All remaining 24 OpenCL conversion/expansion waits are required by that pinned return contract. The 21 temporary-input-release waits are not needed for `cl_mem` lifetime but still ensure the persistent converted representation is complete at return.
- The generated 46-event release patch remains the correct behavior-preserving first fix; synchronization should remain unchanged unless the API contract is deliberately weakened.

**Historical**

- This resolves the previous 21/3 contract-dependent classification for the pinned baseline.

**Open questions**

- Does current upstream retain the same implementations and leak?
- Should the synchronous completion behavior be documented explicitly in `ggml-backend.h`?
- Should the release-only patch be rebased and submitted upstream before any synchronization cleanup?
