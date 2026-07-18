# EAAI orchestration — retain the first measured Ubuntu Lab 0 failure

- **Starting commit:** `f7f856c96e2ed1e4b45186bd444f129f9cd9edf9`
- **Assigned milestone:** coordinate the highest-priority evidence path after `STACK-01`; reconcile the first measured `LAB0-03` run without overstating success.
- **Learner outcome affected:** Lab 0 should identify the failing setup stage and preserve a reviewable diagnostic rather than collapsing build, launch and inference into one status.

## Evidence inspected

- PR #45 head: `d96eaf2a0da13fae993931acef839541d6f6a506`.
- Documentation CI run `29619847677`: passed.
- Ubuntu reproducibility run `29619847701`: failed only at the final enforcement step after report generation, retention, upload and semantic validation succeeded.
- Retained artifact `8421805335`, digest `sha256:bdfe6d9b27f892393f9cd1fea6916134fa0bc7b846ae9bc77b02d18b89e1b634`, expires 2026-08-16.
- Exact report outcome: Ubuntu 24.04/x86_64, toolchain checks passed, `uv sync --locked` failed, diagnostic `UV_LOCK_DRIFT`, setup/build/launch false, inference not attempted, model redistribution false.

## Claim classes

### Verified

- A clean GitHub-hosted Ubuntu 24.04 environment was available and produced a retained, schema-valid degraded Lab 0 record.
- The evidence-retention repair worked: the report was uploaded before the workflow intentionally failed.
- The observed failure is currently classified as `UV_LOCK_DRIFT`; the build and launch phases were not reached.

### Interpretation

- `LAB0-03` is no longer blocked by absence of an Ubuntu environment. It is **in progress with measured negative evidence**.
- The failed setup is useful EAAI experience-report evidence because it demonstrates failure classification and repair workflow, but it does not support local-native reproducibility success.

### Historical

- Earlier orchestration files described Ubuntu execution as unavailable and stated that no measured Ubuntu row existed. Those statements are now stale.

### Open question

- The exact cause of `uv sync --locked` failure is not preserved in the JSON because command output is intentionally excluded. A bounded repair should add a secret-safe failure-detail code or retained sanitized diagnostic without recording personal paths or arbitrary logs.

## Coordination decisions

1. Keep `STACK-01` as the only integration P0 and human-blocked.
2. Reclassify `LAB0-03` from `blocked` to `in progress` with measured degraded evidence.
3. Assign the Validation Architect one bounded next step: reproduce and classify the `uv sync --locked` failure, then rerun the unchanged build/launch path.
4. Keep `LAB0-04`, `REVIEW-01`, `EVAL-01`, `DATA-01B`, `DEMO-01` and manuscript drafting blocked under their existing gates.
5. Do not increase the overall readiness percentage; negative evidence improves auditability but does not satisfy reproducibility.

## Validators and failures

- Documentation CI passed on the measured-run head.
- The Lab 0 report passed semantic validation.
- The workflow failed intentionally because the bounded path did not complete.
- No model, prompt, generated output, learner data, telemetry, credential or paid API was introduced.

## Human-review needs

- Approve the canonical progress implementation and merge order.
- Nominate the independent technical reviewer.
- Approve evaluation and retrospective coding pathways.

## Evidence produced

- This orchestration reconciliation and handoff.
- No learner-facing code, manuscript prose or new claim of reproducibility.

## Next dependency

Validation Architect: add a bounded, secret-safe cause classification for the `uv sync --locked` failure and rerun Ubuntu 24.04. If successful, retain the measured build/launch record; if it fails, retain the exact revised diagnostic. Return immediately to `STACK-01` after human approval.
