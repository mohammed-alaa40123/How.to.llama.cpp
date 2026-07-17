# EAAI-27 double-blind artifact and evidence-release plan

## Purpose and claim boundary

This plan implements `BLIND-01`. It defines how the executable-learning artifact and repository-native case-study evidence can be reviewed without exposing author identity or destroying provenance. It does **not** create the anonymous bundle, certify release readiness, alter repository history, recruit participants, or authorize manuscript drafting.

## Verified venue constraint

The retained official EAAI-27 call requires double-blind review. The artifact therefore cannot expose repository ownership, author names, account handles, pull-request identities, workflow URLs, commit authorship, personal contact details, or unredacted human/agent conversation records during review.

## Design decision

Use a **private anonymized supplement** during review and a **post-decision public release** afterward.

The review artifact is a clean export, not a fork with rewritten public history. It contains only the files needed to inspect the educational progression, deterministic fixtures, validators, static fallbacks and bounded aggregate evidence. A private crosswalk retained by the corresponding author maps opaque source IDs to exact repository paths and immutable revisions. The crosswalk is not submitted before decision.

Rejected alternatives:

- publishing the live repository during double-blind review;
- deleting source revisions and hashes to hide identity;
- rewriting all history and losing the audit trail;
- embedding direct GitHub, PR, issue, Actions or profile links in the anonymous artifact;
- treating supplemental material as necessary to understand a central claim;
- releasing raw prompts, conversations, emails, learner identity or telemetry.

## Public anonymous artifact

The bounded artifact may include:

- a static build of the integrated learner route;
- project-authored synthetic GGUF fixtures, manifests and checksums;
- deterministic figures and cached reviewed media;
- the authored/source-derived trace with opaque source IDs;
- validators, schemas and reproducibility instructions;
- redacted aggregate retrospective tables whose cells satisfy the missing-data policy;
- static, text, transcript and reduced-motion fallbacks.

It must exclude:

- `.git`, remotes, commit authors, branch names and repository-owner metadata;
- repository, pull-request, issue, workflow-run and profile URLs;
- names, usernames, email addresses, affiliations, acknowledgements and self-identifying grant text;
- raw agent conversations, prompts, private logs or personal communications;
- restricted model weights or learner-provided models;
- the source-ID identity crosswalk;
- secrets, API keys, telemetry endpoints and authenticated synchronization.

## Provenance without identity leakage

Every public source anchor uses:

1. an opaque stable ID such as `SRC-GGUF-LOAD-001`;
2. the immutable upstream or artifact SHA-256 needed to verify content;
3. a local excerpt or vendored source fragment only when license-compatible;
4. an evidence-kind label: browser-derived, authored, source-derived or native-captured.

The private crosswalk stores the exact repository path, upstream URL, commit and line range. After acceptance or when the venue permits de-anonymization, a deterministic release step can restore public links without changing the underlying evidence hashes.

## Repository anonymization protocol

1. Pin one canonical submission revision.
2. Export an allowlisted file set into a clean directory with no VCS metadata.
3. Replace public source links with opaque IDs; generate the private crosswalk separately.
4. Scan file contents, generated HTML, metadata, manifests, source maps and archives for identity and repository tokens.
5. Remove or generalize acknowledgements, affiliations, account handles and self-citations only as required by the venue; retain a private restoration patch.
6. Build and validate the anonymous artifact from scratch.
7. Compare deterministic fixture, trace and figure hashes against the canonical revision.
8. Obtain human anonymization, technical, licensing and privacy review.
9. Freeze the submitted archive checksum and retain it with the private crosswalk.

## Supplement and essential-evidence boundary

The main submission must contain the educational framing, key design decisions, methods, central quantitative or qualitative evidence, limitations and disclosure required to evaluate the claims. Reviewers should not need the supplement to discover a central result.

The supplement may provide executable demonstrations, schemas, validators, expanded tables, deterministic fixtures, static transcripts and a redacted reproducibility package. It must clearly label authored/source-derived evidence and must not imply native capture where none exists.

## Automated contract

`schemas/double-blind-release-plan.schema.json` defines the versioned record. `scripts/validate_double_blind_release.py` additionally enforces:

- immutable 40-character submission revision;
- opaque-ID-plus-SHA public anchors;
- private, unpublished identity crosswalk;
- coverage of identity, repository, provenance, supplement, licensing, privacy, accessibility and cost checks;
- blocker details for every blocked check;
- four explicit human approvals;
- `release_ready=true` only when no check is blocked and every approval is true.

The current example is intentionally `release_ready=false`: the anonymous bundle, deterministic identity scan, final license inventory, built-artifact accessibility check and human approvals do not yet exist.

## Accessibility, privacy, licensing and cost gates

- The anonymous bundle must pass the same strict build and built-site accessibility checks as the canonical branch and retain keyboard/static/text fallbacks.
- No personal learner data, silent telemetry, authenticated progress sync or raw evaluation responses are included.
- A final license inventory must cover upstream excerpts, project-authored fixtures, fonts, media and any optional generated asset.
- Ordinary CI may validate cached files but may not call paid image, speech or video APIs.
- Accepted, revised and rejected media records remain auditable; rejected media is not published as educational evidence.

## Human review checklist

Release remains blocked until a human reviewer confirms:

- no direct or indirect identity leak remains in the unpacked archive or generated site;
- opaque anchors resolve through the private crosswalk to the pinned evidence;
- anonymization did not change technical meaning, answer keys, checksums or claim labels;
- license and privacy inventories are complete;
- accessibility fallbacks work in the anonymous build;
- the archive checksum and restoration patch are retained privately.

## Truth labels

- **Verified:** the official EAAI-27 planning state retained by this repository requires double-blind review.
- **Verified:** the current machine-readable example is not release-ready and records its blockers explicitly.
- **Interpretation:** a clean allowlisted export plus private crosswalk preserves stronger provenance than public-history rewriting while reducing identity leakage.
- **Historical:** the live repository and stacked PR history contain author and account metadata and are therefore unsuitable as the review artifact without anonymization.
- **Open Question:** the venue’s final author kit may add artifact-hosting or self-citation details that require a bounded update before submission.
