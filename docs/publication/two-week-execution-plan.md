# Executable-learning two-week execution plan

_Last updated: 2026-07-16 23:00 Africa/Cairo_

This is the dependency-ordered implementation plan for the first executable-learning vertical slice of **How.to.llama.cpp**. It covers July 17-31, 2026 and is intentionally narrower than the long-term interactive-textbook roadmap.

## Status and truth labels

- **Verified:** the repository already has revision-pinned documentation, strict MkDocs CI, interactive explorers, deterministic validators, and the pinned llama.cpp baseline `e3546c7948e3af463d0b401e6421d5a4c2faf565`.
- **Verified:** the requested publication coordination files `orchestrator-state.md`, `evidence-backlog.md`, and `agent-handoffs.md` were not present on `main` at the start of this increment.
- **Interpretation:** the safest first increment is to freeze architecture, learning-objective, fixture, validation, accessibility, privacy, and licensing gates before implementing broad lab or media features.
- **Open question:** which bounded native path should become the first executable lecture: GGUF loading, graph construction, or one-token decode.

## Target learners

The first release targets advanced undergraduate, graduate, and early-stage systems researchers who can read C/C++ and Python but do not yet understand how llama.cpp connects GGUF storage, virtual memory, GGML graph construction, backend scheduling, and token generation.

### Prerequisites

Learners should be able to:

- use a shell and Git;
- read basic C/C++ and Python;
- recognize tensors, matrix multiplication, and transformer layers;
- distinguish files, virtual addresses, and physical memory at an introductory level.

The labs must provide short refreshers and static fallbacks rather than assuming deep operating-systems expertise.

## Initial learning experiences

### Lab 0 — Build and run llama.cpp

| Field | Requirement |
|---|---|
| Intended learner | A learner who can use a terminal but has not built llama.cpp from source |
| Learning objective | Explain which parts are managed by `uv`, CMake/Ninja, the native compiler, llama.cpp, and the model fixture |
| Predicted misconception | `uv` builds llama.cpp or a successful binary alone proves a model/inference path is valid |
| Executable action | Run `uv sync --locked`, configure and compile a bounded target, execute a smoke test, and run `uv run lab check 00` |
| Observable output | Environment report, compiler/build result, smoke-test result, and machine-readable checker summary |
| Formative assessment | Identify which tool owns each dependency and diagnose one seeded setup failure |
| Source revision | Pin both this repository revision and the llama.cpp revision used by the lab |
| Validation | Lockfile check, toolchain detection, bounded build, deterministic smoke test, failure-code assertions |
| Accessibility fallback | Copyable commands, text transcript, non-color status labels, and a static troubleshooting decision tree |

Constraints:

- Python tooling uses `uv sync --locked` and `uv run`.
- Native compilation uses CMake and Ninja where available.
- No restricted model weights are redistributed.
- The smoke test uses a synthetic/tiny legal fixture or a clearly documented user-provided model path.
- Setup, build, and execution times are logged separately.

### Lab 1 — GGUF Anatomy

| Field | Requirement |
|---|---|
| Intended learner | A learner who understands tensors but not GGUF physical layout |
| Learning objective | Parse and explain the header, metadata, tensor descriptors, alignment, offsets, and mapped tensor bytes |
| Predicted misconception | GGUF stores an executable GGML graph or loading metadata means all tensor pages are physically resident |
| Executable action | Predict a field/offset, parse a small fixture in the browser, inspect bytes and descriptors, then explain the result |
| Observable output | Parsed header, metadata table, tensor layout visualization, alignment calculation, and answer record |
| Formative assessment | Predict-Discover-Explain checkpoints for graph storage, tensor offsets, and mapping versus residency |
| Source revision | Pin the GGUF specification and llama.cpp parser revision used by each claim |
| Validation | Fixture checksum, parser golden output, offset/alignment assertions, browser-build test |
| Accessibility fallback | Equivalent table/text dump, keyboard operation, descriptive labels, and downloadable fixture |

The browser implementation may simulate or parse bounded data, but must never imply it executes the native llama.cpp runtime.

### Executable Lecture 0 — Bounded source trace

| Field | Requirement |
|---|---|
| Intended learner | A learner who can read source but struggles to connect call flow, runtime state, and explanation |
| Learning objective | Trace one bounded llama.cpp/GGML path while distinguishing captured runtime evidence from authored explanation |
| Predicted misconception | Every displayed value is captured from native execution, or graph reuse means outputs/token values are reused |
| Executable action | Step forward/back through source locations, inspect call stack and runtime objects, predict the next transition |
| Observable output | Highlighted source, explanation, runtime-state panel, and one deterministic visualization |
| Formative assessment | Code-tracing questions before selected reveal steps |
| Source revision | Every trace points to an immutable upstream revision and file/line/function identity |
| Validation | JSON schema, source-link validation, deterministic replay, bounds tests, missing-field behavior |
| Accessibility fallback | Keyboard navigation, ordered transcript, static trace table, reduced-motion mode |

The first trace must be narrow. Selection order:

1. GGUF loading if it yields the clearest deterministic fixture;
2. graph construction if source-link and tensor-shape capture are feasible without invasive patches;
3. one-token decode only after trace-size and instrumentation risk are bounded.

## Platform architecture

The system has three execution tiers with a shared lesson contract.

| Tier | Purpose | Must support | Must not claim |
|---|---|---|---|
| Browser/static | Zero-install concepts and small fixtures | parsing, simulation, visualization, checkpoints, local progress | full native llama.cpp execution |
| Local native | Real compiler and llama.cpp experiments | `uv`, CMake/Ninja, bounded native targets, diagnostics | uniform performance across machines |
| Cloud container | Reproducible one-click environment | devcontainer, pinned tools, smoke checks, persistent workspace where available | free/unlimited compute or permanent storage |

All tiers use the same lesson metadata fields: learner, prerequisite, objective, misconception, action, output, assessment, source revision, validation, and accessibility fallback.

## Repository structure to introduce incrementally

```text
labs/
  fixtures/
  browser/
  native/
executable_lectures/
  traces/
  explanations/
trace_viewer/
media/
  manifests/
  prompts/
  storyboards/
  provenance/
progress/
scripts/
.devcontainer/
docs/
  labs/
  executable-lectures/
  media/
  progress/
  publication/
```

Directories are created only when their first validated artifact is added. Empty scaffolding is not progress.

## Authoritative technical-media rule

Deterministic SVG, Mermaid, Graphviz, D3, or trace-derived figures are the authoritative representation of code paths, tensor shapes, pointer relationships, ownership, and timing.

Optional generative images, narration, or video are supplemental and must satisfy all of the following before publication:

- manifest-driven generation;
- prompt or storyboard hash;
- generator and model/version record;
- source revision and asset checksum;
- alt text plus captions/transcript where applicable;
- declared technical claims, preferably none;
- licensing/privacy notes;
- human technical review status;
- accepted, revised, or rejected outcome;
- cached artifact and manual/review-gated regeneration.

Ordinary pushes and pull requests must not spend external API budget or silently replace approved media.

## Trace schema minimum contract

A first sample trace must include:

```json
{
  "trace_version": "0.1.0",
  "lesson_id": "gguf-load-00",
  "source": {
    "repository": "ggml-org/llama.cpp",
    "revision": "immutable commit",
    "captured": false
  },
  "steps": [
    {
      "sequence": 0,
      "phase": "entry",
      "location": {
        "file": "path/to/file.cpp",
        "line": 1,
        "function": "function_name"
      },
      "call_stack": [],
      "objects": {},
      "tensor_shapes": [],
      "memory_events": [],
      "explanation_id": "entry",
      "evidence_kind": "authored-example"
    }
  ]
}
```

Required distinctions:

- captured runtime evidence;
- source-derived deterministic data;
- authored explanatory example;
- interpretation or open question.

The viewer must not collapse these categories into one visual style without labels.

## Progress-data boundary

The first progress implementation is local-only:

- browser persistence using local storage or IndexedDB;
- versioned JSON export/import;
- course version and source revision;
- checkpoint state and attempt counts;
- no raw learner code, prompts, email, name, or silent telemetry;
- corruption recovery and schema migration tests.

Authenticated synchronization and research-data collection are separate future decisions requiring hosting, consent, security, and ethics review.

## Week 1 — Foundation, July 17-23

### Milestone W1.1 — Freeze contracts

Deliver:

- target learner and prerequisite statement;
- learning contract for Lab 0, Lab 1, and Executable Lecture 0;
- platform comparison and selected default path;
- legal fixture decision record;
- trace, media-manifest, and progress schemas.

Acceptance gate:

- each artifact has an owner, validator, source revision policy, accessibility fallback, and explicit non-goals.

### Milestone W1.2 — Smallest vertical slice

Deliver:

- Lab 0 bootstrap command contract and checker interface;
- one synthetic/tiny legal fixture decision;
- one sample trace JSON;
- minimal viewer shell that can step through the sample;
- one deterministic figure generated from structured data.

Acceptance gate:

- all pieces run without paid APIs;
- sample output is deterministic;
- CI can reject malformed trace/media/progress data;
- no claim of native capture is made for authored sample data.

### Milestone W1.3 — Validation before expansion

Deliver:

- schema validators and focused tests;
- accessibility checklist and static fallback requirements;
- environment reproducibility matrix template;
- asset provenance and review-state validator design.

Acceptance gate:

- adversarial review has no unresolved fatal architecture flaw;
- Week 2 work is dependency-ordered rather than parallel feature sprawl.

## Week 2 — Vertical slices and evidence, July 24-31

### Milestone W2.1 — Lab 0 end to end

Deliver:

- locked Python environment;
- native build instructions and checker;
- bounded smoke test;
- failure diagnostics;
- local and devcontainer reproducibility evidence.

Acceptance gate:

- a clean environment can reach the expected output using documented commands;
- failures are machine-readable and educationally explained;
- no model licensing ambiguity remains.

### Milestone W2.2 — GGUF browser lab

Deliver:

- small fixture and checksum;
- parser/visualizer;
- Predict-Discover-Explain checkpoints;
- local progress persistence and export/import;
- static text/table fallback.

Acceptance gate:

- golden parsing and alignment tests pass;
- keyboard-only completion is possible;
- native-runtime claims are explicitly excluded.

### Milestone W2.3 — Trace viewer with bounded real evidence

Deliver:

- viewer step controls;
- highlighted source and explanation panel;
- one runtime/object/tensor/memory visualization;
- one real or faithfully captured path;
- transcript/static fallback.

Acceptance gate:

- source links resolve against the pinned revision;
- captured versus authored fields are distinguishable;
- replay is deterministic and trace size remains bounded.

### Milestone W2.4 — Media and publication evidence dry run

Deliver:

- deterministic figure build;
- media manifest/provenance validation;
- optional reviewed sample only when credentials and review are available;
- asset acceptance/revision/rejection log;
- EAAI evidence records for setup, checkpoints, code tracing, accessibility, reproducibility, and agent/human effort.

Acceptance gate:

- ordinary CI uses no external paid generation;
- stale/unreviewed assets fail validation or remain unpublished;
- no participant data is collected without explicit approval and required review.

## CI lanes

Introduce lanes only with their corresponding artifact:

1. `uv lock` and Python-tooling validation;
2. browser-lab build and golden-fixture tests;
3. bounded native smoke test where CI cost is acceptable;
4. trace-schema and source-link validation;
5. media-manifest, checksum, alt-text, caption/transcript, and review-state validation;
6. progress-schema migration/export/import tests;
7. existing strict MkDocs, link, generated-HTML, and accessibility checks.

## Evidence to retain for the EAAI case study

- starting and ending commit;
- assigned objective and dependency;
- generated and rejected alternatives;
- human corrections and review decisions;
- source/reference errors caught;
- validator failures and fixes;
- setup completion and time-to-ready protocol;
- checkpoint and code-tracing assessment design;
- reproducibility matrix;
- accessibility findings;
- API/model/tool cost proxies;
- asset accepted/revised/rejected counts.

These are evidence-design requirements, not claims that learner benefit has already been demonstrated.

## Immediate dependency-ordered backlog

1. Create the publication handoff ledger and have the orchestrator record the authoritative top 3-7 assignments.
2. Decide the legal fixture for Lab 0 and Lab 1.
3. Add machine-readable trace, media-manifest, and progress schemas with focused validators.
4. Add the authored sample trace and minimal static viewer shell.
5. Define the Lab 0 checker interface before adding environment automation.
6. Generate one deterministic figure from structured input.
7. Add the first CI lane only after its artifact exists.

## Definition of done on July 31

A reviewer can reproduce or inspect an integrated demonstration containing:

- Lab 0 setup/build/smoke-check path;
- browser GGUF Anatomy lab;
- bounded executable-lecture trace viewer;
- deterministic technical figure pipeline;
- local progress persistence and JSON export/import;
- trace/media/progress validators;
- accessibility and static fallbacks;
- validation results, known limitations, and next-month roadmap.

The demonstration is not considered complete merely because pages render. Its fixtures, claims, source revisions, validation, privacy boundary, and fallback paths must be explicit.