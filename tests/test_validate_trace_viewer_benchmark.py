from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate_trace_viewer_benchmark.py"
FIXTURE = ROOT / "executable_lectures/benchmarks/gguf-load-static-vs-viewer-v0.json"

spec = importlib.util.spec_from_file_location("validate_trace_viewer_benchmark", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


class TraceViewerBenchmarkValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def _write_and_validate(self, data: dict) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as handle:
            json.dump(data, handle)
            path = Path(handle.name)
        try:
            module.validate_benchmark(path, ROOT)
        finally:
            path.unlink(missing_ok=True)

    def test_committed_benchmark_is_valid(self) -> None:
        module.validate_benchmark(FIXTURE, ROOT)

    def test_rejects_mutable_source_revision(self) -> None:
        data = copy.deepcopy(self.data)
        data["source_revision"] = "main"
        with self.assertRaisesRegex(module.BenchmarkValidationError, "immutable"):
            self._write_and_validate(data)

    def test_rejects_information_inequivalence(self) -> None:
        data = copy.deepcopy(self.data)
        data["conditions"][1]["evidence_ids"] = data["conditions"][1]["evidence_ids"][:-1]
        with self.assertRaisesRegex(module.BenchmarkValidationError, "identical ordered evidence"):
            self._write_and_validate(data)

    def test_rejects_different_question_order(self) -> None:
        data = copy.deepcopy(self.data)
        data["conditions"][1]["question_ids"] = list(reversed(data["conditions"][1]["question_ids"]))
        with self.assertRaisesRegex(module.BenchmarkValidationError, "identical ordered question"):
            self._write_and_validate(data)

    def test_rejects_interactive_feature_in_static_condition(self) -> None:
        data = copy.deepcopy(self.data)
        data["conditions"][0]["allowed_interface_features"].append("coordinated-source-highlighting")
        with self.assertRaisesRegex(module.BenchmarkValidationError, "interactive-only"):
            self._write_and_validate(data)

    def test_requires_transfer_task(self) -> None:
        data = copy.deepcopy(self.data)
        for task in data["tasks"]:
            if task["task_type"] == "transfer":
                task["task_type"] = "evidence-boundary"
        with self.assertRaisesRegex(module.BenchmarkValidationError, "transfer task"):
            self._write_and_validate(data)

    def test_rejects_unknown_evidence(self) -> None:
        data = copy.deepcopy(self.data)
        data["tasks"][0]["evidence_ids"] = ["step:not-real"]
        with self.assertRaisesRegex(module.BenchmarkValidationError, "unknown evidence"):
            self._write_and_validate(data)

    def test_requires_accessibility_fallbacks(self) -> None:
        data = copy.deepcopy(self.data)
        data["accessibility"]["static_fallback"] = False
        with self.assertRaisesRegex(module.BenchmarkValidationError, "static_fallback"):
            self._write_and_validate(data)


if __name__ == "__main__":
    unittest.main()
