# MEDIA-02 — deterministic media lifecycle dry run

## Run metadata

- Starting commit: `a0c4f01c9b9880f016b116e7172772fa572a35e3`
- Assigned milestone: `MEDIA-02`
- Learner outcome supported: distinguish an asset's deterministic provenance from its human review and publication decision.
- Ending commit: recorded in the PR handoff because a commit cannot contain its own SHA.

## Assignment selection

Commit-scoped Documentation CI run `29583844938` passed for `BASE-01A`. Measured `LAB0-03` and `LAB0-04` remained blocked because this environment does not provide Ubuntu-native or devcontainer execution. The highest ready dependency-safe evidence task was therefore `MEDIA-02`.

## Files produced

- `media/lifecycle/media-lifecycle-input-v0.json`
- `media/lifecycle/media-lifecycle-v0.json`
- `media/lifecycle/accepted-v0.svg`
- `media/lifecycle/revised-v0.svg`
- `media/lifecycle/rejected-v0.svg`
- `scripts/validate_media_lifecycle.py`
- `tests/test_validate_media_lifecycle.py`
- `docs/media/lifecycle-dry-run.md`
- state, backlog and handoff updates

## Evidence and validators

The lifecycle batch contains exactly one accepted, revised and rejected deterministic asset record. The validator reuses `validate_media_manifest()`, verifies exact state coverage, blocks external generation in ordinary CI, requires distinct asset/output identities, checks publication and approval semantics, and recomputes every committed input/output SHA-256 and output byte count.

Eight focused tests cover the committed batch, missing lifecycle-state coverage, duplicate asset IDs, external generation, generative mode, stale output checksum, stale input checksum and rejected-asset publication.

## EAAI claim supported or falsified

The increment supports or can falsify the claim that the project's media lifecycle is auditable without ordinary CI regeneration or paid API use. It records both accepted and non-accepted outputs instead of preserving only successful assets.

## Claims

### Verified

- All three review outcomes are represented by committed deterministic fixtures.
- Revised and rejected records remain unpublished and unapproved with explicit reasons.
- The accepted record is approved, published, source-pinned, licensed and accessibility-described.
- Stale input/output hashes and byte counts are validator failures.
- No generator model, prompt, storyboard, credential or external API call is present.

### Interpretation

Retaining non-accepted candidates and reasons may improve retrospective visibility into human supervision and revision cost.

### Historical

`MEDIA-01` validated individual manifest boundaries and `FIG-01` validated deterministic technical-figure replay. This increment adds lifecycle decision evidence rather than another technical explanation.

### Open question

Future generative assets still require asset-specific technical, accessibility, privacy, licensing and pedagogical review. This dry run provides no evidence of generative-media usefulness.

## Failures and limitations

- Local repository execution is unavailable in the connector environment; commit-scoped Documentation CI is the execution authority.
- The fixtures are intentionally text-only lifecycle specimens, not instructional llama.cpp diagrams.
- No participant data, model weights, telemetry, credentials, paid APIs or manuscript prose were introduced.

## Human review needs

- Confirm that retained rejected assets are acceptable repository history rather than publication assets.
- Review whether revision/rejection reasons need a controlled taxonomy before broader retrospective extraction.
- Continue to prohibit ordinary-CI external generation.

## Next dependency

After final-head CI, close `MEDIA-02`. The next dependency-safe work is `REVIEW-02` or a bounded extension of `DATA-01`; measured `LAB0-03` and `LAB0-04` remain preferred when suitable execution environments become available.
