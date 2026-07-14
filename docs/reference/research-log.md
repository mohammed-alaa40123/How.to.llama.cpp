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

**Interpretation**

- The index is a high-value navigation aid for large files, not a compiler-grade call graph.

**Open question**

- Regenerate the pinned inventory when upstream access is available and use it to finish OpenCL teardown.

## 2026-07-13 21:49 — Cross-backend teardown comparison

**Verified**

- Added a pinned comparison matrix covering ordinary CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and the OpenCL gap.
- The matrix separates execution completion from scheduler-resource independence and links each classification to its detailed audit.

**Interpretation**

- Backend-before-scheduler safety requires independent proofs for command completion and valid later deleter state.

## 2026-07-14 01:52 — Guided end-to-end inference atlas

**Verified**

- Added a clickable pipeline linking GGUF, model loading, `llama_model`, `llama_context`, graph construction, scheduler execution, backends, sampling, and decode reuse.
- Added stage/lifetime and audience-specific reading paths.

**Interpretation**

- The atlas is a routing layer over canonical evidence pages, not a claim that runtime is a single linear thread.

## 2026-07-14 02:49 — Backend teardown audit method

**Verified**

- Added a reusable ten-step worksheet separating host-visible command completion from scheduler-resource deleter independence.
- Standardized bounded classifications and added a minimum asynchronous-destruction runtime matrix.

**Open question**

- Generate worksheet evidence from source-index metadata and implement portable destruction tests.

## 2026-07-14 03:51 — CPU repack extra-buffer lifetime

**Verified**

- Repack buffer type and tensor traits are process-static.
- Allocation delegates to the ordinary CPU buffer and does not replace its free callback.
- Execution follows the synchronous CPU graph path.

**Interpretation**

- Repack buffers remain destructible after the CPU backend wrapper is deleted.

## 2026-07-14 04:50 — CPU AMX extra-buffer lifetime

**Verified**

- AMX publication is compile/runtime gated.
- AMX owns a dedicated aligned host allocation and complete buffer interface.
- Traits and type metadata are process-static, and execution remains synchronous.
- AMX buffer destruction does not require `ggml_backend_cpu_context`.

**Open questions**

- Validate allocator pairing, repeated tile-permission initialization, null readback/copy paths, and sanitizer teardown tests.

## 2026-07-14 05:50 — CPU KleidiAI extra-buffer lifetime

**Verified**

- KleidiAI initialization is protected by the GGML critical section and process-static feature/kernel state.
- Allocation delegates to the ordinary CPU buffer; KleidiAI changes the buffer type plus `init_tensor` and `set_tensor` but retains ordinary CPU allocation/free ownership.
- `tensor->extra`, the extra-buffer type, and buffer-type metadata are process-static.
- Q4_0/Q8_0 upload synchronously builds versioned packed slots and falls back to the original representation when no compatible slot exists.
- Supported `MUL_MAT`/`GET_ROWS` execution remains in synchronous CPU graph computation with no independent queue or event.
- KleidiAI buffer destruction is independent of `ggml_backend_cpu_context` for the audited resources.

**Interpretation**

- KleidiAI is teardown-equivalent to the CPU repack overlay for backend-wrapper ownership, while adding richer feature-selected kernel chains, SME policy, and multi-slot packed representations.

**Historical**

- Feature detection, SME policy, kernel chains, packed-header format, fallback behavior, and callback ownership are revision-sensitive.

**Open questions**

- Validate null readback/copy behavior, concurrent initialization, packed-layout portability, packed-slot memory expansion, and backend-free-before-buffer-free ordering under ASan/LSan.

## 2026-07-14 06:50 — CPU SpacemiT IME extra-buffer lifetime

**Verified**

- SpacemiT owns a dedicated 64-byte-aligned allocation through the mutex-protected Spine memory pool, and its free callback returns the allocation through the matching pool API without using `ggml_backend_cpu_context`.
- `tensor->extra` points to process-static IME1, IME2, or RVV trait objects; the extra-buffer type and buffer-type metadata are function-static.
- Repacking and execution are synchronous CPU work using the threadpool and barriers, with no scheduler event or accelerator command queue.
- Worker setup can acquire thread-local TCM state and the paired clear-affinity hook releases that lease.

**Interpretation**

- Weight-buffer destruction is backend-wrapper-independent, but complete SpacemiT worker/process teardown remains conditional on all TCM cleanup hooks and pool-manager shutdown paths executing correctly.

**Historical**

- IME admission, pool chunking, huge-page/TCM devices, thread binding, supported layouts, and callback ownership are revision-sensitive.

**Open questions**

- Audit worker error paths, process-level pool shutdown, null transfer callbacks, repacked memory expansion, and repeated buffer/threadpool teardown under sanitizers on supported hardware.
