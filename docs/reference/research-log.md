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

## 2026-07-14 09:49–10:52 — Documentation CI observability and suite isolation

**Verified**

- The compound documentation validation step was split into named context, link, test, shell, compilation, asset, dependency, and strict-build steps.
- Source-index and interactive-link unit suites now run independently before full discovery.
- This isolated the remaining failure to source-index tests without reducing coverage.

**Interpretation**

- Observability changes identified the defect but did not themselves prove a repair.

## 2026-07-14 11:51–12:50 — Source-index line repair and whitespace regression

**Verified**

- `CLASS_RE` used `^\s*`; because `\s` includes newline, a declaration following a blank line could report the previous line.
- Horizontal-only whitespace corrected the declaration location.
- Regression coverage verifies multiple blank lines and namespace indentation.
- Documentation CI runs `29319949484` and `29323751656` passed all tests and strict MkDocs.

**Interpretation**

- The implementation was wrong, not the expected line: generated links should target declarations rather than adjacent whitespace.

## 2026-07-14 13:51–15:50 — Attributed and trailing-return indexing

**Verified**

- Type indexing recognizes same-line attributes before and after type keywords.
- Function indexing recognizes same-line leading attributes and bounded same-line trailing-return clauses.
- Horizontal whitespace preserves exact physical lines.
- Complete Documentation CI passed through run `29334576467`.

**Interpretation**

- These are bounded navigation improvements, not a claim to parse the full C++ grammar.

## 2026-07-14 16:51 — Constrained C++ function indexing and line accuracy

**Verified**

- Return-type matching still included `\s`, allowing a match to begin on a preceding template line.
- Return-type whitespace is now horizontal-only.
- One bounded same-line C++20 `requires` clause is accepted after ordinary or trailing-return signatures.
- Focused tests preserve physical definition lines after template declarations.
- Documentation CI run `29339261751` passed the complete suite and strict MkDocs.

**Interpretation**

- Exact navigation lines are more valuable than broad syntax acceptance with shifted locations.

**Open questions**

- Multiline constraints and complex requires-expressions remain candidates only if the pinned tree demonstrates sufficient need.

## 2026-07-14 17:49 — Bounded C++ operator-function indexing

**Verified**

- Ordinary function-name extraction cannot represent `operator` names because it accepts only identifier components.
- Conversion operators have no return type before `operator`, requiring a dedicated bounded pattern.
- Added qualified same-line support for symbolic, call, subscript, `new`/`delete`, and single-token conversion operators.
- Focused tests require exact lines for `tensor_view::operator==`, `tensor_view::operator()`, `tensor_view::operator[]`, and `resource::operator bool`.
- The existing ordinary-function and type patterns were not broadened.
- The pinned OpenCL target compiles `ggml-opencl.cpp`; its pinned blob SHA is `f283f65690af7790e163092207647d16dac9fb3e`.
- Large-blob connector output still truncates before OpenCL backend teardown symbols, so no unseen cleanup behavior was inferred.
- Documentation CI run `29343666640` passed the complete suite and strict MkDocs for the final operator-indexing head.

**Interpretation**

- Operator definitions are valuable navigation targets for backend RAII and ownership code. A separate pattern is safer than allowing arbitrary punctuation in the ordinary function-name rule.

**Historical**

- This closes the operator-definition scanner gap recorded after the constrained-function increment.

**Open questions**

- Multiline operator signatures, literals, complex conversion targets, and macro-generated definitions remain unsupported.
- Complete pinned OpenCL teardown still requires searchable access to the end of the translation unit or a regenerated local inventory.

## 2026-07-14 18:51 — Qualified constructor and destructor indexing

**Verified**

- Constructors and destructors have no return type, so they require a dedicated bounded scanner pattern.
- `SPECIAL_MEMBER_RE` recognizes same-line qualified out-of-class constructors and destructors with optional attributes, `noexcept`, and one bounded same-line `requires` clause.
- Requiring at least one scope qualifier limits false positives and targets common RAII definitions.
- Focused tests require exact lines for an ordinary constructor, destructor, and attributed constrained nested constructor.
- Ordinary functions, operators, and type extraction remain separate.
- Documentation CI run `29348084640` passed the complete suite and strict MkDocs for the final special-member head.

**Interpretation**

- Special members are high-value source-index targets because backend acquisition and release logic commonly lives in constructors and destructors. Making the ordinary return-type pattern optional would be less precise.

**Historical**

- This closes the common out-of-class special-member gap after the operator increment.

**Open questions**

- In-class special members, initializer lists, multiline signatures, defaulted/deleted definitions, literals, and generated declarations remain unsupported.

## 2026-07-14 19:53 — Constructor initializer-list indexing

**Verified**

- The previous special-member matcher required `{` immediately after optional `noexcept` and `requires`, so constructors with `: member(value)` initializer lists were absent from the index.
- Added one bounded same-line initializer-list clause excluding newlines, semicolons, and braces.
- Focused tests require exact lines for ordinary parenthesized initializer lists on qualified constructors.
- Destructor behavior and ordinary-function, operator, and type extraction were not broadened.

**Interpretation**

- Constructor initializer lists are valuable navigation targets because backend resource ownership and synchronization state are often established there.

**Historical**

- This extends the bounded qualified special-member scanner while preserving exact physical-line priority.

**Open questions**

- Braced and multiline initializer lists, delegating constructors, function-try-blocks, in-class special members, and macro-generated definitions remain unsupported.
- Complete pinned OpenCL teardown still requires searchable access to the end of the translation unit or a regenerated local inventory.
