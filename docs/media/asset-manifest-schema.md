# Media asset manifest contract

This document defines the Week 1 provenance and review contract for deterministic and optional generated educational media. It does not authorize API calls or make generated media technical evidence.

## Educational contract

- **Intended learner:** advanced undergraduate, graduate, or early-stage systems researcher studying GGUF and llama.cpp internals.
- **Prerequisite:** ability to distinguish source-derived structure, captured runtime evidence, authored explanation, and illustration.
- **Learning objective:** identify which media assets may support technical claims and which are supplemental only.
- **Predicted misconception:** a polished generated diagram, narration, or video is evidence that its technical contents are correct.
- **Executable action:** validate an asset manifest and inspect its authority, provenance, source revision, checksums, accessibility fields, and human-review state.
- **Observable output:** a deterministic pass/fail report with stable semantic error messages.
- **Formative assessment:** explain why a generative API asset cannot be marked `authoritative-technical`, even after human approval.
- **Source revision:** every manifest pins a full 40-character repository revision and hashes every declared structured input.
- **Validation method:** `python scripts/validate_media_manifest.py <manifest>` plus focused unit tests.
- **Accessibility fallback:** diagrams require meaningful alt text; audio/video require transcripts; video additionally requires captions and a static fallback.

## Authority boundary

Two authority levels are permitted:

- `authoritative-technical`: deterministic diagrams derived from structured, hashed repository inputs. These may state bounded technical claims after human review.
- `supplemental`: illustrations, narration, or video that aid orientation or engagement but are never technical evidence by themselves.

A `generative-api` asset is always supplemental. Human approval can permit publication; it cannot promote the asset to authoritative technical evidence.

## Required provenance

Every manifest records:

- schema and asset identifiers;
- asset kind, authority, review status, and publication state;
- repository and immutable source revision;
- repository-relative input paths and SHA-256 hashes;
- generator and generator version;
- output path, MIME type, checksum, and byte size;
- accessibility fields;
- licensing and redistribution notes;
- human-review requirement, decision, role, date, and notes.

Generative API assets additionally require a model identifier, prompt and storyboard paths and hashes, caching, manual triggering, and `ordinary_ci_allowed: false`.

## CI and secret boundary

Ordinary pushes may validate manifests and regenerate deterministic assets. They must not call paid or credentialed generation APIs. A generative media job must be explicitly and manually triggered, use repository/environment secrets without writing them into manifests or logs, cache approved outputs, and require review before publication.

The semantic validator recursively rejects credential-like fields such as API keys, access tokens, authorization values, cookies, and secret fields.

## Review states

- `pending`: not publishable.
- `accepted`: human-approved and publishable only when redistribution is allowed.
- `revised`: changed after review and awaiting a new acceptance decision.
- `rejected`: must have `publication.publish: false`.

Generated assets should be logged as accepted, revised, or rejected so the EAAI case study can report failed generations and human correction effort rather than only final outputs.

## Stale-asset detection

The CLI accepts `--expected-source-revision`. A mismatch reports that the manifest is stale. A later deterministic-figure lane should also recompute every input and output checksum and fail when committed hashes no longer match.

## Truth labels

- **Verified:** this repository now has a machine-readable manifest schema, dependency-free semantic validator, deterministic example, and focused malformed-input tests.
- **Interpretation:** deterministic technical figures are safer as authoritative evidence because their transformation from structured inputs can be replayed and checksum-verified.
- **Historical:** generative media was proposed as part of the roadmap before its provenance and review contract existed.
- **Open question:** current provider-specific API, licensing, privacy, cost, and reproducibility constraints remain assigned to the Literature and Venue Scout and must be verified from official sources before any provider is selected.

## Scope boundary

This increment does not generate an SVG, image, audio file, or video. The example manifest deliberately points to the future `FIG-01` deterministic output and records that its checksum must be replaced by the actual generated checksum when that task is implemented.
