# 05:01 — Media manifest validation contract

- **Starting commit:** `5bbc595b9e2d076ddbc8393514e2a9f26fab9fa8`
- **Assigned milestone:** `MEDIA-01` after `CI-01` passed Documentation CI run `29546570700`
- **Learner outcome:** distinguish authoritative deterministic technical figures from supplemental generated media by inspecting and validating provenance, review, accessibility, licensing, and CI boundaries.

## Files

- `schemas/media-asset-manifest.schema.json`
- `scripts/validate_media_manifest.py`
- `media/manifests/gguf-layout-deterministic-v0.json`
- `tests/test_validate_media_manifest.py`
- `docs/media/asset-manifest-schema.md`
- `docs/reference/project-state.md`
- `docs/publication/evidence-backlog.md`
- `docs/publication/agent-handoffs.md`

## Claims

- **Verified:** strict MkDocs integration passed on the parent branch.
- **Verified:** the contract encodes deterministic authority, source revision and hashes, output checksum, accessibility, licensing, human review, stale-source detection, and generated-media cost/secret boundaries.
- **Interpretation:** human approval permits publication but cannot make generative media authoritative technical evidence.
- **Historical:** media generation was in the roadmap before a machine-checkable provenance contract existed.
- **Open question:** provider-specific API and licensing constraints remain unverified; the deterministic SVG generator remains a separate `FIG-01` task.

## Validators and tests

Nine focused tests cover the valid deterministic manifest, evidence inflation, ordinary-CI API invocation, absent approval, rejected publication, audio transcript requirements, path traversal, forbidden credential fields, stale source revisions, and size bounds.

## Safety and human review

No model, participant data, telemetry, credential, API call, paid generation, image, audio, or video was produced. The example is a contract fixture and explicitly states that its future SVG checksum must be replaced by the generated checksum under `FIG-01`.

## Failure and limitation

The connector environment cannot execute the test suite locally. Commit-scoped Documentation CI is the validation authority. Provider constraints require separate official-source research.

## Evidence produced

A bounded schema/validator/example/test package that supports or falsifies the EAAI claim that optional educational media can be provenance- and review-gated without being confused with technical evidence.

## Next dependency

Obtain passing CI. Then implement one deterministic GGUF layout figure from the structured fixture and recompute its manifest input/output hashes; do not add a paid API call.
