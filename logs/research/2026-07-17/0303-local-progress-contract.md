# Local learner progress contract

- Start commit: `ce6e562127ab09886f7c239bd4142900d2f7b877`
- Assigned milestone: Week 1 machine-readable learner-progress schema
- Learner outcome: export and restore bounded checkpoint state while recognizing the boundary between local resume data, mastery evidence, telemetry, and authenticated sync

## Files

- `schemas/learner-progress.schema.json`
- `scripts/validate_learner_progress.py`
- `progress/examples/local-progress-v0.json`
- `tests/test_validate_learner_progress.py`
- `docs/progress/progress-schema.md`

## Verified

The contract fixes storage scope to `local-only`, pins course and source revisions, bounds file/lesson/checkpoint sizes, and records only lesson status, last step, checkpoint states, and attempt counts. The semantic validator rejects privacy-sensitive fields recursively, mutable revisions, duplicate IDs, impossible status transitions, inconsistent attempt counts, corrupt JSON, and oversized exports.

## Interpretation

Portable progress state supports continuity and auditable privacy minimization, but completion state is not evidence of conceptual mastery. Server sync would introduce a different security, consent, hosting, and ethics boundary.

## Open questions

- browser storage implementation and schema migration are not yet implemented;
- import must be transactional so corrupt input cannot replace valid local state;
- keyboard-only export/import and screen-reader announcements require browser testing;
- no learner or participant evaluation has occurred.

## Validation

Seven focused unit tests were added. This connector environment cannot execute the branch locally, so GitHub Actions is the final execution authority. No external source, participant data, telemetry, credential, model download, paid API, or server endpoint was introduced.

## Evidence produced

A reviewable schema/validator/example/test package that can support or falsify claims of local-first privacy, deterministic export/import semantics, and machine-checkable evidence boundaries.

## Next dependency

After review, implement the media manifest/provenance schema or the minimal viewer shell according to the orchestrator ranking. Do not implement authenticated progress synchronization without explicit approval.
