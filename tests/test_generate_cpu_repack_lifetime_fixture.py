import unittest

from scripts.generate_cpu_repack_lifetime_fixture import PINNED_REVISION, render_patch


class CpuRepackLifetimeFixtureGeneratorTest(unittest.TestCase):
    def test_patch_is_revision_scoped_and_deterministic(self):
        first = render_patch()
        second = render_patch()
        self.assertEqual(first, second)
        self.assertIn(PINNED_REVISION, first)
        self.assertIn("tests/test-cpu-extra-buffer-lifetime.cpp", first)

    def test_patch_contains_path_proof_and_teardown_contract(self):
        patch = render_patch()
        required = [
            "ggml_cpu_has_avx2()",
            "ggml_backend_cpu_repack_buffer_type()",
            "tested_weight->buffer->buft == repack_buft",
            "tested_weight->extra != nullptr",
            "ggml_backend_supports_op(tested_backend, tested_mul_mat)",
            "ggml_backend_free(tested_backend);",
            "ggml_backend_buffer_free(repack_buffer);",
            'return 2;',
        ]
        for token in required:
            with self.subTest(token=token):
                self.assertIn(token, patch)

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

    def test_skeleton_cannot_create_false_success_evidence(self):
        patch = render_patch()
        self.assertIn("INCOMPLETE: generated fixture skeleton", patch)
        self.assertNotIn("return 0;\n+}", patch.split("INCOMPLETE:", 1)[1])


if __name__ == "__main__":
    unittest.main()
