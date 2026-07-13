# OpenCL build and initial buffer-lifetime increment

- Run time: 2026-07-13 18:51 Africa/Cairo
- Scope: pinned OpenCL build composition, kernel deployment, official platform scope, initial `cl_mem` ownership, and teardown-audit boundaries
- Baseline: llama.cpp `e3546c7948e3af463d0b401e6421d5a4c2faf565`

## Artifact

Added `docs/architecture/opencl-build-and-buffer-lifetimes.md` and linked it under Architecture navigation.

## Verified

- The top-level build registers OpenCL as a GGML backend.
- The backend target consists of `ggml-opencl.cpp`, its public header, OpenCL libraries, and a large catalog of OpenCL C kernels.
- Embedded-kernel mode generates headers with Python; non-embedded mode copies kernel files beside the executable.
- Optional Adreno source and binary-kernel paths are separately controlled.
- The catalog includes common tensor operations, attention, quantized matrix operations, and MoE-specific expert kernels.
- The official pinned guide documents intended Adreno-first scope, selected Intel support, tested operating systems, build steps, and known limitations.
- `ggml_cl_buffer` owns one `cl_mem`, releasing it before replacement and at destruction.

## Interpretation

- Kernel build/deployment lifetime and runtime resource lifetime are separate concerns.
- `cl_mem` RAII proves buffer-local ownership, not completion of commands that may still reference the object.
- The large single-file backend needs symbol-level source indexing to make the remaining destructor audit reviewable.

## Historical

- Device support, kernel names, deployment mode, driver/compiler compatibility, and vendor binary coverage are revision-sensitive.

## Open questions

- Exact backend/context free chain and any `clFinish` or event wait.
- Scheduler event and buffer independence after backend-wrapper deletion.
- Program, kernel, event, queue, memory-object, context, and binary-library release order.
- Optional CPU extra-buffer lifetime interaction.

## Sources inspected

- Complete repository README and required reference files.
- Latest detailed CANN note.
- Current `mkdocs.yml`.
- Pinned `ggml/src/CMakeLists.txt`.
- Pinned `ggml/src/ggml-opencl/CMakeLists.txt`.
- Pinned `ggml/src/ggml-opencl/ggml-opencl.cpp` initial ownership definitions.
- Pinned `docs/backend/OPENCL.md`.

## Validation

- Connector-side inspection verified the build and initial buffer-ownership claims.
- Local clone failed with `Could not resolve host: github.com`; project validators and strict MkDocs could not run locally.
- GitHub Actions and Pages checks are recorded in project state after this note.

## Next priority

Finish the exact OpenCL backend/context teardown chain and classify backend-before-scheduler safety; then audit optional CPU extra-buffer deleters.
