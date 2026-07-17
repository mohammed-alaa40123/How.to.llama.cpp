import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_canonical_integration_decision.py"
EXAMPLE = ROOT / "progress" / "examples" / "canonical-integration-decision-pending-v0.json"

spec = importlib.util.spec_from_file_location("decision_validator", SCRIPT)
validator = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(validator)


class CanonicalIntegrationDecisionTests(unittest.TestCase):
    def setUp(self):
        self.record = json.loads(EXAMPLE.read_text(encoding="utf-8"))

    def assert_invalid(self, mutate):
        candidate = copy.deepcopy(self.record)
        mutate(candidate)
        with self.assertRaises(validator.ValidationError):
            validator.validate(candidate)

    def test_pending_example_is_valid(self):
        validator.validate(self.record)

    def test_rejects_mutable_revision(self):
        self.assert_invalid(lambda record: record.__setitem__("repository_revision", "main"))

    def test_rejects_alternate_progress_choice(self):
        self.assert_invalid(lambda record: record["progress_choice"].__setitem__("selected_pr", 23))

    def test_requires_both_preserved_followups(self):
        self.assert_invalid(lambda record: record["progress_choice"].__setitem__("preserved_followups", ["last-known-valid-recovery"]))

    def test_rejects_merge_order_drift(self):
        self.assert_invalid(lambda record: record["merge_order"].reverse())

    def test_rejects_invented_pending_reviewer(self):
        self.assert_invalid(lambda record: record["human_approval"].__setitem__("reviewer", "unapproved-reviewer"))

    def test_approved_requires_identity_and_timestamp(self):
        def mutate(record):
            record["human_approval"]["approved"] = True
            record["integration_status"] = "approved-not-integrated"
        self.assert_invalid(mutate)

    def test_validated_requires_combined_ci_note(self):
        def mutate(record):
            record["human_approval"] = {
                "approved": True,
                "reviewer": "human-reviewer",
                "approved_at": "2026-07-18T00:00:00Z",
                "notes": "Approved without validation evidence."
            }
            record["integration_status"] = "validated"
        self.assert_invalid(mutate)


if __name__ == "__main__":
    unittest.main()
