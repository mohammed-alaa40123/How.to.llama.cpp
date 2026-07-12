# CPU, mmap, CUDA, and Metal buffer compatibility

- Run time: 2026-07-12 08:52 Africa/Cairo
- Upstream baseline: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: concrete buffer-level `is_host`, `set_tensor`, `get_tensor`, and blocking `cpy_tensor` behavior for CPU, CPU_Mapped, CUDA device, CUDA host, and Metal capability boundaries

## Verified

- CPU and CPU_Mapped buffers use direct `memcpy()` for set/get.
- CPU_Mapped wraps an external aligned pointer and does not own/free it.
- CPU and CPU_Mapped report `is_host == true`.
- CPU destination `cpy_tensor` accepts host-visible sources.
- CUDA device buffers do not report host visibility.
- CUDA device set/get issue H2D/D2H CUDA copies and synchronize before returning.
- CUDA blocking direct copy accepts CUDA device sources, using same-device D2D or peer copies, and synchronizes before return.
- Generic host-visible paths avoid the emergency full-tensor heap staging branch.
- Metal backend operations remain ordered through command buffers/events; storage mode does not imply completion.

## Interpretation

- `CPU_Mapped` means directly addressable, not physically resident.
- mmap page faults can appear inside CPU_Mapped-to-accelerator transfer time.
- Avoiding generic heap staging does not imply zero-copy or overlap.
- A backend-native blocking copy can still be a synchronization bubble.

## Historical

- Later backends may add registered-host fast paths, staging pools, unified-memory specializations, or broader direct-copy compatibility.

## Open questions

- Exact Metal shared/private buffer-level branches from `ggml-metal-context.m`.
- Concrete Vulkan, SYCL, RPC, CANN, and other backend matrices.
- Runtime page-fault, queue-stall, overlap, and temporary-RSS evidence.

## Artifact

- `docs/lifecycle/buffer-compatibility.md`
- `mkdocs.yml`

## Evidence

- `ggml/src/ggml-backend.cpp`: generic host visibility, CPU/CPU_Mapped operations, direct copy dispatch.
- `ggml/src/ggml-cuda/ggml-cuda.cu`: device set/get/direct copy and CUDA device buffer type.
- Existing Metal backend page and pinned Metal wrapper/context source map.

## Validation

- Connector-side pinned source reads confirmed CPU and CUDA branches and the exact interface registrations.
- Local clone/build remained blocked by DNS resolution of `github.com`.
- GitHub Actions and Pages were checked separately.

## Next step

- Trace Vulkan and SYCL buffer implementations and extend the compatibility matrix with exact host visibility, direct-copy acceptance, synchronization, and staging behavior.