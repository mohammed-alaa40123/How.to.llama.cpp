# Research log

This is the concise chronological ledger. Detailed notes live under `logs/research/`.

## 2026-07-12 — Baseline, inference path, and core objects

**Verified**

- Baseline pinned to `e3546c7948e3af463d0b401e6421d5a4c2faf565`.
- Documented backend/model loading, tokenization, `llama_context`, decode, sampling, token feedback, GGUF, model placement, graph/MoE, scheduler, memory, and backends.
- GGUF stores tensors and metadata, not an executable graph; architecture code builds GGML operations over loaded tensors.

**Interpretation**

- Graph reuse preserves compatible topology/allocation, not token values or outputs.
- CPU addressability and logical cache state do not prove physical residency.

## 2026-07-13 — Subsystem synthesis and teardown audits

**Verified**

- Published file-by-file Pass A pages for public API, loader, context memory, scheduler, and persistent KV/recurrent implementations.
- Added model/context and generic scheduler plus CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL teardown audits.
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

- Added an exact-line OpenCL lifecycle extractor with masking, bounded context, focused tests, and a pinned-source artifact workflow.
- Verified process-lifetime queue/context state, unsupported scheduler events, buffer-local deleters, and Adreno binary-library lifetime.
- Audited 51 direct waits: five waited events are released and 46 local command-event references are not.
- Classified 22 waits before same-queue blocking reads and 24 synchronous set-tensor waits.
- Established a pinned de facto synchronous tensor-set completion contract across generic, CUDA, SYCL, and OpenCL behavior.

**Interpretation**

- Event ownership repair and synchronization cleanup are separate changes; the first behavior-preserving fix retains every wait and releases all 46 event references.

## 2026-07-16 00:52–03:49 — Current-upstream OpenCL re-audit and proposal

**Verified**

- Audited exact revision `505b1ed15ca80e2a19f12ff4ac365e40fb374053` with a current-upstream workflow.
- Current upstream retained 51 direct waits, 46 unmatched simple event references, and the 22/24 split.
- The generated current-source patch inserted 46 releases and reached zero unmatched records without removing synchronization.
- Reviewed all insertions and staged an upstream-ready issue/PR proposal.

**Open question**

- Direct upstream submission is blocked by connected GitHub App permission.

## 2026-07-16 04:52–12:50 — CPU_REPACK fixture and upstream proposal

**Verified**

- Selected a dedicated `tests/test-cpu-extra-buffer-lifetime.cpp` executable and the smallest admitted pinned x86 case: Q4_0 `[32, 8] × F32 [32, 1]`.
- Added deterministic generation, two no-allocation graphs, exact CPU_REPACK allocation/path proof, shared quantized inputs, compute/readback, `1e-7` NMSE, and backend-before-buffer teardown.
- Added an AVX2-required ASan/LSan workflow requiring twenty non-skipped process executions.
- Workflow `29481384561` passed all twenty processes with stable NMSE `3.82787e-16`; artifact `8368782428` has digest `sha256:ef4f0a36e27f7811b106e0a870c278724f1e620aed991807b7f2c3e443d1efaf`.
- Reviewed current upstream `8ee54c8b32a1b0cf13c03fc5723142bc62c775f6` and staged a narrow two-file upstream proposal.

**Interpretation**

- Correct output alone does not prove CPU_REPACK ran; pointer identity, selected traits, and admission checks are required.
- The bounded admitted case supports backend-wrapper-before-buffer teardown, not every packed layout, architecture, or concurrent use.

## 2026-07-16 13:16–15:51 — Website information architecture and static accessibility

**Verified**

- Grouped 27 Architecture pages into task-oriented navigation categories and added an Architecture overview with six goal-based entry points and audience reading paths.
- Added `scripts/validate_built_site_accessibility.py` for generated HTML language, main, H1, image-alt, iframe-title, and button-name checks.
- Documentation CI run `29496291134` passed the strict MkDocs build and accessibility validator without exceptions.
- PR #1 merged to `main` at `f33d16945433581e484c3b1112dc36c9f807861c`.

**Interpretation**

- Static structure validation is a regression guard, not full accessibility conformance.

## 2026-07-16 16:51 — Representative browser smoke lane

**Verified**

- Added Playwright/Chromium validation for the homepage, Architecture index, a diagram-heavy page, and an interactive page at desktop and mobile widths.
- Checks cover HTTP success, landmarks/headings, search, overflow, reduced motion, keyboard focus, Architecture links, iframe titles, Mermaid rendering, and browser errors.
- Failure screenshots, server logs, and per-case JSONL diagnostics are retained.

## 2026-07-16 17:52–18:52 — Browser diagnostic attribution corrections

**Verified**

- Runs `29504440262` and `29509089935` passed every pre-browser stage and failed only on the first Chromium case.
- Evidence showed successful local resources and no same-origin HTTP failure.
- The validator now classifies console/request records as same-origin, cross-origin, or unlocated.
- Same-origin failures and all functional assertions remain fatal; cross-origin and unlocated records are retained warnings.

**Interpretation**

- Missing or external source attribution is not evidence of a local-site error; visible functionality must be checked directly.

## 2026-07-16 19:50 — Mermaid readiness race

**Verified**

- Documentation CI run `29513543532` passed all pre-browser stages and failed at `home/desktop` with `rendered 0 of 1 Mermaid diagrams`.
- The browser step failed about 2.6 seconds after starting, before bounded application-level render readiness was established.
- Artifact `8381667636` has digest `sha256:08294cbc09e5699e261abafd6c4b5e3153a2fadf2b4b6586303ec413e1cdbf81`.
- The validator now waits up to 15 seconds for every `main .mermaid` container to contain an SVG, then enforces exact rendered/count equality.
- The timeout is configurable through `MERMAID_RENDER_TIMEOUT_MS`; timeout remains a hard failure.
- The complete four-route by two-viewport matrix and every non-Mermaid assertion remain unchanged.

**Interpretation**

- `networkidle` proves network quiet, not completion of asynchronous Mermaid DOM rendering.
- Waiting for the exact SVG postcondition is stronger than an arbitrary sleep and distinguishes delayed readiness from a true bounded render failure.

**Historical**

- The two prior failures removed unsupported console-origin assumptions; the third exposed the first genuine functional readiness race.

**Open questions**

- Whether all eight route/viewport cases now pass.
- Whether recurring CDN delay/failure justifies vendoring Mermaid locally.
- Which retained warnings recur after the matrix advances beyond the first case.
