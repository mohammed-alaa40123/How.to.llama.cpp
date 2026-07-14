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

- Published Pass A pages for the public API/minimal example, model/GGUF loader, runtime context/memory, backend scheduler, and concrete context-memory implementations.
- Published the cross-subsystem ownership/execution map.
- The pinned tree contains ordinary KV, iSWA, DSA, DSV4, recurrent, hybrid, and hybrid-iSWA persistent memory implementations.
- Scheduler copy allocation, current-generation validity, and previous-consumer completion are separate states.
- Published model/context, generic scheduler, CPU, CUDA, Metal, Vulkan, SYCL, RPC, and CANN teardown audits.
- Published the pinned OpenCL build, kernel deployment, platform scope, and initial `cl_mem` ownership map.

**Interpretation**

- The loader is a transactional publisher, `llama_context` is a mutable session around a borrowed model, and the scheduler is an execution planner.
- Backend-before-scheduler safety depends on both resource-deleter independence and queued-work completion.
- OpenCL buffer-local RAII does not itself prove command completion before release.

## 2026-07-13 19:51–20:51 — Generated source navigation

**Verified**

- `scripts/index_upstream.py` emits untruncated, source-ordered `symbol_locations` with approximate declaration kind and 1-based line.
- Generated file and symbol records can carry revision-pinned GitHub URLs with `#L<line>` fragments derived from the selected revision.
- The legacy compact symbol list remains for compatibility and regression tests cover ordering and link generation.

**Open question**

- Regenerate the pinned inventory when upstream access is available and use it to finish OpenCL teardown.

## 2026-07-13 21:49 — Cross-backend teardown comparison

**Verified**

- Added a pinned comparison matrix covering ordinary CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and the OpenCL gap.
- The matrix separates execution completion from scheduler-resource independence and links each classification to its detailed audit.

## 2026-07-14 01:52–02:49 — Inference atlas and teardown method

**Verified**

- Added a clickable inference pipeline linking GGUF, model loading, `llama_model`, `llama_context`, graph construction, scheduler execution, backends, sampling, and decode reuse.
- Added a reusable ten-step teardown worksheet separating host-visible completion from scheduler-resource deleter independence.
- Standardized bounded classifications and a minimum asynchronous-destruction runtime matrix.

## 2026-07-14 03:51–06:50 — CPU optional extra-buffer audits

**Verified**

- CPU repack delegates allocation/free to ordinary CPU buffers and uses process-static traits.
- AMX owns a dedicated aligned host allocation and complete buffer interface.
- KleidiAI retains ordinary CPU allocation/free ownership while publishing process-static feature/kernel state and packed slots.
- SpacemiT owns pooled weight allocations and uses process-static IME/RVV traits while adding worker-local TCM coordination.
- All four execute synchronously through ordinary CPU graph computation and do not introduce scheduler events or accelerator queues.

**Interpretation**

- Weight-buffer destruction is independent of `ggml_backend_cpu_context` for all four audited paths, while AMX and SpacemiT retain platform- or process-level cleanup questions.

**Historical**

- Admission rules, callback tables, packed layouts, allocator APIs, and worker hooks are revision-sensitive.

**Open questions**

- Validate AMX allocator pairing, KleidiAI initialization/readback behavior, SpacemiT TCM/process-pool shutdown, and sanitizer ordering tests.

## 2026-07-14 07:49–08:49 — CPU comparison and destruction harness

**Verified**

- Added one ownership/completion comparison for repack, AMX, KleidiAI, and SpacemiT IME.
- Added a portable destruction-test matrix and an implementation-ready tiny admitted `MUL_MAT` fixture specification.
- The fixture separates admission, output correctness, synchronous completion, backend-free-before-buffer-free ordering, and sanitizer-clean final destruction.
- CPU repack is the first portable target; hardware-gated skips are not evidence that a lifetime claim passed.

**Interpretation**

- A tiny deterministic graph is stronger than a full model for this ownership question because fallback placement, allocation owners, and destruction order remain visible.

**Open questions**

- Select the smallest stable upstream helper, define LSan treatment for intentional static metadata, and add explicit SpacemiT pool shutdown coverage.

## 2026-07-14 09:49 — Documentation CI validation observability

**Verified**

- Documentation CI run `29309938483` failed after startup-context reading inside the compound `Validate project context, interactive links, and scripts` step.
- Checkout and Python setup succeeded; dependency installation and strict MkDocs building were skipped.
- The connector-decoded log was truncated before the failing command or assertion.
- `.github/workflows/docs-ci.yml` now runs durable-context validation, interactive-link validation, verbose unit tests, shell syntax, Python compilation, and asset checks as separately named steps.

**Interpretation**

- This is an observability fix, not proof that the underlying validation defect is repaired. The next run should identify the exact failing subsystem without speculative edits.

**Historical**

- Workflow step names and run IDs describe PR #1 as observed on 2026-07-14.

**Open questions**

- Which named step fails on the updated workflow head, and does strict MkDocs reveal a second independent issue once validation passes?

## 2026-07-14 10:52 — Python unit-test suite isolation

**Verified**

- Documentation CI run `29312885959` passed durable project-context and interactive-link validation, then failed in the aggregate Python unit-test step.
- Shell syntax, Python compilation, asset checks, dependency installation, and strict MkDocs building were skipped after that failure.
- The repository currently contains two unit-test modules: source-index tests and interactive-link validator tests.
- CI now runs those modules in separate named steps and retains full discovery as a final guard.

**Interpretation**

- The remaining ambiguity is limited to the exact unit-test module and assertion; isolating suites preserves coverage while avoiding speculative implementation changes.

**Historical**

- Run and job identifiers describe PR #1 as observed on 2026-07-14.

**Open questions**

- Which isolated suite fails, what is the exact traceback, and does strict MkDocs expose a later independent defect?
