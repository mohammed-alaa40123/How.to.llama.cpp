# How.to.llama.cpp

<div class="hero">
  <p class="eyebrow">SOURCE-GUIDED SYSTEMS DOCUMENTATION</p>
  <h2>Follow one token through llama.cpp.</h2>
  <p>From a GGUF file on storage, through virtual memory, GGML graph construction, backend scheduling, kernels, logits, and sampling.</p>
  <p><strong>Initial pinned baseline:</strong> <code>e3546c7948e3</code></p>
</div>

## The map

```mermaid
flowchart LR
    A[Application / CLI] --> B[Public llama API]
    B --> C[Model loader]
    C --> D[GGUF metadata and tensors]
    B --> E[llama_context]
    E --> F[Architecture graph builder]
    F --> G[GGML computation graph]
    G --> H[Backend scheduler]
    H --> I[CPU backend]
    H --> J[GPU / accelerator backends]
    I --> K[Thread pool and kernels]
    J --> L[Device queues and kernels]
    K --> M[Outputs / logits]
    L --> M
    M --> N[Sampler]
    N --> O[Next token]
    O --> E
```

## Reading modes

=== "Five-minute overview"

    Read [Brief end to end](lifecycle/end-to-end.md) and use the [interactive workflow](interactive/inference-workflow.md).

=== "Source deep dive"

    Start at the [repository map](architecture/repository-map.md), then follow source links and the generated index.

=== "Systems foundations"

    Begin with [What GGML is](ggml/what-is-ggml.md), followed by memory, scheduling, concurrency, and backend chapters as they are added.

## Evidence convention

!!! success "Verified"
    The behavior is directly visible in the pinned source or official documentation.

!!! info "Interpretation"
    The explanation connects several verified implementation facts. It is useful, but is not itself a source comment or formal guarantee.

!!! warning "Historical"
    The material describes an older commit, branch, PR, or reverted design.

!!! question "Open question"
    The behavior still needs source, test, maintainer, or runtime confirmation.

## Current status

- [x] Pin an initial source baseline.
- [x] Trace the public example through model load, context creation, decode, and sampling.
- [x] Create a Mermaid overview.
- [x] Build the first clickable inference explorer.
- [x] Create source-mirror and indexing automation.
- [ ] Complete the full repository inventory against every upstream ref.
- [ ] Deep-trace context construction, graph reuse, and scheduler allocation.
- [ ] Add backend-by-backend chapters and runtime experiments.
