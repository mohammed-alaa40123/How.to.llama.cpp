# Model and GGUF loader Pass A

- Run time: 2026-07-13 02:51 Africa/Cairo
- Scope: bounded file-by-file inventory of the model/GGUF loader group
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Added `docs/architecture/model-gguf-loader-pass-a.md` and linked it under Architecture navigation.

The page maps:

- `src/llama-model-loader.cpp` and `.h`;
- `src/llama-model.cpp` and `.h`;
- `src/llama-mmap.cpp` and `.h`;
- `ggml/src/gguf.cpp`.

It includes a five-minute flow, file inventory, construction order, unified tensor index, ownership transitions, five population paths, cancellation/cleanup, synchronization boundaries, backend/OS variants, and truth labels.

## Verified

- The loader parses GGUF with `no_alloc=true` and builds source tensor metadata before allocating runtime payloads.
- `llama_tensor_weight` stores source split index, absolute source offset, and descriptor tensor; the offset is bounds checked against the source file.
- Split models require the first shard, validate split number/count, and reject duplicate tensor names while building one `weights_map`.
- Architecture loading creates destination tensor metadata in a context associated with the selected backend buffer type.
- Buffer selection tests expected GGML operations against backend/device support.
- `init_mappings()` creates one mapping per source file only when mmap is enabled and computes total bytes for progress.
- Population paths include mapped alias, mapped source copy/upload, direct read, asynchronous staging with four host buffers/events, and synchronous fallback.
- Event waits prevent staging-slot reuse before upload completion; final synchronization precedes staging cleanup and model publication.
- Progress cancellation returns `false`; malformed files, invalid tensors, unsupported placement, I/O errors, or allocation failures use exception unwinding.

## Interpretation

- The loader is a transactional bridge from temporary file/metadata/mapping state into persistent model-owned buffers and mappings.
- `weights_map` is the central join between GGUF physical layout and architecture/backend-aware destination construction.
- “Loaded” should mean destination tensor bytes are valid and required asynchronous operations have completed, not merely that metadata parsed or virtual addresses exist.
- Mmap aliasing is one branch, not a model-wide guarantee; other mmap paths still copy or upload.

## Historical

- GGUF versions, split conventions, direct-I/O behavior, buffer-selection tests, and asynchronous upload capabilities are revision-sensitive. Claims remain pinned to the baseline.

## Open questions

- Exact `llama_model` implementation members receiving mappings and buffers, including declaration and destruction order.
- Direct-I/O alignment/fallback behavior and platform coverage in traces.
- Runtime cost attribution across parsing, mapping/prefetch, page faults, explicit reads, validation, staging, upload, and synchronization.
- Which backend host-pointer wrappers preserve source aliasing versus copying internally.

## Sources inspected

Repository context:

- complete `README.md`;
- `docs/reference/project-state.md`;
- `docs/reference/research-log.md`;
- `docs/reference/research-ledger.md`;
- latest detailed note `logs/research/2026-07-13/0152-public-api-minimal-example.md`;
- current `mkdocs.yml` and documentation structure.

Pinned upstream:

- `src/llama-model-loader.cpp` and `.h`;
- `src/llama-model.cpp` and `.h`;
- `src/llama-mmap.cpp` and `.h`;
- `ggml/src/gguf.cpp`.

No new secondary source was introduced. The research ledger therefore remains unchanged.

## Validation

Repository writes and connector-side re-fetch are used for durable validation.

The execution container again failed DNS resolution for `github.com`, so it could not obtain a checkout to run:

```bash
python3 scripts/validate_project_context.py
python3 scripts/validate_interactive_links.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -m py_compile scripts/*.py tests/*.py
bash -n scripts/*.sh
mkdocs build --strict
./scripts/check_site.sh
```

CI and Pages are checked after the final state commit. Empty or unavailable connector results are recorded as verification blockers rather than interpreted as failures.

## Next priority

Continue Pass A with runtime-context and memory implementations, then synthesize the public API, loader, model, and context groups into one ownership and synchronization relationship map.