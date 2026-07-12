# Research log

This is the concise chronological ledger. Detailed notes live under `logs/research/`.

## 2026-07-12 — Milestone 0/1 start

**Verified**

- Baseline pinned to `e3546c7948e3af463d0b401e6421d5a4c2faf565`.
- The minimal example loads backends and a model, tokenizes, creates `llama_context`, decodes, samples, and feeds the next token back.
- Model loading dispatches architecture-specific construction, device preparation, metadata, vocabulary, statistics, and tensors.
- Load-time accounting explicitly acknowledges mmap-deferred page faults.

**Open questions**

- Complete graph-reuse predicates, memory-module selection, CPU work partitioning, backend combinations, and version-changing PRs.

## 2026-07-12 — Repository publication and durable context

**Verified**

- The root README is the scheduled-run operating manual.
- Startup reads README, project state, research log, source ledger, and latest detailed note.
- CI includes context validation, source indexing, strict MkDocs validation, Pages deployment, and website health checking.

## 2026-07-12 02:51 — Decode and graph reuse

**Verified**

- `llama_decode()` delegates to `llama_context::decode()`.
- Decode prepares scheduler and memory state and processes `llama_ubatch` units.
- Reuse requires specialized compatibility checks to accept new inputs.
- Pipeline-parallel reuse synchronizes before rewriting inputs.
- Rebuild resets graph/scheduler state, calls `model.build_graph()`, and allocates through the backend scheduler.

**Interpretation**

- Reuse preserves compatible topology and allocation, not token values or outputs.

## 2026-07-12 03:52 — Backend scheduler execution

**Verified**

- Allocation selects a copy-ring slot, assigns backends, builds splits, and allocates destination copies and dependency views.
- Execution waits before slot reuse, tries backend async copy, falls back to synchronized blocking copy, submits splits, and records events.
- Scheduler synchronization waits every backend.
- The pinned `MUL_MAT_ID` path copies selected expert ranges rather than implementing a persistent expert cache.

## 2026-07-12 04:51–06:49 — CPU, CUDA, and Metal semantics

**Verified**

- CPU graph compute blocks inside the threadpool-backed graph call and exposes no scheduler async-copy/event hooks.
- CUDA normally queues kernels and uses events for device-side ordering, while ordinary buffer set/get/direct-copy calls synchronize before return.
- The CUDA scheduler callback accepts only compatible CUDA device-buffer pairs; CPU/mmap and CUDA-host sources are rejected.
- Metal graph work and blits use command buffers and event ordering; explicit synchronization establishes host-visible completion.

**Interpretation**

- Internal parallelism and APIs named `async` do not by themselves prove scheduler-level overlap or host-visible completion.

## 2026-07-12 07:52 — Generic tensor-copy fallback

**Verified**

- Missing or rejected async copy synchronizes both source and destination backends.
- Blocking copy checks host-visible source, host-visible destination, destination direct-copy callback, then full `malloc → get → set → free` staging.
- CPU/mmap-to-accelerator paths may avoid generic heap staging while remaining synchronized and page-fault prone.

**Interpretation**

- Async rejection is a correctness-preserving serialization point.
- No generic heap allocation does not imply zero-copy or overlap.

## 2026-07-12 08:52 — Buffer compatibility foundation

**Verified**

- CPU and CPU_Mapped use direct `memcpy()` operations and report host visibility.
- CPU_Mapped wraps external storage and does not own physical residency.
- CUDA device buffers are not host-visible and establish completion in blocking callbacks.
- Metal storage mode does not remove command-completion requirements.

## 2026-07-12 09:11 — Scheduler figure repair

**Verified**

- A deployed Mermaid renderer failure was replaced with an accessible static SVG preserving allocation, split execution, asynchronous return, and later synchronization.

## 2026-07-12 09:49–10:52 — Vulkan capability and transfer path

**Verified**

- Default Vulkan buffers are not publicly host-visible, even when internally mapped.
- Blocking set/get/copy paths use mapped access or staging with barriers and fence completion.
- Same-device Vulkan and registered Vulkan-host sources can use scheduler asynchronous copy.
- Ordinary CPU/mmap and cross-device Vulkan sources are rejected by the scheduler callback.

**Interpretation**

- Vulkan registration, not generic host visibility, enables the queued host-to-device scheduler path.
- UMA can remove staging without removing synchronization requirements.

## 2026-07-12 11:49 — SYCL buffer and transfer semantics

**Verified**

- Default, split, and optional system-USM buffers report `is_host == false`.
- Dedicated SYCL host buffers inherit CPU host visibility.
- Blocking set/get operations wait; non-Windows set performs a full temporary host copy for the documented mmap/PVC workaround.
- Direct device copy waits devices and uses Level Zero, SYCL peer access, or host-forward staging.
- Backend async set/get queues work, but the pinned scheduler interface installs `cpy_tensor_async = NULL`.

**Interpretation**

- Queue-based explicit async set/get does not imply graph-split tensor-copy overlap.
- Backend-specific staging may occur even when generic emergency staging does not.

**Historical**

- Later revisions may change callback registration, staging, USM, and dependency behavior.

## 2026-07-12 12:52 — SYCL compatibility matrix integration

**Verified**

- The shared buffer matrix now includes CPU/mmap → SYCL, SYCL-host → device, device → CPU, same-device, peer-device, and host-forward paths.
- Every pinned SYCL scheduler split-copy row is asynchronous-copy rejected because the interface callback is `NULL`.
- Same-device and peer copies may use native transfer paths but remain blocking at the scheduler boundary.
- CPU/mmap → SYCL avoids generic emergency staging yet can allocate a full backend temporary buffer on non-Windows.
- Non-peer SYCL device copies use full-size backend host-forward staging.

**Interpretation**

- Generic heap staging, SYCL mmap/PVC staging, and SYCL host-forward staging must be counted separately.
- `generic_heap_staging_used = false` is insufficient evidence that no full-tensor host allocation occurred.
- The absent callback is a likely multi-backend overlap boundary in the pinned revision.

**Historical**

- Findings remain pinned to `e3546c7948e3af463d0b401e6421d5a4c2faf565`.

**Open questions**

- Which later upstream revision first registers or replaces SYCL scheduler tensor-copy asynchrony.
- Whether current PVC and non-Intel runtimes still require the mmap workaround.
- Runtime page faults, temporary RSS, queue waits, and overlap.

## 2026-07-12 13:52 — Documentation quality and interaction roadmap

**Verified**

- Added a canonical roadmap for object-centred documentation, a clickable symbol/source explorer, synchronized diagrams, memory and execution visualizers, page navigation contracts, and pinned-version/backend comparisons.
- Added a ten-part object-page contract covering purpose, creation, ownership, mutation, destruction, lifetime, memory, callers/callees, synchronization, and source evidence.
- Added a website review rubric covering discoverability, source traceability, ownership clarity, memory and synchronization clarity, diagrams, accessibility, cross-links, version clarity, open questions, and next-step guidance.
- Added bounded first implementation slices, beginning with a canonical `llama_context` object page.
- Published the roadmap in MkDocs navigation and linked it from the main implementation roadmap and README context map.
- Added daily website-quality review responsibility to the durable scheduling plan.

**Interpretation**

- Object-centred entry points address a major discoverability gap left by file- and chapter-centred documentation.
- Stable metadata shared by diagrams, object pages, and symbol pages is the most maintainable path to synchronized interactions.

**Historical**

- This extends the original linear end-to-end walkthrough without replacing it; readers will gain multiple entry points into the same pinned evidence.

**Open questions**

- Which interactions can remain static MkDocs assets and which require a generated data bundle or client-side application.
- The first later SYCL scheduler-copy revision remains unresolved because the available code index did not expose a reliable exact commit or PR.

## 2026-07-12 14:55 — Interactive foundations and file-by-file plan

**Verified**

- Added a large interactive foundations explorer with six tabs covering system layers, end-to-end code flow, memory lifecycle, GGUF/graph construction, execution/synchronization, and file groups.
- System layers support hover summaries and click-to-open details for representative symbols, pinned source areas, ownership, and synchronization.
- Added an explicit correction that mmap demand paging and OS reclaim are not equivalent to a universal application-level “load one layer, execute, free it” policy.
- Published the explorer as the first Foundations page and made it the primary homepage entry point.
- Expanded the roadmap with file-by-file inventory, subsystem grouping, cross-file composition, and complete-workflow reconstruction passes.

**Interpretation**

- Foundations need multiple synchronized views because no single linear diagram can explain API control flow, object ownership, virtual memory, graph construction, and backend synchronization simultaneously.
- File listings become useful only after they are synthesized into object, memory, and execution relationships.

**Open questions**

- Identify the exact canonical GGUF image from an authoritative upstream path and verify attribution/license before adding it.
- Replace curated JavaScript data with generated, versioned metadata shared across object pages, source index, and visualizers.
- Add architecture-specific graph-builder, KV/recurrent, MoE, prefill/decode, and runtime-measurement layers.

## 2026-07-12 15:05 — Canonical `llama_context` object page

**Verified**

- Added a source-pinned object page for `llama_context` creation, ownership, lifetime, memory, mutation, decode, threading, synchronization, and teardown.
- The context stores a non-owning model reference while owning mutable runtime state, scheduler resources, outputs, and memory modules.
- The model must outlive every context that references it.
- Published the page under an **Objects** navigation section.

**Interpretation**

- `llama_context` is the mutable execution session around a reusable loaded model.
- Scheduler ownership does not imply ownership or physical residency of mmap-backed model pages.

**Open questions**

- Locate an explicit public thread-safety contract for concurrent context mutation.
- Map every concrete memory-module selection and cleanup completion guarantee.

## 2026-07-12 15:49 — Interactive Context link

**Verified**

- The interactive **llama_context runtime** layer now links to the canonical `llama_context` object page.
- The **Construct context** end-to-end workflow step links to the same page.
- Local canonical-page navigation uses `target="_top"`, so the object page replaces the enclosing MkDocs page instead of opening inside the iframe.
- The explorer now centralizes the pinned upstream baseline, source root, and documentation root in one metadata object.
- Existing six-view coverage remains intact: system layers, workflow, memory, GGUF/graph, synchronization, and file groups.

**Interpretation**

- Linking both the conceptual object node and the concrete construction step creates a better bridge between overview and detailed source-level documentation.
- Centralized in-file metadata reduces duplicated literals but is only an intermediate step toward generated versioned JSON.

**Historical**

- This is the first interactive node-to-canonical-object-page bridge in the project.

**Open questions**

- Which object should be linked next: `llama_model`, scheduler, `ggml_cgraph`, or memory modules.
- Whether CI should parse interactive JavaScript and verify every local page route.

**Artifacts changed**

- `docs/assets/interactive/llama-foundations-explorer.html`
- `README.md`
- `docs/reference/project-state.md`
- `docs/reference/research-log.md`
- `logs/research/2026-07-12/1549-interactive-context-link.md`

**Source ledger**

- No new external source was introduced; the pinned baseline and existing canonical object page were reused.

**Next step**

- Deepen the GGUF format and model-loader chapter and link its interactive tab to the resulting detailed page.
