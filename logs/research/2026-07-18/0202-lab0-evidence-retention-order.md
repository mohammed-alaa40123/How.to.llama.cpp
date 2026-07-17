# LAB0-03 evidence-retention ordering repair

## Run identity

- **Starting commit:** `86fab5b60c78f125b3611ee6f737c1c906e8b427`
- **Assigned milestone:** `STACK-01` remained human-blocked; next dependency-safe P0 evidence task was the failing `LAB0-03` Ubuntu run
- **Learner outcome:** preserve exact setup/build/launch evidence and failure diagnostics so a learner or reviewer can identify the failing stage rather than seeing an opaque workflow failure
- **Implementation commit:** `cbf715820906339ee32d237c9a5137d9e8adaa82`

## Evidence inspected

- Workflow run `29619592906` executed on Ubuntu `24.04.4`.
- The bounded runner step completed, but semantic validation and artifact upload both failed.
- No workflow artifact was retained, so the first measured run could not be independently inspected after failure.
- Documentation CI run `29619592930` passed on the same pull-request head.

## Bounded change

Updated `.github/workflows/lab0-ubuntu-reproducibility.yml` only for evidence ordering and observability:

1. stage the emitted JSON to an explicit `$RUNNER_TEMP` path;
2. fail with stable diagnostic `LAB0_REPORT_MISSING` when the runner emits no report;
3. print the retained report SHA-256;
4. upload the exact report **before** semantic validation;
5. validate the same retained path that was uploaded;
6. fail the job when runner, retention, or validation is unsuccessful.

No Lab 0 command, fixture, source revision, tool version, model policy, timing semantic, schema, or educational claim changed.

## Truth labels

- **Verified:** run `29619592906` failed after the runner step and retained no artifact.
- **Interpretation:** artifact upload must precede semantic validation so malformed or contradictory measured evidence remains available for diagnosis rather than disappearing with the failed check.
- **Historical:** the original workflow validated before upload and used a workspace-relative path for both operations.
- **Open question:** the next commit-scoped run must reveal whether the report itself is semantically invalid or whether the failure was path/retention related.

## Validation and safety

- YAML scope is limited to the existing Ubuntu 24.04 model-free lane.
- Ordinary CI still performs no inference, model download, telemetry, paid API call, personal-data collection, or secret recording.
- A failed report is retained as evidence, not relabelled as a successful environment.
- Commit-scoped workflow results and the uploaded JSON are authoritative.

## Human-review needs and limitations

- `STACK-01` still requires the explicit canonical progress/merge decision.
- `LAB0-03` remains in progress until a retained report passes semantic validation or an exact failed report is reviewed and repaired.
- `LAB0-04`, independent technical review, evaluation approval, and canonical demo execution remain open.

## Next dependency

Inspect the next Ubuntu workflow artifact and validator result. Make at most one evidence-backed repair to the runner or contract; do not broaden Lab 0 or claim reproducibility before the retained record validates.
