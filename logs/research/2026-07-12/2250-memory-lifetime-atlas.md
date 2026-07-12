# Canonical memory-lifetime atlas

- Run time: 2026-07-12 22:50 Africa/Cairo
- Scope: unify storage, mapping, model, context, graph, scheduler, backend, output, synchronization, and teardown lifetimes
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Published `docs/foundations/memory-lifetimes.md` and added it to MkDocs Foundations navigation.

The chapter contains:

- a full ownership/lifetime atlas;
- mapping, page-fault, page-cache, RSS, and advice caveats;
- persistent model storage paths;
- KV, recurrent, and hybrid context memory;
- graph metadata, activations, reuse, scheduler copies, and staging;
- CPU-only, discrete accelerator, and shared/unified-memory distinctions;
- prefill/decode comparison;
- synchronization and teardown order;
- a runtime measurement checklist;
- Verified, Interpretation, Historical, and Open question sections.

## Verified

- `llama_model` owns persistent tensor storage and retained mappings; `llama_context` references the model.
- `llama_context` owns mutable memory, scheduler resources, runtime backends, graph results, and host-facing outputs.
- Model tensor placement and scheduler graph allocation are separate phases.
- Mmap may directly back a model buffer or serve as a source for an explicit copy/upload.
- Copy-ring slots, staging buffers, graph inputs under pipeline reuse, and host-visible outputs have synchronization-sensitive reuse boundaries.
- KV, recurrent, and hybrid memory are architecture-selected mutable context state, not immutable model weights.

## Interpretation

- Memory should be modeled as overlapping ownership and synchronization lifetimes rather than one global cache.
- Mapping, allocation, physical residency, byte validity, command completion, and release eligibility need separate trace fields.
- A logical MoE cache hit does not prove mapped pages are resident or that a backend destination copy is valid.
- RSS is useful as a process-level signal but cannot identify the residency of one expert or tensor.

## Historical

- Buffer types, memory implementations, graph reuse, copy APIs, event behavior, and backend teardown semantics evolve rapidly.
- The atlas deliberately composes only claims already pinned and reviewed in the repository; later upstream behavior must remain separately labelled.

## Open questions

- Map every architecture to its concrete `llama_memory_i` implementation.
- Locate explicit backend destructor synchronization contracts.
- Measure first-token file-page touches by architecture, quantization, and offload configuration.
- Build runtime overlays correlating file offsets, page faults, graph tensors, scheduler copies, queue events, RSS/PSS, and device memory.

## Sources inspected

- Complete repository `README.md`.
- `docs/reference/project-state.md`.
- `docs/reference/research-log.md`.
- `docs/reference/research-ledger.md`.
- Latest detailed note: `logs/research/2026-07-12/2151-interactive-model-link.md`.
- `docs/objects/llama-context.md`.
- Existing GGUF, model-placement, model-object, graph, scheduler, copy-fallback, and backend compatibility chapters.
- Current `mkdocs.yml` and repository navigation.

No new external source was introduced, so `docs/reference/research-ledger.md` was intentionally unchanged.

## Validation

- Repository-side creation and navigation updates succeeded.
- Static re-fetch is used to confirm the new page, navigation entry, truth labels, ownership table, and next-priority updates.
- Local `mkdocs build --strict` depends on a checkout and remains subject to the existing execution-environment DNS/authentication blocker.
- CI and Pages verification are attempted after durable updates; exact access limitations are recorded in project state and README TODOs.

## Next priority

Connect every memory-lifecycle explorer card to the canonical atlas and add a compact interactive overlay showing owner, backing storage, residency/validity, synchronization boundary, and release condition.