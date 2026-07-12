# SYCL compatibility matrix integration

- Run time: 2026-07-12 12:52 Africa/Cairo
- Baseline: `ggml-org/llama.cpp@e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: merge exact pinned SYCL source/destination paths into the shared buffer-compatibility artifact

## Verified

- Default, split, and optional system-USM SYCL buffers report `is_host == false` through the public GGML buffer interface.
- The dedicated SYCL host buffer inherits CPU buffer operations and host visibility.
- The pinned SYCL backend interface installs `cpy_tensor_async = NULL`; graph-split tensor copies therefore synchronize source and destination and use blocking generic dispatch.
- CPU/mmap to SYCL reaches the host-source branch and calls SYCL `set_tensor`.
- On non-Windows builds, that SYCL write allocates a full-size temporary host buffer, copies the source into it, submits a host-to-device queue copy, waits, and frees the allocation.
- SYCL device to CPU reaches the host-destination branch and performs a waited device-to-host copy.
- Same-device and peer-accessible SYCL copies use the backend direct-copy callback but remain blocking at the scheduler boundary.
- When Level Zero and SYCL peer paths are unavailable, the backend performs full-size host-forward staging.

## Interpretation

- Generic emergency staging and backend-specific SYCL staging are separate events and must be measured separately.
- A trace reporting no generic `malloc → get → set → free` allocation can still hide a full-tensor SYCL temporary allocation.
- The absent scheduler callback is a likely overlap boundary for multi-backend graphs even when a native peer path exists.

## Historical

- Findings are pinned to `e3546c7948e3af463d0b401e6421d5a4c2faf565`.
- Later revisions may register a replacement callback, add event dependencies, pool temporary buffers, or remove the mmap/PVC workaround.

## Open questions

- Which later upstream revision first restores scheduler-level SYCL tensor-copy asynchrony.
- Whether current PVC and non-Intel runtimes still require the non-Windows temporary host copy.
- Measured page faults, temporary RSS, queue waits, and overlap for model loading and graph-split copies.

## Artifact changed

- `docs/lifecycle/buffer-compatibility.md`

The shared page now contains exact CPU/mmap, SYCL-host, same-device, peer-device, and host-forward rows; a separate staging taxonomy; completion semantics; and additional runtime fields.

## Source changes

- No new external source was added. Existing pinned llama.cpp source links were reused, so `docs/reference/research-ledger.md` did not change.

## Validation

- Connector-side source reads verified the previously documented pinned branches.
- Repository cloning remains unavailable in the execution container because `github.com` DNS resolution fails.
- GitHub Actions and the public Pages site are checked separately after publication.

## Next step

- Identify the first later upstream revision that registers or replaces the SYCL scheduler tensor-copy callback and compare dependency and completion semantics.
