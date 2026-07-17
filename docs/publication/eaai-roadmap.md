# EAAI publication roadmap

_Last updated: 2026-07-17 06:01 Africa/Cairo_

This roadmap turns repository milestones into evidence gates for an EAAI experience report. It does not authorize manuscript drafting.

## Phase A — Foundation, July 17-23, 2026

### A1. Coordination and contracts

- Freeze target audience, educational problem, three lesson contracts and research questions.
- Maintain authoritative orchestrator state, evidence backlog, handoff ledger and readiness scorecard.
- Keep browser, local-native and cloud-container tiers intentionally unequal and explicitly labelled.
- Integrate adversarial-review findings into dependency ordering without treating parallel PR artifacts as merged evidence.

**Exit evidence:** coordination files exist; each artifact has an owner, dependency, validator, non-goals and accessibility fallback.

### A2. Deterministic evidence foundations

- Integrate legal fixture decision and deterministic synthetic GGUF.
- Integrate Lab 0 report contract, trace schema/sample and local-progress schema.
- Integrate media manifest/provenance contract.
- Maintain passing strict MkDocs and commit-scoped Documentation CI.

**Current status:** contract stack through `agent/media-manifest-validation` passed Documentation CI run `29549208249`.

**Exit evidence:** all schemas have valid examples, malformed-input tests and passing CI; ordinary CI performs no paid API calls or model downloads.

### A3. Smallest vertical slice

- Validate source links, replay semantics, missing-data behavior and browser bounds before viewer expansion.
- Generate one deterministic GGUF-layout figure from structured fixture data with recomputed checksums.
- Add a narrow keyboard-operable viewer for the authored GGUF trace only after trace validation passes.

**Exit evidence:** deterministic local reproduction; evidence labels visible; transcript/static fallback; no native-capture overclaim.

### A4. Case-study evidence foundation

- Freeze a retrospective extraction schema for assignments, commits, failures, corrections, CI outcomes, human decisions, cost proxies and accepted/rejected outputs.
- Preserve failed generations, duplicated work, blocked runs and integration repairs rather than reporting only successful artifacts.
- Define the future baseline tasks before running comparative conditions.

**Exit evidence:** one machine-readable retrospective dataset extraction can be reproduced from repository history without participant data.

## Phase B — Vertical slices, July 24-31, 2026

### B1. Lab 0 end to end

- `uv sync --locked` for Python tooling.
- CMake/Ninja native build and bounded executable-launch smoke test.
- Stable failure taxonomy, machine-readable report and time-to-ready instrumentation.
- Local and devcontainer reproducibility matrix.

**Exit evidence:** clean supported environments reach expected output; model-free success is not called inference; optional learner-provided model path is separated.

### B2. Browser GGUF Anatomy lab

- Parse the synthetic fixture in-browser.
- Verify browser/Python golden agreement.
- Add Predict-Discover-Explain checkpoints, keyboard completion and static table/text fallback.
- Persist local progress with export/import and corruption recovery.

**Exit evidence:** deterministic parsing, checkpoint logic, privacy-minimizing progress and explicit exclusion of native-runtime claims.

### B3. Executable lecture and media dry run

- Connect viewer to one real or faithfully captured bounded path only after authored-trace validation and accessible viewer behavior are established.
- Validate source links, evidence kinds, replay, size bounds and missing fields.
- Run deterministic figure/media manifest pipeline; optional AI media only with credentials, caching, provenance and human approval.

**Exit evidence:** coherent local/deployed demo with no paid generation in ordinary CI.

## Phase C — Evidence development, August-September 2026

- Extract retrospective repository dataset from scheduled runs, commits, tests, CI failures, corrections and handoffs.
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

## July 17-31 scope cuts

- Optional generated image, narration and video samples are noncritical.
- Hosted/authenticated progress synchronization is out of scope.
- Codespaces polish must not displace one reproducible devcontainer and local-native path.
- Native trace instrumentation must not precede source-link, replay, keyboard and static-fallback validation.

## Generalization boundary

The artifact is llama.cpp/GGML-specific. The potentially generalizable contribution is the method: source-pinned executable explanations, evidence-labelled traces, deterministic validators, local-first learner state and human-supervised repository agents. Generalization beyond this codebase must be argued from replicated tasks or explicitly presented as a design hypothesis.

## Ethics and AI-use boundary

- No participant recruitment or personal-data collection without explicit approval and required review.
- No silent telemetry.
- No authenticated progress sync during the two-week vertical slice.
- Deterministic technical graphics are authoritative.
- Generated images/audio/video are optional supplements with provenance, accessibility, licensing/privacy review and human technical approval.
- Manuscript AI-use disclosure must report agent roles, model/tool versions when known, human corrections, validation, failures and retained evidence.
