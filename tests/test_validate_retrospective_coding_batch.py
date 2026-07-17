import copy, importlib.util, json, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validator", ROOT / "scripts" / "validate_retrospective_coding_batch.py")
validator = importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(validator)

class CodingBatchTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((ROOT / "progress/examples/retrospective-coding-batch-v0.json").read_text())
    def assertInvalid(self, data):
        with self.assertRaises(validator.ValidationError): validator.validate(data)
    def test_fixture_valid(self): validator.validate(self.data)
    def test_duplicate_run_rejected(self):
        d=copy.deepcopy(self.data); d["records"].append(copy.deepcopy(d["records"][0])); self.assertInvalid(d)
    def test_mutable_revision_rejected(self):
        d=copy.deepcopy(self.data); d["source_revision"]="main"; self.assertInvalid(d)
    def test_partial_requires_missing_fields(self):
        d=copy.deepcopy(self.data); d["records"][0]["missing_fields"]=[]; self.assertInvalid(d)
    def test_complete_forbids_missing_fields(self):
        d=copy.deepcopy(self.data); d["records"][0]["evidence_completeness"]="complete_for_protocol"; self.assertInvalid(d)
    def test_blocked_requires_blocker_detail(self):
        d=copy.deepcopy(self.data); d["records"][0]["assignment_outcome"]="blocked_reassigned"; d["records"][0]["missing_fields"].append("blocker_detail"); self.assertInvalid(d)
    def test_disagreement_requires_fields(self):
        d=copy.deepcopy(self.data); d["records"][0]["coding_status"]="double_coded_disagree"; self.assertInvalid(d)
    def test_adjudication_requires_note(self):
        d=copy.deepcopy(self.data); d["records"][0]["coding_status"]="adjudicated"; self.assertInvalid(d)
    def test_path_traversal_rejected(self):
        d=copy.deepcopy(self.data); d["records"][0]["evidence_path"]="logs/research/../secret.md"; self.assertInvalid(d)
if __name__ == "__main__": unittest.main()
