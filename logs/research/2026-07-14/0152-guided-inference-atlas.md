# Guided inference atlas increment

- Run time: 2026-07-14 01:52 Africa/Cairo
- Scope: improve information architecture and discoverability without making unsupported new backend claims
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Startup and repository inspection

Read the complete root README, project state, research log, research ledger, and the latest detailed note before editing. Inspected `mkdocs.yml`, the existing interactive inference workflow, current navigation, and the OpenCL source-access blocker.

## Artifact

Added `docs/lifecycle/inference-atlas.md` and placed it first under **Inference lifecycle** in the site navigation.

The page provides:

- a clickable Mermaid pipeline from GGUF through loading, model/context, graph, scheduler, execution, sampling, and the next decode step;
- a stage-by-stage object/lifetime table;
- five audience-specific reading paths;
- links to the canonical existing pages rather than duplicating their detailed evidence;
- Verified, Interpretation, Historical, and Open question labels.

## Verified

- The linked pages are the current canonical project pages for the major stages shown in the atlas.
- The pinned documentation separates persistent model state, mutable context state, graph construction, scheduler planning, backend execution, persistent KV/recurrent memory, and teardown.
- The existing interactive workflow remains a decoder-centric prototype and now has a static guided entry point beside it.

## Interpretation

- A linear atlas is useful for learning and navigation, but the runtime is not a single linear thread: mappings/uploads, graph splits, asynchronous queues, copy generations, and persistent state cross several boundaries.
- The atlas should remain a routing layer over detailed evidence pages, not become another competing implementation description.

## Historical

- Navigation structure and backend behavior are revision-sensitive. This atlas describes the current documentation state and the pinned baseline.

## Open questions

- Replace curated atlas/workflow metadata with generated, versioned JSON.
- Add runtime overlays for page faults, copies, event waits, KV/recurrent growth, and backend queues.
- Extend built-site validation to Mermaid click targets and generated routes.

## Blocker encountered

The pinned oversized `ggml-opencl.cpp` can now be retrieved as a Git blob, but the connector exposes only a truncated response and no usable symbol search over the hidden remainder. The exact OpenCL teardown chain was therefore not guessed in this run.

## Validation

- Repository contents API created the atlas and linked it in `mkdocs.yml`.
- Full local tests and strict MkDocs build remain unavailable because the execution environment cannot resolve GitHub and has no checkout.
- CI and Pages were checked after the documentation updates; exact outcomes are recorded in project state.

## Next priority

Regenerate or otherwise obtain searchable access to the complete pinned OpenCL translation unit, then finish the OpenCL backend/context teardown and command-completion classification.
