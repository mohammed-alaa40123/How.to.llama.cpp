import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validator", ROOT / "scripts" / "validate_agent_workflow_run.py")
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validator)
EXAMPLE = json.loads((ROOT / "progress" / "examples" / "agent-workflow-run-v0.json").read_text(encoding="utf-8"))


class AgentWorkflowRunValidationTests(unittest.TestCase):
    def test_valid_example(self):
        validator.validate(copy.deepcopy(EXAMPLE))

    def test_rejects_blocked_assignment_without_blocker(self):
        data = copy.deepcopy(EXAMPLE)
        data["assignment"]["dependency_state"] = "blocked"
        with self.assertRaises(validator.ValidationError):
            validator.validate(data)

    def test_rejects_mutable_revision(self):
        data = copy.deepcopy(EXAMPLE)
        data["revisions"]["ending_commit"] = "main"
        with self.assertRaises(validator.ValidationError):
            validator.validate(data)

    def test_rejects_verified_claim_without_evidence(self):
        data = copy.deepcopy(EXAMPLE)
        data["claims"][0]["evidence_paths"] = []
        with self.assertRaises(validator.ValidationError):
            validator.validate(data)

    def test_rejects_rejected_output_without_reason(self):
        data = copy.deepcopy(EXAMPLE)
        data["outputs"][0]["decision"] = "rejected"
        data["outputs"][0].pop("reason")
        with self.assertRaises(validator.ValidationError):
            validator.validate(data)

    def test_rejects_paid_calls_without_cost(self):
        data = copy.deepcopy(EXAMPLE)
        data["effort"]["paid_generation_calls"] = 1
        with self.assertRaises(validator.ValidationError):
            validator.validate(data)

    def test_rejects_sensitive_identity_field(self):
        data = copy.deepcopy(EXAMPLE)
        data["human_supervision"]["username"] = "learner"
        with self.assertRaises(validator.ValidationError):
            validator.validate(data)

    def test_rejects_passed_ci_without_run_id(self):
        data = copy.deepcopy(EXAMPLE)
        data["validation"].pop("ci_run_id")
        with self.assertRaises(validator.ValidationError):
            validator.validate(data)


if __name__ == "__main__":
    unittest.main()
