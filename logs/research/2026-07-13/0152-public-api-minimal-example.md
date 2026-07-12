# Public API and minimal example Pass A

- Run time: 2026-07-13 01:52 Africa/Cairo
- Scope: first file-by-file Pass A artifact for the public API and minimal example group
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Added `docs/architecture/public-api-minimal-example.md` and linked it under Architecture navigation.

The page maps:

- `examples/simple/simple.cpp`;
- `include/llama.h`;
- `src/llama.cpp`;
- `src/llama-model.cpp`;
- `src/llama-context.cpp`.

It includes a subsystem relationship diagram, file/symbol/caller/callee inventory, application call sequence, ownership and synchronization table, error-path map, backend caveats, truth labels, and the next file group.

## Verified

- The pinned simple example loads backend registrations before model creation.
- It creates caller-owned `llama_model`, `llama_context`, and `llama_sampler` objects.
- It obtains a model-associated vocabulary reference rather than a separately owned vocabulary object.
- Tokenization uses a two-pass required-capacity pattern.
- `llama_batch_get_one()` is used as a caller-backed batch view over prompt and sampled-token storage.
- Encoder-decoder models take an optional `llama_encode()` path before autoregressive decode.
- Decoder evaluation repeatedly calls `llama_decode()`, samples the last output row, converts the token to text, and feeds the token back as the next one-token batch.
- Teardown order is sampler, context, then model, preserving the context's non-owning model dependency.
- Model loading delegates into model-loader, architecture factory, metadata/vocabulary loading, device selection, and tensor loading.

## Interpretation

- The simple example is an ownership and control-flow skeleton, not a complete production resource-management template.
- Prefill and one-token decode share the public `llama_decode()` entry point but should be treated as different runtime phases.
- Public API stability intentionally hides architecture and backend differences; performance analysis requires following the facade into model, context, scheduler, memory, and backend code.
- `n_gpu_layers` expresses a placement request and does not prove that a particular backend exists or every requested layer is offloaded.

## Historical

- Initialization conventions, sampler APIs, parameter fields, and batch helpers have changed across llama.cpp revisions. This page is pinned and should not absorb examples from other revisions without explicit labels.

## Open questions

- Strongest public thread-safety contract for shared models and concurrent contexts.
- Exact output-access synchronization guarantees.
- Whether upstream should use RAII cleanup for every early-return path in the minimal example.
- Process-level backend/global-cache shutdown requirements for embedded applications.
- Encoder/decoder memory ownership differences across architectures.

## Sources inspected

Repository context:

- complete `README.md`;
- `docs/reference/project-state.md`;
- `docs/reference/research-log.md`;
- `docs/reference/research-ledger.md`;
- latest detailed note `logs/research/2026-07-13/0052-interactive-link-validation.md`;
- current `mkdocs.yml` and documentation structure.

Pinned upstream:

- `examples/simple/simple.cpp`;
- `include/llama.h`;
- `src/llama.cpp`;
- `src/llama-model.cpp`;
- `src/llama-context.cpp`.

No new external secondary source was introduced, so the research ledger remains unchanged.

## Validation

Repository writes and connector-side re-fetch are used for durable validation.

The execution container could not resolve `github.com`, so it could not obtain a checkout to run:

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

Continue Pass A with the model/GGUF loader group and document exact construction order, file/mapping ownership, split indexing, tensor offsets, population paths, cancellation, and cleanup.