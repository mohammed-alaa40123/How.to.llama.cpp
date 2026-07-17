# Deterministic media lifecycle dry run

`MEDIA-02` exercises the review lifecycle without calling an external generation service. The committed fixture contains exactly one **accepted**, one **revised**, and one **rejected** deterministic specimen.

## Purpose

The dry run tests whether media decisions remain auditable after generation. It is not a gallery and it does not treat the three placeholder specimens as evidence about llama.cpp.

| State | Publication | Human approval | Required retained evidence |
|---|---:|---:|---|
| Accepted | Yes | Yes | source revision, input/output hashes, accessible fallback, licensing note, reviewer role and timestamp |
| Revised | No | No | cached candidate plus a concrete revision reason |
| Rejected | No | No | cached candidate plus a rejection reason; publication remains prohibited |

## Validation

Run:

```bash
python3 scripts/validate_media_lifecycle.py media/lifecycle/media-lifecycle-v0.json --repo-root .
python3 -m unittest tests.test_validate_media_lifecycle
```

The validator:

- reuses the canonical media-manifest semantic validator for every record;
- requires exactly one accepted, revised and rejected state;
- requires deterministic, ordinary-CI-safe generation with no model, prompt or storyboard API fields;
- verifies committed input and output SHA-256 values and byte counts;
- rejects duplicate identities or output paths;
- blocks publication of revised or rejected assets;
- detects stale, missing or path-escaping inputs and outputs.

Ordinary CI only validates cached committed files. It does not call image, speech, realtime or video APIs and cannot spend external API budget.

## Accessibility fallback

Each SVG is text-only, contains `<title>` and `<desc>`, uses no animation, and is fully represented by the lifecycle table above. No color is required to distinguish review state.

## Claim labels

### Verified

The lifecycle fixture and validator encode accepted, revised and rejected decisions, publication gates, deterministic generation fields, accessibility metadata, licensing metadata and hash-based stale detection.

### Interpretation

Retaining revised and rejected candidates alongside explicit reasons should make human intervention and asset-selection costs more visible in the longitudinal repository record.

### Historical

`MEDIA-01` established the manifest contract and `FIG-01` established deterministic technical-figure replay. `MEDIA-02` tests the decision lifecycle rather than adding another technical figure.

### Open question

The dry run does not establish that future generative assets are technically correct, pedagogically useful, license-compatible or cost-effective. Those decisions require asset-specific human review; generated media remains supplemental.
