import unittest

from scripts.generate_cpu_repack_lifetime_fixture import PINNED_REVISION, render_patch


class CpuRepackLifetimeFixtureGeneratorTest(unittest.TestCase):
    def test_patch_is_revision_scoped_and_deterministic(self):
        first = render_patch()
        second = render_patch()
        self.assertEqual(first, second)
        self.assertIn(PINNED_REVISION, first)
        self.assertIn("tests/test-cpu-extra-buffer-lifetime.cpp", first)

    def test_patch_contains_exact_single_tensor_allocation_contract(self):
        patch = render_patch()
        required = [
            "ggml_backend_buft_get_alloc_size(buft, tensor)",
            "ggml_backend_buft_alloc_buffer(buft, alloc_size)",
            "ggml_backend_buffer_get_base(buffer)",
            "ggml_backend_buffer_get_alignment(buffer)",
            "ggml_backend_tensor_alloc(buffer, tensor, addr) == GGML_STATUS_SUCCESS",
            "allocate_single_tensor(weight_buft, f.weight)",
        ]
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, patch)

    def test_patch_contains_complete_graph_execution(self):
        patch = render_patch()
        required = [
            "ggml_init_params params = {};",
            "params.no_alloc = true;",
            "ggml_new_tensor_2d(f.ctx, GGML_TYPE_Q4_0, k, m)",
            "ggml_new_tensor_2d(f.ctx, GGML_TYPE_F32,  k, n)",
            "ggml_mul_mat(f.ctx, f.weight, f.input)",
            "ggml_build_forward_expand(f.graph, f.output)",
            "ggml_gallocr_new(ordinary_buft)",
            "ggml_gallocr_alloc_graph(f.allocator, f.graph)",
            "ggml_backend_graph_compute(reference_backend, reference.graph)",
            "ggml_backend_graph_compute(tested_backend, tested.graph)",
            "read_output(reference.output)",
            "read_output(tested.output)",
        ]
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, patch)

    def test_patch_uses_identical_deterministic_inputs_and_nmse(self):
        patch = render_patch()
        required = [
            "make_q4_0_weights()",
            "ggml_quantize_chunk(",
            "written == quantized.size()",
            "ggml_backend_tensor_set(reference.weight, weights.data(), 0, weights.size())",
            "ggml_backend_tensor_set(tested.weight, weights.data(), 0, weights.size())",
            "ggml_backend_tensor_set(reference.input, input.data()",
            "ggml_backend_tensor_set(tested.input, input.data()",
            "const double error = nmse(reference_output, tested_output);",
            "error <= 1e-7",
        ]
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, patch)

    def test_patch_contains_path_proof_and_teardown_contract(self):
        patch = render_patch()
        required = [
            "ggml_cpu_has_avx2()",
            "ggml_backend_cpu_repack_buffer_type()",
            "tested.weight->buffer->buft == repack_buft",
            "tested.weight->extra != nullptr",
            "ggml_backend_supports_op(tested_backend, tested.output)",
            "ggml_backend_free(tested_backend);",
            "ggml_gallocr_free(tested.allocator);",
            "ggml_free(tested.ctx);",
            "ggml_backend_buffer_free(repack_buffer);",
            "PASS: CPU_REPACK path executed",
            "return 0;",
        ]
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, patch)

        self.assertLess(
            patch.index("ggml_backend_free(tested_backend);"),
            patch.index("ggml_backend_buffer_free(repack_buffer);"),
        )

    def test_patch_encodes_minimal_shape_and_cmake_target(self):
        patch = render_patch()
        self.assertIn("constexpr int64_t k = 32;", patch)
        self.assertIn("constexpr int64_t m = 8;", patch)
        self.assertIn("constexpr int64_t n = 1;", patch)
        self.assertIn(
            'llama_build_and_test(test-cpu-extra-buffer-lifetime.cpp LABEL "backend-lifetime")',
            patch,
        )
        self.assertIn("${PROJECT_SOURCE_DIR}/ggml/src", patch)

    def test_incomplete_boundary_is_removed(self):
        patch = render_patch()
        self.assertNotIn("INCOMPLETE:", patch)
        self.assertNotIn("return 2;", patch)


if __name__ == "__main__":
    unittest.main()
