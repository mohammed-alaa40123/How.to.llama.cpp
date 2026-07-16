#!/usr/bin/env python3
"""Generate the pinned CPU_REPACK lifetime-regression patch."""

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
#include <cstdint>
#include <vector>

static void require(bool condition, const char * message) {
    if (!condition) {
        std::fprintf(stderr, "CPU_REPACK lifetime fixture failed: %s\n", message);
        std::abort();
    }
}

struct fixture_graph {
    ggml_context * ctx;
    ggml_cgraph * graph;
    ggml_tensor * weight;
    ggml_tensor * input;
    ggml_tensor * output;
    ggml_gallocr_t allocator;
};

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

static fixture_graph make_graph(
        ggml_backend_buffer_type_t ordinary_buft,
        ggml_backend_buffer_type_t weight_buft) {
    constexpr int64_t k = 32;
    constexpr int64_t m = 8;
    constexpr int64_t n = 1;

    ggml_init_params params = {};
    params.mem_size = 4 * ggml_tensor_overhead() + ggml_graph_overhead();
    params.mem_buffer = nullptr;
    params.no_alloc = true;

    fixture_graph f = {};
    f.ctx = ggml_init(params);
    require(f.ctx != nullptr, "GGML context initialization");

    f.weight = ggml_new_tensor_2d(f.ctx, GGML_TYPE_Q4_0, k, m);
    f.input  = ggml_new_tensor_2d(f.ctx, GGML_TYPE_F32,  k, n);
    f.output = ggml_mul_mat(f.ctx, f.weight, f.input);
    f.graph  = ggml_new_graph(f.ctx);
    ggml_build_forward_expand(f.graph, f.output);

    if (weight_buft != nullptr) {
        allocate_single_tensor(weight_buft, f.weight);
    }

    f.allocator = ggml_gallocr_new(ordinary_buft);
    require(f.allocator != nullptr, "graph allocator initialization");
    require(ggml_gallocr_alloc_graph(f.allocator, f.graph), "graph allocation");
    return f;
}

static std::vector<uint8_t> make_q4_0_weights() {
    constexpr int64_t k = 32;
    constexpr int64_t m = 8;
    std::vector<float> source(k * m);
    for (size_t i = 0; i < source.size(); ++i) {
        source[i] = std::sin(static_cast<float>(i) * 0.173f) * 0.75f;
    }

    std::vector<uint8_t> quantized(ggml_row_size(GGML_TYPE_Q4_0, k) * m);
    const size_t written = ggml_quantize_chunk(
        GGML_TYPE_Q4_0, source.data(), quantized.data(), 0, m, k, nullptr);
    require(written == quantized.size(), "deterministic Q4_0 quantization size");
    return quantized;
}

static std::vector<float> make_input() {
    constexpr int64_t k = 32;
    std::vector<float> input(k);
    for (size_t i = 0; i < input.size(); ++i) {
        input[i] = std::cos(static_cast<float>(i) * 0.117f) * 0.5f;
    }
    return input;
}

static std::vector<float> read_output(const ggml_tensor * tensor) {
    std::vector<float> output(ggml_nelements(tensor));
    ggml_backend_tensor_get(tensor, output.data(), 0, output.size() * sizeof(float));
    return output;
}

static double nmse(const std::vector<float> & reference, const std::vector<float> & tested) {
    require(reference.size() == tested.size(), "output size equality");
    double squared_error = 0.0;
    double reference_energy = 0.0;
    for (size_t i = 0; i < reference.size(); ++i) {
        const double delta = static_cast<double>(reference[i]) - static_cast<double>(tested[i]);
        squared_error += delta * delta;
        reference_energy += static_cast<double>(reference[i]) * static_cast<double>(reference[i]);
    }
    require(reference_energy > 0.0, "non-zero reference output");
    return squared_error / reference_energy;
}

int main() {
    if (!ggml_cpu_has_avx2()) {
        std::puts("SKIP: AVX2 is unavailable; CPU_REPACK lifetime was not exercised");
        return 0;
    }

    ggml_backend_t reference_backend = ggml_backend_cpu_init();
    ggml_backend_t tested_backend = ggml_backend_cpu_init();
    require(reference_backend != nullptr, "reference CPU backend initialization");
    require(tested_backend != nullptr, "tested CPU backend initialization");

    ggml_backend_buffer_type_t ordinary_buft = ggml_backend_cpu_buffer_type();
    ggml_backend_buffer_type_t repack_buft = ggml_backend_cpu_repack_buffer_type();
    require(ordinary_buft != nullptr, "ordinary CPU buffer type");
    require(repack_buft != nullptr, "CPU_REPACK buffer type");

    fixture_graph reference = make_graph(ordinary_buft, nullptr);
    fixture_graph tested = make_graph(ordinary_buft, repack_buft);
    ggml_backend_buffer_t repack_buffer = tested.weight->buffer;

    require(tested.weight->buffer != nullptr, "tested weight buffer");
    require(tested.weight->buffer->buft == repack_buft, "exact CPU_REPACK buffer identity");
    require(tested.weight->extra != nullptr, "CPU_REPACK traits selected");
    require(ggml_backend_supports_op(tested_backend, tested.output), "CPU_REPACK MUL_MAT admission");

    const std::vector<uint8_t> weights = make_q4_0_weights();
    const std::vector<float> input = make_input();
    ggml_backend_tensor_set(reference.weight, weights.data(), 0, weights.size());
    ggml_backend_tensor_set(tested.weight, weights.data(), 0, weights.size());
    ggml_backend_tensor_set(reference.input, input.data(), 0, input.size() * sizeof(float));
    ggml_backend_tensor_set(tested.input, input.data(), 0, input.size() * sizeof(float));

    require(ggml_backend_graph_compute(reference_backend, reference.graph) == GGML_STATUS_SUCCESS,
            "reference graph compute");
    require(ggml_backend_graph_compute(tested_backend, tested.graph) == GGML_STATUS_SUCCESS,
            "CPU_REPACK graph compute");

    const std::vector<float> reference_output = read_output(reference.output);
    const std::vector<float> tested_output = read_output(tested.output);
    const double error = nmse(reference_output, tested_output);
    require(error <= 1e-7, "normalized mean squared error <= 1e-7");

    ggml_backend_free(tested_backend);
    tested_backend = nullptr;

    ggml_gallocr_free(tested.allocator);
    ggml_free(tested.ctx);
    ggml_backend_buffer_free(repack_buffer);

    ggml_backend_free(reference_backend);
    ggml_gallocr_free(reference.allocator);
    ggml_free(reference.ctx);

    std::printf("PASS: CPU_REPACK path executed; NMSE=%g\n", error);
    return 0;
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
