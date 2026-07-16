import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_lab0_report", ROOT / "scripts" / "validate_lab0_report.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class Lab0ReportValidationTests(unittest.TestCase):
    def setUp(self):
        self.report = json.loads(
            (ROOT / "labs" / "lab0" / "examples" / "model-free-passing-report.json").read_text()
        )

    def test_model_free_passing_report_is_valid(self):
        self.assertEqual([], MODULE.validate_report(self.report))

    def test_compile_cannot_pass_before_configure(self):
        report = copy.deepcopy(self.report)
        report["phases"]["configure"]["state"] = "failed"
        report["claims"]["native_configured"] = False
        self.assertIn("compile=passed requires configure=passed", MODULE.validate_report(report))

    def test_model_free_launch_cannot_claim_inference(self):
        report = copy.deepcopy(self.report)
        report["claims"]["inference_succeeded"] = True
        self.assertIn(
            "claims.inference_succeeded must equal whether inference=passed",
            MODULE.validate_report(report),
        )

    def test_inference_requires_model_load(self):
        report = copy.deepcopy(self.report)
        report["model_input"] = {"kind": "learner_provided", "redacted_basename": "model.gguf"}
        report["phases"]["inference"]["state"] = "passed"
        report["claims"]["inference_succeeded"] = True
        self.assertIn("inference=passed requires model_load=passed", MODULE.validate_report(report))

    def test_model_basename_must_not_leak_path(self):
        report = copy.deepcopy(self.report)
        report["model_input"] = {"kind": "learner_provided", "redacted_basename": "/home/mo/model.gguf"}
        self.assertIn(
            "model_input.redacted_basename must not contain a path",
            MODULE.validate_report(report),
        )


if __name__ == "__main__":
    unittest.main()
