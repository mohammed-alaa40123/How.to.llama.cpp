# REVIEW-02 adversarial EAAI evidence gates

- **Starting commit:** `065c2d521261e9f9d0e3016f223771cb287a92f3`
- **Assigned milestone:** `REVIEW-02`
- **Role:** Adversarial Reviewer
- **Date:** 2026-07-17 17:15 Africa/Cairo

## Inspected

- root README and current project state;
- publication orchestrator state, evidence backlog, two-week execution plan and handoff ledger;
- active stacked PRs through MEDIA-02;
- component CI records and current MEDIA-02 final-head CI;
- Lab 0, Lab 1, trace/viewer, progress, media and retrospective evidence boundaries.

## Verified

- MEDIA-02 final head `065c2d521261e9f9d0e3016f223771cb287a92f3` passed Documentation CI run `29587245436`.
- The repository has deterministic contracts and passing component CI for the fixture, browser GGUF slice, trace anchors/replay, viewer, progress integration, information-equivalent benchmark and media lifecycle.
- No measured Ubuntu 24.04 or devcontainer Lab 0 record exists.
- No approved learner/expert evaluation has been completed.
- No independent llama.cpp/GGML technical review has been retained.
- DATA-01 contains a three-archetype first batch, not a longitudinal dataset.
- The active trace remains authored/source-derived rather than native-captured.

## Interpretation

The primary rejection risk is evidence inflation: contract validation and component CI are substantially stronger than ordinary planning documents, but they do not establish learner benefit, clean-environment reproducibility, independent correctness, integrated deployability or agent-workflow superiority.

## Increment produced

- `docs/publication/reviewer-notes.md`
- `docs/publication/claims-evidence-table.md`
- `docs/publication/rejection-risks.md`
- `docs/publication/eaai-review-scorecard.md`
- evidence-backlog update that converts the review findings into explicit gates

## Fatal flaws recorded

1. no approved/completed usefulness evaluation;
2. no independent technical correctness review;
3. no measured local-native or devcontainer Lab 0 evidence;
4. no longitudinal agent-workflow dataset.

## Review score

Adversarial reviewer readiness: **38/100**. Current disposition: **reject — promising artifact, insufficient experience-report evidence**.

## Human review needs

- nominate an independent llama.cpp/GGML reviewer;
- approve the learner or expert evaluation pathway and ethics decision;
- resolve overlapping/stacked PR merge order;
- provide clean Ubuntu and devcontainer execution environments.

## Limitations

This review does not test learner outcomes, execute the blocked native environments, perform assistive-technology testing, audit every historical run, or verify an unpublished EAAI-27 call. It adds no manuscript prose and authorizes no recruitment.

## Next dependency

After commit-scoped CI, the orchestrator should integrate these gates and prioritize: `REVIEW-01`, `LAB0-03`, `LAB0-04`, `DEMO-01`, `EVAL-01`/`BASE-01`, then broader audited `DATA-01`. Broad feature expansion should remain lower priority.