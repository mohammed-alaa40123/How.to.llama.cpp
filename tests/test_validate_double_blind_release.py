import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validator", ROOT / "scripts" / "validate_double_blind_release.py")
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(validator)


class DoubleBlindReleaseTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "progress/examples/double-blind-release-plan-v0.json").read_text())

    def test_example_is_valid_and_not_ready(self):
        validator.validate(self.data)
        self.assertFalse(self.data["release_ready"])

    def test_rejects_mutable_revision(self):
        self.data["submission_revision"] = "main"
        with self.assertRaises(ValueError):
            validator.validate(self.data)

    def test_rejects_identity_leak(self):
        self.data["public_artifact"]["included"].append("github.com/example/repo")
        with self.assertRaises(ValueError):
            validator.validate(self.data)

    def test_rejects_public_crosswalk(self):
        self.data["private_crosswalk"]["published_before_decision"] = True
        with self.assertRaises(ValueError):
            validator.validate(self.data)

    def test_rejects_blocker_without_detail(self):
        del self.data["checks"][0]["blocker"]
        with self.assertRaises(ValueError):
            validator.validate(self.data)

    def test_rejects_missing_category(self):
        self.data["checks"] = [c for c in self.data["checks"] if c["category"] != "cost"]
        with self.assertRaises(ValueError):
            validator.validate(self.data)

    def test_rejects_false_ready_claim(self):
        self.data["release_ready"] = True
        with self.assertRaises(ValueError):
            validator.validate(self.data)

    def test_accepts_ready_only_when_all_gates_pass(self):
        ready = copy.deepcopy(self.data)
        for check in ready["checks"]:
            check["status"] = "pass"
            check.pop("blocker", None)
        for key in ready["approvals"]:
            ready["approvals"][key] = True
        ready["release_ready"] = True
        validator.validate(ready)


if __name__ == "__main__":
    unittest.main()
