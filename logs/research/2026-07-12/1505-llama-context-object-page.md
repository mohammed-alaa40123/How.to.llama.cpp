# Canonical `llama_context` object page

- Run time: 2026-07-12 15:05 Africa/Cairo
- Scope: implement the first canonical object-centred documentation page from the documentation-quality roadmap
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Verified

- `llama_init_from_model()` validates context/model compatibility and allocates `new llama_context(*model, params)`; `llama_free()` deletes the context.
- `llama_context` stores a non-owning `const llama_model &` reference and owns runtime-specific configuration, memory, scheduler, backend instances, graph-result caches, outputs, adapters, batch allocation, sampling state, and performance state.
- The constructor normalizes context parameters, initializes device/accelerator/CPU backends, reserves output storage, calls `model.create_memory()`, chooses backend compute-buffer types, checks pipeline-parallel capabilities, creates/reserves the scheduler, and initializes backend-sampler vocabulary state.
- Decode mutates batch, memory, graph, scheduler, output, and sampling state; graph reuse preserves compatible topology/allocation while rewriting inputs.
- CPU thread-pool selection and backend synchronization are coordinated through the context.
- Public state and output APIs synchronize before completion-sensitive host access.
- The destructor does not delete the referenced model.

## Interpretation

- `llama_context` is the mutable execution session around a loaded model, not the model itself.
- The model must outlive contexts created from it because the context stores a reference.
- Scheduler ownership does not imply ownership or physical residency of mmap-backed model pages.
- Applications should externally serialize concurrent mutation of one context unless a stronger public thread-safety contract is found.

## Historical

- The page intentionally describes the pinned baseline. Later revisions may change memory implementations, graph reservation, backend sampling, scheduler lifetime, or ownership details.

## Open questions

- Which context APIs, if any, have an explicit thread-safety guarantee?
- Which concrete memory implementation is selected for every architecture and hybrid configuration?
- Do all backend cleanup paths guarantee completion when a context is freed without an explicit prior synchronization?
- Which later commits materially change context ownership or construction?

## Artifact

Created `docs/objects/llama-context.md` with:

- prerequisites and five-minute explanation;
- construction flow and Mermaid lifecycle;
- ownership/lifetime table;
- memory, mmap/page-fault, mutation, decode, threading, synchronization, and teardown sections;
- pinned source map;
- backend/version differences;
- Verified, Interpretation, Historical, and Open question labels;
- related objects and next-page guidance.

Published it under a new **Objects** navigation section in `mkdocs.yml` and marked the README TODO complete.

## Sources

- Pinned `src/llama-context.h`
- Pinned `src/llama-context.cpp`
- Existing source-pinned decode, scheduler, and buffer-compatibility pages

No new external or secondary source was introduced, so the research ledger did not change.

## Validation and publication

- Connector-side file creation and updates succeeded.
- The repository changed concurrently during this run: the interactive-foundations increment landed between reads. Updates were re-fetched and merged rather than overwriting that work.
- Full local `mkdocs build --strict` was unavailable because the execution environment had no authenticated repository checkout or `gh` CLI.
- GitHub Actions and Pages checks are recorded separately after the final commits.

## Next priority

Deepen the GGUF foundations/model-loader chapter, then connect the interactive Context node to the canonical object page and shared versioned source metadata.