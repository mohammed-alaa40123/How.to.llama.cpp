from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validate_media_lifecycle import validate_lifecycle

FIXTURE = ROOT / "media/lifecycle/media-lifecycle-v0.json"


class MediaLifecycleValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def errors(self, data: dict) -> list[str]:
        return validate_lifecycle(data, repo_root=ROOT)

    def test_committed_lifecycle_passes(self) -> None:
        self.assertEqual(self.errors(self.data), [])

    def test_requires_all_three_review_states(self) -> None:
        broken = copy.deepcopy(self.data)
        broken["manifests"][2]["review_status"] = "revised"
        self.assertTrue(any("exactly one accepted" in error for error in self.errors(broken)))

    def test_rejects_duplicate_asset_ids(self) -> None:
        broken = copy.deepcopy(self.data)
        broken["manifests"][1]["asset_id"] = broken["manifests"][0]["asset_id"]
        self.assertIn("asset_id values must be unique", self.errors(broken))

    def test_rejects_external_generation_in_ordinary_ci(self) -> None:
        broken = copy.deepcopy(self.data)
        broken["ordinary_ci_external_generation"] = True
        self.assertIn("ordinary CI external generation must be false", self.errors(broken))

    def test_rejects_generative_mode(self) -> None:
        broken = copy.deepcopy(self.data)
        broken["manifests"][1]["generation"]["mode"] = "generative-api"
        self.assertTrue(any("must use deterministic generation" in error for error in self.errors(broken)))

    def test_rejects_stale_output_checksum(self) -> None:
        broken = copy.deepcopy(self.data)
        broken["manifests"][0]["output"]["sha256"] = "0" * 64
        self.assertTrue(any("output checksum is stale" in error for error in self.errors(broken)))

    def test_rejects_stale_input_checksum(self) -> None:
        broken = copy.deepcopy(self.data)
        broken["manifests"][0]["source"]["input_sha256"][0] = "0" * 64
        self.assertTrue(any("input 0 is stale" in error for error in self.errors(broken)))

    def test_rejected_asset_cannot_publish(self) -> None:
        broken = copy.deepcopy(self.data)
        broken["manifests"][2]["publication"]["publish"] = True
        self.assertTrue(any("rejected assets cannot be published" in error for error in self.errors(broken)))


if __name__ == "__main__":
    unittest.main()
