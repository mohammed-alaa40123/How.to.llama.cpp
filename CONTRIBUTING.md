# Contributing to How.to.llama.cpp

Thank you for helping build a durable map of llama.cpp and GGML.

## Documentation truth labels

Use one of these labels near non-trivial claims:

- **Verified** — directly supported by the pinned source revision or an official project statement.
- **Interpretation** — an explanation inferred from multiple source locations.
- **Historical** — behavior from an older branch, commit, PR, or discussion.
- **Open question** — not yet resolved confidently.

## Source links

Implementation claims should link to a commit-pinned URL, not `master`. Include the repository path and symbol name in prose so links remain understandable when source lines move.

## Diagrams

- Prefer Mermaid for maintainable architecture and sequence diagrams.
- Store complex interactive diagrams as data-driven SVG/HTML components.
- Add alt text and a text explanation.
- Every diagram must declare the source revision it describes.
- Avoid diagrams that imply a single backend path when behavior is backend-dependent.

## Suggested workflow

1. Choose one narrow question.
2. Trace it from the public API through implementation and backend interfaces.
3. Record files, symbols, conditions, and ownership/lifetime rules.
4. Validate against tests, examples, PRs, and discussions.
5. Add or update a diagram.
6. Add unresolved edge cases to the research log.

## Scope boundaries

Do not copy large portions of upstream source. Link to it and quote only the small fragment required to explain a behavior.
