# Integrated executable-learning demo acceptance

_Last updated: 2026-07-17 19:59 Africa/Cairo_

This document is the bounded `DEMO-01A` acceptance contract. It defines one coherent learner route through Lab 0, Lab 1, and Executable Lecture 0 before any claim that the repository is an integrated demo. It does not claim deployment success, learner benefit, native trace capture, cross-environment reproducibility, or manuscript readiness.

## Intended learner and prerequisite

- **Intended learner:** advanced undergraduate or beginning graduate learner in systems, computer architecture, or ML systems.
- **Prerequisite:** can read basic C/C++ and Python, use a shell, and recognize files, processes, functions, arrays, and command exit status.
- **Explicitly not assumed:** prior knowledge of GGUF binary layout, `mmap`, GGML graph construction, backend scheduling, llama.cpp build internals, or source-level tracing.

## Educational problem

Learners commonly collapse several distinct states into one idea of “the model runs”:

1. a toolchain is available;
2. llama.cpp configures and compiles;
3. an executable launches;
4. a GGUF file has valid storage structure;
5. llama.cpp loads model metadata and tensors;
6. GGML constructs an executable graph;
7. inference produces tokens.

The demo is acceptable only if its route repeatedly makes those boundaries observable and assessable.

## Frozen cross-experience objectives

After the route, the learner should be able to:

1. classify a failure as environment, configure, compile, executable-launch, model-load, or inference;
2. explain why a browser parser inspecting deterministic GGUF bytes is not native llama.cpp execution;
3. identify metadata, tensor descriptors, alignment, tensor offsets, and payload ranges in the synthetic GGUF;
4. reconstruct a bounded, revision-pinned GGUF-loading source path from ordered trace evidence;
5. distinguish authored explanation, source-derived evidence, browser-derived output, and native-captured evidence;
6. preserve and restore anonymous local progress without treating stored step state as proof of mastery.

## Predicted misconceptions

| Misconception | Required counterexample or check |
|---|---|
| A successful build means inference succeeded. | Lab 0 reports separate configure, compile, launch, model-load, and inference stages. |
| A browser GGUF parser behaves like native llama.cpp. | Lab 1 labels every result `browser-derived` and states excluded native behaviors. |
| File offsets are tensor objects or graph nodes. | Lab 1 maps descriptor offsets to byte ranges, then the lecture separately shows source-level loading steps. |
| A source-linked animation is a runtime capture. | The viewer labels the current trace `authored/source-derived`; absent captured fields remain absent. |
| Completing a UI step proves learning. | Progress records `in-progress` and unanswered checkpoints independently. |
| Generated media is technical evidence. | Only deterministic, source/trace-derived figures are authoritative. |

## One canonical learner route

The integrated demo must expose a single ordered route, not a menu of disconnected tools.

### Step 0 — Orientation and prediction

- **Executable action:** read the evidence-kind legend and predict which stages can be demonstrated in browser-only, local-native, and cloud-container tiers.
- **Observable output:** a static comparison table with browser-derived, source-derived, authored, and native-captured labels.
- **Formative assessment:** classify four example claims by evidence kind.
- **Accessibility fallback:** equivalent text table and numbered route; no interaction required.

### Step 1 — Lab 0: separate the native stages

- **Executable action:** run or inspect the bounded Lab 0 bootstrap sequence: `uv sync --locked`, compiler/CMake/Ninja checks, configure, compile, and model-free executable launch.
- **Observable output:** a versioned Lab 0 report with stage status, exact commands, revisions, diagnostics, and monotonic timing fields.
- **Formative assessment:** given one failed report, select the responsible stage and the next diagnostic action.
- **Source revision:** repository commit plus pinned llama.cpp revision recorded in the report.
- **Validation method:** Lab 0 schema and semantic validator; measured Ubuntu/devcontainer evidence remains a separate gate.
- **Accessibility fallback:** command transcript, expected exit states, and diagnostic table.
- **Explicit non-claim:** model-free launch is not model loading, inference, or time-to-first-token.

### Step 2 — Bridge question: what exists before native loading?

- **Executable action:** predict which information can be proven from GGUF bytes alone.
- **Observable output:** saved prediction for metadata, tensor descriptors, alignment, payload ranges, page residency, graph nodes, and generated tokens.
- **Formative assessment:** the learner must mark page residency, graph construction, and token generation as not derivable from browser byte inspection.
- **Accessibility fallback:** radio controls must have a plain-text answer sheet and rationale.

### Step 3 — Lab 1: Predict–Discover–Explain GGUF anatomy

- **Executable action:** parse the project-owned synthetic GGUF, inspect metadata and tensor ranges, then explain one descriptor-to-payload relationship.
- **Observable output:** deterministic values matching the golden parse, including the 32-byte alignment boundary and bounded tensor byte ranges.
- **Formative assessment:** one prediction item, one range/alignment calculation, and one explanation item.
- **Source revision:** fixture manifest/generator revision and repository commit.
- **Validation method:** generator check, golden agreement, corruption tests, browser/static output agreement.
- **Accessibility fallback:** static byte-layout table, alt text for deterministic figure, keyboard controls, and no-motion explanation.
- **Explicit non-claim:** the browser lab does not execute llama.cpp, `mmap`, model loading, GGML graph construction, backend scheduling, or inference.

### Step 4 — Progress portability checkpoint

- **Executable action:** save the reached Lab 1 step, export progress JSON, clear project-owned local state, import the JSON, and resume.
- **Observable output:** restored route position with checkpoint answers still represented independently.
- **Formative assessment:** explain why a restored `in-progress` state is not evidence of correctness or completion.
- **Validation method:** progress schema/version gate, validation-before-mutation, privacy-field rejection, and canonical/published module identity.
- **Accessibility fallback:** labelled native controls, live status text, and a manual JSON procedure.
- **Privacy boundary:** no identity, telemetry, raw free-text response, server sync, or authenticated account.

### Step 5 — Executable Lecture 0: reconstruct the loading path

- **Executable action:** step forward and backward through the bounded GGUF-loading trace while matching source anchor, call stack, runtime object, explanation, and deterministic figure.
- **Observable output:** ordered, deterministic replay with source revision, evidence labels, transcript, and one runtime-state visualization.
- **Formative assessment:** reconstruct the next function/source step and distinguish a captured fact from explanatory inference.
- **Source revision:** immutable llama.cpp commit and repository trace revision.
- **Validation method:** trace schema, source-anchor validation, contiguous sequence checks, deterministic replay, and forward/back state tests.
- **Accessibility fallback:** keyboard navigation, complete transcript, static ordered table, reduced-motion mode, and figure text equivalent.
- **Explicit non-claim:** the current trace is authored/source-derived unless a later capture record proves otherwise.

### Step 6 — Synthesis and transfer

- **Executable action:** place six artifacts in order: compiled executable, GGUF descriptor, mapped/model object, graph node, backend execution, generated token.
- **Observable output:** one evidence-labelled causal chain with unknown/unobserved states left explicit.
- **Formative assessment:** a held-out source-path or failure-classification item using no additional evidence beyond the frozen benchmark condition.
- **Accessibility fallback:** sortable interaction must have a numbered text response alternative.

## Acceptance checklist

A combined branch may label the route an **integrated demo prototype** only when every required item below is satisfied on one commit.

### A. Route coherence

- [ ] One documented entry point links all six route steps in order.
- [ ] Each transition states why the next experience resolves a question raised by the previous one.
- [ ] The route has one shared evidence-kind legend and one shared source-revision policy.
- [ ] No required step sends the learner to an unrelated feature menu.
- [ ] A complete static route can be followed without JavaScript.

### B. Lesson contracts

- [ ] Lab 0, Lab 1, and Lecture 0 each declare learner, prerequisite, objective, misconception, action, output, assessment, revision, validator, and accessibility fallback.
- [ ] Browser-derived results are visually and textually separated from native behavior.
- [ ] Authored/source-derived trace content is not labelled native-captured.
- [ ] Progress state never substitutes for scored correctness.

### C. Reproducibility and legal boundary

- [ ] `uv sync --locked`, compiler, CMake, and Ninja checks are represented in Lab 0.
- [ ] Exact repository, upstream, fixture, trace, and lock revisions are retained.
- [ ] The mandatory route redistributes no third-party model weights.
- [ ] Optional model use requires an explicit learner-provided path and separate outcome labels.
- [ ] Ordinary CI performs no paid or secret-dependent media generation.

### D. Deterministic evidence

- [ ] Synthetic GGUF regeneration and golden parse agree.
- [ ] Trace replay is deterministic and bounded.
- [ ] At least one authoritative figure is regenerated from structured data and checksum-verified.
- [ ] Media manifests record accepted/revised/rejected status and stale-asset checks.
- [ ] Every technical claim links to deterministic evidence or is labelled Interpretation/Open Question.

### E. Progress and privacy

- [ ] Save/export/clear/import/resume works with the versioned local schema.
- [ ] Invalid imports do not mutate the current valid state.
- [ ] Export excludes identity, telemetry, credentials, raw prompts, and unnecessary free text.
- [ ] No server-side or authenticated synchronization is present.
- [ ] Research-data collection remains a separate, unapproved pathway.

### F. Accessibility

- [ ] All required actions are keyboard-operable.
- [ ] Focus order and visible focus receive browser-level review, not only static markup checks.
- [ ] Diagrams have alt text and complete text/static equivalents.
- [ ] Trace motion can be reduced or removed without losing information.
- [ ] Audio/video supplements, if present, have captions/transcripts and are optional.
- [ ] The route remains understandable when local storage is unavailable.

### G. Validation on one head

- [ ] Context, link, schema, unit, compilation, shell, strict MkDocs, asset, and built-site accessibility checks pass on the same commit.
- [ ] The deployed site or a locally served build is checked for the route, assets, keyboard operation, and broken links.
- [ ] Ubuntu 24.04 and devcontainer Lab 0 records are retained separately; absence is not hidden by component CI.
- [ ] Known failures and degraded-mode behavior are visible in the demo limitations.

### H. Review and claim discipline

- [ ] Independent technical review covers the fixture, Lab 1 explanations, trace anchors, deterministic figure, and benchmark answer key.
- [ ] The demo does not claim learner benefit before an approved and completed evaluation.
- [ ] The demo does not call authored replay native instrumentation.
- [ ] The demo does not frame attractiveness, clicks, or completion alone as an educational outcome.
- [ ] Human supervision, corrections, rejected outputs, missing effort data, and maintenance burden remain visible for the case study.

## Machine-reviewable acceptance record

`DEMO-01` should later add a versioned JSON acceptance record with:

- repository and upstream revisions;
- route entry URL/path;
- component revisions and validator results;
- environment records for browser/static, Ubuntu, and devcontainer tiers;
- accessibility checks and human-review status;
- progress round-trip result;
- deterministic figure/media lifecycle result;
- known failures, exclusions, and claim boundaries.

This run defines the fields conceptually; it does not add a validator or report success.

## Claims and evidence boundary

### Verified

- The repository has separate validated contracts or prototypes for Lab 0 reporting, the synthetic GGUF lab, authored/source-derived trace replay, local progress portability, deterministic figures, media lifecycle, and a fair viewer benchmark.
- The current evidence backlog lacks one explicit acceptance contract tying them into a learner route.

### Interpretation

- Requiring every transition to answer a question raised by the previous experience is a practical guard against the “collection of tools” rejection risk.
- A synthesis task that orders storage, loading, graph, execution, and output states is the narrowest shared outcome across the three experiences.

### Historical

- Component CI has passed on separate stacked heads; this does not prove one combined artifact.

### Open question

- Whether the route is usable on one combined branch and supported environments.
- Whether learners or experts improve setup diagnosis, GGUF reasoning, or code tracing.
- Whether the current authored trace should later be replaced or supplemented by a faithfully captured native path.

## Rejected alternatives

- **Feature dashboard as the demo:** rejected because navigation among tools does not establish a learning progression.
- **Require a downloadable model:** rejected because the core route can teach stage boundaries and GGUF structure without redistributing restricted weights.
- **Treat browser and native tiers as interchangeable:** rejected because their executable capabilities and evidence semantics differ.
- **Use generated illustrations as architecture evidence:** rejected because technical correctness must remain deterministic and source/trace-derived.
- **Add authenticated progress sync now:** rejected because it adds privacy, hosting, consent, and maintenance risk without supporting the first educational claim.
- **Begin native instrumentation before integrated replay review:** rejected because provenance, trace bounds, and learner tasks must be stable first.

## Exact next dependency

`STACK-01` still requires human progress-branch approval and a passing combined head. After that, implement a machine-readable `DEMO-01` acceptance record and exercise this checklist on the canonical branch. Measured `LAB0-03` and `LAB0-04`, independent `REVIEW-01`, and approved `EVAL-01` remain separate gates.