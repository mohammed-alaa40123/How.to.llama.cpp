# SYCL buffer and transfer semantics

- Run time: 2026-07-12 11:49 Africa/Cairo
- Scope: pinned SYCL allocation, host visibility, blocking and asynchronous copies, cross-device behavior, and scheduler registration
- Baseline: `ggml-org/llama.cpp@e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Verified

### Allocation and visibility

- Default SYCL buffers allocate device memory with `ggml_sycl_malloc_device()` unless large system-USM mode is enabled, the aligned allocation is at least 1 GiB, and the device reports system-USM support.
- System-USM mode uses aligned host allocation, but the default GGML buffer type still leaves `is_host` unset.
- Split buffers explicitly report `is_host == false`.
- The dedicated SYCL host-buffer type wraps aligned host memory with the CPU buffer interface, inherits CPU host visibility, and falls back to an ordinary CPU buffer on allocation failure.

### Blocking operations

- `set_tensor` waits device queues before copying.
- On non-Windows builds it copies the source into a temporary full-size host allocation before a waited host-to-device queue copy; the source comment identifies an mmap/PVC workaround.
- Windows copies directly from the caller pointer and waits.
- `get_tensor` submits device-to-host `memcpy` and waits.
- Blocking direct copy accepts only SYCL-buffer sources, waits both devices, then uses Level Zero, SYCL peer access, or full host-forward staging.

### Backend asynchronous operations

- Backend async set/get callbacks submit stream-zero queue copies without waiting.
- Backend synchronization waits stream zero.

### Scheduler copy boundary

- `ggml_backend_sycl_cpy_tensor_async()` exists in source but is not installed.
- The backend interface sets `.cpy_tensor_async = NULL` with a TODO to update for the new interface.
- Scheduler graph-split copies therefore synchronize source and destination and use the generic blocking path, including for same-device SYCL tensors.

## Interpretation

- System USM changes allocation mechanics but not the public GGML host-visibility contract.
- Non-Windows model loading can incur mmap page faults, a full CPU copy, temporary RSS equal to the tensor, a host-to-device transfer, and a queue wait.
- SYCL peer access may avoid host staging, but the blocking callback still establishes completion before return.
- Queue-based async set/get support does not imply scheduler-level tensor-copy overlap.
- The disabled callback is likely a major performance boundary for multi-backend graph splits at the pinned revision.

## Historical

- Findings are pinned to `e3546c7948e3af463d0b401e6421d5a4c2faf565`.
- Later revisions may register a replacement scheduler callback, add dependency events, remove the mmap/PVC workaround, or alter USM and Level Zero behavior.

## Open questions

- Which upstream revision first restores scheduler-level SYCL tensor-copy asynchrony.
- Whether the mmap staging workaround is still needed on current PVC drivers.
- Runtime page-fault, temporary-RSS, and queue-wait costs during GGUF loading.
- Differences among Level Zero, OpenCL, and non-Intel SYCL runtimes.
- Interaction between stream-zero async set/get and additional internal compute streams.

## Artifacts changed

- `docs/lifecycle/sycl-buffer-capabilities.md`
- `mkdocs.yml`
- `docs/reference/project-state.md`
- `README.md`
- `docs/reference/research-log.md`
- `logs/research/2026-07-12/1149-sycl-buffer-semantics.md`

## Validation

- Connector-side reads verified pinned source branches for allocation, buffer visibility, host-buffer construction, blocking set/get, direct device copy, async set/get, synchronization, and disabled scheduler callback registration.
- Local clone and strict MkDocs validation remain blocked because the execution environment cannot resolve `github.com`.
- GitHub Actions and Pages status were checked separately at the end of the run.

## Next step

- Add exact SYCL rows to the shared compatibility matrix, then identify and compare the first later upstream revision that restores scheduler tensor-copy asynchrony.
