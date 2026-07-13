# RPC backend teardown increment

- Run time: 2026-07-13 16:49 Africa/Cairo
- Scope: client/backend free, shared socket lifetime, remote buffer release, server dispatch/completion, session cleanup, and backend-before-scheduler classification
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Added `docs/architecture/rpc-backend-teardown.md` and linked it under Architecture navigation.

## Verified

- `ggml_backend_rpc_free()` deletes only endpoint/device/name metadata and the generic backend wrapper; it performs no network operation or synchronization.
- RPC buffer contexts own `std::shared_ptr<socket_t>` plus the remote buffer handle, so scheduler buffers retain transport ownership independently of the deleted backend wrapper.
- Buffer free sends `RPC_CMD_FREE_BUFFER`; the server frees the concrete backend buffer and acknowledges the command before the client deletes its buffer context.
- RPC buffer types are function-static and intentionally never freed.
- Client graph compute uses the request-only RPC helper and returns after sending bytes; it receives no completion response.
- RPC synchronize is a no-op and the backend exposes no events or async tensor methods.
- The server handles commands serially per connection, but graph handlers call the concrete server backend's `ggml_backend_graph_compute()` without a following generic synchronize.
- The server tracks remote buffers per client session and frees remaining buffers when the connection handler exits.
- The socket cache stores weak references; buffer contexts provide strong ownership, and final socket destruction closes TCP and optional RDMA resources.

## Interpretation

- Backend-before-scheduler destruction is structurally safe for ordinary pinned RPC client objects.
- Remote work completion remains conditional on the concrete backend running inside the RPC server.
- A later free-buffer command is ordered after the graph command in the server loop, but command ordering does not prove accelerator completion when the server backend queues work.
- RPC teardown is therefore a distributed synchronization problem rather than only a local ownership problem.

## Historical

- Request-only graph commands, single-connection dispatch, RDMA negotiation, graph reuse, and error semantics are revision-sensitive.

## Open questions

- Should synchronize become a real RPC command that invokes `ggml_backend_synchronize()` remotely?
- Should graph compute return a completion/status response?
- Can queued server-side CUDA/SYCL work still reference a buffer when the next RPC command frees it?
- Is the shared socket externally serialized for concurrent client users?
- Which regression tests cover immediate graph-compute followed by client teardown or connection loss?

## Sources inspected

Repository context:

- complete `README.md`;
- `docs/reference/project-state.md`;
- `docs/reference/research-log.md`;
- `docs/reference/research-ledger.md`;
- latest detailed note `logs/research/2026-07-13/1549-sycl-backend-teardown.md`;
- current `mkdocs.yml`.

Pinned upstream source:

- `ggml/src/ggml-rpc/ggml-rpc.cpp`;
- `ggml/src/ggml-rpc/transport.h`;
- `ggml/src/ggml-rpc/transport.cpp`.

No new external secondary source passed the verification bar, so the research ledger was unchanged.

## Validation

- Connector-side source inspection confirmed the ownership and protocol paths above.
- Local checkout validation was unavailable in this environment.
- GitHub Actions and Pages checks are performed after this note; exact results or blockers are recorded in project state and README TODOs.

## Next priority

Audit the pinned CANN backend teardown, synchronization, events, allocator buffers, and backend-before-scheduler ordering.
