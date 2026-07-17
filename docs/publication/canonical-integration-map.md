# Canonical EAAI integration map

_Last updated: 2026-07-17 19:04 Africa/Cairo_

This document is the bounded `STACK-01` merge plan. It does not merge branches, close pull requests, or claim that the integrated demo exists. Its purpose is to let a human reviewer integrate the executable-learning work without reconstructing the branch graph from dozens of draft pull requests.

## Decision summary

**Recommended canonical implementation spine:** PRs **#3 → #4 → #5 → #6 → #7 → #9 → #11 → #13 → #15 → #16 → #17 → #18 → #21 → #22 → #24 → #25 → #27 → #28 → #29**.

After that spine is integrated, reconcile the non-spine evidence/state branches in this order:

1. PR **#31** — official EAAI-27 venue facts;
2. PR **#32** — retrospective missing-data policy;
3. PR **#30** — orchestration state, manually reconciled rather than merged verbatim because its venue state predates PR #31 and its DATA-01 state predates PR #32;
4. this `STACK-01` branch — merge map, state update, run record and handoff.

The final integration target must be a new branch from current `main`, not a merge of every open draft PR. Each retained increment should be applied once, in dependency order, followed by the complete Documentation CI suite.

## Why this is the canonical spine

The spine preserves the dependency chain that produced the currently validated learner-facing artifacts:

| Stage | PR | Retained outcome | Recorded CI evidence |
|---|---:|---|---|
| Foundation | #3 | two-week plan, legal fixture decision and deterministic synthetic GGUF package | retained in branch/PR evidence |
| Trace contract | #4 | versioned trace schema and authored sample | superseded in part by #13 corrections, but schema foundation retained |
| Progress contract | #5 | local-only privacy-minimized progress schema | retained |
| Orchestration bootstrap | #6 | initial backlog and authority model | later state is reconciled, but foundational files are retained |
| CI repair | #7 | strict MkDocs handoff-link repair | Documentation CI `29546570700` |
| Media contract | #9 | manifest, provenance and secret-safe generation boundary | `29549208249` |
| Deterministic figure | #11 | replayable GGUF SVG and checksum validation | `29553868078` |
| Trace correction | #13 | correct pinned anchors, source lock and deterministic replay | `29556540213` |
| Viewer | #15 | keyboard-operable narrow trace viewer and transcript fallback | `29559239071` |
| Viewer orchestration refresh | #16 | state needed by downstream Lab 1 branch | retained as ancestry; final state is reconciled later |
| Browser GGUF lab | #17 | Predict–Discover–Explain vertical slice and browser/native boundary | `29562479577` |
| Lab 0 evidence contract | #18 | reproducibility schema, diagnostics and timing definitions | `29565651085` |
| Agent evidence contract | #21 | versioned scheduled-agent run schema | `29568983813` |
| First retrospective batch | #22 | success, CI-repair and blocked-reassignment examples | `29572506104` |
| Progress implementation | #24 | local import/export, validation-before-mutation and privacy checks | `29575542793` |
| Lab 1 progress integration | #25 | anonymous resume state and export/import controls | `29579032392` |
| Fair viewer benchmark | #27 | information-equivalent static-versus-viewer task contract | `29583741909` |
| Media lifecycle | #28 | accepted/revised/rejected states and stale-asset detection | `29587245436` |
| Adversarial review | #29 | claims/evidence table, rejection risks and reviewer scorecard | final-head CI must be rechecked during integration |

CI identifiers above are historical evidence for the named component heads. They do not prove that the proposed combined branch passes.

## Duplicate and overlap decisions

### Trace validation: retain PR #13; supersede PR #14

PRs #13 and #14 independently correct the same false-but-plausible trace anchors. PR #13 is selected because the downstream viewer and Lab 1 spine was built from it. PR #14 must not be merged independently.

**Preservation check:** before closing #14, compare its validation-plan wording and tests against #13. Any materially stronger invariant not already present must become a separate reviewed follow-up rather than a second trace implementation.

### Progress implementation: retain PR #24; do not merge PR #23 into the spine

PRs #23 and #24 start from the same DATA-01 batch and implement overlapping local progress stores. PR #24 is selected because PR #25 and every later learner-facing vertical slice in the canonical spine depend on it.

PR #23 contains two potentially useful behaviors that are not silently claimed as retained:

- explicit migration from progress schema `0.0.1` to `0.1.0`;
- last-known-valid snapshot recovery when the primary snapshot is corrupt.

These behaviors should become a later bounded `PROGRESS-04` proposal after canonical integration, with tests adapted to the selected #24/#25 store. PR #23 should remain open or be closed as superseded only after that human decision is recorded.

### Reviewer packages: retain PR #29; supersede PR #8 as current disposition

PR #8 is the first architecture-stage skeptical review. PR #29 is the current, broader adversarial review and should be authoritative for present rejection risks. Preserve PR #8's run record as historical evidence if it is not already present in the spine; do not maintain two current scorecards.

### Orchestration snapshots: reconcile, do not merge every snapshot

PRs #10, #20, #26 and #30 are time-specific state snapshots. Their durable run logs are useful longitudinal evidence, but their mutable authority files conflict by design. The final integration branch should contain:

- all unique durable run logs;
- one current `orchestrator-state.md`;
- one current `evidence-backlog.md`;
- one current roadmap, scorecard and two-week plan.

Older authority-file versions must not overwrite later verified venue or evidence facts.

### Literature branches

PRs #12 and #19 are evidence-bearing literature branches that are not on the implementation spine. Their unique literature-map, ledger, platform/media recommendations and benchmark rationale must be compared and applied once. PR #31 then updates the venue facts using the official EAAI-27 call. No manuscript prose is introduced.

## Exact human-review workflow

1. Create `integration/eaai-july-vertical-slice` from current `main`.
2. Apply the canonical spine in the listed order, stopping at the first conflict.
3. After each logical cluster, run unit tests and strict documentation validation; do not rely only on historical component CI.
4. Compare PR #14 against retained #13, PR #23 against retained #24/#25, and PR #8 against retained #29 before closing or superseding them.
5. Apply unique literature evidence from #12 and #19 once.
6. Apply PR #31 and PR #32.
7. Reconcile the authority files using PR #30 as a structural base while correcting the EAAI-27 and DATA-01 status fields.
8. Apply this merge-map increment and append the final integration result.
9. Run the complete Documentation CI suite on the combined head.
10. Only after passing CI, open one draft integration PR to `main` and link every superseded PR to it.

## Required final validation

The canonical branch is not accepted until all of the following pass on one commit:

```text
python3 scripts/validate_project_context.py
python3 scripts/validate_interactive_links.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -m py_compile scripts/*.py tests/*.py
bash -n scripts/*.sh
mkdocs build --strict
python3 scripts/validate_built_site_accessibility.py site
```

Also require:

- no duplicate progress-store implementation or conflicting published module;
- no stale authored trace or source-lock fixture;
- no ordinary-CI external media API call;
- no model redistribution or model-free launch described as inference;
- no authority file that says the official EAAI-27 call is unavailable;
- no claim that component CI proves integrated deployability, educational benefit or native reproducibility.

## Claim classification

### Verified

- The executable-learning work is distributed across a long draft-PR stack with parallel branches.
- PRs #13/#14 and #23/#24 are overlapping implementations from common bases.
- PR #25 and later learner-facing work depend on PR #24, not PR #23.
- PRs #30, #31 and #32 are parallel descendants of PR #29 and require reconciliation rather than blind sequential merging.
- Component CI identifiers exist for the retained artifacts listed above.

### Interpretation

- Selecting #24 minimizes integration risk because it preserves the tested downstream Lab 1 progress path.
- A clean integration branch with one current authority state is more reviewable than merging every historical orchestration snapshot.
- Unique features from superseded branches should be reintroduced only as bounded follow-ups after the canonical branch is stable.

### Historical

- The stack grew through hourly specialist increments while native Ubuntu and devcontainer execution remained unavailable.
- Earlier orchestration snapshots and reviewer packages were accurate at their respective times but are not current authority.

### Open questions

- Human approval of #24 as the canonical progress implementation.
- Whether PR #14 or #23 contains a uniquely stronger invariant worth a later follow-up.
- Final-head CI for PR #29 and the eventual combined branch.
- Whether every unique literature/run-log artifact is already reachable from the proposed spine.

## Acceptance status

`STACK-01` has a concrete proposed merge map and overlap decisions, but remains **in progress** until a human approves the progress choice and one canonical integration branch passes the full validation suite. The next dependency-safe documentation task is `DEMO-01A`; actual integration and measured Lab 0 runs remain separate assignments.