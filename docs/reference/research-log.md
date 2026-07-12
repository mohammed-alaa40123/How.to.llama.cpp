# Research log

## 2026-07-12 — Milestone 0/1 start

**Pinned baseline**

- Commit: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Reason: first connector-verified revision used to ground the initial call trace.
- Caution: upstream evolves rapidly; this is a documentation baseline, not a claim that all pages describe the newest commit indefinitely.

**Verified findings**

- The minimal example loads dynamic backends before loading a model.
- It loads the model, tokenizes the prompt, constructs `llama_context`, repeatedly calls decode, samples a token, and feeds a one-token batch back into the loop.
- The model-loading path constructs a loader and architecture-specific model object, selects devices, then loads hyperparameters, vocabulary, statistics, and tensors.
- A source comment explicitly accounts for mmap-deferred page faults in load-time measurement.
- Backend tensor async APIs can fall back to synchronization and synchronous data movement when the backend interface does not implement the async method.

**Interpretations to validate**

- Treat `llama_context` as the active inference runtime boundary, but document its exact ownership graph before presenting this as a formal invariant.
- Treat graph construction, allocation, backend placement, copies, and execution as separate conceptual phases even when some code paths fuse their orchestration.

**Open questions**

- Exact graph reuse compatibility checks at the pinned revision.
- Prompt versus token-generation scheduler reservation strategy.
- Complete memory-module selection by architecture.
- Scheduler copy/event ordering for every backend combination.
- CPU thread-pool work partitioning for major operations and `MUL_MAT_ID`.
- Branches/PRs that materially changed these paths.

**Artifacts created**

- MkDocs project scaffold.
- End-to-end Mermaid diagram.
- Interactive SVG inference explorer prototype.
- Upstream mirror and source-index scripts.
- Pages and refresh workflows.

## 2026-07-12 — Repository publication and durable scheduling context

**Scope**

- Documentation repository: `mohammed-alaa40123/How.to.llama.cpp`
- Process and automation infrastructure rather than upstream runtime behavior.

**Verified changes**

- The root README is now the canonical scheduled-run operating manual.
- Every scheduled workflow invokes `scripts/start_scheduled_run.sh`, which reads the complete README, project state, research log, ledger, and latest detailed research note before work begins.
- `scripts/validate_project_context.py` checks that the durable context contract remains intact.
- GitHub Actions now includes an hourly context check, a daily source-index refresh, and strict MkDocs Pages deployment.

**Interpretation**

- Keeping a small project-state checkpoint plus a concise canonical research log should reduce context loss more effectively than placing every raw note in one growing README.

**Open questions**

- Whether the hourly research executor should eventually create one PR per increment or batch related increments into milestone PRs.
- Whether detailed research logs need a generated index page once their count grows.

**Artifacts changed**

- `README.md`
- `docs/reference/project-state.md`
- `logs/README.md`
- `scripts/start_scheduled_run.sh`
- `scripts/validate_project_context.py`
- `.github/workflows/hourly-context-check.yml`
- `.github/workflows/refresh-source-index.yml`
- `.github/workflows/pages.yml`

**Next step**

- Trace `llama_decode` through context graph construction/reuse and backend scheduler execution at the pinned revision.

## 2026-07-12 01:54 Africa/Cairo — CI and Pages repair

**Scope**

- Repository automation and deployment health for `mohammed-alaa40123/How.to.llama.cpp`.

**Verified findings**

- The documentation corpus builds locally with `mkdocs build --strict`.
- The published repository was missing `docs/assets/interactive/inference-flow.html`, even though the documentation and README referenced it.
- The Pages workflow previously called `actions/configure-pages` unconditionally. The action documents that enabling Pages requires a token stronger than the standard `GITHUB_TOKEN`; therefore a repository with Pages disabled can fail after a successful MkDocs build.
- The repaired workflow separates strict documentation CI from deployment, detects whether Pages is enabled, skips deployment cleanly when it is not, and performs an HTTP/title health check after a successful deployment.

**Interpretation**

- The reported failure was deployment-configuration related rather than a reproducible MkDocs content failure. Independent CI makes that distinction visible.

**Open questions**

- Confirm the new Documentation CI and Deploy documentation runs finish successfully on GitHub.
- Enable Pages in repository settings and confirm the live site returns HTTP 200 with the expected title.

**Artifacts changed**

- `.github/workflows/docs-ci.yml`
- `.github/workflows/pages.yml`
- `scripts/check_site.sh`
- `scripts/validate_project_context.py`
- `docs/assets/interactive/inference-flow.html`
- `README.md`
- `docs/reference/project-state.md`

**Next step**

- Enable GitHub Pages, rerun deployment, verify the website, then continue the pinned `llama_decode` scheduler trace.

## 2026-07-12 02:51 Africa/Cairo — Decode and graph-reuse trace

**Scope**

- Pinned path from the public decode API through graph compatibility, rebuild/allocation, and scheduler submission.

**Verified findings**

- `llama_decode()` delegates directly to `llama_context::decode()`.
- `decode()` initializes the batch allocator, reserves scheduler capacity, applies pending memory work, initializes the active memory batch context, and processes one `llama_ubatch` at a time.
- `process_ubatch()` reuses the previous graph only when graph reuse is enabled and all graph-result/input compatibility checks accept the new graph parameters.
- Pipeline-parallel graph reuse synchronizes before rewriting inputs because a previous asynchronous GPU execution may still read those tensors.
- The rebuild branch resets graph and scheduler state, calls `model.build_graph()`, and allocates the concrete graph with `ggml_backend_sched_alloc_graph()`.
- `graph_compute()` selects the batch or single-token CPU threadpool and submits through `ggml_backend_sched_graph_compute_async()`.
- Scheduler reserve and per-graph allocation are distinct: reserve plans buffer capacity; allocation binds a rebuilt graph into that capacity.

**Interpretation**

- Graph reuse is a topology-and-shape cache, not a token-value or output cache. Compatible graph structure and allocations survive while input tensors are rewritten for each micro-batch.

**Open question**

- Trace scheduler splitting, inter-backend copies/events, split submission, and synchronization after `ggml_backend_sched_graph_compute_async()`.

**Artifacts changed**

- `docs/lifecycle/decode-graph-reuse.md`
- `mkdocs.yml`
- `docs/reference/project-state.md`
- `README.md`
- `logs/research/2026-07-12/0251-decode-graph-reuse.md`

**Next step**

- Document the scheduler split/copy/event execution path at the same pinned revision.

## 2026-07-12 03:52 Africa/Cairo — Backend scheduler split execution

**Scope**

- Pinned `ggml_backend_sched_graph_compute_async()` path through backend assignment, split construction, destination copies, events, submission, and synchronization.

**Verified findings**

- Graph allocation selects a copy-ring slot before splitting and allocating the augmented scheduler graph.
- Backend assignment is multi-pass and treats the final registered backend as the CPU fallback.
- Splits are contiguous graph regions; a new split starts on a backend change and may also start to shorten incompatible weight-copy lifetimes or respect split-input limits.
- Cross-backend sources are replaced with scheduler-owned destination-layout copies, while dependency views keep original source storage alive until the copy completes.
- Execution waits before overwriting a destination copy slot, tries backend asynchronous copy support, and falls back to synchronized tensor copy when needed.
- Each split is submitted with `ggml_backend_graph_compute_async()`, then an event is recorded for the active backend/copy slot.
- The synchronous scheduler wrapper waits for every backend after asynchronous submission.
- The pinned MoE specialization reads routing IDs and copies only used consecutive expert ranges for host-resident `MUL_MAT_ID` weights.

**Interpretation**

- Copy-slot events are reuse fences for scheduler-owned destination storage.
- The MoE specialization reduces transfer volume but is not a persistent expert cache or a guarantee that mmap source pages remain resident.
- Scheduler-level `async` permits but does not guarantee overlap; concrete backend interfaces determine whether execution and copies are truly asynchronous.

**Open questions**

- Which pinned CUDA, Metal, Vulkan, SYCL, and RPC interfaces implement true asynchronous compute, peer copies, and events?
- What overlap is observable in prompt processing versus one-token decode?
- Which later PRs changed copy/event ordering or MoE partial transfers?

**Artifacts changed**

- `docs/lifecycle/backend-scheduler-execution.md`
- `mkdocs.yml`
- `docs/reference/project-state.md`
- `README.md`
- `logs/research/2026-07-12/0352-backend-scheduler-execution.md`

**Next step**

- Compare concrete CPU and one accelerator backend implementations behind graph compute, copies, events, and synchronization.

## 2026-07-12 04:51 Africa/Cairo — CPU and CUDA backend semantics

**Scope**

- Pinned concrete backend behavior behind scheduler graph submission, copies, events, and synchronization.

**Verified findings**

- `ggml_backend_cpu_graph_compute()` creates a CPU plan and returns `ggml_graph_compute()` directly; scheduler submission therefore blocks until the CPU graph completes.
- CPU leaves asynchronous tensor-copy, synchronization, and event callbacks unset at the pinned revision.
- CUDA graph compute queues kernels or launches a captured CUDA graph on a backend stream without a trailing stream synchronization.
- CUDA scheduler events map to `cudaEventRecord` and `cudaStreamWaitEvent`, creating device-side dependencies rather than host waits.
- CUDA ordinary buffer set/get/copy operations use asynchronous CUDA primitives followed by immediate stream synchronization, so those calls remain synchronous to their caller.
- CUDA advertises asynchronous capability and conditionally advertises events depending on peer-copy build configuration.

**Interpretation**

- CPU threadpool parallelism is internal to a blocking graph call and must not be described as scheduler-level asynchrony.
- `ggml_backend_graph_compute_async()` means the generic API does not force global completion; the concrete backend decides whether callback return means completion or only command submission.
- An `Async` API name or `cudaMemcpyAsync` call alone is not proof of host-visible overlap.

**Open questions**

- Exact accepted and rejected branches in `ggml_backend_cuda_cpy_tensor_async()`.
- Metal or Vulkan ordering primitives compared with CUDA streams and events.
- Runtime overlap during prompt processing and token decode on discrete and UMA systems.

**Artifacts changed**

- `docs/lifecycle/cpu-cuda-backend-semantics.md`
- `mkdocs.yml`
- `docs/reference/project-state.md`
- `README.md`
- `logs/research/2026-07-12/0451-cpu-cuda-backend-semantics.md`

**Next step**

- Trace CUDA asynchronous copy branches, then compare one second accelerator backend.

## 2026-07-12 05:50 Africa/Cairo — CUDA asynchronous tensor-copy branches

**Scope**

- Exact pinned acceptance, transfer, ordering, and fallback branches in `ggml_backend_cuda_cpy_tensor_async()`.

**Verified findings**

- The callback resolves tensor views through their owning buffers and requires both backend objects and both resolved buffers to be CUDA device-backed.
- Backend context devices must match the devices recorded by their tensor buffers.
- Same-backend copies queue device-to-device `cudaMemcpyAsync()` on the source stream and rely on same-stream order.
- Different backend objects on one CUDA device queue the copy on the source stream, record a lazily created source-context event, and make the destination stream wait.
- Different CUDA devices use `cudaMemcpyPeerAsync()` when peer copy is enabled; `GGML_CUDA_NO_PEER_COPY` returns `false`.
- CPU/mmap sources, CUDA host buffers, mixed backend pairs, and backend/buffer device mismatches return `false`.
- Accepted branches copy `ggml_nbytes(dst)`, return `true`, and do not host-synchronize.

**Interpretation**

- This is a device-resident fast path rather than a universal host/device async-copy API.
- `true` means the transfer and its dependencies were queued, not that the destination is host-visible.
- `false` is capability negotiation that selects the scheduler's correctness-preserving fallback, though that fallback may introduce synchronization.

**Open questions**

- Exact generic fallback route for CPU/mmap and CUDA-host sources.
- Measured copy/compute overlap during prefill and one-token decode.
- Metal command-buffer and event semantics compared with CUDA source-stream/event/destination-wait ordering.
- Later PRs that changed peer-copy gating, copy-event ownership, or stream selection.

**Artifacts changed**

- `docs/lifecycle/cuda-async-copy.md`
- `mkdocs.yml`
- `docs/reference/project-state.md`
- `README.md`
- `logs/research/2026-07-12/0550-cuda-async-copy.md`

**Next step**

- Trace the pinned Metal backend and build a CUDA-versus-Metal capability comparison.

## 2026-07-12 06:49 Africa/Cairo — Metal backend submission and synchronization

**Scope**

- Pinned Metal graph submission, command-buffer lifecycle, asynchronous blit copies, event ordering, synchronization, and CUDA comparison.

**Verified findings**

- `ggml_backend_metal_graph_compute()` delegates to `ggml_metal_graph_compute()`, whose ordinary path encodes graph regions into one or more `MTLCommandBuffer` objects and returns without waiting for GPU completion.
- The first graph region is encoded by the calling thread while optional dispatch workers encode remaining regions; `cmd_buf_last` tracks the final queued command buffer needed by synchronization.
- Capture/debug execution is exceptional and explicitly waits for completion.
- Metal async set/get operations commit blit command buffers, retain them in `cmd_bufs_ext`, and defer host completion.
- Metal-to-Metal async copy blits the tensor bytes, signals a source-context copy event, commits, and queues a destination-context event wait.
- Event record and wait are themselves command-buffer operations and do not host-wait.
- `ggml_metal_synchronize()` waits for `cmd_buf_last`, checks graph and extra command-buffer status, releases completed extra command buffers, and sets persistent `has_error` after failure.

**Interpretation**

- `cmd_buf_last` is a coarse host-completion fence, while Metal events provide finer queue dependencies.
- Unified memory can reduce transfer cost but does not imply completion, safe reuse, or immediate host visibility.
- Pinned Metal and CUDA expose similar scheduler-visible asynchronous behavior through command buffers/events and streams/events respectively.

**Historical**

- Findings apply to the pinned source baseline; newer Metal queue ownership, event implementation, graph optimization, and multi-device behavior may differ.

**Open questions**

- Exact Metal event primitive and fallback across supported Apple OS/GPU generations.
- Cross-context or multi-device Metal copy legality and performance.
- Measured command-buffer preparation/compute overlap in prefill and one-token decode.
- Later PRs changing `cmd_buf_last`, copy-event ownership, synchronization, or error propagation.

**Artifacts changed**

- `docs/lifecycle/metal-backend-semantics.md`
- `mkdocs.yml`
- `docs/reference/project-state.md`
- `README.md`
- `logs/research/2026-07-12/0649-metal-backend-semantics.md`

**Next step**

- Trace the generic synchronized fallback after a backend asynchronous-copy callback returns `false`, including CPU/mmap, CUDA-host/device, and Metal shared/private combinations.
