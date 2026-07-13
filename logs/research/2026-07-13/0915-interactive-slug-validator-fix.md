# Interactive heading-slug validator CI fix

- Run time: 2026-07-13 09:15 Africa/Cairo
- Scope: repair the failing Documentation CI unit test for Markdown heading anchors containing inline code with underscores

## Verified

- Documentation CI failed in `test_heading_slug_handles_code_links_and_explicit_ids`.
- The validator converted `` `llama_model` `` to `llamamodel` because it unwrapped inline code and then globally removed underscore characters as possible Markdown emphasis markers.
- Python-Markdown/MkDocs preserves the underscore inside rendered inline code, so the expected anchor is `llama_model-and-context`.
- `markdown_slug()` now temporarily replaces inline-code spans with placeholders, removes emphasis markers outside those spans, restores literal code content, and then applies the existing slug normalization.
- The corrected function returns `llama_model-and-context` for ``## `llama_model` and [context](other.md)``.

## Interpretation

- Markdown syntax characters and literal characters inside code spans must be handled in separate phases. A global character-removal pass cannot accurately approximate rendered heading text.

## Historical

- The first validator implementation used one global `[*_~]` removal after code-span unwrapping, which caused this CI regression.

## Open question

- The source-level slug approximation should eventually be checked against IDs emitted by the built MkDocs HTML for plugin-generated and renderer-specific anchors.

## Validation

- Reproduced the failing case from the unit test.
- Evaluated the corrected slug function locally; it returns `llama_model-and-context`.
- Push-triggered GitHub Actions must rerun to confirm the complete workflow.

## Next priority

- Check the rerun of Documentation CI, then continue the scheduler/backend deleter trace.
