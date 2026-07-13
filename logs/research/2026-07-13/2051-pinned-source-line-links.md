# Pinned source-line links increment

- Run time: 2026-07-13 20:51 Africa/Cairo
- Scope: turn generated symbol locations into direct revision-pinned GitHub navigation targets
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Updated `scripts/index_upstream.py`, `scripts/update_upstream.sh`, `tests/test_index_upstream.py`, and `docs/reference/source-index.md`.

## Verified

- `index_upstream.py` accepts an optional `--source-url-base` argument.
- Each indexed file receives a pinned `source_url` when that base is supplied.
- Every `symbol_locations` record receives a pinned `source_url` with a GitHub `#L<line>` fragment.
- The helper normalizes a trailing slash on the URL base.
- Source-link enrichment copies symbol records instead of mutating the extraction result.
- `update_upstream.sh` derives the URL prefix from the exact `LLAMA_CPP_REV`, so generated links follow the selected pinned revision.
- Regression tests cover URL normalization, absent-base behavior, line-fragment generation, and non-mutation.

## Interpretation

- Line-aware indexing and pinned links now form a complete navigation primitive: a reviewer can move from generated inventory metadata to the exact candidate declaration without manually rebuilding a URL.
- This improves audit efficiency for very large files such as `ggml-opencl.cpp`, but the regex index remains a locator rather than implementation proof.

## Historical

- The prior inventory contained line numbers but required readers or scripts to construct source links manually.

## Open question

- The pinned inventory still needs regeneration in an environment that can fetch or already contains the llama.cpp worktree.
- Generated links should later be validated against GitHub blob URLs and optionally rendered into subsystem-specific symbol landing pages.

## Validation

- Connector-side inspection confirmed the updated script, invocation, tests, and documentation.
- A local upstream regeneration remains blocked because the execution environment cannot resolve `github.com`.
- The bounded helper behavior is covered by the added unit-test cases, but the full repository test suite and strict MkDocs build require a usable checkout.

## Next priority

Regenerate `data/generated/source-index.json` at the pinned revision, use the new direct line links to locate the exact OpenCL free/synchronize/event/buffer/program/kernel paths, and complete the OpenCL backend-before-scheduler classification.
