# Backend scheduler Pass A

- Run time: 2026-07-13 06:49 Africa/Cairo
- Scope: bounded file-by-file and subsystem inventory for GGML backend scheduler internals
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Added `docs/architecture/backend-scheduler-pass-a.md` and linked it under Architecture navigation.

The page connects:

```text
ggml_cgraph
→ backend assignment
→ contiguous splits
→ incompatible cross-backend inputs
→ per-backend/per-copy-slot destination tensors
→ augmented allocation graph
→ event or synchronized copy readiness
→ asynchronous split submission
→ event record
→ graph-allocation and copy-slot reuse
→ synchronization and teardown
```

## Verified

- `ggml_backend_sched` owns backend and buffer-type references, graph allocator state, tensor-backend IDs, tensor-copy pointers, split records, previous assignments, temporary GGML context storage, copy-slot indices, and backend events.
- Backend assignment preserves preallocated constraints, follows compatible weight placement, expands supported accelerator regions, assigns remaining nodes by supported inputs, and uses CPU as the lowest-priority fallback.
- Splits are contiguous backend-specific graph intervals, not global groups of every node assigned to one backend.
- Incompatible split inputs receive destination-layout tensors indexed by source tensor, destination backend, and copy slot.
- Dependency views keep original source allocations live until copies complete.
- Copy tensors are scheduler execution storage rather than model-owned weights or context-owned KV/recurrent state.
- `GGML_TENSOR_FLAG_INPUT` invokes a stricter capture path because caller-owned input storage may be overwritten after the asynchronous scheduler call returns.
- Asynchronous peer-copy failure falls back only after relevant source/destination synchronization.
- Events fence copy-slot reuse; graph reallocation synchronizes because queued work may still reference old split-input storage.
- The synchronous scheduler wrapper submits asynchronously and then synchronizes all registered backends.
- The pinned `GGML_OP_MUL_MAT_ID` path can transfer only selected expert ranges from host-resident weights to an offloaded destination.

## Interpretation

- Scheduler placement is constrained operation placement, not merely a direct reflection of `n_gpu_layers`.
- Destination allocation, current-generation byte validity, and prior-consumer completion are separate conditions.
- Copy-slot events are reuse fences, not just timing markers.
- Graph-allocation reuse preserves compatible structure, not input values, destination-copy generations, outputs, or sequence state.
- The selected-expert transfer specialization is transfer-volume optimization, not a persistent expert-cache policy.

## Historical

- PR #20793 documents synchronization and pipeline-parallel history.
- PR #25319 discusses newer asynchronous scheduler memory-copy work.
- Both are useful design history but cannot replace behavior pinned to `e3546c7`.

## Open questions

- Which concrete CPU, CUDA, Metal, Vulkan, SYCL, RPC, CANN, and OpenCL backends implement asynchronous peer copy and real event primitives at the pinned revision?
- How often do representative prefill and decode graphs force scheduler reallocation?
- How much transfer overlap occurs, and how frequently does fallback synchronization execute?
- What instrumentation can expose split timing, copy generation, bytes, event waits, and fallback paths with low perturbation?
- Which later commits changed partial MoE transfer and destination-copy validity?

## Sources inspected

Repository context:

- complete `README.md`;
- `docs/reference/project-state.md`;
- `docs/reference/research-log.md`;
- `docs/reference/research-ledger.md`;
- latest detailed note `logs/research/2026-07-13/0552-system-ownership-execution-map.md`;
- current `mkdocs.yml`;
- existing scheduler execution, generic-copy fallback, buffer compatibility, memory-lifetime, and system-ownership pages.

Pinned upstream source:

- `ggml/src/ggml-backend.cpp`;
- `ggml/include/ggml-backend.h`;
- `ggml/src/ggml-alloc.c`.

Historical sources already present in the ledger:

- llama.cpp PR #20793;
- llama.cpp PR #25319.

No new external source was introduced, so `docs/reference/research-ledger.md` was unchanged.

## Validation

- GitHub connector writes succeeded for the page, navigation, README, project state, research log, and this detailed note.
- Connector-side re-fetch is required to confirm the final published content.
- Local validation remains blocked because no usable local checkout is available in this execution environment.
- GitHub Actions and Pages verification are performed after the final commit; exact results or blockers are recorded in project state and README TODOs.

## Next priority

Enumerate every concrete `llama_memory_i` and `llama_memory_context_i` implementation and map architecture factories to ordinary KV, recurrent, hybrid, iSWA, and specialized memory.
