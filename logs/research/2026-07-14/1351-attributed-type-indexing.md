# Attributed C++ type indexing

- Run time: 2026-07-14 13:51 Africa/Cairo
- Repository branch: `automation/backend-teardown-audit-method`
- Scope: extend the approximate source index to recognize same-line C++ attributes without weakening physical-line accuracy

## Startup and inspection

Read the complete repository README first, then project state, research log, research ledger, and the latest detailed note. Inspected PR #1, `scripts/index_upstream.py`, and `tests/test_index_upstream.py` before editing.

## Artifact

Extended `CLASS_RE` so type declarations remain discoverable when a C++ attribute appears:

```cpp
[[nodiscard]] struct before_keyword {};
struct [[gnu::packed]] after_keyword {};
[[deprecated("use replacement")]] enum class [[nodiscard]] attributed_enum {};
```

Added a focused unit test requiring all three symbols to retain their physical declaration lines.

## Verified

- The prior regex recognized plain `class`, `struct`, `enum`, and `enum class` declarations but required the type keyword to be the first non-horizontal-whitespace token.
- C++ attributes may legally appear before the type keyword or between the type keyword and declared name.
- The updated pattern accepts one or more same-line `[[...]]` attribute groups in either position.
- Every whitespace matcher remains horizontal (`[\t ]`), so attributes cannot reintroduce the preceding-blank-line defect.
- The change does not alter function extraction, duplicate retention, source ordering, or pinned link construction.

## Interpretation

This increment improves navigation coverage without pretending the regex is a C++ parser. Same-line standard attributes are common enough to index directly; multiline attributes, declaration macros, and complicated generated syntax remain human-review cases.

## Historical

The source index was intentionally introduced as an approximate navigation aid. The previous run repaired physical-line drift caused by multiline `\s`; this run expands accepted declaration syntax while preserving that repaired invariant.

## Open questions

- Decide whether multiline attributes are common enough in the pinned llama.cpp tree to justify a small stateful scanner rather than a larger regex.
- Assess declaration macros and export annotations separately; matching arbitrary macros risks false positives.
- Regenerate the pinned source inventory once a usable pinned checkout is available.

## Validation and CI

The new source-index unit test is committed on PR #1. GitHub-hosted Documentation CI must verify the isolated source-index suite, full discovery, and strict MkDocs build. Full local checkout validation remains blocked because direct GitHub DNS resolution is unavailable in this runtime.

## Next priority

Inspect the commit-scoped CI run. If green, resume pinned OpenCL teardown source recovery or implement the admitted CPU repack backend-free-before-buffer-free fixture.
