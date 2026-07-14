# Project state

_Last updated: 2026-07-14 20:52 Africa/Cairo_

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
- Pass A pages for the public API/minimal example, model/GGUF loading, runtime context/memory, scheduler, and concrete context-memory implementations.
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
- Python unit tests split into source-index and interactive-link suites, followed by a full discovery guard.
- Source-index type-declaration line locations corrected so blank lines are not consumed as leading whitespace.
- Regression coverage for multiple blank lines and namespace-indented type declarations.
- Same-line C++ attributes before and after type keywords recognized without weakening physical-line accuracy.
- Same-line C++ attributes before function return types recognized with focused free-function and qualified-method coverage.
- Same-line trailing-return function definitions recognized with focused free-function and attributed qualified-method coverage.
- Function return-type matching restricted to horizontal whitespace so preceding template lines cannot steal the source location.
- Bounded same-line C++20 `requires` clauses recognized after ordinary or trailing-return signatures.
- Bounded qualified operator definitions recognized for symbolic, call, subscript, allocation, deletion, and single-token conversion forms.
- Bounded qualified out-of-class constructor and destructor definitions recognized with exact source lines.
- Bounded same-line constructor initializer lists recognized for out-of-class constructors without weakening exact source-line accuracy.
- Same-line delegating constructors verified as already accepted by the bounded initializer-list rule; the false unsupported-capability TODO was removed.
- Successful full Documentation CI through the initializer-list expansion.

## Latest concrete findings

- Documentation CI run `29352222406` completed successfully for initializer-list head `f427ab95f3a9147acfc58a7248ebc2bd312f1a24`.
- The current `SPECIAL_MEMBER_RE` initializer-list clause accepts both member initialization and constructor delegation when the entire list and opening body brace occur on one physical line.
- A focused reproduction using the exact branch regex indexed `backend_state::backend_state` at line 1 and `nested::resource::resource` at line 4 for delegating-constructor examples.
- The class-name backreference continues to constrain extraction to qualified constructors/destructors, while newlines, semicolons, and braces remain excluded from the initializer-list body.
- No scanner implementation change was required; an explicit regression fixture remains needed before treating the behavior as a permanent compatibility guarantee.
- The pinned OpenCL CMake target compiles `ggml-opencl.cpp`, whose blob SHA is `f283f65690af7790e163092207647d16dac9fb3e`.
- The connector can expose the beginning of that 24k-line blob and confirms buffer-local `cl_mem` RAII, but output remains truncated before backend teardown symbols; no hidden teardown behavior was inferred.

## In progress

- Regeneration of the pinned source inventory with line-aware records and pinned source links.
- Exact OpenCL backend/context teardown, queue completion, scheduler events/buffers, and program/kernel/context release order.
- Explicit delegating-constructor regression coverage for the source index.
- Implementation of the first CPU repack backend-free-before-buffer-free test fixture under ASan/LSan.
- CPU extra-buffer destruction tests for KleidiAI, AMX, and SpacemiT plus TSan and hardware-specific cleanup coverage.
- Shared generated metadata for the static inference atlas and interactive workflow.
- Runtime overlays for page faults, scheduler copies, event waits, KV/recurrent growth, and backend queues.
- CANN reset semantics, RPC completion, CUDA all-stream coverage, SYCL all-queue coverage, and Vulkan query-pool ownership.

## Immediate next task

Resume one of the two highest-value implementation tracks:

```text
A. add the explicit same-line delegating-constructor regression,
   then regenerate pinned symbol locations and finish OpenCL teardown
B. implement the admitted CPU repack MUL_MAT fixture
   → reference comparison
   → CPU backend wrapper free
   → repack buffer free
   → ASan/LSan repetition
```

## Publication and verification state

- Work is published in PR #1 from branch `automation/backend-teardown-audit-method`; the PR remains open and mergeable.
- Added detailed note `logs/research/2026-07-14/2052-delegating-constructor-indexing-audit.md`.
- The preceding initializer-list implementation passed Documentation CI and strict MkDocs in run `29352222406`.
- This run changed durable documentation only; the newly documented delegating-constructor behavior was reproduced with the exact current regex.
- Full local checkout validation remains unavailable because direct GitHub DNS resolution is blocked in this runtime.
- Direct Pages checks remain unavailable, and branch-only content cannot deploy until PR #1 merges.

## Known blockers and caveats

- **Pinned regeneration blocker:** no usable local pinned llama.cpp checkout is available, so the source index could not be regenerated here.
- **Large upstream file blocker:** the connector exposes the pinned OpenCL blob as truncated output and exact hidden symbols remain difficult to search.
- **Local validation blocker:** direct cloning fails with `Could not resolve host: github.com`; full local Python tests, strict MkDocs build, and `check_site.sh` require a usable checkout. GitHub-hosted Documentation CI is the authoritative validation path for this branch.
- **Pages verification blocker:** direct live-site checks are unavailable, and branch-only documentation cannot deploy until PR #1 merges.
- **Source-index caveat:** same-line standard attributes, trailing-return definitions, bounded same-line constraints, bounded operators, qualified out-of-class special members, and bounded parenthesized member/delegating constructor initializer lists are recognized; multiline forms, braced initializer lists, function-try-blocks, in-class special members, defaulted/deleted definitions, literals, arbitrary declaration macros, and generated syntax remain approximate or unresolved.
- **Harness caveat:** a skipped hardware-gated path is not evidence that the lifetime ordering passed.
- **SpacemiT caveat:** buffer lifetime is distinct from thread-local TCM leases and process-level pool-manager lifetime.
- **Scope caveat:** optional CPU extra-buffer audits do not prove behavior for HBM or future implementations.
- Mapping, allocation, residency, validity, command completion, ownership, reset, thread-local leases, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, memory, and teardown ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
