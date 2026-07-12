# SYCL buffer and transfer semantics

> **Source baseline:** llama.cpp commit [`e3546c7948e3af463d0b401e6421d5a4c2faf565`](https://github.com/ggml-org/llama.cpp/commit/e3546c7948e3af463d0b401e6421d5a4c2faf565)

This page documents the pinned SYCL backend's memory ownership, host visibility, blocking buffer operations, backend-level asynchronous set/get callbacks, direct device copies, and the scheduler-copy limitation that matters most for graph splitting.

## Five-minute explanation

The pinned SYCL backend exposes several memory paths that must not be conflated:

1. **Default SYCL device buffers** normally allocate device USM with `ggml_sycl_malloc_device()` and report `is_host == false`.
2. **Optional large USM-system buffers** allocate aligned host memory when `GGML_SYCL_USM_SYSTEM` is enabled, the allocation is at least 1 GiB, and the device advertises system-USM support. Even then, the public GGML buffer type still reports `is_host == false`.
3. **SYCL host buffers** are aligned host allocations wrapped with the CPU buffer interface. They report host visibility and fall back to an ordinary CPU buffer if allocation fails.
4. **Blocking set/get operations** wait before returning. On non-Windows model loading, `set_tensor` first copies mmap-backed bytes into a temporary host allocation as a workaround for a PVC mmap issue.
5. **Blocking direct copies** accept SYCL-buffer sources. They wait both devices before copying, use direct Level Zero or SYCL peer access when possible, and otherwise stage the full tensor through a temporary host allocation.
6. **Backend `set_tensor_async` and `get_tensor_async`** enqueue queue copies without waiting. Completion is established by backend synchronization.
7. **Scheduler `cpy_tensor_async` is disabled in the backend interface at the pinned revision.** A helper function exists, but the interface installs `NULL`, so graph-split copies fall through the generic synchronized blocking path.

The last point is the most important: queue-based asynchronous primitives exist, but the scheduler cannot use them for tensor-to-tensor split copies in this revision.

## Allocation and ownership

### Verified

The default buffer allocator rounds large allocations to a 2 MiB boundary when deciding whether to use system USM. System USM is selected only when all of the following are true:

- `g_ggml_sycl_usm_system` is enabled;
- the aligned allocation is at least 1 GiB;
- the selected device reports `usm_system_allocations` support.

When selected, the backend uses aligned host allocation and later frees it with `free_aligned_mem_host()`. Otherwise it calls `ggml_sycl_malloc_device()` and frees through the SYCL device allocator.

The default and split buffer types report `is_host == false`. This remains true for the optional system-USM allocation because host accessibility of the underlying allocation is not exposed through the generic GGML buffer capability.

The dedicated SYCL host-buffer type:

- allocates aligned host memory;
- wraps it with `ggml_backend_cpu_buffer_from_ptr()`;
- inherits CPU set/get/copy behavior and CPU `is_host`;
- substitutes a SYCL-specific free callback;
- falls back to the ordinary CPU buffer type if allocation fails.

### Interpretation

System USM and GGML host visibility answer different questions. System USM may permit device access to host-backed virtual addresses, while `is_host` controls whether generic GGML code may directly dereference the public tensor pointer.

## Blocking set and get

### Verified

`ggml_backend_sycl_buffer_set_tensor()` first waits all device queues. On non-Windows builds it then:

```text
malloc(size)
  -> memcpy(mmap-or-host source, temporary host buffer)
  -> queue.memcpy(device destination, temporary host buffer).wait()
  -> free(temporary host buffer)
```

The source comment identifies this as a workaround for an mmap issue on Intel PVC GPUs during model loading.

On Windows, the function copies directly from the caller's pointer to the destination and waits.

`ggml_backend_sycl_buffer_get_tensor()` submits device-to-host `queue.memcpy()` and immediately waits.

Therefore both buffer callbacks establish completion before returning.

### Interpretation

For mmap-backed model loading on non-Windows systems, SYCL can transiently duplicate every copied tensor in pageable host memory even though the generic GGML fallback did not allocate its emergency staging buffer. This backend-specific staging can add:

- mmap page faults and storage reads;
- one full host `memcpy()`;
- temporary RSS equal to the copied tensor;
- a host-to-device queue copy;
- a queue wait before return.

## Blocking direct tensor copy

### Verified

The destination-buffer `cpy_tensor` callback accepts only sources whose buffers are recognized as SYCL buffers.

Before copying, it waits queues for both source and destination devices. It then calls `dev2dev_memcpy()`:

1. When configured for Level Zero and both devices are compatible discrete GPUs, it attempts an immediate Level Zero memory copy.
2. Otherwise, when SYCL peer access is supported, it submits `q_dst.memcpy(...).wait()`.
3. Otherwise it allocates a full-size host buffer, waits a device-to-host copy, waits a host-to-device copy, and frees the temporary buffer.

The callback returns `true` only after the selected path has completed.

### Interpretation

Cross-device compatibility is broader than cross-device overlap. The host-forward path is functionally valid but serializes both devices and transiently duplicates the tensor in host RAM.

## Backend asynchronous set and get

### Verified

The backend interface installs `ggml_backend_sycl_set_tensor_async()` and `ggml_backend_sycl_get_tensor_async()`.

Each callback:

- requires the tensor to reside in the selected device's default SYCL buffer type;
- submits `queue.memcpy()` on stream zero;
- does not call `wait()` before returning.

`ggml_backend_sycl_synchronize()` waits that stream, establishing completion for previously queued copies and graph work on it.

### Interpretation

These callbacks are genuinely asynchronous with respect to the host return boundary, but only for explicit backend set/get operations. Their presence does not imply scheduler tensor-to-tensor copy support.

## Scheduler tensor-copy boundary

### Verified

A function named `ggml_backend_sycl_cpy_tensor_async()` exists and would enqueue a copy when the destination belongs to the backend's default SYCL buffer type and the source is a SYCL buffer.

However, the pinned backend interface contains:

```cpp
/* .cpy_tensor_async = */ NULL, // ggml_backend_sycl_cpy_tensor_async,
                                   // TODO: update for the new interface
```

Consequently, `ggml_backend_tensor_copy_async()` sees no SYCL scheduler callback. For graph-split input copies it must synchronize source and destination backends and use the generic blocking tensor-copy decision tree.

Effective pinned paths include:

| Source | Destination | Scheduler async accepted? | Blocking path |
|---|---|---:|---|
| CPU or mmap | SYCL device | No | generic host-source branch → SYCL `set_tensor`; non-Windows adds backend temporary host staging |
| SYCL host buffer | SYCL device | No | generic host-source branch → SYCL `set_tensor` |
| SYCL device | CPU | No | generic host-destination branch → SYCL `get_tensor` |
| SYCL device | same-device SYCL device | No | synchronized SYCL direct copy |
| SYCL device | peer-accessible SYCL device | No | synchronized peer/Level Zero direct copy |
| SYCL device | non-peer SYCL device | No | synchronized full-size host-forward staging |

### Interpretation

The scheduler-level performance consequence is stronger than the buffer implementation alone suggests. Even same-device SYCL tensor copies cannot overlap through the generic scheduler interface at this revision because the callback registration is absent.

## Queue, graph, and completion caveats

### Verified

The graph path enqueues operations through the SYCL backend and later relies on backend synchronization for host-visible completion.

The optional SYCL command-graph path rejects several operations whose implementations perform host waits or unsupported allocations while recording, including `MUL_MAT_ID`, `CONCAT`, and some `MUL_MAT` configurations.

### Interpretation

A backend may support asynchronous queue submission while still disabling graph capture for operations containing host waits. Queue asynchrony, scheduler-copy asynchrony, and command-graph compatibility are three independent capabilities.

## Truth-labelled summary

### Verified

- Default and split SYCL buffers report `is_host == false`.
- Large optional system-USM allocation does not change that GGML capability bit.
- The dedicated SYCL host buffer inherits CPU host visibility.
- Blocking set/get callbacks wait before returning.
- Non-Windows `set_tensor` performs a full temporary host copy for mmap/PVC compatibility.
- Blocking device copies wait both devices and use Level Zero, SYCL peer copy, or full host forwarding.
- Backend async set/get callbacks enqueue without waiting.
- Backend synchronization waits stream zero.
- Scheduler `cpy_tensor_async` is not registered at the pinned revision.

### Interpretation

- SYCL can incur backend-specific full-tensor host staging even when the generic fallback avoids its own emergency staging allocation.
- Optional system USM changes allocation mechanics, not the generic buffer's public host-visibility contract.
- Existing asynchronous set/get functions do not provide graph-split tensor-copy overlap.
- Peer-access support avoids host staging but the blocking callback still establishes completion before returning.

### Historical

These findings apply to `e3546c7948e3af463d0b401e6421d5a4c2faf565`. Later revisions may register the scheduler callback, alter mmap staging, use dependency events, broaden USM modes, or change Level Zero interoperability.

### Open questions

- Which upstream revision first re-enables or replaces SYCL scheduler `cpy_tensor_async`.
- Whether the temporary mmap staging workaround is required on current PVC drivers and non-Intel SYCL implementations.
- Actual temporary-RSS and page-fault cost while loading GGUF tensors through the non-Windows path.
- Queue ordering when graph execution, async set/get, and multiple internal streams interact.
- Runtime differences among Level Zero, OpenCL, and other SYCL backends.

## Pinned source map

| Concern | Source |
|---|---|
| Device capability and system-USM detection | [`ggml-sycl.cpp`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-sycl/ggml-sycl.cpp#L98-L170) |
| Buffer ownership and default allocation | [`ggml-sycl.cpp`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-sycl/ggml-sycl.cpp#L480-L500) and [`#L839-L892`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-sycl/ggml-sycl.cpp#L839-L892) |
| Blocking set/get | [`ggml-sycl.cpp`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-sycl/ggml-sycl.cpp#L585-L628) |
| Blocking device copy | [`ggml-sycl.cpp`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-sycl/ggml-sycl.cpp#L641-L742) |
| Host-buffer type | [`ggml-sycl.cpp`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-sycl/ggml-sycl.cpp#L1411-L1454) |
| Backend async set/get and synchronization | [`ggml-sycl.cpp`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-sycl/ggml-sycl.cpp#L5230-L5307) |
| Disabled scheduler async copy registration | [`ggml-sycl.cpp`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-sycl/ggml-sycl.cpp#L5470-L5478) |
