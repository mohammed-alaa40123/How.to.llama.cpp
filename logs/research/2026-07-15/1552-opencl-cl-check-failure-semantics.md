# OpenCL `CL_CHECK` failure semantics

- Run time: 2026-07-15 15:52 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Pinned source: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: `CL_CHECK`, `GGML_ASSERT`, `GGML_ABORT`, and `ggml_abort()` behavior relevant to the 46 waited-but-unreleased OpenCL events

## Verified

Pinned `ggml/src/ggml-opencl/ggml-opencl.cpp` defines `CL_CHECK(expr)` as follows:

1. Evaluate the expression into a local `cl_int`.
2. On any result other than `CL_SUCCESS`, emit an error containing the expression, error code, source file, and line.
3. Execute `GGML_ASSERT(0)`.

Pinned `ggml/include/ggml.h` defines:

```c
#define GGML_ABORT(...) ggml_abort(__FILE__, __LINE__, __VA_ARGS__)
#define GGML_ASSERT(x) if (!(x)) GGML_ABORT("GGML_ASSERT(%s) failed", #x)
```

Pinned `ggml/src/ggml.c` implements `ggml_abort()` by formatting the failure, invoking an optional abort callback or printing a backtrace, and then unconditionally calling `abort()`.

Therefore, a failed OpenCL enqueue, wait, release, or other `CL_CHECK` operation does not return an error to the caller, throw a recoverable C++ exception, or continue to later cleanup statements. It terminates the process.

## Interpretation

The earlier concern that adding `clReleaseEvent(evt)` after a successful wait might create a recoverable error path that skips cleanup does not apply to the pinned implementation. There is no continuing error path after a failed `CL_CHECK`; process termination delegates final reclamation to operating-system and driver teardown.

For the existing 46 successful waits, the minimal pinned-compatible correction is therefore straightforward:

```cpp
CL_CHECK(clWaitForEvents(1, &evt));
CL_CHECK(clReleaseEvent(evt));
```

An RAII event wrapper is still useful for maintainability and for future code that may adopt nonfatal error propagation, but it is not required to make the current fatal-error path leak-free. A scope guard cannot execute after `abort()` either.

The two cleanup concerns must remain separate:

- **Successful path:** every application-owned returned event must be released.
- **Fatal failure path:** normal C++ cleanup is not guaranteed because `abort()` does not unwind the stack; the process is ending, so deterministic in-process cleanup is no longer observable.

## Historical

The previous pairing audit left `CL_CHECK` behavior open and therefore treated RAII as potentially required for error safety. Reading the complete pinned macro chain narrows that conclusion: RAII is an engineering improvement, while explicit post-wait release calls are sufficient for the current successful execution paths.

## Open questions

- Which of the 46 waits are unnecessary because a following same-queue blocking operation already supplies host-visible completion?
- Should an upstream patch first add explicit releases with minimal behavioral change, then separately remove proven redundant waits?
- Would maintainers prefer a small move-only `cl_event` owner despite the backend's current fatal error policy?
- Should a source regression test count locally returned events that are waited but not released, while clearly documenting that it is a bounded heuristic rather than full ownership analysis?

## Recommended bounded patch sequence

1. Add `clReleaseEvent(evt)` after all 46 successful waits without changing synchronization.
2. Add a focused static regression that covers the known simple local pattern.
3. Validate model loading and conversion paths with an OpenCL leak checker or vendor tooling.
4. In a separate performance patch, remove only waits proven redundant by a following ordered blocking command.

## Next priority

Classify the 46 waits into **required completion** versus **redundant before a same-queue blocking command**, then prepare the minimal release-only patch as the low-risk first upstream change.