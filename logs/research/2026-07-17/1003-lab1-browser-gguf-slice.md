# Lab 1 browser-first GGUF anatomy vertical slice

## Run scope

- **Starting commit:** `17d6da2c269df7d1e524cd4f5b94f677d90e9c32`
- **Assigned milestone:** `LAB1-01`, the highest orchestrator-assigned Documentation Builder item.
- **Bounded increment:** deterministic browser parser plus three Predict–Discover–Explain checkpoints; progress persistence remains a separate dependency.
- **Learner outcome:** parse and explain the synthetic GGUF header, metadata, tensor descriptors, alignment and payload ranges without confusing browser-derived format evidence with native runtime behavior.

## Evidence inspected

The run inspected the mandatory README, project state, research log and ledger, publication orchestration files, handoffs, latest run log, current PR/CI state, deterministic fixture generator and golden record, and MkDocs integration.

No new external source was added; the research ledger does not require a bibliographic change.

## Evidence produced

- deterministic payload builder derived from the project-owned generator;
- checked-in base64 fixture plus Python golden output;
- bounded framework-free browser parser using `DataView`;
- browser/Python canonical-field agreement check;
- text tensor-layout visualization;
- three formative checkpoints for graph storage, alignment and mapping versus residency;
- static table fallback and explicit evidence labels;
- focused deterministic and contract tests;
- MkDocs navigation and JavaScript integration.

## Claims

### Verified

- The fixture is 428 bytes with SHA-256 `688d0ef28c83d6972e291cc0342e695540eae8496b3ec8e92bdbb91e3982a564`.
- The browser payload is derived from the same Python fixture builder and golden parser.
- The browser parser supports only the bounded teaching subset and rejects truncation, unsupported types, unsafe counts, invalid dimensions, misalignment and out-of-file tensor ranges.

### Interpretation

- Parsing the small fixture in-browser isolates GGUF layout concepts before native toolchain and OS-memory behavior are introduced.
- Predict–Discover–Explain checkpoints make misconception boundaries visible, but their educational effect is not yet measured.

### Historical

- Technical claims remain scoped to pinned llama.cpp baseline `e3546c7948e3af463d0b401e6421d5a4c2faf565`.

### Open question

- Browser/Python agreement awaits commit-scoped CI.
- Native llama.cpp acceptance of this format-teaching fixture remains unclaimed.
- Learner benefit and checkpoint validity require an approved evaluation pathway.

## Validation and limitations

- No model weights, model download, native execution, `mmap`, telemetry, participant data, credentials, paid API, generative media or manuscript prose were introduced.
- Progress persistence is intentionally excluded until `PROGRESS-02`.
- The browser output does not establish inference, physical page residency or graph construction.
- This runtime lacks a local checkout and `gh`; final-head GitHub Actions is the execution authority.

## Human review needs

- Independent GGUF/llama.cpp technical review remains required.
- Deployed keyboard and screen-reader verification should occur after the stack merges and Pages deploys.

## Ending state

- **Branch:** `agent/lab1-browser-gguf-slice`
- **Next dependency:** obtain passing final-head Documentation CI; then connect local progress only after `PROGRESS-02` is evidenced.
