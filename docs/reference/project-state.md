# Project state

_Last updated: 2026-07-15 18:51 Africa/Cairo_

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
- Generic scheduler plus ordinary CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL teardown audits.
- Cross-backend teardown comparison matrix and reusable teardown audit method.
- Pinned OpenCL build composition, exact lifecycle inventory, source-backed queue/context ownership, and Adreno binary-library lifetime classification.
- Line-aware generated source indexing with pinned file and symbol links.
- Guided end-to-end inference atlas with clickable reading paths.
- Bounded CPU repack, AMX, KleidiAI, and SpacemiT IME extra-buffer lifetime audits.
- Cross-implementation CPU optional-buffer comparison and portable destruction-test matrix.
- Implementation-ready CPU optional-buffer destruction-harness specification with admission, correctness, lifetime-ordering, and sanitizer assertions.
- Documentation CI validation commands split into named steps with verbose unittest output.
- Python unit tests split into source-index, boundary, unsupported-syntax, function-try-block, OpenCL lifecycle/follow-up, and interactive-link suites, followed by a full discovery guard.
- Source-index exact-line support for attributes, trailing returns, bounded constraints, operators, qualified special members, parenthesized initializer lists, and delegating constructors.
- Negative boundary tests plus bounded telemetry for braced/multiline constructor initializers and constructor function-try-blocks.
- Bounded OpenCL lifecycle-call extractor for direct queue/context creation and retention plus completion/wait and queue/context/program/kernel/event/buffer releases.
- C/C++ comment and quoted-literal masking for lifecycle extraction while preserving exact source offsets and line numbers.
- Function-try initializer-line guard preventing `try : member(...) {` from becoming a false ordinary-function symbol.
- Optional bounded original-source context for every lifecycle record, with exact clamped line ranges and backward-compatible default output.
- GitHub-hosted pinned OpenCL workflow that verifies the exact baseline checkout and preserves the complete source, generated report, and SHA-256 manifest.
- Verified OpenCL backend-wrapper order: queue completion occurs before wrapper reference drop, while the actual device/backend context remains process-lifetime.
- Verified OpenCL scheduler events are unsupported and buffer deleters use buffer-local `cl_mem` ownership rather than the destroyed wrapper.
- Resolved optional Adreno binary-library lifetime: the raw loader handle is not retained or closed, so the library, exported lookup function, and accepted binary-kernel path remain process-lifetime.
- Portable OpenCL evidence manifest: artifact-root basenames, pre-upload `sha256sum -c`, and an exact-filename guard make the downloaded artifact directly verifiable after extraction.
- Classified the pinned `transpose_2d()` nonblocking sub-buffer release as locally safe under the official OpenCL memory-object lifetime contract.
- Audited every pinned `transpose_2d*()` call site: all 53 typed-wrapper calls omit the final argument and use `blocking=true`; no caller selects the nonblocking branch.
- Classified the pinned Q4_0 conversion group: both conversion branches explicitly wait before releasing temporary `data_device`, but both retain the returned command event indefinitely by omitting `clReleaseEvent(evt)`.
- Completed the full direct-wait pairing audit: 5 of 51 waited events are released, while 46 local command-event references have no release or ownership transfer.
- Resolved `CL_CHECK` failure semantics: any non-success OpenCL status logs, triggers `GGML_ASSERT(0)`, enters `ggml_abort()`, and ends in unconditional `abort()` rather than recoverable error propagation.
- Added a bounded simple-local waited-event diagnostic that machine-checks the pinned 50 simple identifier records, 4 released, and 46 unmatched ownership counts.
- Classified 22 of the 46 unmatched waits as redundant before an immediate same-queue `clEnqueueReadBuffer(..., CL_TRUE, ...)`; 24 waits remain for separate API-contract and consumer-order analysis.
- Added a separate machine-readable blocking-read follow-up annotation and pinned workflow guard for the reviewed 22/24 split without changing event ownership status.

## Latest concrete findings

- The lifecycle report now stores `followed_by_same_queue_blocking_read` and `next_read_line` beside simple waited-event records.
- The annotator requires the immediately following statement to call `clEnqueueReadBuffer`, use literal queue `queue`, and pass `CL_TRUE` as the blocking argument.
- The pinned workflow independently guards ownership (`4 released`, `46 unmatched`) and synchronization hints (`22 immediate blocking reads`, `24 other unmatched`).
- The distinction is intentional: a blocking read can make a wait redundant but cannot release the event reference.
- Focused tests reject nonblocking reads, different queues, intervening statements, and call-shaped text in comments or literals.

## In progress

- Preparing a minimal release-only upstream correction for all 46 unmatched events and using the ownership diagnostic to require zero unmatched entries.
- Classifying the remaining 24 unmatched waits, primarily upload/conversion paths, against the backend `set_tensor` completion contract and same-queue consumer chain.
- Determining whether repeated OpenCL registration, registry teardown, or shared-library unload is supported.
- Regeneration of the pinned source inventory with line-aware records, pinned source links, and unsupported-syntax counts.
- Implementation of the first CPU repack backend-free-before-buffer-free test fixture under ASan/LSan.
- CPU extra-buffer destruction tests for KleidiAI, AMX, and SpacemiT plus TSan and hardware-specific cleanup coverage.
- Shared generated metadata for the static inference atlas and interactive workflow.
- Runtime overlays for page faults, scheduler copies, event waits, KV/recurrent growth, and backend queues.
- CANN reset semantics, RPC completion, CUDA all-stream coverage, SYCL all-queue coverage, and Vulkan query-pool ownership.

## Immediate next task

```text
Prepare release-only OpenCL event fix
  → add clReleaseEvent(evt) after every successful unmatched wait
  → preserve all existing synchronization in the first patch
  → validate 0 unmatched_in_scope ownership records
  → retain the independent 22/24 synchronization annotation
  → separately remove the 22 waits proven redundant before blocking reads
  → classify the remaining 24 waits against set_tensor completion semantics
```

In parallel or if blocked, implement the admitted CPU repack `MUL_MAT` fixture with reference comparison, CPU backend-wrapper free, repack-buffer free, and ASan/LSan repetition.

## Publication and verification state

- Work is published in PR #1 from branch `automation/backend-teardown-audit-method`.
- Added detailed note `logs/research/2026-07-15/1851-opencl-wait-followup-annotation.md`.
- Added `scripts/annotate_opencl_wait_followups.py` and focused regression tests.
- The required startup files and current repository files were inspected before editing.
- Documentation CI and pinned OpenCL report runs were triggered for the implementation commits; final-head results must be checked before the run closes.
- Full local checkout validation remains unavailable because direct GitHub DNS resolution is blocked in this runtime and `gh` is not installed.
- Public Pages verification remains blocked for branch-only content until PR #1 merges.

## Known blockers and caveats

- **Systematic OpenCL event leak:** 46 of 51 direct host-waited command events have no matching release or ownership transfer in the pinned translation unit.
- **Synchronization split:** 22 of those 46 waits are redundant before an immediate same-queue blocking read; the remaining 24 require a different completion-contract analysis.
- **Diagnostic scope:** the simple-local wait/release guard recognizes only literal count-one waits and same-identifier releases in the same lexical brace scope; it is not proof of general C++ ownership.
- **Follow-up annotation scope:** the new annotator requires an immediate semicolon-terminated statement, literal queue name `queue`, and literal `CL_TRUE`; aliases, macros, branches, and general control flow remain human-review work.
- **Fatal-error policy:** `CL_CHECK` terminates via `abort()`; normal C++ destructors and scope guards do not run after a checked failure, so deterministic cleanup is meaningful only on successful paths or after a future nonfatal error redesign.
- **Deterministic-release gap:** the pinned translation unit intentionally keeps device/backend contexts process-lifetime and contains no explicit queue/context release or per-device backend-context deletion path.
- **Adreno library lifetime:** the optional binary-kernel loader loses its raw `dl_handle`. This prevents early unload but omits deterministic release and also retains invalid-symbol loads until process exit.
- **Local validation blocker:** direct cloning fails with `Could not resolve host: github.com`, and `gh` is unavailable; GitHub-hosted Actions are the authoritative validation path for this branch.
- **Pages verification blocker:** branch-added content cannot deploy until PR #1 merges; live response verification remains unavailable independently of strict-build success.
- **Dormant-branch caveat:** `blocking=false` is locally retention-safe but has no pinned callers; future revisions must be re-audited if the branch becomes reachable.
- **Retention classification caveat:** `clReleaseMemObject()` safely defers deletion for queued users, but that does not protect event references, unrelated host storage, wrapper callbacks, pooled-region reuse, or missing cross-queue dependencies.
- **Lifecycle-extractor caveat:** selected direct APIs and bounded context are navigation evidence only; wrapper constructors, ownership, error paths, macro wrappers, disabled code, raw strings, and semantic ordering still require human source review.
- **Source-index caveat:** same-line standard attributes, trailing-return definitions, bounded same-line constraints, bounded operators, qualified out-of-class special members, and bounded parenthesized member/delegating constructor initializer lists are recognized. Braced and multiline constructor initializers and constructor function-try-blocks remain intentionally omitted from navigation but are counted as bounded candidates.
- **Telemetry caveat:** unsupported-syntax counts are prioritization signals, not parser-completeness metrics.
- **Harness caveat:** a skipped hardware-gated path is not evidence that the lifetime ordering passed.
- **SpacemiT caveat:** buffer lifetime is distinct from thread-local TCM leases and process-level pool-manager lifetime.
- Mapping, allocation, residency, validity, command completion, event ownership, reset, thread-local leases, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, memory, and teardown ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
