import copy
import json
import unittest
from pathlib import Path

from scripts.validate_media_manifest import validate_manifest


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "media" / "manifests" / "gguf-layout-deterministic-v0.json"


class MediaManifestValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.valid = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def test_deterministic_authoritative_manifest_passes(self):
        self.assertEqual(validate_manifest(self.valid), [])

    def test_generative_asset_cannot_be_authoritative(self):
        data = copy.deepcopy(self.valid)
        data["generation"]["mode"] = "generative-api"
        data["generation"]["model"] = "example-model"
        data["generation"]["manual_trigger"] = True
        data["generation"]["ordinary_ci_allowed"] = False
        data["generation"]["prompt_path"] = "media/prompts/example.txt"
        data["generation"]["prompt_sha256"] = "a" * 64
        data["generation"]["storyboard_path"] = "media/storyboards/example.md"
        data["generation"]["storyboard_sha256"] = "b" * 64
        errors = validate_manifest(data)
        self.assertTrue(any("cannot be authoritative" in error for error in errors))

    def test_generative_api_must_not_run_in_ordinary_ci(self):
        data = copy.deepcopy(self.valid)
        data["authority"] = "supplemental"
        data["generation"].update({
            "mode": "generative-api",
            "model": "example-model",
            "manual_trigger": True,
            "cached": True,
            "ordinary_ci_allowed": True,
            "prompt_path": "media/prompts/example.txt",
            "prompt_sha256": "a" * 64,
            "storyboard_path": "media/storyboards/example.md",
            "storyboard_sha256": "b" * 64,
        })
        self.assertTrue(any("ordinary CI" in error for error in validate_manifest(data)))

    def test_accepted_asset_requires_human_approval(self):
        data = copy.deepcopy(self.valid)
        data["human_review"]["approved"] = False
        self.assertTrue(any("human approval" in error for error in validate_manifest(data)))

    def test_rejected_asset_cannot_be_published(self):
        data = copy.deepcopy(self.valid)
        data["review_status"] = "rejected"
        self.assertIn("rejected assets cannot be published", validate_manifest(data))

    def test_audio_requires_transcript(self):
        data = copy.deepcopy(self.valid)
        data["asset_kind"] = "audio"
        data["authority"] = "supplemental"
        data["generation"]["mode"] = "human-authored"
        self.assertTrue(any("require a transcript" in error for error in validate_manifest(data)))

    def test_rejects_path_traversal_and_secrets(self):
        data = copy.deepcopy(self.valid)
        data["output"]["path"] = "../outside.svg"
        data["generation"]["api_key"] = "do-not-store"
        errors = validate_manifest(data)
        self.assertTrue(any("repository-relative" in error for error in errors))
        self.assertTrue(any("forbidden" in error for error in errors))

    def test_stale_source_revision_is_detected(self):
        errors = validate_manifest(self.valid, expected_source_revision="0" * 40)
        self.assertIn("manifest is stale for the expected source revision", errors)

    def test_manifest_size_is_bounded(self):
        self.assertEqual(validate_manifest(self.valid, raw_size=256 * 1024), [])
        self.assertTrue(any("exceeds" in error for error in validate_manifest(self.valid, raw_size=256 * 1024 + 1)))


if __name__ == "__main__":
    unittest.main()
