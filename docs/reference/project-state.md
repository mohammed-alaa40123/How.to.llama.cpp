# Project state

_Last updated: 2026-07-16 01:52 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream OpenCL revision audited: `505b1ed15ca80e2a19f12ff4ac365e40fb374053`
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
- Python unit tests split into source-index, boundary, unsupported-syntax, function-try-block, OpenCL lifecycle/follow-up/classification/release-fix, and interactive-link suites, followed by a full discovery guard.
- Source-index exact-line support for attributes, trailing returns, bounded constraints, operators, qualified special members, parenthesized initializer lists, and delegating constructors.
- Negative boundary tests plus bounded telemetry for braced/multiline constructor initializers and constructor function-try-blocks.
- Bounded OpenCL lifecycle-call extractor for direct queue/context creation and retention plus completion/wait and queue/context/program/kernel/event/buffer releases.
- C/C++ comment and quoted-literal masking for lifecycle extraction while preserving exact source offsets and line numbers.
- Function-try initializer-line guard preventing `try : member(...) {` from becoming a false ordinary-function symbol.
- Optional bounded original-source context for every lifecycle record, with exact clamped line ranges and backward-compatible default output.
- GitHub-hosted pinned OpenCL workflow that verifies the exact baseline checkout and preserves the complete source, generated report, wait-group report, generated release-only patch, post-patch report, and SHA-256 manifest.
- Verified OpenCL backend-wrapper order: queue completion occurs before wrapper reference drop, while the actual device/backend context remains process-lifetime.
- Verified OpenCL scheduler events are unsupported and buffer deleters use buffer-local `cl_mem` ownership rather than the destroyed wrapper.
- Resolved optional Adreno binary-library lifetime: the raw loader handle is not retained or closed, so the library, exported lookup function, and accepted binary-kernel path remain process-lifetime.
- Portable OpenCL evidence manifest: artifact-root basenames, pre-upload `sha256sum -c`, and an exact-filename guard make the downloaded artifact directly verifiable after extraction.
- Classified the pinned `transpose_2d()` nonblocking sub-buffer release as locally safe under the official OpenCL memory-object lifetime contract.
- Audited every pinned `transpose_2d*()` call site: all 53 typed-wrapper call sites use `blocking=true`; no caller selects the nonblocking branch.
- Classified the pinned Q4_0 conversion group: both branches wait before releasing temporary `data_device`, but retain the returned command event by omitting `clReleaseEvent(evt)`.
- Completed the full direct-wait pairing audit: 5 of 51 waited events are released, while 46 local command-event references have no release or ownership transfer.
- Resolved `CL_CHECK` failure semantics: any non-success OpenCL status logs, triggers `GGML_ASSERT(0)`, enters `ggml_abort()`, and ends in unconditional `abort()` rather than recoverable error propagation.
- Added a bounded simple-local waited-event diagnostic that machine-checks the pinned 50 simple identifier records, 4 released, and 46 unmatched ownership counts.
- Classified 22 of the 46 unmatched waits as redundant before an immediate same-queue `clEnqueueReadBuffer(..., CL_TRUE, ...)`; 24 waits remained for separate API-contract and consumer-order analysis.
- Added a separate machine-readable blocking-read follow-up annotation and pinned workflow guard for the reviewed 22/24 split without changing event ownership status.
- Added a bounded release-only patch generator that inserts 46 `clReleaseEvent(evt)` calls from the audited report, preserves all 51 waits, emits a unified patch, and CI-validates 50 released / 0 unmatched simple events.
- Classified the remaining 24 waits: 21 are immediately followed by `clReleaseMemObject(data_device)`, 3 end nested lexical scopes, all are inside `ggml_backend_opencl_buffer_set_tensor()`, and no record falls into `other`.
- Added the 21/3 `set_tensor` wait grouping to the pinned workflow and artifact so source drift now fails CI instead of silently invalidating the review.
- Traced the three nested-scope records to MoE scale/min expansion kernels immediately before effective return.
- Compared the pinned generic wrapper, CUDA, and SYCL implementations: ordinary `ggml_backend_tensor_set()` has a strong de facto synchronous completion contract, so all remaining 24 OpenCL conversion/expansion waits are required by the pinned return behavior even though the public header does not state it normatively.
- Added a current-upstream OpenCL lifecycle workflow that resolves an exact master SHA, preserves complete source and reports, generates a current release-only candidate, and uploads a checksummed evidence artifact without freezing counts.
- Audited current upstream revision `505b1ed15ca80e2a19f12ff4ac365e40fb374053`: it retains the same 51 direct waits, 46 unmatched simple event references, and 22/24 follow-up split as the pinned baseline; its generated release-only candidate reaches zero unmatched events without removing synchronization.

## Latest concrete findings

- Current upstream run `29453611188` resolved `505b1ed15ca80e2a19f12ff4ac365e40fb374053` and uploaded evidence artifact `8358479508` with digest `sha256:e2293f8a6aeaaa173c0430f4714d0b83ac564c7e2250298b9a7863338a84c30d`.
- The current source still contains 51 direct `clWaitForEvents()` calls and only six direct `clReleaseEvent()` calls.
- The bounded simple-local diagnostic still reports 50 identifier waits: four released in scope and 46 unmatched.
- The current follow-up split is unchanged: 22 unmatched waits immediately precede same-queue blocking reads and 24 are other synchronous tensor-set waits.
- The current-source patch generator inserts 46 releases; the post-patch report reaches zero unmatched simple waits while preserving every wait.
- The generic `ggml_backend_tensor_set()` wrapper performs direct buffer-interface dispatch and adds no synchronization; each backend owns the completion contract.
- Pinned CUDA enqueues the host-to-device copy and calls `cudaStreamSynchronize(cudaStreamPerThread)` before returning.
- Pinned SYCL waits device queues, waits the submitted copy, and frees its temporary mmap staging buffer only after completion.
- OpenCL's 21 conversion waits and 3 return-boundary expansion waits therefore preserve parity with the pinned synchronous CUDA/SYCL behavior.
- The public header's distinction between ordinary and explicitly asynchronous APIs supports this reading but does not provide a normative prose guarantee.

## In progress

- Reviewing the generated current-source 46-release patch for upstream style and branch context.
- Deciding whether to submit the explicit-release patch directly or open an issue first.
- Deciding whether a move-only event owner is preferable to 46 explicit releases.
- Determining whether repeated OpenCL registration, registry teardown, or shared-library unload is supported.
- Regeneration of the pinned source inventory with line-aware records, pinned source links, and unsupported-syntax counts.
- Implementation of the first CPU repack backend-free-before-buffer-free test fixture under ASan/LSan.
- CPU extra-buffer destruction tests for KleidiAI, AMX, and SpacemiT plus TSan and hardware-specific cleanup coverage.
- Shared generated metadata for the static inference atlas and interactive workflow.
- Runtime overlays for page faults, scheduler copies, event waits, KV/recurrent growth, and backend queues.
- CANN reset semantics, RPC completion, CUDA all-stream coverage, SYCL all-queue coverage, and Vulkan query-pool ownership.

## Immediate next task

```text
Prepare the current-upstream OpenCL ownership correction
  → extract artifact 8358479508 and review all 46 generated insertions
  → verify each insertion follows the exact waited event in current source
  → preserve all synchronization under the de facto synchronous tensor-set contract
  → choose explicit releases versus a small event owner
  → prepare an upstream-ready pull request or issue with pinned and current evidence
```

In parallel or if blocked, implement the admitted CPU repack `MUL_MAT` fixture with reference comparison, CPU backend-wrapper free, repack-buffer free, and ASan/LSan repetition.

## Publication and verification state

- Work is published in PR #1 from branch `automation/backend-teardown-audit-method`.
- Added machine-readable record `data/opencl-current-audit-505b1ed.json`.
- Added detailed note `logs/research/2026-07-16/0152-current-opencl-event-audit-result.md`.
- Updated README living TODOs, this project checkpoint, and the concise research log.
- The research ledger was reviewed and unchanged because no external source changed; this increment used the already-recorded llama.cpp primary source and the repository's generated evidence.
- The required startup files and current repository files were inspected before editing.
- Before durable-context updates, Documentation CI run `29453611196`, pinned OpenCL run `29453611136`, and current-upstream OpenCL run `29453611188` all passed.
- Final-head workflow results must be checked after all durable-context updates.
- Full local checkout validation remains unavailable because direct GitHub DNS resolution is blocked in this runtime and `gh` is not installed.
- Public Pages verification remains blocked for branch-only content until PR #1 merges.

## Known blockers and caveats

- **Systematic OpenCL event leak persists upstream:** current revision `505b1ed1` retains the same 46 unmatched simple waited-event references as the pinned baseline; a generated current-source patch exists but has not been submitted upstream.
- **Synchronous contract status:** CUDA, SYCL, and OpenCL pinned implementations provide completion-before-return for ordinary tensor set, but the public header does not state this guarantee normatively.
- **Synchronization split:** 22 waits are redundant before immediate same-queue blocking reads; the other 24 are required by the pinned de facto synchronous tensor-set return contract.
- **Diagnostic scope:** the simple-local wait/release guard recognizes only literal count-one waits and same-identifier releases in the same lexical brace scope; it is not proof of general C++ ownership.
- **Set-tensor classifier scope:** the classifier is lexical. It reports the immediate next statement and nearest preceding function-shaped declaration; it does not model macros, aliases, branches, dataflow, or the backend API contract.
- **Patch-generator scope:** the generator trusts the reviewed report but verifies the exact wait line and identifier. It does not discover aliases, helper ownership, arrays, or semantic control flow.
- **Follow-up annotation scope:** the annotator requires an immediate semicolon-terminated statement, literal queue name `queue`, and literal `CL_TRUE`; aliases, macros, branches, and general control flow remain human-review work.
- **Fatal-error policy:** `CL_CHECK` terminates via `abort()`; normal C++ destructors and scope guards do not run after a checked failure, so deterministic cleanup is meaningful only on successful paths or after a future nonfatal error redesign.
- **Deterministic-release gap:** the pinned translation unit intentionally keeps device/backend contexts process-lifetime and contains no explicit queue/context release or per-device backend-context deletion path.
- **Adreno library lifetime:** the optional binary-kernel loader loses its raw `dl_handle`. This prevents early unload but omits deterministic release and retains invalid-symbol loads until process exit.
- **Local validation blocker:** direct cloning fails with `Could not resolve host: github.com`, and `gh` is unavailable; GitHub-hosted Actions are the authoritative validation path for this branch.
- **Pages verification blocker:** branch-added content cannot deploy until PR #1 merges; live response verification remains unavailable independently of strict-build success.
- **Dormant-branch caveat:** `blocking=false` is locally retention-safe but has no pinned callers; future revisions must be re-audited if the branch becomes reachable.
- **Retention classification caveat:** `clReleaseMemObject()` safely defers deletion for queued users, but that does not protect event references, unrelated host storage, wrapper callbacks, pooled-region reuse, or missing cross-queue dependencies.
- **Lifecycle-extractor caveat:** selected direct APIs and bounded context are navigation evidence only; wrapper constructors, ownership, error paths, macro wrappers, disabled code, raw strings, and semantic ordering still require human source review.
- **Source-index caveat:** bounded syntax support remains navigation-oriented, not a full C++ parser.
- **Harness caveat:** a skipped hardware-gated path is not evidence that the lifetime ordering passed.
- Mapping, allocation, residency, validity, command completion, event ownership, reset, thread-local leases, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, memory, and teardown ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
