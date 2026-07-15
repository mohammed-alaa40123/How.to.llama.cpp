# OpenCL nested-scope wait trace

- Run time: 2026-07-15 22:49 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Pinned source: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Scope: trace the three `nested_scope_exit` waits inside `ggml_backend_opencl_buffer_set_tensor()`

## Verified

The source-bearing artifact from successful workflow run `29442575118` identifies the three waits at pinned lines 8303, 8709, and 9089. Direct source inspection resolves all three branches:

| Line | Tensor path | Expansion kernel | Device outputs | Operation after nested scope |
|---:|---|---|---|---|
| 8303 | Adreno Q5_0 generic dp4a MoE path | `kernel_moe_expand_scale_q5_0` | `extra->scale`, `extra->min` | outer branch returns from `ggml_backend_opencl_buffer_set_tensor()` |
| 8709 | Q8_0 generic dp4a MoE path | `kernel_moe_expand_scale_q8_0` | `extra->scale` | optional transpose block is mutually exclusive because expansion requires `ne[2] > 1` while transpose asserts `ne[2] == 1`; function then returns |
| 9089 | Adreno Q5_K generic dp4a MoE path | `kernel_moe_expand_scale_q5_K` | `extra->scale`, `extra->min` | outer branch returns from `ggml_backend_opencl_buffer_set_tensor()` |

All three events are local command events. Each kernel is enqueued on the backend's single in-order queue, followed by `clWaitForEvents(1, &evt)`, and the event reference is not released in the pinned source.

The public pinned backend header distinguishes explicitly asynchronous tensor-set functions from `ggml_backend_tensor_set()`, but its declaration comment only defines the meaning of `offset`; it does not state a device-output-completion guarantee for the synchronous form.

## Interpretation

These three waits are best classified as **return-boundary completion waits**:

```text
conversion kernel produces persistent device-side auxiliary buffers
        ↓
optional MoE scale/min expansion kernel
        ↓
clWaitForEvents()
        ↓
set_tensor branch returns
```

They are not protecting a temporary `cl_mem` release, host-input lifetime, a following host read, or a cross-queue dependency. Their only observable effect is to ensure the auxiliary expansion kernel has completed before `ggml_backend_opencl_buffer_set_tensor()` returns.

For later graph execution on the same queue, explicit waiting is not required for device ordering: subsequent consumers are naturally ordered after the expansion kernel. Removing these waits would therefore preserve same-queue consumer correctness, but would change the point at which the synchronous tensor-set call returns relative to device completion.

The strongest current classification is:

- **Required** if the synchronous tensor-set API promises that all backend conversion and auxiliary materialization is complete at return.
- **Redundant for same-queue consumers** if the contract only requires the upload/conversion commands to be enqueued before return.
- **Contract-dependent overall** because the pinned public header does not state the stronger completion guarantee.

The event-ownership defect is independent: whether the waits remain or are later removed, every event requested from the command enqueue must either be released or not created.

## Historical

The previous 21/3 lexical classifier called these sites `nested_scope_exit`. This source trace narrows that generic label: all three scopes end immediately before their tensor-type branch returns, and all three kernels materialize persistent MoE auxiliary scale/min buffers.

## Open questions

- Do tests or callers observe immediate device completion from synchronous `ggml_backend_tensor_set()`, or only safe host-buffer reuse and later ordered consumption?
- Do other accelerator backends synchronize their internal conversion kernels before synchronous tensor-set return, establishing a de facto cross-backend contract?
- Should the classifier rename these three records to `return_boundary_expansion_completion` and record tensor type plus output buffers?
- Should upstream first land the behavior-preserving 46-event release patch, leaving synchronization unchanged, before considering removal of any waits?

## Validation

- Downloaded artifact `8354046371` from workflow run `29442575118`.
- Verified the artifact contains the exact pinned source and the 21/3 wait-group JSON.
- Inspected bounded source windows around lines 8303, 8709, and 9089.
- Confirmed PR #1 was open and mergeable before this commit.
- Local cloning remains blocked by `Could not resolve host: github.com`; GitHub-hosted Actions remain authoritative.

## Next priority

Compare the synchronous tensor-set behavior of at least two other accelerator backends and the generic wrapper implementation. Use that evidence to decide whether these three return-boundary waits—and then the 21 temporary-input-release waits—are required or contract-dependent. Keep the generated release-only ownership patch separate from any synchronization optimization.
