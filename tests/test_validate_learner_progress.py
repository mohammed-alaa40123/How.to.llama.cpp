import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_learner_progress", ROOT / "scripts" / "validate_learner_progress.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class LearnerProgressValidationTests(unittest.TestCase):
    def setUp(self):
        self.example_path = ROOT / "progress" / "examples" / "local-progress-v0.json"
        self.example = json.loads(self.example_path.read_text(encoding="utf-8"))

    def assert_invalid(self, data):
        with self.assertRaises(MODULE.ProgressValidationError):
            MODULE.validate_progress(data)

    def test_committed_example_passes(self):
        MODULE.validate_file(self.example_path)

    def test_rejects_privacy_sensitive_field_anywhere(self):
        data = copy.deepcopy(self.example)
        data["lessons"][0]["email"] = "learner@example.com"
        self.assert_invalid(data)

    def test_rejects_mutable_source_revision(self):
        data = copy.deepcopy(self.example)
        data["source_revision"] = "main"
        self.assert_invalid(data)

    def test_rejects_unanswered_checkpoint_with_attempt(self):
        data = copy.deepcopy(self.example)
        data["lessons"][0]["checkpoints"][2]["attempt_count"] = 1
        self.assert_invalid(data)

    def test_rejects_completed_lesson_with_unpassed_checkpoint(self):
        data = copy.deepcopy(self.example)
        data["lessons"][0]["status"] = "completed"
        self.assert_invalid(data)

    def test_rejects_duplicate_checkpoint_ids(self):
        data = copy.deepcopy(self.example)
        data["lessons"][0]["checkpoints"][1]["checkpoint_id"] = data["lessons"][0]["checkpoints"][0]["checkpoint_id"]
        self.assert_invalid(data)

    def test_rejects_oversized_export_before_json_parse(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "large.json"
            path.write_bytes(b" " * (MODULE.MAX_FILE_BYTES + 1))
            with self.assertRaises(MODULE.ProgressValidationError):
                MODULE.validate_file(path)


if __name__ == "__main__":
    unittest.main()
