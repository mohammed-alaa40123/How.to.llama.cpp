# Strict MkDocs handoff-link repair

- **Starting commit:** `a2e49f668633ef843df3e5b49188cc9dc614c708`
- **Assigned milestone:** Week 1 integration gate; resolve the highest-priority strict MkDocs blocker before media or viewer expansion.
- **Learner outcome protected:** executable-learning artifacts remain navigable and reviewable without publishing internal run logs as broken site pages.

## Evidence inspected

Documentation CI run `29544077919`, job `87772333049`, passed every pre-MkDocs check and failed at `mkdocs build --strict` with exactly two warnings:

1. `docs/publication/agent-handoffs.md` linked to `logs/research/2026-07-17/0100-synthetic-gguf-fixture.md` outside the MkDocs documentation tree.
2. The same page linked to `logs/research/2026-07-17/0158-lab0-checker-interface.md` outside the MkDocs documentation tree.

## Bounded change

Converted the two Markdown links into explicit code-form repository paths. The durable run records remain under repository-root `logs/research/`; they are no longer represented as generated-site destinations.

Updated:

- `docs/publication/agent-handoffs.md`
- `docs/reference/project-state.md`
- this run record

No schema, fixture, trace, progress data, source claim, model path, learner data, API call, or manuscript content changed.

## Claims

- **Verified:** CI emitted exactly the two unresolved-target warnings above and aborted strict mode.
- **Interpretation:** internal run records should remain repository evidence rather than public MkDocs pages unless intentionally promoted and reviewed.
- **Historical:** the links were introduced by earlier stacked increments before authoritative orchestration state existed.
- **Open question:** commit-scoped CI must pass before the P0 blocker is closed.

## Validators

Authoritative validator: `.github/workflows/docs-ci.yml`, especially `mkdocs build --strict` followed by built-site accessibility validation.

## Human review needs

Confirm that repository-root run logs are intentionally excluded from the public site. No technical-content review is otherwise required for this path-only repair.

## Evidence produced

- Root-cause mapping from CI warnings to the two exact handoff entries.
- Minimal path-only repair with no feature expansion.
- Updated shared handoff and project-state records.

## Ending state

- **Ending branch:** `agent/fix-strict-mkdocs-handoff-links`
- **Next dependency:** obtain passing commit-scoped Documentation CI; only then begin the media manifest/provenance validator.