#!/usr/bin/env python3
"""Generate the pinned CPU_REPACK lifetime-regression patch.

The output is intentionally revision-scoped to llama.cpp
`e3546c7948e3af463d0b401e6421d5a4c2faf565`.  It is a reviewable
candidate patch, not proof that the fixture compiles on newer revisions.
"""

from __future__ import annotations

import argparse
from pathlib import Path

PINNED_REVISION = "e3546c7948e3af463d0b401e6421d5a4c2faf565"

CPP_SOURCE = r'''#include "ggml.h"
#include "ggml-alloc.h"
#include "ggml-backend.h"
#include "ggml-cpu.h"
#include "ggml-cpu/repack.h"

#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <vector>

static void require(bool condition, const char * message) {
    if (!condition) {
        std::fprintf(stderr, "CPU_REPACK lifetime fixture failed: %s\n", message);
        std::abort();
    }
}

// Pinned ggml_backend_tensor_alloc() takes an address inside an already
// allocated backend buffer, not a byte offset.  This helper keeps one tensor
// per buffer so the ownership boundary under test remains explicit.
static ggml_backend_buffer_t allocate_single_tensor(
        ggml_backend_buffer_type_t buft,
        ggml_tensor * tensor) {
    const size_t alloc_size = ggml_backend_buft_get_alloc_size(buft, tensor);
    ggml_backend_buffer_t buffer = ggml_backend_buft_alloc_buffer(buft, alloc_size);
    require(buffer != nullptr, "single-tensor backend buffer allocation");

    void * addr = ggml_backend_buffer_get_base(buffer);
    require(addr != nullptr, "single-tensor backend buffer base");
    require(reinterpret_cast<uintptr_t>(addr) % ggml_backend_buffer_get_alignment(buffer) == 0,
            "single-tensor backend buffer alignment");
    require(ggml_backend_tensor_alloc(buffer, tensor, addr) == GGML_STATUS_SUCCESS,
            "single-tensor backend tensor initialization");
    return buffer;
}

int main() {
    if (!ggml_cpu_has_avx2()) {
        std::puts("SKIP: AVX2 is unavailable; CPU_REPACK lifetime was not exercised");
        return 0;
    }

    // Pinned minimal admitted shape:
    // Q4_0 [32, 8] x F32 [32, 1] -> F32 [8, 1].
    constexpr int64_t k = 32;
    constexpr int64_t m = 8;
    constexpr int64_t n = 1;

    ggml_backend_t reference_backend = ggml_backend_cpu_init();
    ggml_backend_t tested_backend    = ggml_backend_cpu_init();
    require(reference_backend != nullptr, "reference CPU backend initialization");
    require(tested_backend    != nullptr, "tested CPU backend initialization");

    ggml_backend_buffer_type_t repack_buft = ggml_backend_cpu_repack_buffer_type();
    require(repack_buft != nullptr, "CPU_REPACK buffer type");

    // The final pinned-tree implementation should construct identical no-alloc
    // graphs.  Allocate the tested weight with allocate_single_tensor(repack_buft,
    // tested_weight), then let an ordinary CPU graph allocator allocate the
    // activation and output while recognizing the weight as externally allocated.
    // Upload the same Q4_0 bytes to both weights and compare F32 outputs with
    // normalized mean squared error <= 1e-7.
    //
    // These assertions are mandatory path proof rather than diagnostic-name matching:
    //
    //   tested_weight->buffer->buft == repack_buft
    //   tested_weight->extra != nullptr
    //   ggml_backend_supports_op(tested_backend, tested_mul_mat)
    //
    // Teardown must preserve the unusual order under test:
    //
    //   ggml_backend_free(tested_backend);
    //   ggml_free(tested_ctx);
    //   ggml_backend_buffer_free(repack_buffer);
    //
    // The executable remains deliberately incomplete until compiled against
    // the pinned source tree; returning success here would create false lifetime
    // evidence, so fail loudly after proving the hardware gate and allocation API.
    (void) k;
    (void) m;
    (void) n;
    (void) repack_buft;
    (void) allocate_single_tensor;

    ggml_backend_free(tested_backend);
    ggml_backend_free(reference_backend);
    std::fprintf(stderr,
        "INCOMPLETE: generated fixture skeleton requires pinned-tree graph integration\n");
    return 2;
}
'''

CMAKE_FRAGMENT = r'''# Pinned CPU_REPACK lifetime regression.
# The target includes an internal CPU header, so expose ggml/src only here.
llama_build_and_test(test-cpu-extra-buffer-lifetime.cpp LABEL "backend-lifetime")
target_include_directories(test-cpu-extra-buffer-lifetime PRIVATE ${PROJECT_SOURCE_DIR}/ggml/src)
'''


def render_patch() -> str:
    cpp_lines = CPP_SOURCE.splitlines()
    cmake_lines = CMAKE_FRAGMENT.splitlines()
    parts = [
        f"# Generated for llama.cpp {PINNED_REVISION}",
        "# Apply only after review against the exact pinned tree.",
        "",
        "--- /dev/null",
        "+++ b/tests/test-cpu-extra-buffer-lifetime.cpp",
        f"@@ -0,0 +1,{len(cpp_lines)} @@",
        *[f"+{line}" for line in cpp_lines],
        "",
        "--- a/tests/CMakeLists.txt",
        "+++ b/tests/CMakeLists.txt",
        "@@",
        " llama_build_and_test(test-backend-ops.cpp)",
        *[f"+{line}" for line in cmake_lines],
        "",
    ]
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    text = render_patch()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())