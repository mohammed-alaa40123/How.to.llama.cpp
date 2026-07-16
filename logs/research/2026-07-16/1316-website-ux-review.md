# Website UX review and architecture-navigation grouping

- Review time: 2026-07-16 13:16 Africa/Cairo
- Documentation branch: `automation/backend-teardown-audit-method`
- Bounded implementation: group the flat Architecture navigation into task-oriented subsections without changing routes

## Verified

- The root page gives readers four reading modes and clearly links the interactive foundations map, brief end-to-end path, repository map, and GGML foundations.
- The Material configuration enables instant navigation, section navigation, search suggestions/highlighting, theme switching, heading permalinks, code copy, tabs, and Mermaid rendering.
- The interactive foundations iframe has a descriptive `title` attribute, and the page supplies a prose explanation plus Verified/Interpretation/Historical/Open-question text outside the embedded experience.
- Before this increment, the Architecture navigation exposed 27 pages in one flat list. The same routes are now grouped under Core architecture, Ownership and teardown, CPU optional buffers, and Accelerator backends.
- No page path changed, so existing URLs, source links, and bookmarks remain stable.

## Interpretation

The site already has strong technical depth and evidence conventions, but its navigation increasingly reflects repository growth rather than reader tasks. The flat Architecture section required readers to scan unrelated loader, ownership, CPU-buffer, and accelerator topics together. Task-oriented grouping improves recognition and lowers navigation cost without requiring content rewrites.

The homepage is a useful starting point, but the distinction between Foundations, Architecture, Inference lifecycle, and Interactive is not always obvious to a first-time reader. The duplicated foundations explorer under both Foundations and Interactive also weakens the mental model of where canonical entry points live.

## Prioritized improvements

### P0 — Verify the deployed experience

1. Merge or deploy the branch and verify HTTP 200, expected title/content, navigation expansion, search, theme switching, Mermaid rendering, iframe loading, and mobile layout in a real browser.
2. Add a built-site accessibility check covering heading order, landmark names, link names, color contrast, keyboard focus, iframe titles, and reduced-motion behavior.

### P1 — Improve first-time discoverability

1. Add a compact “Choose your path” landing page or homepage card grid for Beginner, Inference path, Memory and mmap, Graph and scheduler, CPU internals, and Accelerator backends.
2. Remove or explain duplicate navigation entries for the foundations explorer so each page has one obvious canonical home.
3. Add section index pages for Architecture and Inference lifecycle with short summaries and recommended reading order.

### P1 — Make diagrams resilient and accessible

1. Give each major diagram a one-paragraph text equivalent and a small legend defining object, operation, ownership, copy, synchronization, and lifetime notation.
2. Add visible fallback links below interactive iframes: open full screen, view static overview, and read text transcript.
3. Audit Mermaid diagrams at narrow viewport widths and in dark mode; large left-to-right graphs may require vertical/mobile variants.

### P2 — Improve consistency and orientation

1. Standardize page headers with baseline/revision, audience, estimated reading time, prerequisites, and “next page.”
2. Add breadcrumbs or “You are here” cues on long source-level pages.
3. Standardize terminology for backend wrapper, backend buffer, buffer type, graph allocation, scheduler split, mapping, residency, and representation validity.
4. Add page-level last-verified revision and distinguish baseline claims from current-upstream notes visually.

### P2 — Strengthen interaction quality

1. Persist the selected tab in interactive explorers and support deep links to a layer or workflow stage.
2. Ensure every clickable visual element is keyboard reachable and exposes an accessible name and state.
3. Add a no-JavaScript/static pathway for essential navigation and diagrams.

## Historical

The project began with a smaller flat navigation tree. Rapid addition of teardown audits and optional-buffer pages made the Architecture section substantially denser, creating the current information-architecture issue.

## Open questions

- Whether Material’s nested navigation remains comfortable on mobile with the four new Architecture groups.
- Whether the interactive HTML assets expose complete keyboard navigation and visible focus states internally.
- Whether diagram colors meet WCAG contrast requirements in both palettes.
- Whether the public Pages deployment currently serves the expected project content; direct live-site retrieval was blocked in this environment.

## Validation

- Read the complete README, project state, research log, research ledger, and latest detailed research note before editing.
- Inspected `mkdocs.yml`, the homepage, interactive foundations page, and custom stylesheet.
- Preserved every existing Architecture route while replacing one flat list with four semantic groups.
- Previous branch head CI was green for Documentation CI, pinned/current OpenCL evidence, and CPU_REPACK sanitizer workflows.

## Blocker

The live GitHub Pages site could not be fetched through the browsing environment, so visual rendering, responsive behavior, keyboard interaction, search behavior, and actual HTTP status could not be independently confirmed in this run.

## Next priority

After the grouped navigation passes strict MkDocs CI, add an Architecture section index with audience-based reading paths and verify it on deployed desktop and mobile views.
