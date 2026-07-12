# Documentation quality and interaction roadmap

- Run time: 2026-07-12 13:52 Africa/Cairo
- Scope: convert the previously proposed website improvements into a durable, bounded implementation plan and publish it in the documentation
- Baseline: repository documentation at the start of this run; no new upstream llama.cpp implementation claim

## Verified

- The repository already contains source-pinned lifecycle pages, a searchable MkDocs site, an inference workflow, a source index, backend copy/memory documentation, and durable research context.
- A new `docs/reference/documentation-quality-roadmap.md` artifact now defines:
  - an object-centred encyclopedia;
  - a clickable source and symbol explorer;
  - synchronized diagram/source metadata;
  - separate memory and execution visualizers;
  - a mature-page navigation contract;
  - pinned-version and backend comparisons;
  - a ten-category website review rubric;
  - bounded implementation slices.
- `docs/roadmap.md` now includes Milestone 10 for object-centred and searchable documentation.
- `mkdocs.yml` publishes the quality roadmap under Reference.
- `README.md` now includes daily website review responsibility, the roadmap in the context map, reordered implementation TODOs, and the canonical `llama_context` page as a top priority.

## Interpretation

- File-centred and linear lifecycle documentation is necessary but insufficient for readers asking ownership, lifetime, call-graph, or synchronization questions.
- Stable identifiers and reusable metadata shared across object pages, source symbols, and interactive nodes provide a more maintainable architecture than manually duplicating links in every diagram.
- The first object page should be `llama_context` because it connects model state, memory modules, graph construction, backend scheduling, outputs, and decode lifecycle.

## Historical

- The project began with one vertical inference slice. The new roadmap preserves that path while adding object, symbol, memory, backend, and version entry points.

## Open questions

- Which interactions can remain static MkDocs HTML/SVG/JavaScript assets.
- Which interactions require a generated JSON data bundle or a dedicated client-side component.
- Which exact later upstream commit first replaces or registers SYCL scheduler tensor-copy asynchrony; available search results were insufficient for a reliable claim.

## Source changes

- No external source was added, so `docs/reference/research-ledger.md` did not change.

## Validation

- Connector-side file writes succeeded for the new page, roadmap, navigation, README, project state, research log, and this note.
- The connected combined-status interface returned no status entries for the documentation commit checked during the run.
- The connected commit-workflow interface returned an empty list and cannot establish push-triggered CI or Pages conclusions.
- Browser fetch of the public Pages root returned a cache-miss error; search did not expose the site or the newly added page.
- These are tooling visibility blockers rather than evidence of deployment failure.

## Next step

Create `llama_context` as the first canonical object page using the complete page contract: purpose, construction, ownership, lifetime, memory, mutation, call chain, threading/synchronization, teardown, source map, related pages, truth labels, and open questions.
