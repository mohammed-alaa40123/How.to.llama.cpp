# Project state

_Last updated: 2026-07-13 18:51 Africa/Cairo_

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
- Generic scheduler plus ordinary CPU, CUDA, Metal, Vulkan, SYCL, RPC, and CANN teardown audits.
- Pinned OpenCL build composition, kernel deployment, official platform scope, and initial `cl_mem` RAII ownership map.

## Latest concrete findings

- The pinned build registers OpenCL through `ggml_add_backend(OpenCL)` and builds `ggml-opencl` from one large host implementation plus OpenCL C kernels.
- Embedded mode generates headers with Python; non-embedded mode copies kernel files to the runtime output directory.
- Optional Adreno source kernels and an external binary-kernel library are separately controlled.
- The pinned kernel list includes attention, quantized matrix operations, and MoE-specific expert sorting, reorder, combine, and `MUL_MAT_ID` paths.
- The pinned host source defines `ggml_cl_buffer`, which releases its `cl_mem` before replacement and at destruction.
- Buffer-local ownership does not prove completion of queued commands that still reference the memory object.
- The full OpenCL backend-before-scheduler classification remains open.

## In progress

- Exact OpenCL backend/context teardown, queue completion, scheduler events/buffers, and program/kernel/context release order.
- Optional CPU extra-buffer teardown audit.
- CANN reset semantics and multi-context runtime validation.
- RPC remote synchronization/completion protocol and shared-socket concurrency.
- CUDA concurrent-stream synchronization coverage.
- SYCL all-queue completion coverage and implicit destructor semantics.
- Vulkan performance-query-pool ownership and process-exit device teardown.
- Architecture-specific graph-builder downcasts and exact state tensors.
- Runtime evidence for synchronization, event waits, page faults, memory updates, and teardown.

## Immediate next task

Finish the pinned OpenCL teardown audit:

```text
OpenCL backend/context free
→ queue completion and event waits
→ scheduler event and buffer ownership
→ program and kernel release
→ cl_mem and context release
→ optional binary-library handle lifetime
→ backend-before-scheduler classification
```

Then audit optional CPU extra-buffer deleters independently.

## Publication and verification state

- New page: `docs/architecture/opencl-build-and-buffer-lifetimes.md`.
- Page commit: `08a974873443f48ca124f40ab6eeaad7626f76ad`.
- Navigation commit: `7a522ea7177737fd2736326e54ade3eb197745b0`.
- README/TODO commit: `4002db9bc6da03f7dc648746e06f1e2dd9ba55d1`.
- Ledger commit: `529f92a26d4c2298979eeb8429089f21c99d8535`.
- Research-log commit: `511c969a3e41b81f86e13b398e083f70eb63c280`.
- Detailed note commit: `f4877f4793c7d3bee168271ff3f5ccf594dda07f`.
- Connector-side inspection verified the build and initial buffer-ownership claims.
- Local clone failed with `Could not resolve host: github.com`; project validators, tests, strict MkDocs, and `check_site.sh` could not run locally.
- Combined status for the project-state commit returned no status records, and the commit-scoped workflow endpoint returned `workflow_runs: []`; Documentation CI, Pages deployment, and hourly-context validation are unverified rather than confirmed failed.
- Public search returned no indexed result for the site root or new OpenCL route. Direct access was rejected by the safe-URL gate, so HTTP status and rendered content remain unverified.

## Known blockers and caveats

- **Large-source extraction blocker:** `ggml-opencl.cpp` is a very large single translation unit. The connector exposed its blob but not arbitrary symbol ranges, so the complete destructor chain could not be reviewed safely in this increment.
- **Local validation blocker:** cloning failed because the execution environment could not resolve `github.com`.
- **CI visibility blocker:** combined status was empty and the available commit workflow endpoint returned no runs for the checked commit.
- **Pages verification blocker:** search found no indexed result and the safe-URL gate rejected direct access to both the root and OpenCL route.
- **OpenCL completion caveat:** `cl_mem` ownership is verified, but command completion before release is not yet established.
- **CANN reset-order caveat:** device-wide completion is explicit, but the validity of later ACL destroy/free calls after `aclrtResetDevice()` is unverified.
- **RPC completion caveat:** graph compute has no completion response and RPC synchronize remains a no-op.
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
