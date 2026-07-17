from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class GGUFProgressIntegrationTests(unittest.TestCase):
    def test_published_store_matches_canonical_module(self):
        self.assertEqual(
            (ROOT / "progress/progress-store.mjs").read_bytes(),
            (ROOT / "docs/assets/javascripts/progress-store.mjs").read_bytes(),
        )

    def test_lab_uses_local_only_versioned_adapter(self):
        script = (ROOT / "docs/assets/javascripts/gguf-anatomy-lab.js").read_text()
        self.assertIn('import(PROGRESS_MODULE)', script)
        self.assertIn('createLocalStorageAdapter(window.localStorage)', script)
        self.assertIn('payload.source_revision.revision', script)
        self.assertIn('checkpoint answers remain unrecorded', script.lower())
        self.assertNotIn('fetch("http', script)
        self.assertNotIn("navigator.sendBeacon", script)

    def test_accessible_import_export_controls_and_claim_boundary(self):
        page = (ROOT / "docs/labs/gguf-anatomy.md").read_text()
        for marker in (
            "data-progress-export",
            "data-progress-import",
            'role="status"',
            'aria-live="polite"',
            "does not record an answer",
            "synchronize with a server",
        ):
            self.assertIn(marker, page)


if __name__ == "__main__":
    unittest.main()
