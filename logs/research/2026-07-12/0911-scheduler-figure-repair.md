# Backend scheduler figure repair

- Run time: 2026-07-12 09:11 Africa/Cairo
- Scope: replace the broken Mermaid sequence on the backend scheduler page with a static accessible SVG

## Verified

- The deployed page showed `Syntax error in text` under Mermaid 11.1.0 for the backend scheduler sequence.
- `docs/lifecycle/backend-scheduler-execution.md` now references `docs/assets/figures/backend-scheduler-execution.svg`.
- The SVG is valid XML, includes `<title>` and `<desc>` accessibility metadata, and preserves the documented phases: allocation, per-split copies/submission, return after submission, and later synchronization.
- The broken Mermaid block was removed from the rendered page.

## Interpretation

- A static SVG is more robust for this dense sequence than a complex Mermaid sequence diagram while remaining scalable and readable on mobile.
- The figure is conceptual; the surrounding pinned prose and source map remain authoritative for exact branch behavior.

## Historical

- The replaced Mermaid source represented the same pinned scheduler baseline but failed in the deployed renderer.

## Open question

- Whether other complex Mermaid diagrams fail under the current MkDocs Mermaid integration and should receive the same static-figure treatment.

## Artifacts changed

- `docs/assets/figures/backend-scheduler-execution.svg`
- `docs/lifecycle/backend-scheduler-execution.md`
- `README.md`
- `docs/reference/project-state.md`
- `docs/reference/research-log.md`

## Validation

- SVG XML parsing succeeded locally.
- Connector-side reads will verify the asset and Markdown reference after publication.
- GitHub Actions and the deployed website must still be checked separately.

## Next step

- Continue the planned Vulkan and SYCL buffer compatibility trace after confirming the figure renders in Documentation CI and Pages.
