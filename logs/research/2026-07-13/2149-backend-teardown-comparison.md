# Backend teardown comparison increment

- Run time: 2026-07-13 21:49 Africa/Cairo
- Scope: synthesize the completed backend teardown audits into one cross-backend decision matrix
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Added `docs/architecture/backend-teardown-comparison.md` and linked it in the Architecture navigation.

## Verified

- Ordinary CPU execution is synchronous and has no scheduler-event interface; its audited backend-before-scheduler order is safe.
- Metal and Vulkan backend cleanup establish explicit completion boundaries before context-owned submission resources are released.
- CUDA and SYCL ordinary scheduler event/buffer deleters retain state independent of the deleted per-backend wrapper, while complete queued-work coverage remains conditional.
- RPC buffers retain their socket and remote handle, but graph submission has no remote completion response and synchronize is a no-op.
- CANN performs device-wide synchronization, but device reset precedes later context and scheduler destructor calls.
- OpenCL remains unclassified beyond the already documented build composition and initial `cl_mem` ownership path.

## Interpretation

- Backend-before-scheduler safety requires two independent proofs: command completion and resource-deleter independence.
- The strongest audited contract combines explicit host-visible completion with event/buffer deleters that use persistent device or buffer-local state.
- A backend can be completion-safe yet teardown-order conditional, as the pinned CANN reset sequence demonstrates.
- Distributed RPC teardown adds another boundary: transmitted and serially dispatched commands are not necessarily complete on the remote accelerator.

## Historical

- Queue counts, graph capture, event types, allocation pools, registries, and destructor order are revision-sensitive. The comparison applies only to the pinned baseline.

## Open questions

- Complete the exact OpenCL destructor chain.
- Test immediate asynchronous graph submission followed by context destruction across accelerator backends.
- Verify CUDA all-stream and SYCL all-queue synchronization coverage.
- Validate CANN post-reset resource destruction.
- Add a real RPC completion command.
- Audit optional CPU extra buffers separately.

## Validation

- The new page was created through the repository contents API and linked in `mkdocs.yml`.
- Local strict MkDocs and test execution remain blocked because the environment cannot resolve `github.com` and has no checkout.
- CI and Pages are checked separately at the end of the run; exact visibility or deployment blockers are recorded in project state.

## Next priority

Finish the pinned OpenCL backend/context free and queue-completion audit when the oversized upstream translation unit becomes accessible, then audit optional CPU extra-buffer deleters.
