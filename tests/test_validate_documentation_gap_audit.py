import copy
import json
import unittest
from pathlib import Path

from scripts.validate_documentation_gap_audit import validate


class DocumentationGapAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads(
            Path("progress/examples/documentation-gap-audit-protocol-v0.json").read_text(encoding="utf-8")
        )

    def test_example_is_valid(self):
        self.assertEqual(validate(copy.deepcopy(self.fixture)), [])

    def test_gap_cannot_be_prejudged(self):
        data = copy.deepcopy(self.fixture)
        data["hypothesis_status"] = "verified"
        self.assertTrue(validate(data))

    def test_requires_all_strata(self):
        data = copy.deepcopy(self.fixture)
        data["strata"].pop()
        self.assertTrue(validate(data))

    def test_requires_frozen_top_twenty_sampling(self):
        data = copy.deepcopy(self.fixture)
        data["sampling"]["results_per_query"] = 10
        self.assertTrue(validate(data))

    def test_requires_independent_coders(self):
        data = copy.deepcopy(self.fixture)
        data["coding"]["independent_coders"] = 1
        self.assertTrue(validate(data))

    def test_single_coder_cannot_close_task(self):
        data = copy.deepcopy(self.fixture)
        data["coding"]["single_coder_closes_task"] = True
        self.assertTrue(validate(data))

    def test_requires_immutable_revision(self):
        data = copy.deepcopy(self.fixture)
        data["repository_revision"] = "main"
        self.assertTrue(validate(data))

    def test_requires_inconclusive_as_possible_result(self):
        data = copy.deepcopy(self.fixture)
        data["allowed_conclusions"].remove("inconclusive")
        self.assertTrue(validate(data))


if __name__ == "__main__":
    unittest.main()
