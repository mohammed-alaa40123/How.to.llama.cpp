# Project state

_Last updated: 2026-07-15 03:51 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream reference used for the graph/MoE chapter: `6b4dc2116a92c5c8f2782bfe51fabe5ee66fb5ef`
- Policy: baseline claims stay pinned; newer refs are documented separately and labelled.

## Active milestone

**Foundations deepening — interactive system map plus file-by-file subsystem synthesis**

## Completed

- MkDocs Material site, strict documentation CI, Pages deployment, health checks, source indexing, and durable run context.
- Canonical GGUF, model placement, model/context, graph/MoE, scheduler, memory-lifetime, and system-ownership pages.
- Pass A pages for the public API/minimal example, model/GGUF loader, runtime context/memory, backend scheduler, and concrete context-memory implementations.
- Exact pinned declaration and reverse-destruction map for `llama_model` and `llama_context`.
- Generic scheduler plus ordinary CPU, CUDA, Metal, Vulkan, SYCL, RPC, and CANN teardown audits.
- Cross-backend teardown comparison matrix and reusable teardown audit method.
- Pinned OpenCL build composition and initial `cl_mem` ownership map.
- Line-aware generated source indexing with pinned file and symbol links.
- Guided end-to-end inference atlas with clickable reading paths.
- Bounded CPU repack, AMX, KleidiAI, and SpacemiT IME extra-buffer lifetime audits.
- Cross-implementation CPU optional-buffer comparison and portable destruction-test matrix.
- Implementation-ready CPU optional-buffer destruction-harness specification with admission, correctness, lifetime-ordering, and sanitizer assertions.
- Documentation CI validation commands split into named steps with verbose unittest output.
- Python unit tests split into source-index, boundary, unsupported-syntax, function-try-block, OpenCL lifecycle, and interactive-link suites, followed by a full discovery guard.
- Source-index exact-line support for attributes, trailing returns, bounded constraints, operators, qualified special members, parenthesized initializer lists, and delegating constructors.
- Negative boundary tests plus bounded telemetry for braced/multiline constructor initializers and constructor function-try-blocks.
- Bounded OpenCL lifecycle-call extractor for completion/wait and queue/context/program/kernel/event/buffer release calls.
- C/C++ comment and quoted-literal masking for lifecycle extraction while preserving exact source offsets and line numbers.
- Function-try initializer-line guard preventing `try : member(...) {` from becoming a false ordinary-function symbol.

## Latest concrete findings

- The original direct lifecycle-call regex could classify call-shaped text inside comments or strings as teardown evidence.
- `mask_comments_and_literals()` replaces line comments, block comments, string literals, and character literals with spaces while preserving newlines and source length.
- Direct code calls remain available to the bounded OpenCL API regex; focused regression coverage checks comments, strings, escaped character literals, multiline comments, and exact post-mask lines.
- A local focused reproduction returned only the real `clFlush` call on line 6 after several masked false-positive candidates.
- Dedicated CI proved the OpenCL lifecycle suite passes independently.
- The full-discovery failure was isolated to constructor function-try-block coverage: `FUNC_RE` treated `try : device(device) {` as a function definition named `device`.
- A bounded `(?!try[\t ]*:)` guard prevents that partial record while preserving constructor function-try telemetry.
- Documentation CI run `29380673982` passed the complete suite and strict MkDocs for implementation head `540add358890507fb04f48f4a8e239e1a060971a`.
- The pinned OpenCL blob remains `f283f65690af7790e163092207647d16dac9fb3e`.

## In progress

- Regeneration of the pinned source inventory with line-aware records, pinned source links, unsupported-syntax counts, and the masked OpenCL lifecycle-call report.
- Exact OpenCL backend/context teardown, queue completion, scheduler events/buffers, and program/kernel/context release order.
- Implementation of the first CPU repack backend-free-before-buffer-free test fixture under ASan/LSan.
- CPU extra-buffer destruction tests for KleidiAI, AMX, and SpacemiT plus TSan and hardware-specific cleanup coverage.
- Shared generated metadata for the static inference atlas and interactive workflow.
- Runtime overlays for page faults, scheduler copies, event waits, KV/recurrent growth, and backend queues.
- CANN reset semantics, RPC completion, CUDA all-stream coverage, SYCL all-queue coverage, and Vulkan query-pool ownership.

## Immediate next task

Resume one of the two highest-value implementation tracks:

```text
A. obtain the complete pinned ggml-opencl.cpp in CI or a checkout
   → run the masked extract_opencl_lifecycle_calls.py
   → inspect every completion/release site in context
   → finish OpenCL teardown and update the backend matrix
B. implement the admitted CPU repack MUL_MAT fixture
   → reference comparison
   → CPU backend wrapper free
   → repack buffer free
   → ASan/LSan repetition
```

## Publication and verification state

- Work is published in PR #1 from branch `automation/backend-teardown-audit-method`.
- Added detailed note `logs/research/2026-07-15/0351-opencl-lifecycle-lexical-masking.md`.
- Documentation CI run `29380673982` passed completely for the implementation head.
- Later durable-state commits require their own commit-scoped CI run, but they do not alter the validated scanner logic or fixtures.
- Full local checkout validation remains unavailable because direct GitHub DNS resolution is blocked in this runtime.
- Public search returned no indexed Pages result, direct safe-URL access remained unavailable, and branch-only content cannot deploy until PR #1 merges.

## Known blockers and caveats

- **Pinned regeneration blocker:** no usable local pinned llama.cpp checkout is available, so the source index and OpenCL lifecycle report could not be regenerated here.
- **Large upstream file blocker:** connector blob rendering truncates the pinned OpenCL file; line-ranged reads return empty content and exact hidden teardown functions remain unavailable.
- **Local validation blocker:** direct cloning fails with `Could not resolve host: github.com`; GitHub-hosted Documentation CI is the authoritative validation path for this branch.
- **Pages verification blocker:** branch-added content cannot deploy until PR #1 merges; live response verification remains unavailable independently of strict-build success.
- **Lifecycle-extractor caveat:** selected direct API calls are navigation evidence only; ownership, error paths, macro wrappers, preprocessor-disabled code, raw strings, and semantic ordering still require human source review.
- **Source-index caveat:** same-line standard attributes, trailing-return definitions, bounded same-line constraints, bounded operators, qualified out-of-class special members, and bounded parenthesized member/delegating constructor initializer lists are recognized. Braced and multiline constructor initializers and constructor function-try-blocks remain intentionally omitted from navigation but are counted as bounded candidates.
- **Telemetry caveat:** unsupported-syntax counts are prioritization signals, not parser-completeness metrics, and may undercount or overcount unusual C++ forms.
- **Harness caveat:** a skipped hardware-gated path is not evidence that the lifetime ordering passed.
- **SpacemiT caveat:** buffer lifetime is distinct from thread-local TCM leases and process-level pool-manager lifetime.
- Mapping, allocation, residency, validity, command completion, ownership, reset, thread-local leases, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, memory, and teardown ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
