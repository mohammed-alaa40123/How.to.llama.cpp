# Project state

_Last updated: 2026-07-13 17:51 Africa/Cairo_

Read this file after the root README on every run. It is the compact checkpoint for the current milestone, verified work, blockers, and next priority.

## Source baseline

- Repository: `ggml-org/llama.cpp`
- Pinned revision: `e3546c7948e3af463d0b401e6421d5a4c2faf565`
- Current upstream reference used for the graph/MoE chapter: `6b4dc2116a92c5c8f2782bfe51fabe5ee66fb5ef`
- Policy: baseline claims stay pinned; newer refs are documented separately and labelled.

## Active milestone

**Foundations deepening — interactive system map plus file-by-file subsystem synthesis**

## Completed

- MkDocs Material site, strict documentation CI, Pages deployment, health checks, source indexing, and durable run context.
- Canonical GGUF, model placement, model/context, graph/MoE, scheduler, memory-lifetime, and system-ownership pages.
- Pass A pages for public API, model/GGUF loading, runtime context/memory, scheduler, and concrete context-memory implementations.
- Exact pinned declaration and reverse-destruction map for `llama_model` and `llama_context`.
- Exact pinned generic scheduler teardown path.
- Ordinary pinned CPU backend teardown classification.
- Pinned CUDA backend teardown dependency audit and conditional safety classification.
- Pinned Metal backend teardown audit and verified-safe backend-before-scheduler classification.
- Pinned Vulkan command-lifetime map and verified-safe ordinary backend teardown classification.
- Pinned SYCL backend teardown audit and conditional queued-work classification.
- Pinned RPC backend teardown audit and distributed completion classification.
- Pinned CANN backend teardown audit and reset-order conditional classification.

## Latest concrete findings

- `ggml_backend_cann_free()` calls `aclrtSynchronizeDevice()`, then `aclrtResetDevice()`, then deletes the backend context and wrapper.
- Device-wide synchronization establishes an explicit queued-work completion boundary before teardown.
- The context owns lazy streams, an optional copy event, a memory pool, rope/tensor caches, and optional ACL graph-cache state.
- Scheduler CANN events own independent ACL event handles and registry-device references.
- Scheduler CANN buffers own buffer-local device allocations and free them without dereferencing the backend context.
- Registry/device objects are function-static and outlive individual backend wrappers.
- The unresolved risk is resource validity after reset: context and scheduler destructors later call `aclrtDestroyEvent`, `aclrtDestroyStream`, and `aclrtFree`.
- Current upstream still contains the same reset-before-context-delete order as the pinned baseline.

## In progress

- Remaining concrete backend teardown audit for OpenCL.
- Optional CPU extra-buffer teardown audit.
- CANN reset semantics and multi-context runtime validation.
- RPC remote synchronization/completion protocol and shared-socket concurrency.
- CUDA concurrent-stream synchronization coverage.
- SYCL all-queue completion coverage and implicit destructor semantics.
- Vulkan performance-query-pool ownership and process-exit device teardown.
- Architecture-specific graph-builder downcasts and exact state tensors.
- Runtime evidence for synchronization, event waits, page faults, memory updates, and teardown.

## Immediate next task

Audit pinned OpenCL teardown and optional CPU extra-buffer implementations:

```text
OpenCL backend wrapper free
→ command-queue completion and release
→ events and scheduler-resource ownership
→ buffer/context/program/kernel lifetime
→ static registry and device lifetime
→ optional CPU extra-buffer deleters
→ classify backend-before-scheduler ordering
```

Required deliverables:

1. exact OpenCL backend/context free chain;
2. completion behavior for queued commands;
3. event and scheduler-buffer ownership after backend-wrapper deletion;
4. program/kernel/buffer/context release order and error paths;
5. optional CPU extra-buffer lifetime boundaries;
6. safety classification for the pinned context member order;
7. truth labels and durable context updates.

## Publication and verification state

- New page: `docs/architecture/cann-backend-teardown.md`.
- Page commit: `230c8adf4a26d572e5c57c69c8f4efa86741f869`.
- Navigation commit: `fa5491dfda8dc0121b1ef3671a971637085fba34`.
- Detailed note commit: `3eed9cc1e331a550e9be8995b67703b0e23b51b5`.
- README/TODO commit: `87ba63285699722ea7e414a5c125f8a70457dacd`.
- Research-log commit: `f8faef79a7a0e7159d6a00f41efb8e754463d0ba`.
- Connector-side inspection confirmed the CANN backend free, device synchronization/reset, context-member, event, buffer, and registry paths.
- Local clone and validation failed with `Could not resolve host: github.com`.
- Commit-scoped workflow lookup for `f8faef79a7a0e7159d6a00f41efb8e754463d0ba` returned `workflow_runs: []`; Documentation CI, Pages deployment, and hourly-context validation are unverified rather than confirmed failed.
- Public search returned no indexed result for the site root or CANN route; the safe-URL gate rejected direct opening, so HTTP status and rendered content remain unverified.
- No new external source passed the ledger verification bar; the research ledger remains unchanged.

## Known blockers and caveats

- **Local validation blocker:** cloning failed because the execution environment could not resolve `github.com`, so project validators, tests, strict MkDocs build, and `check_site.sh` could not run locally.
- **CI visibility blocker:** the available commit-scoped workflow endpoint returned an empty run list and currently exposes only a limited class of workflow runs.
- **Pages verification blocker:** public search found no indexed site result and direct access was rejected by the safe-URL gate; HTTP response and expected CANN page content could not be inspected.
- **CANN reset-order caveat:** device-wide completion is explicit, but the validity of later ACL destroy/free calls after `aclrtResetDevice()` is unverified.
- **CANN shared-device caveat:** freeing one backend resets the device; impact on another backend instance using the same device remains unverified.
- **RPC completion caveat:** graph compute has no completion response and the no-op RPC synchronize does not invoke server-side synchronization.
- **RPC concurrency caveat:** one socket can be shared through endpoint-level weak caching and buffer-held strong references; the inspected request helpers do not establish a per-socket request mutex.
- **SYCL completion caveat:** backend free does not explicitly wait before destroying context-owned resources.
- **Vulkan query-pool caveat:** the optional performance query pool still needs a focused ownership audit.
- Mapping, allocation, residency, validity, command completion, ownership, reset, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, memory, and teardown ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.