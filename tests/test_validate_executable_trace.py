import copy
import json
import unittest
from pathlib import Path

from scripts.validate_executable_trace import validate_trace


ROOT = Path(__file__).resolve().parents[1]
TRACE_PATH = ROOT / "executable_lectures" / "traces" / "gguf-load-authored-v0.json"


class ExecutableTraceValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid = json.loads(TRACE_PATH.read_text(encoding="utf-8"))

    def test_authored_fixture_passes(self):
        self.assertEqual(validate_trace(self.valid), [])

    def test_sequences_must_be_contiguous(self):
        data = copy.deepcopy(self.valid)
        data["steps"][1]["sequence"] = 3
        self.assertIn(
            "step sequences must be contiguous, ordered, and zero-based",
            validate_trace(data),
        )

    def test_authored_trace_cannot_claim_native_capture(self):
        data = copy.deepcopy(self.valid)
        data["steps"][0]["evidence_kind"] = "native-captured"
        errors = validate_trace(data)
        self.assertTrue(any("cannot claim native capture" in error for error in errors))

    def test_rejects_unpinned_source_revision(self):
        data = copy.deepcopy(self.valid)
        data["source"]["revision"] = "main"
        self.assertIn(
            "source.revision must be a full 40-character lowercase commit SHA",
            validate_trace(data),
        )

    def test_rejects_path_traversal(self):
        data = copy.deepcopy(self.valid)
        data["steps"][0]["location"]["file"] = "../secret.cpp"
        self.assertTrue(any("safe repository-relative path" in error for error in validate_trace(data)))

    def test_static_fallback_is_required(self):
        data = copy.deepcopy(self.valid)
        del data["steps"][0]["static_summary"]
        self.assertTrue(any("static fallback" in error for error in validate_trace(data)))

    def test_trace_size_is_bounded(self):
        self.assertEqual(validate_trace(self.valid, raw_size=2 * 1024 * 1024), [])
        self.assertTrue(any("exceeds" in error for error in validate_trace(self.valid, raw_size=2 * 1024 * 1024 + 1)))


if __name__ == "__main__":
    unittest.main()
