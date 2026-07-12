# Metal backend submission, copies, and synchronization

- Run time: 2026-07-12 06:49 Africa/Cairo
- Upstream baseline: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: pinned Metal graph submission, command-buffer lifecycle, blit copies, event ordering, synchronization, and CUDA comparison

## Verified

- `ggml_backend_metal_graph_compute()` delegates to `ggml_metal_graph_compute()`.
- The ordinary graph path creates multiple `MTLCommandBuffer` objects, encodes an initial graph region on the calling thread, encodes remaining regions through dispatch workers, remembers `cmd_buf_last`, and returns without waiting for GPU completion.
- Capture/debug operation is exceptional: it explicitly waits and checks command-buffer status.
- Async tensor set/get operations use blit command buffers, commit without waiting, retain command buffers in `cmd_bufs_ext`, and update `cmd_buf_last`.
- Metal-to-Metal async copy blits `ggml_nbytes(src)`, signals the source context copy event, commits, and queues a destination-context event wait.
- Event record/wait each create and commit command buffers that encode signal/wait operations; they do not host-wait.
- `ggml_metal_synchronize()` waits on `cmd_buf_last`, checks graph and extra command-buffer completion, releases extra buffers, and sets persistent `has_error` after failure.
- The backend exposes shared and private Metal buffer types through the same copy interface.

## Interpretation

- `cmd_buf_last` is a coarse host-completion fence; Metal events express finer queue dependencies.
- Source copy signal plus destination wait preserves producer/consumer ordering without blocking the CPU.
- Metal's unified-memory environment can reduce data movement but does not eliminate completion, safe-reuse, or host-visibility requirements.
- Pinned Metal and CUDA provide similar scheduler-visible asynchronous behavior through command buffers/events and streams/events respectively.

## Historical

- These findings apply to the pinned source baseline. Newer Metal queue ownership, multi-device behavior, graph optimization, and event code must be compared separately.

## Open questions

- Exact Metal event primitive and fallback behavior across supported Apple OS/GPU generations.
- Legality and performance of cross-context or simulated multi-device Metal blits.
- Measured overlap between command-buffer preparation and GPU execution in prefill versus one-token decode.
- Later PRs changing `cmd_buf_last`, copy-event ownership, synchronization, or error propagation.

## Artifact

- `docs/lifecycle/metal-backend-semantics.md`
- `mkdocs.yml`

## Evidence

- `ggml/src/ggml-metal/ggml-metal.cpp`: backend wrappers and interface registration.
- `ggml/src/ggml-metal/ggml-metal-context.m`: graph command buffers, blits, events, synchronization, and error state.
- Existing CUDA and scheduler pages for comparison.

## Validation

- Connector-side pinned source reads verified the documented wrappers and underlying Objective-C paths.
- Connector-side repository reads will verify publication and navigation.
- GitHub Actions and Pages are checked separately at the end of the run.

## Next step

- Trace the generic synchronized fallback after a backend async-copy callback returns `false`, including CPU/mmap, CUDA-host/device, and Metal shared/private combinations.
