# EAAI publication roadmap

_Last updated: 2026-07-17 12:03 Africa/Cairo_

This roadmap turns repository milestones into evidence gates for an EAAI experience report. It does not authorize manuscript drafting.

## Phase A — Foundation, July 17-23, 2026

### A1. Coordination and contracts

- Freeze target audience, educational problem, three lesson contracts and research questions.
- Maintain authoritative orchestrator state, evidence backlog, handoff ledger and readiness scorecard.
- Keep browser, local-native and cloud-container tiers intentionally unequal and explicitly labelled.

**Status:** substantially evidenced. Reviewer-package integration and a systematic documentation-gap audit remain.

### A2. Deterministic evidence foundations

- Integrate legal fixture decision and deterministic synthetic GGUF.
- Integrate Lab 0 report/reproducibility contracts, trace schema/sample and local-progress schema.
- Add media manifest/provenance contract.
- Maintain passing strict MkDocs and documentation CI.

**Status:** evidenced as contracts and deterministic artifacts. Ordinary CI performs no paid API calls or model downloads.

### A3. Smallest vertical slice

- Add a narrow keyboard-operable viewer for the authored GGUF trace.
- Generate one deterministic technical figure from structured data.
- Add source-link and replay validation.
- Add the browser-first GGUF parser/checkpoint slice.

**Status:** evidenced by immutable source anchors, deterministic trace replay, the generated GGUF-layout SVG, the static viewer, the browser GGUF slice and passing commit-scoped CI.

**Boundary:** the viewer remains authored/source-derived and Lab 1 remains browser-derived. Native capture, learner benefit and independent technical correctness remain unevidenced.

## Phase B — Vertical slices, July 24-31, 2026

### B1. Lab 0 end to end

- Require `uv sync --locked` for Python tooling.
- Require CMake/Ninja native build and bounded executable-launch smoke test.
- Use the validated stable failure taxonomy, machine-readable report and time-to-ready instrumentation.
- Execute a supported local/container reproducibility matrix.
- Keep optional learner-provided model loading and time-to-first-token separate from the model-free core.

**Current status:** the reproducibility contract passed Documentation CI run `29565651085`. No real matrix row exists yet.

**Next evidence:** Ubuntu 24.04 local-native first, then the devcontainer. Verify the pinned native target/options during the first run rather than treating the illustrative example as execution evidence.

**Exit evidence:** clean supported environments reach expected output; model-free success is not called inference; optional model paths are not redistributed.

### B2. Browser GGUF Anatomy lab

- Parse the synthetic fixture in-browser.
- Verify browser/Python golden agreement.
- Add Predict-Discover-Explain checkpoints, keyboard completion and static table/text fallback.
- Persist local progress with export/import and corruption recovery.

**Current status:** deterministic parsing, golden agreement and checkpoints are evidenced by run `29562479577`; progress persistence remains blocked on `PROGRESS-02`.

**Exit evidence:** deterministic parsing, checkpoint logic, privacy-minimizing progress and explicit exclusion of native-runtime claims.

### B3. Executable lecture and media dry run

- Preserve the validated authored/source-derived viewer as the baseline artifact.
- Add one bounded real or faithfully captured path only after instrumentation and trace-size risks are reviewed.
- Define a fair static-source/text comparison before claiming that the viewer improves code tracing.
- Run deterministic media-manifest acceptance/revision/rejection and stale-asset checks.

**Exit evidence:** coherent local/deployed demo with no paid generation in ordinary CI and no evidence-kind inflation.

## Phase C — Evidence development, August-September 2026

- Extract a retrospective repository dataset from scheduled runs, commits, tests, CI failures, corrections and handoffs.
- Freeze benchmark tasks and run fair workflow baselines.
- Obtain independent llama.cpp/GGML correctness review.
- Pilot expert or learner evaluation only after approval and any required ethics review.
- Record negative results, failed generations, human labor, infrastructure maintenance and cost proxies.

**Exit evidence:** longitudinal dataset, baseline comparison, independent review and approved evaluation pathway.

## Phase D — Venue and manuscript readiness

- Reverify official EAAI call, area, deadlines, author kit, length and anonymity requirements.
- Freeze claims-evidence table and limitations.
- Resolve fatal and major adversarial-review concerns.
- Activate Paper Integrator only after the gate in `orchestrator-state.md` is met.

## Immediate dependency order

1. `DATA-01` retrospective extraction schema.
2. `LAB0-03` measured Ubuntu 24.04 local-native row.
3. `LAB0-04` measured devcontainer row.
4. `PROGRESS-02` local persistence/export/import.
5. `REVIEW-02` active-stack adversarial review integration.
6. Static-source/text baseline literature and benchmark design.
7. `VENUE-01` official EAAI-27 verification.

## Scope-control decisions

- Do not add broad cloud polish before the local/devcontainer bounded path works.
- Do not add native trace instrumentation before the authored viewer has a fair baseline and instrumentation risks are bounded.
- Do not add authenticated progress synchronization in the July vertical slice.
- Do not add optional generated media unless the deterministic core demo is complete and human review is available.
- Do not treat contract examples, CI integration, or attractive visualizations as learner-outcome evidence.

## Generalization boundary

The artifact is llama.cpp/GGML-specific. The potentially generalizable contribution is the method: source-pinned executable explanations, evidence-labelled traces, deterministic validators, local-first learner state and human-supervised repository agents. Generalization beyond this codebase must be argued from replicated tasks or explicitly presented as a design hypothesis.

## Ethics and AI-use boundary

- No participant recruitment or personal-data collection without explicit approval and required review.
- No silent telemetry.
- No authenticated progress sync during the two-week vertical slice.
- Deterministic technical graphics are authoritative.
- Generated images/audio/video are optional supplements with provenance, accessibility, licensing/privacy review and human technical approval.
- Manuscript AI-use disclosure must report agent roles, model/tool versions when known, human corrections, validation, failures and retained evidence.