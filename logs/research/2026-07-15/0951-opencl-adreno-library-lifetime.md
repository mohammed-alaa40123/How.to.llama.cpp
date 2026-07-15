# OpenCL Adreno binary-library lifetime resolution

- Run time: 2026-07-15 09:51 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: trace the optional Adreno binary-kernel dynamic-library handle, exported function pointer, binary bytes, OpenCL programs/kernels, and teardown ordering in pinned llama.cpp revision `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Verified

- Under `GGML_OPENCL_USE_ADRENO_BIN_KERNELS`, `ggml_cl_init()` calls `dl_load_library(KERNEL_LIB_NAME)` and stores the result only in block-local raw pointer `kernel_lib_handle`.
- `ggml/src/ggml-opencl/libdl.h` defines `dl_handle_deleter`, which would call `FreeLibrary()` on Windows or `dlclose()` on POSIX, but the pinned loader does not wrap `kernel_lib_handle` in an owning smart pointer and never invokes the deleter.
- On successful lookup, only `get_adreno_bin_kernel_func` is copied into the process-lifetime `ggml_backend_opencl_context`; the library handle itself is neither retained in that object nor closed.
- If the library loads but the `get_adreno_kernels` symbol is missing, the handle is also not closed before the code falls back to built-in kernels.
- The retained function pointer is called later by `get_adreno_bin_kernel()` to obtain a pointer and size for binary bytes.
- Five pinned binary-kernel paths pass those bytes to `clCreateProgramWithBinary()`, create a `cl_kernel`, and immediately release the temporary `cl_program` reference.
- The per-device backend context, its binary-kernel function pointer, and accepted `cl_kernel` objects persist for process lifetime because the context is never deleted in the pinned translation unit.
- No `dlclose()`/`FreeLibrary()` path exists in `ggml-opencl.cpp`; therefore there is no close-before-kernel-destruction ordering risk in the pinned implementation. The library remains loaded until process teardown.

## Interpretation

The optional Adreno binary library has an implicit process-lifetime policy implemented by losing the raw loader handle. This preserves the exported function pointer and any library-owned binary storage for all later lazy kernel lookups, but it is not deterministic ownership. The successful, invalid-symbol, and repeated-initialization cases can all retain a library reference until process exit.

Once `clCreateProgramWithBinary()` has consumed a returned binary and a kernel has been created, the OpenCL kernel's executable lifetime is governed by OpenCL reference counting rather than by the original host binary pointer. However, the library must remain mapped for future calls through `get_adreno_bin_kernel_func`; the pinned leak guarantees that mapping only by omitting unload.

## Historical

Earlier documentation left `dl_handle` ownership and close ordering open because only the large OpenCL translation unit was preserved. Reading the pinned `libdl.h` alongside the preserved source reveals both the available deleter and its non-use.

## Open questions

- Should `ggml_backend_opencl_context` own the dynamic-library handle explicitly with `std::unique_ptr<dl_handle, dl_handle_deleter>` and release it during a new deterministic registry teardown?
- Should the invalid-symbol fallback close the just-opened library immediately?
- Can OpenCL device registration or backend loading execute more than once in one process and increment the loader reference count repeatedly?
- Is shared-library unload of the OpenCL backend officially unsupported, or should an unload-safe registry destructor be added?

## Classification

> **Adreno binary library is process-lifetime by leaked raw handle; close ordering is absent rather than unsafe.**

## Next priority

Classify enqueue-then-release sites that depend only on OpenCL command-retention semantics, beginning with temporary `cl_mem` objects released immediately after kernel enqueue.