# EAAI adversarial reviewer notes

_Last reviewed: 2026-07-17_

## Overall recommendation

**Reject in current form; encourage resubmission after evidence collection.** The architecture is increasingly disciplined, but the prospective contribution is still mostly contracts, schemas, validators, and plans. That is useful engineering groundwork, not yet an EAAI experience report.

## Fatal flaws

None at the architecture level, provided the project continues to distinguish authored/source-derived/browser evidence from native capture and does not claim learner benefit before evaluation.

## Major concerns

1. **No educational-effect evidence.** The repository defines objectives and formative checks, but has no learner or expert outcome data. Tool completion, schema validity, and visual polish cannot substitute for code-tracing accuracy, misconception correction, or expert usefulness.
2. **The artifact risks becoming a collection of tools.** Lab 0, GGUF parsing, trace replay, media generation, progress storage, and multi-agent maintenance need one coherent instructional sequence and shared assessment logic.
3. **The multi-agent claim is not identified.** There is no retrospective dataset, baseline, accepted/rejected-output accounting, human correction time, or cost/maintenance record sufficient to distinguish the scheduled specialist workflow from ordinary AI-assisted repository work.
4. **Native reproducibility is unproven.** `uv sync --locked`, a schema, and a devcontainer plan do not establish that clean local and cloud environments can build the pinned native target and produce comparable bounded outputs.
5. **Trace-viewer learning value is untested.** The authored trace contract is defensible, but a viewer may add visual novelty without improving source navigation or code tracing.
6. **Independent technical review is absent.** A llama.cpp/GGML expert must review the synthetic fixture, source locations, explanations, trace classifications, and deterministic figures.
7. **The scope remains aggressive for July 17-31.** Week 2 should prioritize one coherent vertical slice over parallel browser, native, viewer, progress, media, and cloud completeness.

## Required architecture decisions

- Keep browser execution explicitly non-native and label outputs in the interface, exported progress, screenshots, and evaluation instruments.
- Treat the model-free Lab 0 path as setup/build evidence only. Optional user-provided inference must have a separate success state and timing field.
- Make deterministic figures the only authoritative technical diagrams. Reject generative diagrams that depict exact architecture, ownership, tensor shape, pointer flow, timing, or call order.
- Keep progress local-first, transactional on import, privacy-minimized, and separate from any research dataset.
- Do not add native instrumentation until source-link resolution, replay semantics, trace bounds, keyboard operation, and static fallback are validated for the authored trace.

## Week 1 acceptance judgment

The contracts are plausible, but Week 1 should not be declared complete until:

- strict integrated CI passes on the full stack;
- the media manifest validator exists;
- the trace source-link resolver verifies pinned paths/lines/functions;
- the Lab 0 reproducibility matrix and diagnostic taxonomy are specified;
- the first viewer design has keyboard and transcript acceptance tests;
- an independent technical reviewer is nominated.

## Week 2 minimum publishable vertical slice

A credible minimum is: one clean-environment Lab 0 build path, one browser GGUF lesson with three assessed misconceptions, one bounded source-pinned trace viewer, local progress round-trip, one deterministic figure, and documented failures/corrections. Optional generated media and Codespaces polish should be cut before any of these core items.

## Concrete evidence required

- pre/post or matched checkpoint performance on GGUF layout, mapping-versus-residency, build-versus-inference, and source tracing;
- task time, completion, confidence, and cognitive-load measures;
- expert correctness rubric and dated review record;
- clean-environment reproducibility runs with failure classifications;
- trace-viewer comparison against a static source+text baseline;
- retrospective agent-run extraction and at least one fair workflow baseline;
- human labor, failed generations, API cost, CI cost proxies, maintenance burden, and rejected assets.

## Generalization boundary

Any generalization beyond llama.cpp must be framed as design hypotheses about source-pinned executable learning and repository-native validation. It cannot be claimed from a single codebase without transfer evidence.