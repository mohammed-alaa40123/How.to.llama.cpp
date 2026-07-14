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

- Run and job identifiers describe PR #1 as observed on July 14, 2026.

**Open questions**

- Which isolated suite fails, what is the exact traceback, and does strict MkDocs expose a later independent defect?

## 2026-07-14 11:51 — Source-index type line-number repair

**Verified**

- Documentation CI run `29316377253` failed specifically in the isolated `Test source indexing` step after both context validators passed.
- `CLASS_RE` used `^\s*`; because `\s` includes newline, a type declaration following a blank line could be matched from the preceding line.
- The test fixture expected `enum class second_type` on line 8, while the old regex produced line 7.
- Replacing leading and separating whitespace with horizontal `[\t ]*` and `[\t ]+` reports the actual declaration line.
- A bounded local regex reproduction confirmed the corrected line result.

**Interpretation**

- The implementation was wrong, not the test: generated source links should point to the declaration, not the blank line before it.

**Historical**

- The defect was introduced with line-aware source indexing on the current branch and is fixed in the branch implementation.

**Open questions**

- Does the next Documentation CI run pass both isolated suites, discovery, and strict MkDocs, and should coverage be expanded to multiple blank lines and nested indentation?

## 2026-07-14 12:50 — Source-index whitespace regression coverage

**Verified**

- Documentation CI run `29319949484` completed successfully for commit `0e486859740650a998ee07531389dccc19e88e00`.
- The successful run confirms the type-line repair passes both isolated suites, full unittest discovery, shell and Python validation, asset checks, dependency installation, and strict MkDocs.
- Added a focused regression with two type declarations after multiple blank lines and at different indentation depths inside a namespace.
- The expected symbol locations are the physical declaration lines: line 4 and line 9.

**Interpretation**

- The original defect is closed. The new test hardens the invariant that vertical whitespace must never shift a declaration's source location while horizontal indentation remains accepted.

**Historical**

- This coverage follows the branch's repair from multiline `\s*` to horizontal `[\t ]*` matching.

**Open questions**

- Verify the new test on its own commit-scoped CI run, then consider nested classes, attributes, and templates only if the approximate regex index expands.

## 2026-07-14 13:51 — Attributed C++ type indexing

**Verified**

- The type index previously required `class`, `struct`, `enum`, or `enum class` to be the first non-horizontal-whitespace token on the declaration line.
- The type pattern now recognizes same-line C++ `[[...]]` attributes before the type keyword and between the keyword and declared name.
- A focused test covers attributed `struct` and `enum class` declarations and requires their physical declaration lines to remain unchanged.
- All whitespace matching remains horizontal, so the preceding-blank-line defect cannot be reintroduced by this extension.

**Interpretation**

- Same-line attributes are a useful bounded expansion for a navigation index. Multiline attributes, arbitrary declaration macros, and generated syntax should remain explicit limitations rather than encouraging a regex to impersonate a parser.

**Historical**

- This increment builds on the earlier line-number repair and whitespace regression coverage.

**Open questions**

- Determine from the pinned tree whether multiline attributes or export/declaration macros justify a stateful scanner or targeted additional rules.

## 2026-07-14 14:52 — Attributed C++ function indexing

**Verified**

- The function index previously required the return type to be the first non-horizontal-whitespace token, so a leading same-line `[[...]]` attribute prevented indexing.
- The updated function pattern accepts one or more same-line attribute groups before the return type.
- A focused test covers an attributed free function and namespace-qualified `const noexcept` method at physical lines 1 and 5.
- Type extraction, duplicate retention, source ordering, and pinned link construction are unchanged.
- The pinned OpenCL blob was retrieved, but connector output remained truncated before the teardown section; no hidden teardown behavior was inferred.

**Interpretation**

- Leading same-line function attributes are a bounded navigation improvement. Multiline attributes, trailing-return syntax, requires clauses, declaration macros, and complex declarators remain explicit scanner limitations.

**Historical**

- This increment applies the previous run's bounded same-line attribute policy to function definitions.

**Open questions**

- Verify the focused test and strict MkDocs through Documentation CI, then evaluate additional syntax only from observed pinned-tree needs.

## 2026-07-14 15:50 — Trailing-return C++ function indexing

**Verified**

- Documentation CI run `29330951186` completed successfully for the preceding attributed-function increment.
- The function pattern previously stopped after optional `const` and `noexcept`, so a same-line `-> return_type` clause prevented definition matching.
- The updated pattern accepts one bounded same-line trailing-return clause while excluding newlines, semicolons, and braces.
- A focused test covers a free function and an attributed namespace-qualified `const noexcept` method at physical lines 1 and 5.
- Type extraction, duplicate retention, source ordering, and pinned URL construction are unchanged.

**Interpretation**

- Same-line trailing-return definitions are a useful bounded navigation expansion. Multiline returns, requires clauses, macros, operators, lambdas, and complex declarators remain explicit scanner limitations.

**Historical**

- This increment follows the source-line repair and same-line attribute support and closes one limitation recorded by the preceding run.

**Open questions**

- Verify the focused regression and strict MkDocs through Documentation CI, then return to pinned OpenCL source recovery or the CPU repack destruction fixture.

## 2026-07-14 16:51 — Constrained C++ function indexing and line accuracy

**Verified**

- `FUNC_RE` still used `\s` inside its return-type character class, allowing a match to begin on a preceding template line.
- Return-type whitespace is now horizontal-only, preserving the physical function definition line.
- The scanner accepts one bounded same-line C++20 `requires` clause after optional qualifiers and trailing-return syntax.
- A focused test covers an ordinary constrained function and an attributed namespace-qualified `const noexcept` trailing-return method at physical lines 2 and 7.
- The constraint matcher excludes newlines, semicolons, and braces.

**Interpretation**

- Exact navigation lines are more valuable than broad but line-shifting grammar acceptance. Common same-line constraints can be supported without treating the regex as a complete C++ parser.

**Historical**

- This increment applies the horizontal-whitespace invariant from type declarations to function return types and closes the previously listed same-line `requires` gap.

**Open questions**

- Evaluate multiline constraints, operators, and declaration/export macros only after regenerating and inspecting the pinned tree; then return to OpenCL teardown or the CPU repack destruction fixture.
