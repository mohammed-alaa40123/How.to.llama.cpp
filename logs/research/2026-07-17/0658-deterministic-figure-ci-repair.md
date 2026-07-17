# Deterministic figure CI repair

## Run metadata

- Starting commit: `d64c073e33af7bc22667787829429421e5f61b74`
- Assigned milestone: `FIG-01` — obtain passing commit-scoped validation for the deterministic GGUF-layout figure
- Learner outcome: preserve an exact, auditable diagram of GGUF byte layout without allowing manually edited geometry or stale provenance to pass as deterministic evidence

## Failure observed

Documentation CI run `29551621279` passed context, interactive-link, and source-index checks, then failed at unit-test discovery with exactly two failures:

1. `test_checked_in_svg_is_exact_generator_output`
2. `test_manifest_hashes_and_size_match_files`

The committed SVG used header width `775.25`, while the current generator and golden record produced `775.18`. The stale checked-in SVG therefore also disagreed with the manifest output checksum and byte count.

## Bounded repair

- Regenerated `media/generated/gguf-layout-deterministic-v0.svg` from the committed generator and golden record.
- Updated the manifest output SHA-256 to `d93ab0a5eafe0fe7a4ee2db737ce077d2babb275a5c656c07b81105ae851cd25`.
- Updated the manifest output size to 2525 bytes.
- Updated project state with the exact failure, repair, evidence boundary, and remaining CI requirement.

No generator logic, fixture data, technical claim, model, external source, API call, learner data, telemetry, or manuscript content changed.

## Truth labels

- **Verified:** run `29551621279` failed only the two figure replay/manifest assertions after 95 other discovered tests passed.
- **Verified:** the repaired SVG text is the direct output of `scripts/generate_gguf_layout_figure.py` for `synthetic-v0.golden.json`.
- **Interpretation:** treating exact replay drift as a hard failure is necessary for the EAAI claim that deterministic technical media are auditable repository evidence rather than manually curated illustrations.
- **Open question:** the repaired branch must obtain passing commit-scoped Documentation CI before `FIG-01` is marked evidenced.

## Human review and limitations

Independent GGUF/llama.cpp correctness review remains required under `REVIEW-01`. The figure remains authoritative only for the project-owned synthetic fixture byte layout; it does not represent native loading, graph construction, or inference.

## Next dependency

Wait for repaired-head Documentation CI. Do not begin `VIEW-01` until the Validation Architect closes `TRACE-02`.
