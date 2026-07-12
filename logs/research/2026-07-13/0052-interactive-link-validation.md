# Interactive route and anchor validation

- Run time: 2026-07-13 00:52 Africa/Cairo
- Scope: add automated validation for canonical local routes and section anchors embedded in interactive HTML and JavaScript assets
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Added `scripts/validate_interactive_links.py` and `tests/test_validate_interactive_links.py`, then integrated both into `.github/workflows/docs-ci.yml`.

The validator currently checks:

- literal HTML `href` attributes relative to the interactive asset;
- JavaScript `page` records relative to the MkDocs site root;
- the foundations explorer's separate memory-atlas `anchor` records;
- Markdown source-page existence;
- heading-derived section IDs, including explicit `{#id}` attributes;
- actionable errors containing the asset, original reference, expected route candidates, or missing anchor target.

It excludes external URLs, non-document schemes, and dynamically generated template links that cannot be resolved statically.

## Verified

- The validator is dependency-free and uses only the Python standard library.
- Route resolution supports root index pages, clean MkDocs routes, `.html` routes, Markdown pages, and directory index pages.
- The foundations explorer's object, GGUF, model-placement, graph, MoE, and memory-atlas links are within the validator's extraction scope.
- Five fixture tests cover valid routes and anchors, missing routes, missing anchors, ignored external/dynamic links, and Markdown heading slug generation.
- Documentation CI now runs context validation, interactive-link validation, fixture tests, Python compilation, shell syntax checks, required interactive-asset checks, and `mkdocs build --strict`.
- `scripts/validate_project_context.py` now requires the new validator, its tests, and the foundations explorer.

## Interpretation

- Static source validation is useful because it catches hand-authored route drift before deployment and produces a more precise error than a generic broken-link report.
- Strict MkDocs build remains the authoritative renderer-level check; the source validator is an earlier, narrower guardrail.

## Historical

- Before this increment, interactive routes and anchors were hand-authored and reviewed only through static inspection or live-site checks.
- The earlier README and project-state blocker explicitly identified missing route and anchor validation as the highest-priority task.

## Open questions

- Python-Markdown and MkDocs plugins can generate IDs that differ from the standard-library slug approximation; built-HTML ID validation should be added later.
- The memory-atlas `anchor` records require an asset-specific rule because their route is supplied by the renderer rather than stored with each record.
- Dynamically generated local links should eventually be represented in generated versioned metadata so they can be validated without template evaluation.
- Non-HTML interactive assets and pinned upstream source links are not yet covered.

## Sources inspected

- Complete repository `README.md`.
- `docs/reference/project-state.md`.
- `docs/reference/research-log.md`.
- `docs/reference/research-ledger.md`.
- Latest detailed note: `logs/research/2026-07-12/2351-interactive-memory-overlay.md`.
- Existing `scripts/validate_project_context.py`.
- Existing `.github/workflows/docs-ci.yml`.
- `docs/assets/interactive/llama-foundations-explorer.html`.
- `docs/assets/interactive/inference-flow.html`.

No new external source was introduced, so `docs/reference/research-ledger.md` remains unchanged.

## Validation plan and status

Relevant commands are now part of Documentation CI:

```bash
python3 scripts/validate_project_context.py
python3 scripts/validate_interactive_links.py
python3 -m unittest discover -s tests -p 'test_*.py'
python3 -m py_compile scripts/*.py tests/*.py
bash -n scripts/*.sh
mkdocs build --strict
```

Connector-side file creation, replacement, and re-fetch are used for durable verification. GitHub Actions and the deployed Pages site are checked after the final state commit; any unavailable run listing, DNS failure, or browser restriction remains a verification blocker rather than evidence of failure.

## Next priority

Begin file-by-file Pass A with the public API and minimal example group, mapping `include/llama.h` and `examples/simple/simple.cpp` to implementation entry points, object ownership, synchronization, error paths, and teardown.
