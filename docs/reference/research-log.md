# Research log

This is the concise chronological ledger. Detailed notes live under `logs/research/`.

## 2026-07-12 — Baseline, inference path, and core objects

**Verified**

- Baseline pinned to `e3546c7948e3af463d0b401e6421d5a4c2faf565`.
- Documented the path from backend/model loading through tokenization, `llama_context`, decode, sampling, and token feedback.
- Published canonical GGUF, model placement, `llama_model`, `llama_context`, graph/MoE, scheduler, memory, and backend pages.
- GGUF stores tensors and metadata, not an executable graph; architecture code builds GGML operations over loaded tensors.

**Interpretation**

- Graph reuse preserves compatible topology/allocation, not token values or outputs.
- CPU addressability and logical cache state do not prove physical residency.

## 2026-07-13 — Subsystem synthesis and teardown audits

**Verified**

- Published file-by-file Pass A pages for public API, loader, context memory, scheduler, and persistent KV/recurrent implementations.
- Added model/context, generic scheduler, CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL teardown audits.
- Added line-aware source indexing with pinned file and symbol links.

**Interpretation**

- Backend-before-scheduler safety depends on queued-work completion and resource-deleter independence.

## 2026-07-14 — Inference atlas, CPU optional buffers, and CI observability

**Verified**

- Added a clickable inference atlas and reusable teardown worksheet.
- Audited CPU repack, AMX, KleidiAI, and SpacemiT optional-buffer lifetimes.
- Added the CPU optional-buffer destruction-harness specification.
- Split Documentation CI into named validators and expanded bounded C++ source-index tests.

## 2026-07-15 — OpenCL lifecycle evidence and ownership

**Verified**

- Added an exact-line OpenCL lifecycle extractor with comment/string masking, bounded context, focused tests, and a pinned-source artifact workflow.
- Verified process-lifetime queue/context state, unsupported scheduler events, buffer-local deleters, and Adreno binary-library lifetime.
- Audited all 51 direct waits: five waited events are released and 46 local command-event references are not.
- Added machine-readable wait/release, blocking-read follow-up, set-tensor grouping, and release-only patch validation.
- Classified 22 waits before same-queue blocking reads and 24 synchronous set-tensor waits.
- Compared generic, CUDA, SYCL, and OpenCL tensor-set behavior and established a pinned de facto synchronous completion contract.

**Interpretation**

- Event ownership repair and synchronization cleanup are separate changes.
- The behavior-preserving first fix retains every wait and releases all 46 event references.

## 2026-07-16 00:52–03:49 — Current-upstream OpenCL re-audit and proposal

**Verified**

- Added a current-upstream lifecycle workflow and audited exact revision `505b1ed15ca80e2a19f12ff4ac365e40fb374053`.
- Current upstream retains the same 51 direct waits, 46 unmatched simple event references, and 22/24 split.
- The generated current-source patch inserts 46 releases and reaches zero unmatched records without removing synchronization.
- Reviewed all insertions and staged an upstream-ready issue/PR proposal.

**Open question**

- Direct upstream submission is blocked by connected GitHub App permission.

## 2026-07-16 04:52 — CPU repack fixture integration point

**Verified**

- Existing `test-backend-ops.cpp` already provides quantization, upload, graph execution, readback, dequantization, and numerical comparison patterns.
- The CPU extra-dispatch path is distinct from ordinary CPU fallback and must be proven through exact buffer identity and operation admission.
- Selected `tests/test-cpu-extra-buffer-lifetime.cpp` as a dedicated executable so unusual teardown ordering does not affect the general backend-op runner.

**Interpretation**

- Reuse backend-op helpers, but isolate backend-wrapper-before-buffer destruction and sanitizer repetition in a focused target.

## 2026-07-16 05:51 — Minimal admitted CPU repack case

**Verified**

- Pinned CPU CMake always includes `ggml-cpu/repack.cpp`; runtime feature/layout admission controls use.
- Pinned Q4_0 AVX2 traits require `weight->ne[1] % 8 == 0`.
- The smallest bounded x86 case is Q4_0 weight `[32, 8]` × F32 activation `[32, 1]` → F32 `[8, 1]`.
- Admission requires a two-dimensional weight allocated from the exact repack buffer type, non-null repack traits, host activation storage, and F32 activation type.
- The fixture must assert buffer pointer identity, non-null `tensor->extra`, and `ggml_backend_supports_op()` before compute.

**Interpretation**

- This case is the smallest pinned x86 fixture that exercises repack initialization, upload, optional dispatch, correctness, synchronous completion, and backend-wrapper-before-buffer teardown.
- Diagnostic name matching is insufficient; pointer identity and trait admission are the path proof.
- A non-AVX2 skip is not lifetime evidence, so sanitizer CI needs an AVX2-confirmed runner.

**Historical**

- The prior run resolved the integration point; this run resolves the exact type and dimensions.

**Open questions**

- Whether hosted-runner AVX2 is a guaranteed contract.
- Whether to extract shared test helpers or duplicate a bounded subset.
- Which existing Q4_0 tolerance should be reused.
- Whether ARM NEON+dotprod should be the immediate second fixture.
