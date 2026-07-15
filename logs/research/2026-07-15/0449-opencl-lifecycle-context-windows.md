# OpenCL lifecycle context windows

- Run time: 2026-07-15 04:49 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: make generated OpenCL lifecycle inventories reviewable without reopening the complete translation unit

## Startup and inspection

Read the complete README first, then project state, research log, research ledger, and the latest detailed note. Inspected the current lifecycle extractor, its focused tests, PR state, and the current source-recovery blockers before editing.

## Artifact

Extended `scripts/extract_opencl_lifecycle_calls.py` with optional bounded original-source context. `--context-lines N` adds `N` lines before and after every matched call, along with exact `start_line`, `end_line`, and source text. The matching path remains unchanged: comments and quoted literals are masked only for detection, while context is sliced from the original source.

Added focused tests for context content, exact bounds, beginning/end-of-file clamping, and rejection of negative context radii.

## Verified

- Default extraction remains backward-compatible: with `context_lines=0`, call records contain only `name` and exact 1-based `line`.
- Context is taken from original source, so comments and surrounding ownership/release statements remain visible to reviewers.
- Context bounds clamp to the real file rather than manufacturing line numbers outside the source.
- Negative context radii fail explicitly.
- The lifecycle regex and lexical masker were not broadened, so this increment does not add new API-call classifications or parser claims.

## Interpretation

A release-only inventory is insufficient when every record requires a second full-file lookup. Bounded context turns the generated report into a practical first-pass teardown worksheet while retaining exact-line navigation. It still does not prove ownership, completion, or safe release ordering; those remain human classifications.

## Historical

The previous increment removed false positives from comments and literals. This increment addresses the next bottleneck: reviewing true-positive calls in a large pinned translation unit when connector rendering is truncated.

## Open questions

- What context radius is sufficient for the pinned OpenCL file: three, five, or more lines?
- Should future reports include the enclosing function name after source indexing is regenerated?
- Should release calls be paired with creation/retention calls if local context remains ambiguous?
- The complete pinned `ggml-opencl.cpp` is still needed to produce the real lifecycle report.

## Validation

- Focused regression tests were added for bounded context behavior.
- GitHub-hosted Documentation CI is the authoritative full validation path because no local checkout is available in this runtime.
- Public Pages content remains unchanged until PR #1 merges.

## Next priority

Run the extractor with a small context radius against the complete pinned OpenCL translation unit, classify each completion/release site, and update the OpenCL teardown matrix. If source recovery remains blocked, implement the first CPU repack lifetime-ordering fixture.
