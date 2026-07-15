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

## 2026-07-15 13:52 — Q4_0 conversion event lifetime

**Verified**

- Both Q4_0 conversion branches wait before releasing temporary `data_device` but omit `clReleaseEvent(evt)`.
- Each successful conversion therefore leaks one application-owned command-event reference.

**Interpretation**

- Classification: **explicit completion before temporary-buffer release; persistent event-reference leak**.

## 2026-07-15 14:52 — Complete waited-event pairing audit

**Verified**

- Paired all 51 direct `clWaitForEvents()` sites with producers and ownership paths.
- Five waited events are released; 46 local command events are waited without release or transfer.
- The unmatched events span eleven quantized tensor-type groups and conversion/upload/readback helpers.

**Interpretation**

- The event leak is systematic and primarily scales with tensor conversion/readback and repeated model/backend initialization, not decode tokens.

## 2026-07-15 15:52 — `CL_CHECK` fatal failure semantics

**Verified**

- Pinned `CL_CHECK` logs any non-success OpenCL result and executes `GGML_ASSERT(0)`.
- `GGML_ASSERT` maps to `GGML_ABORT`; pinned `ggml_abort()` invokes an optional callback or prints diagnostics and then unconditionally calls `abort()`.
- A checked enqueue, wait, release, or other OpenCL failure does not return, throw, or continue to later cleanup statements.

**Interpretation**

- The 46 observed successful-path leaks can be corrected by adding `clReleaseEvent(evt)` after each successful wait without designing recoverable-error cleanup for the pinned code.
- RAII remains useful for maintainability and future nonfatal error propagation, but it cannot unwind after the current `abort()` path.
- The safest patch sequence is release-only first, then separately remove waits proven redundant by a following same-queue blocking operation.

**Historical**

- The previous pairing audit treated RAII as potentially required because `CL_CHECK` behavior was unresolved. The pinned macro-to-abort chain narrows it to an optional design improvement.

**Open questions**

- Which of the 46 waits are required versus redundant before ordered blocking operations?
- Should upstream prefer 46 explicit releases or a small move-only event owner?
- Can a bounded source regression detect the known local wait-without-release pattern without claiming full ownership analysis?

## 2026-07-15 16:51 — Simple waited-event regression

**Verified**

- Added a bounded lexical diagnostic for literal `clWaitForEvents(1, &identifier)` calls.
- Each record reports exact wait and scope lines plus a same-scope release line or `unmatched_in_scope`.
- Focused tests cover same-scope release, nested-scope boundaries, unmatched waits, comments/literals, and unsupported non-simple waits.
- The pinned OpenCL workflow now guards the audited contract: 51 simple waits, 5 released in scope, and 46 unmatched.

**Interpretation**

- The manual pairing result is now a reproducible source-evidence regression suitable for validating a release-only patch.
- The heuristic remains intentionally narrower than C++ ownership analysis and does not model aliases, macros, helper releases, arrays, transfer, or control-flow reachability.

**Historical**

- The 5/46 result previously existed only as a detailed human audit; this increment makes it machine-readable and CI-enforced.

**Open questions**

- Which unmatched waits are redundant before a same-queue blocking operation?
- Should a patched upstream revision be required to reach zero `unmatched_in_scope` entries?
- Is a bounded next-blocking-command hint useful without conflating completion and ownership?
