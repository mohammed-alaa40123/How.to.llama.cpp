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

## 2026-07-13 19:51–21:49 — Source navigation and teardown comparison

**Verified**

- `scripts/index_upstream.py` emits untruncated, source-ordered `symbol_locations` with approximate declaration kind, exact 1-based lines, and revision-pinned file/symbol URLs.
- Added a pinned teardown matrix for ordinary CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and the OpenCL gap.

**Open question**

- Regenerate the pinned inventory when upstream access is available and use it to finish OpenCL teardown.

## 2026-07-14 01:52–08:49 — Inference atlas and CPU optional buffers

**Verified**

- Added a clickable inference pipeline and reusable ten-step teardown worksheet.
- Audited CPU repack, AMX, KleidiAI, and SpacemiT IME extra-buffer ownership and synchronous execution.
- Added a cross-implementation comparison, portable destruction-test matrix, and an implementation-ready admitted `MUL_MAT` fixture.

**Interpretation**

- A tiny deterministic graph is stronger than a full model for the lifetime-ordering question because admission, fallback placement, owners, and destruction order remain visible.

**Open questions**

- Validate AMX allocator pairing, KleidiAI initialization/readback behavior, SpacemiT TCM/process-pool shutdown, and sanitizer ordering tests.

## 2026-07-14 09:49–12:50 — CI observability and source-line repair

**Verified**

- Split Documentation CI into named validators and isolated unit suites before full discovery.
- Found that regex `\s` crossed newlines and shifted type/function records to preceding blank or template lines.
- Replaced relevant leading whitespace with horizontal-only matching and added regression coverage.
- Complete CI passed through runs `29319949484` and `29323751656`.

**Interpretation**

- Generated links should target definitions, not adjacent whitespace; exact location is more valuable than broad approximate parsing.

## 2026-07-14 13:51–19:53 — Bounded C++ syntax indexing

**Verified**

- Added exact-line support for same-line attributes, trailing returns, bounded `requires`, qualified operators, constructors/destructors, and parenthesized constructor initializer lists.
- Dedicated rules avoid weakening ordinary function extraction.
- Complete CI passed through run `29352222406`.

**Interpretation**

- These are bounded navigation features, not claims to parse full C++ grammar.

**Open questions**

- Multiline syntax, complex requires-expressions, literals, macros, in-class members, and brace-containing initializer lists require pinned-tree evidence before expansion.

## 2026-07-14 20:52–23:51 — Constructor boundaries and telemetry

**Verified**

- Confirmed same-line parenthesized delegating constructors were already recognized and added explicit regression coverage.
- Added negative tests proving braced and multiline initializer lists do not emit partial symbols.
- Added per-file and aggregate unsupported-syntax counters for braced and multiline constructor initializer candidates.

**Interpretation**

- Measurable false-negative telemetry can prioritize scanner work without weakening navigation accuracy.

## 2026-07-15 01:50 — Constructor function-try-block telemetry

**Verified**

- Added bounded candidate counts for qualified constructor function-try-blocks with same-line or next-line `try`.
- These forms remain excluded from navigation records.

**Open question**

- Regenerate the pinned tree to determine whether stateful extraction is justified and which line a future record should target.

## 2026-07-15 02:51 — OpenCL lifecycle-call extractor

**Verified**

- Added `scripts/extract_opencl_lifecycle_calls.py` for selected OpenCL completion/wait and release calls.
- Records are source ordered and contain exact 1-based lines and per-name counts.
- The pinned blob SHA remains `f283f65690af7790e163092207647d16dac9fb3e`; visible content confirms `ggml_cl_buffer` releases `cl_mem` with `clReleaseMemObject`.

**Interpretation**

- A call inventory narrows review but does not establish ownership, error-path cleanup, release ordering, or command completion.

## 2026-07-15 03:51 — Lifecycle lexical masking and function-try repair

**Verified**

- Masked line comments, block comments, string literals, and character literals while preserving source offsets/newlines.
- Added regressions for call-shaped comments/literals and exact lines after masked regions.
- Full discovery exposed `try : device(device) {` being misread as a function named `device`; a bounded guard fixed it.
- Documentation CI run `29380673982` passed all suites and strict MkDocs.

**Interpretation**

- Lexical masking removes a concrete false-positive class without pretending to parse C++.

**Open questions**

- Raw strings, disabled preprocessor regions, macros, and wrappers remain outside the bounded model.
- Run the extractor against the complete pinned OpenCL file and inspect each result in context.

## 2026-07-15 04:49 — Bounded lifecycle source context

**Verified**

- `extract_opencl_lifecycle_calls()` now accepts an optional non-negative `context_lines` radius.
- Default zero preserves the existing `{name, line}` record shape.
- `--context-lines N` adds original-source `start_line`, `end_line`, and `text` around each call.
- Context clamps at file boundaries and is taken from the unmasked source, while detection still uses masked source.
- Focused tests cover exact context, boundary clamping, and negative-radius rejection.
- The lifecycle API set and matching semantics were not broadened.

**Interpretation**

- Bounded context turns the generated inventory into a usable first-pass teardown worksheet while remaining evidence for human review rather than proof of ownership or safe ordering.

**Historical**

- The preceding increment removed false-positive calls. This increment addresses the next bottleneck: reviewing true positives in a large translation unit whose connector rendering is truncated.

**Open questions**

- Determine the smallest useful context radius from the pinned report.
- Add enclosing-function metadata or creation/release pairing only if context remains insufficient.
- Obtain the complete pinned `ggml-opencl.cpp`, generate the real report, and finish the teardown matrix.

## 2026-07-15 05:51 — GitHub-hosted pinned OpenCL report generation

**Verified**

- Added `.github/workflows/opencl-lifecycle-report.yml`.
- The workflow fetches exactly llama.cpp revision `e3546c7948e3af463d0b401e6421d5a4c2faf565` and verifies the pinned OpenCL translation unit is non-empty.
- It runs the tested lifecycle extractor with three context lines, rejects an unexpectedly empty inventory, prints per-call counts, and uploads the JSON report as a 30-day artifact.
- The workflow is manually dispatchable and also runs when the extractor, its tests, or the workflow definition changes.
- Preceding Documentation CI run `29382836507` completed successfully.

**Interpretation**

- This replaces the runtime-specific local checkout blocker with a repository-owned, reproducible GitHub-hosted source-recovery path.
- The artifact remains navigation evidence; each call still requires human ownership, completion, and release-order classification.

**Historical**

- The extractor and bounded context existed, but the repository did not yet have a mechanism to obtain the complete pinned translation unit and preserve the report.

**Open questions**

- Inspect the first generated artifact and determine whether three context lines are sufficient.
- Add enclosing-function metadata or creation/retention pairing only if the artifact leaves material ambiguity.

## 2026-07-15 06:49 — Pinned OpenCL lifecycle first-pass classification

**Verified**

- Workflow run `29385330482` successfully generated and uploaded the complete pinned report; Documentation CI run `29385330547` also passed for the preceding head.
- The report contains 556 selected direct calls: 343 memory-object releases, 121 program releases, 51 event waits, 23 kernel releases, 11 queue finishes, 6 event releases, and 1 queue flush.
- The bounded inventory contains no direct command-queue or OpenCL-context release call.
- The shared OpenCL `free()` path calls `clFinish(queue)` before decrementing its reference count and releases pooled image/sub-buffer views only at the final reference.
- Cross-device synchronization uses peer-queue marker events and `clFlush()`, then a destination-queue barrier waiting on those events before their references are released.
- Multiple temporary conversion/readback paths wait before releasing temporary memory objects.

**Interpretation**

- OpenCL teardown can now be classified as conditional with verified local completion evidence, not globally safe.
- Missing direct queue/context release calls are an unresolved ownership signal, not proof of a leak.
- Three context lines are sufficient for the shared-free and synchronization idioms but not every enclosing owner.

**Historical**

- The first complete pinned artifact removes the earlier large-file/source-recovery blocker.

**Open questions**

- Locate final queue/context ownership, verify scheduler-resource independence, classify retention-only enqueue/release groups, and resolve optional Adreno binary-library lifetime.

## 2026-07-15 07:52 — OpenCL queue/context ownership-call inventory

**Verified**

- Expanded the lifecycle matcher to include `clCreateContext`, `clCreateContextFromType`, `clRetainContext`, `clCreateCommandQueue`, `clCreateCommandQueueWithProperties`, and `clRetainCommandQueue`.
- Exact source ordering, 1-based lines, lexical masking, and optional original-source context remain unchanged.
- Focused tests cover direct creation/retention calls, context-from-type creation, similar identifiers, and call-shaped comments/literals.
- The existing pinned-report workflow already triggers on extractor and test changes.

**Interpretation**

- The regenerated report can now distinguish “no direct releases” from a symmetric direct-call inventory containing creation/retention sites. Zero direct creation calls would shift attention toward wrappers, generated code, globals, or process-lifetime ownership rather than proving a leak.

**Historical**

- The first complete report inventoried completion and release calls only, leaving direct queue/context ownership transitions outside the generated evidence.

**Open questions**

- Inspect the regenerated pinned report, map each direct ownership call to its enclosing owner, verify scheduler-resource independence, and update the OpenCL teardown matrix.
