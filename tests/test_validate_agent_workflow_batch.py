from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_agent_workflow_batch import ValidationError, classify, validate_batch

SUCCESS = ROOT / "progress/examples/agent-workflow-run-viewer-success-v0.json"
REPAIR = ROOT / "progress/examples/agent-workflow-run-figure-ci-repair-v0.json"
BLOCKED = ROOT / "progress/examples/agent-workflow-run-lab0-blocked-data01-v0.json"


class AgentWorkflowBatchTests(unittest.TestCase):
    def test_first_batch_covers_three_required_archetypes(self) -> None:
        validate_batch([SUCCESS, REPAIR, BLOCKED])

    def test_archetype_classification_is_explicit(self) -> None:
        success = json.loads(SUCCESS.read_text(encoding="utf-8"))
        repair = json.loads(REPAIR.read_text(encoding="utf-8"))
        blocked = json.loads(BLOCKED.read_text(encoding="utf-8"))
        self.assertEqual(classify(success), {"successful_increment"})
        self.assertEqual(classify(repair), {"ci_repair"})
        self.assertEqual(classify(blocked), {"blocked_reassignment"})

    def test_duplicate_records_do_not_satisfy_batch(self) -> None:
        with self.assertRaises(ValidationError):
            validate_batch([SUCCESS, SUCCESS, BLOCKED])

    def test_missing_archetype_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            validate_batch([SUCCESS, BLOCKED, BLOCKED])


if __name__ == "__main__":
    unittest.main()
