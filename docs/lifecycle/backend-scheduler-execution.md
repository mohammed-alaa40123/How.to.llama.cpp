# Backend scheduler splits, copies, and synchronization

> **Source baseline:** llama.cpp commit [`e3546c7948e3af463d0b401e6421d5a4c2faf565`](https://github.com/ggml-org/llama.cpp/commit/e3546c7948e3af463d0b401e6421d5a4c2faf565)
>
> This page describes the scheduler implementation in `ggml/src/ggml-backend.cpp` at that revision. Later scheduler work must be documented separately rather than silently merged into this account.

## Five-minute explanation

A GGML graph can contain nodes assigned to different execution backends. The scheduler therefore does more than call one `compute()` function:

1. assign every graph node and source tensor to a backend;
2. divide the graph into contiguous backend-specific **splits**;
3. create backend-local copies for inputs that cannot be consumed in-place;
4. allocate the original tensors, copy tensors, and dependency views;
5. before each split runs, populate its backend-local inputs;
6. wait until the selected copy slot is no longer in use;
7. submit the split to its backend;
8. record an event so that the copy slot can be reused safely later.

The public asynchronous entry point returns after submitting the work. A later scheduler synchronization, an explicit event dependency, or a backend-specific synchronization point makes results safe to read or buffers safe to overwrite.

## The execution path

```mermaid
sequenceDiagram
    participant C as llama_context
    participant S as GGML backend scheduler
    participant A as graph allocator
    participant Src as source backend
    participant Dst as split backend

    C->>S: ggml_backend_sched_graph_compute_async(graph)
    alt graph not allocated
        S->>S: ggml_backend_sched_alloc_graph(graph)
        S->>S: choose cur_copy; advance next_copy
        S->>S: assign backends and split graph
        S->>A: allocate graph, copies, dependencies
    end

    loop each backend split
        loop each cross-backend input
            S->>Dst: wait for cur_copy slot
            alt backend supports async peer copy
                S->>Dst: cpy_tensor_async(source, copy)
            else fallback
                S->>Src: synchronize source backend
                S->>Dst: synchronize copy slot/backend
                S->>Dst: synchronous tensor copy
            end
        end
        S->>Dst: ggml_backend_graph_compute_async(split graph)
        S->>Dst: record event for cur_copy
    end

    S-->>C: submission status
    C->>S: synchronize when outputs must be visible
    S->>Dst: synchronize every backend
```

## Allocation-time work versus execution-time work

The scheduler has two related but separate phases.

### Allocation time

`ggml_backend_sched_alloc_graph()` selects the current copy index, advances the ring index, calls the graph-splitting machinery, and allocates the resulting augmented graph.

The split pass:

- assigns nodes to backends using existing tensor placement, operation support, backend priority, and compatible buffer types;
- starts a new split when the backend changes;
- may also start a new split when incompatible offloaded weights should be released earlier or the split-input limit would be exceeded;
- replaces incompatible cross-backend sources with a backend-local tensor copy;
- inserts dependency views so the original source remains alive until its copy completes;
- inserts copy tensors early in the augmented graph so the allocator gives them storage before split execution.

### Execution time

`ggml_backend_sched_compute_splits()` iterates over the already-built split list. For each split, it copies or refreshes required inputs, submits the split graph, and records an event for the active copy slot.

This means the scheduler does **not** rediscover graph topology for each individual split submission. The split structure and copy tensors are prepared during graph allocation; execution fills and consumes that prepared structure.

## How backend assignment becomes a split

### Verified

Backend assignment is multi-pass:

1. use existing tensor/backend constraints and operation support;
2. expand non-CPU backend assignments across adjacent compatible nodes;
3. assign remaining nodes to the backend supporting the largest number of their inputs, or upgrade them to a higher-priority backend sharing a compatible buffer type;
4. propagate placement through views and still-unassigned sources;
5. walk nodes in graph order and create contiguous splits.

The last backend in the scheduler array is asserted to be the CPU backend and acts as the fallback. Non-CPU backends are considered higher priority during the expansion pass.

### Interpretation

A split is best understood as a contiguous execution island, not as an arbitrary set of all nodes assigned to one device. The same backend may appear in multiple splits when another backend lies between its regions or when memory/input constraints force an additional boundary.

## Cross-backend copy ownership

### Verified

For a source tensor that is incompatible with the destination split backend, the scheduler creates one destination-layout tensor per copy slot. These tensors are owned by the scheduler's temporary GGML context and allocated through the scheduler graph allocator on the destination backend's buffer type.

The original tensor remains the source of truth. The split's node input is rewritten to point to the destination copy for `cur_copy`.

A dependency view of the original source is added to the augmented allocation graph so the allocator cannot reclaim or reuse source storage before the copy is complete. The destination copy is also added before the split nodes so it is allocated at the beginning of the split lifetime.

### Interpretation

The copy tensor is not a persistent model-weight duplicate in the model object. It is scheduler-managed execution storage whose lifetime follows the allocated scheduler graph and copy-slot ring.

## Why there are multiple copy slots

When pipeline parallelism is disabled, the scheduler uses one copy slot. When enabled, it uses `GGML_SCHED_MAX_COPIES` slots and creates backend events for each backend/slot pair.

`ggml_backend_sched_alloc_graph()` chooses `cur_copy = next_copy` and advances `next_copy` modulo the number of slots. Before overwriting a destination copy, execution waits for the event associated with that backend and slot. After submitting a split that consumed copied inputs, it records a new event into the same slot.

### Interpretation

The ring allows a later graph invocation to prepare one input copy while earlier work may still be executing with another copy. The event is therefore a reuse fence for scheduler-owned input storage, not merely a timing marker.

## User inputs are handled differently

### Verified

If a split input has `GGML_TENSOR_FLAG_INPUT`, the scheduler first synchronizes the destination copy slot and then performs an immediate tensor copy. The source comment states the reason: user-owned input data might be overwritten after the scheduler call returns.

Other split inputs may use backend-to-backend asynchronous copy support. If the destination backend does not implement a usable asynchronous copy path, the scheduler synchronizes the source backend and destination slot/backend before using the synchronous tensor-copy fallback.

### Interpretation

The input flag changes the ownership assumption. For ordinary internal tensors, backend ordering can preserve the source until the transfer is launched. For user inputs, the scheduler defensively captures the value before control returns to code that may reuse the original memory.

## MoE weight-copy specialization

### Verified

At the pinned revision, the split executor contains a special case for host-resident weight tensors consumed by `GGML_OP_MUL_MAT_ID` on an offloaded backend. It reads the expert-ID tensor, builds a bitset of used experts, groups consecutive expert IDs, and copies only those expert ranges into the destination weight copy. A small padding region may also be copied for CUDA MMQ correctness.

This path introduces explicit synchronization while reading routing IDs: the source weight backend and the backend holding the ID tensor are synchronized before host-side ID inspection completes.

### Interpretation

This is transfer-volume optimization, not an expert cache policy. The scheduler still refreshes the active destination copy for the selected experts; it does not by itself define long-lived LRU admission or prove physical residency of mmap-backed source pages.

## Submission and output visibility

### Verified

For each split, the normal path calls `ggml_backend_graph_compute_async(split_backend, &split->graph)`. If an evaluation callback is installed, the scheduler may submit smaller graph views and synchronizes after each view so callback-visible tensor data is ready.

`ggml_backend_sched_graph_compute_async()` returns the submission/error status without globally synchronizing. The synchronous wrapper `ggml_backend_sched_graph_compute()` calls the asynchronous function and then `ggml_backend_sched_synchronize()`, which synchronizes every registered backend.

### Interpretation

"Async" is an API-level promise that global completion is not forced by the scheduler wrapper. Actual overlap depends on each backend implementation. A backend may implement an asynchronous queue, or its interface may fall back to synchronous work.

## CPU-only versus multi-backend execution

| Case | Splits | Cross-backend copies | Events/copy ring | Practical behavior |
|---|---:|---:|---:|---|
| CPU-only, non-parallel | Usually one | None for ordinary graph edges | One slot; no useful pipeline overlap | Scheduler mainly performs allocation and calls the CPU backend |
| CPU plus accelerator, non-parallel | One or more | Required at incompatible placement boundaries | One slot | Boundaries can synchronize and copy before accelerator/CPU splits |
| Pipeline-parallel multi-backend | One or more | Same logical boundaries, with per-slot copies | Multiple slots and backend events | Later invocations can reuse different copy storage while earlier work is in flight |
| Evaluation callback enabled | Split may be subdivided into graph views | Same input preparation | Backend synchronized for callback visibility | Observability reduces asynchronous freedom |

## Failure and fallback behavior

### Verified

- If graph allocation fails, the asynchronous scheduler entry point returns `GGML_STATUS_ALLOC_FAILED`.
- If a split backend returns a non-success status, split execution stops and returns that status.
- A failed asynchronous peer copy falls back to explicit source and destination synchronization followed by `ggml_backend_tensor_copy()`.
- If graph allocation must be redone, all backends are synchronized first because reallocation may move split-input storage.

## Source map

| Concern | Pinned source symbol |
|---|---|
| Public async scheduler entry | `ggml_backend_sched_graph_compute_async()` |
| Synchronous wrapper | `ggml_backend_sched_graph_compute()` |
| Graph allocation and copy-slot selection | `ggml_backend_sched_alloc_graph()` |
| Backend assignment and split construction | `ggml_backend_sched_split_graph()` |
| Allocation/reallocation | `ggml_backend_sched_alloc_splits()` |
| Copy, submit, and event loop | `ggml_backend_sched_compute_splits()` |
| Global completion | `ggml_backend_sched_synchronize()` |
| Scheduler creation and event allocation | `ggml_backend_sched_new()` |

All symbols above are in [`ggml/src/ggml-backend.cpp`](https://github.com/ggml-org/llama.cpp/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/ggml/src/ggml-backend.cpp).

## Open questions

- Which concrete CUDA, Metal, Vulkan, SYCL, and RPC backends provide true asynchronous peer-copy implementations at this revision?
- Which backend event implementations map to device events, command-buffer completion, host synchronization, or no-op/fallback behavior?
- How much overlap is achieved in representative prompt and token-decode workloads?
- Which later PRs changed the MoE partial-copy path, event ordering, or copy ownership?
- Under graph reuse, exactly when can a stable `cur_copy` improve CUDA/accelerator graph capture?

## Next investigation

Trace the concrete backend interfaces behind `ggml_backend_graph_compute_async()`, `cpy_tensor_async`, event wait/record, and synchronization for CPU and one accelerator backend. That comparison will separate scheduler-level ordering from backend-specific execution semantics.
