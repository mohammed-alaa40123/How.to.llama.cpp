# Validation Architect handoff — DATA-01 explicit unknown effort

## Assignment

`DATA-01` remained the highest-priority dependency-safe Validation Architect gap. The preceding missing-value policy identified a concrete blocker: schema `1.0.0` required numeric effort values, which forced incomplete historical records to remain excluded or risk fabricated zeros.

## Increment completed

- Added schema `1.1.0` support for explicit `measured`, `not_available`, and `not_applicable` effort measurements.
- Preserved validator compatibility with legacy `1.0.0` records.
- Added an explicit-unknown historical example.
- Added focused tests rejecting zero-as-unknown, measured values without evidence, unknown values without reasons, and fractional count measurements.
- Documented the migration in `docs/publication/data-schema.md`.

## Claim boundary

**Verified:** the committed semantic validator encodes the missingness rules and the tests exercise the main failure modes.

**Interpretation:** explicit missingness is necessary for an auditable longitudinal case study because historical labor, tool-call, and cost data are not uniformly retained.

**Historical:** schema `1.0.0` required numeric effort fields and could not distinguish measured zero from unavailable data.

**Open Question:** commit-scoped CI, independent coding agreement, broader historical extraction, and the provenance of legacy zeros remain unresolved.

## Validation and limitations

CI is authoritative because this connector run did not execute the repository test suite locally. No participant data, model, telemetry, paid API, generated media, or server-side synchronization was introduced.

## Next dependency

After final-head CI, extract one additional historical run using schema `1.1.0` and have a second coder independently classify its missingness. Do not begin baseline comparisons until coding disagreement and adjudication are recorded.
