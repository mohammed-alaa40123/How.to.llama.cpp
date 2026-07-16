# Initial executable-learning legal fixture decision

- Run time: 2026-07-17 00:00 Africa/Cairo
- Starting commit: `1c9432c079f69c094d7981f1e8c439f0579e03ee`
- Branch: `agent/eaai-two-week-execution-plan`
- Assigned milestone: close the first Week 1 legal-fixture dependency
- Learner outcome targeted: distinguish build validation, GGUF format reasoning, and real inference without ambiguous success claims

## Startup inspection

Read the root README, project state, research log, research ledger, two-week execution plan, handoff ledger, and the previous detailed run note. `docs/publication/orchestrator-state.md` and `docs/publication/evidence-backlog.md` were still unavailable on the active branch, so the run followed the prior dependency-safe recommendation recorded in the handoff ledger.

## Bounded increment

Created `docs/labs/legal-fixture-decision.md`.

The decision establishes:

- mandatory Lab 0 uses no redistributed model and validates the locked Python environment, native configure/build, binary discovery, and model-free executable launch;
- optional inference is a separately labelled extension using a learner-provided local GGUF path;
- Lab 1 uses a deterministic project-owned synthetic GGUF containing educational metadata, tensor descriptors, alignment, offsets, and non-model payload bytes;
- Executable Lecture 0 may begin from a bounded GGUF-loading authored/source-derived trace, but every trace field must declare its evidence kind.

## Verified

- The repository baseline remains pinned to llama.cpp commit `e3546c7948e3af463d0b401e6421d5a4c2faf565`.
- The repository policy already separates project-owned MIT content from upstream llama.cpp content.
- No external source, model file, corpus, prompt, personal data, paid API, or network download was introduced.
- The active branch previously identified fixture selection as the next dependency-safe task.

## Interpretation

A single redistributed tiny model is not the safest first fixture. It would couple unrelated outcomes, introduce provenance and licensing review, and make it easier to overclaim that compilation or parsing proves inference. Separate evidence paths are more precise and easier to validate.

## Historical

The 2026-07-16 23:00 run froze the two-week executable-learning architecture and explicitly deferred implementation until fixture, schema, accessibility, privacy, and validation boundaries were set.

## Open questions

- Exact synthetic metadata keys, tensor types/shapes, alignment, and payload pattern.
- Whether to commit the generated binary or generate it from a committed script and manifest.
- Which pinned llama.cpp GGUF loading functions provide the clearest first trace.

## Validation and limitations

The decision defines deterministic regeneration, SHA-256, golden parsing, alignment/range assertions, corruption rejection, browser/Python agreement, source revision recording, keyboard operation, and static text/table fallbacks.

No generator or binary fixture was added in this increment. Full local tests and MkDocs execution were unavailable in the connector environment. Commit-scoped CI was requested after the context updates.

## Human review needs

- Confirm that mandatory Lab 0 may be model-free while real inference remains an optional learner-provided-model extension.
- Review the synthetic fixture field list before freezing fixture format version `0.1.0`.

## Evidence produced

- `docs/labs/legal-fixture-decision.md`
- updated `docs/reference/project-state.md`
- updated `docs/reference/research-log.md`
- updated `docs/publication/agent-handoffs.md`
- updated README living TODOs
- this run note

## Next dependency

Implement the deterministic synthetic GGUF generator, manifest schema, golden parser output, checksum, and bounded truncated/corrupted variants. Do not call model-free executable launch “inference.”