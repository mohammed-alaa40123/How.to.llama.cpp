from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from validate_retrospective_coverage import ValidationError, validate

EXAMPLE = json.loads((ROOT / "progress/examples/agent-workflow-coverage-first-batch-v0.json").read_text(encoding="utf-8"))


class RetrospectiveCoverageTests(unittest.TestCase):
    def test_valid_first_batch_coverage(self) -> None:
        validate(copy.deepcopy(EXAMPLE))

    def test_observed_dimension_requires_evidence(self) -> None:
        data = copy.deepcopy(EXAMPLE)
        data["dimensions"][0]["evidence_paths"] = []
        with self.assertRaises(ValidationError):
            validate(data)

    def test_non_observed_dimension_rejects_evidence(self) -> None:
        data = copy.deepcopy(EXAMPLE)
        item = next(value for value in data["dimensions"] if value["status"] == "not_reconstructable")
        item["evidence_paths"] = ["logs/research/2026-07-17/1715-review02-adversarial-evidence-gates.md"]
        with self.assertRaises(ValidationError):
            validate(data)

    def test_duplicate_dimension_is_rejected(self) -> None:
        data = copy.deepcopy(EXAMPLE)
        data["dimensions"].append(copy.deepcopy(data["dimensions"][0]))
        with self.assertRaises(ValidationError):
            validate(data)

    def test_missing_required_dimension_is_rejected(self) -> None:
        data = copy.deepcopy(EXAMPLE)
        data["dimensions"] = [value for value in data["dimensions"] if value["field"] != "effort.human_minutes"]
        with self.assertRaises(ValidationError):
            validate(data)

    def test_all_observed_claim_is_rejected(self) -> None:
        data = copy.deepcopy(EXAMPLE)
        for item in data["dimensions"]:
            if item["status"] == "not_reconstructable":
                item["status"] = "observed"
                item["evidence_paths"] = ["progress/examples/agent-workflow-run-viewer-success-v0.json"]
        with self.assertRaises(ValidationError):
            validate(data)

    def test_duplicate_record_ids_are_rejected(self) -> None:
        data = copy.deepcopy(EXAMPLE)
        data["records"].append(data["records"][0])
        with self.assertRaises(ValidationError):
            validate(data)


if __name__ == "__main__":
    unittest.main()
