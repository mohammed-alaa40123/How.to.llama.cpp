import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_lab0_reproducibility",
    ROOT / "scripts" / "validate_lab0_reproducibility.py",
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class Lab0ReproducibilityValidationTests(unittest.TestCase):
    def setUp(self):
        self.report = json.loads(
            (ROOT / "labs" / "lab0" / "examples" / "reproducibility-local-linux-v0.json").read_text()
        )

    def assert_invalid(self, report):
        with self.assertRaises(MODULE.ValidationError):
            MODULE.validate(report)

    def test_valid_model_free_report(self):
        MODULE.validate(self.report)

    def test_requires_locked_uv_sync(self):
        report = copy.deepcopy(self.report)
        report["commands"]["python_sync"] = "uv sync"
        self.assert_invalid(report)

    def test_validated_environment_requires_success(self):
        report = copy.deepcopy(self.report)
        report["result"]["build_success"] = False
        report["result"]["launch_success"] = False
        report["result"]["diagnostics"] = ["COMPILE_FAILED"]
        self.assert_invalid(report)

    def test_model_free_run_cannot_claim_first_token(self):
        report = copy.deepcopy(self.report)
        report["timings"]["first_token_monotonic_ms"] = 95000
        report["timings"]["time_to_first_token_ms"] = 94000
        self.assert_invalid(report)

    def test_time_to_ready_is_derived(self):
        report = copy.deepcopy(self.report)
        report["timings"]["time_to_ready_ms"] += 1
        self.assert_invalid(report)

    def test_cached_offline_mode_forbids_network_dependency(self):
        report = copy.deepcopy(self.report)
        report["environment"]["offline_mode"] = "ready_from_cache"
        report["security"]["network_required_after_cache"] = True
        self.assert_invalid(report)

    def test_setup_success_rejects_missing_tool(self):
        report = copy.deepcopy(self.report)
        report["toolchain"]["ninja"]["passed"] = False
        report["result"]["diagnostics"] = ["NINJA_MISSING"]
        self.assert_invalid(report)

    def test_learner_model_can_record_first_token(self):
        report = copy.deepcopy(self.report)
        report["result"]["model_kind"] = "learner_provided"
        report["result"]["inference_state"] = "passed"
        report["commands"]["optional_inference"] = "build/lab0/bin/llama-cli -m MODEL.gguf -p test -n 1"
        report["timings"]["first_token_monotonic_ms"] = 95000
        report["timings"]["time_to_first_token_ms"] = 94000
        MODULE.validate(report)


if __name__ == "__main__":
    unittest.main()
