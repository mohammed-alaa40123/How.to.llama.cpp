# Project state

_Last updated: 2026-07-13 08:50 Africa/Cairo_

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
- Exact pinned declaration and reverse-destruction map for `llama_model` and `llama_context`, including partial construction, RAII, model mappings/buffers, output and memory resources, backends, scheduler, and application teardown.

## Latest concrete findings

- `llama_model::~llama_model()` explicitly deletes registered LoRA adapters; `pimpl` then releases model storage through RAII.
- `llama_model::impl` reverse destruction releases `ctxs_bufs` before mlock objects and retained mappings. Within each pair, backend buffers are destroyed before the GGML metadata context.
- `llama_context::~llama_context()` records scheduler buffer diagnostics and explicitly frees `opt_ctx`, but does not explicitly synchronize or reset the scheduler.
- Context reverse declaration order releases `mem_storage`, output buffer, graph results, metadata, and owning `backends` before `sched`; scheduler safety under this ordering requires lower-level deleter verification.
- `llama_context` borrows `llama_model`; the model must outlive every context. Attached thread pools are also borrowed.

## In progress

- Resolve scheduler/backend teardown safety by tracing `ggml_backend_sched_free`, events, scheduler buffers, and concrete backend deleters.
- Architecture-specific graph-builder downcasts to concrete memory-context types and exact state tensors read/written.
- Runtime evidence for synchronization, event waits, page faults, memory updates, and teardown.
- Concrete backend async-copy, event, graph-submission, synchronization, and destruction behavior.

## Immediate next task

Trace the scheduler and backend deleter chain:

```text
ggml_backend_sched_ptr deleter
→ ggml_backend_sched_free
→ scheduler-owned events and buffers
→ backend references used during free
→ concrete backend free/synchronize behavior
→ queued-work requirements
→ validate or refute safety of context member order
```

Required deliverables:

1. exact scheduler free call chain and resource order;
2. CPU and accelerator backend differences;
3. whether explicit synchronization is required before context destruction;
4. a conclusion on `backends`-before-`sched` safety at the pinned revision;
5. runtime or test evidence where available;
6. truth labels and durable context updates.

## Publication and verification state

- New page: `docs/architecture/model-context-teardown-order.md`.
- Page commit: `5a5178afb4d676460f1b89dc3c4def934f47bc57`.
- Navigation commit: `8d25991a54702137a2135492205abc6fcb128a27`.
- README/TODO commit: `ddffc257ad0d052315d1096dd437110322b3bd67`.
- Research-log commit: `4df41bd1481792e174fb1ec22ea67ea482f5c07d`.
- Detailed-note commit: `328745e192f271aca476ea5cb04b44df120b36fa`.
- Connector-side re-fetch confirmed the page, pinned baseline, reverse-order tables, truth labels, source map, and related links.
- Workflow lookup for `328745e192f271aca476ea5cb04b44df120b36fa` returned `workflow_runs: []`; this endpoint only reliably exposes pull-request-triggered runs, so push-triggered Documentation CI, Pages deployment, and hourly-context validation remain unverified rather than failed.
- Site-specific searches returned no indexed project or teardown page. Direct opening of the Pages root and `architecture/model-context-teardown-order/` was rejected by the safe-URL gate because those exact URLs were absent from search results.
- No new external secondary source was introduced; the research ledger remains unchanged.

## Known blockers and caveats

- **Local validation blocker:** this environment cannot resolve `github.com`, so a checkout and local validators, tests, script checks, and strict MkDocs build cannot run.
- **CI visibility blocker:** commit workflow lookup returned an empty run list and cannot verify push-triggered workflows.
- **Pages verification blocker:** search returned no indexed result and direct open was blocked by the safe-URL gate; live HTTP status and rendered content remain unverified.
- The observed context member order is verified C++ behavior, but scheduler safety is an open question until lower-level deleters are traced.
- Mapping, allocation, physical residency, data validity, queued completion, ownership, and release remain distinct states.

## Definition of done for the foundations deepening phase

- Comprehensive clickable system map with accessible interaction.
- Source-pinned end-to-end workflow and deep GGUF/model-loading chapters.
- Canonical model/context, graph, scheduler, memory, and teardown ownership pages.
- File-by-file source inventory grouped into subsystem explanations.
- Prefill, decode, CPU-only, GPU-offload, multi-backend, KV/recurrent, and MoE variants.
- Runtime evidence overlays where conceptual explanations are insufficient.
