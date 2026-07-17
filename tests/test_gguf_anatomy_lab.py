import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "build_gguf_anatomy_lab.py"
SPEC = importlib.util.spec_from_file_location("build_gguf_anatomy_lab", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class GgufAnatomyLabTests(unittest.TestCase):
    def test_checked_in_payload_matches_builder_semantically(self):
        checked_in = json.loads((ROOT / "docs/assets/data/gguf-anatomy-v0.json").read_text(encoding="utf-8"))
        self.assertEqual(MODULE.build_payload(), checked_in)

    def test_payload_matches_fixture_contract(self):
        payload = MODULE.build_payload()
        self.assertEqual(payload["evidence_kind"], "browser-derived")
        self.assertEqual(payload["fixture"]["byte_length"], 428)
        self.assertEqual(payload["fixture"]["sha256"], "688d0ef28c83d6972e291cc0342e695540eae8496b3ec8e92bdbb91e3982a564")
        self.assertEqual(payload["golden"]["data_offset"], 384)
        self.assertEqual([item["id"] for item in payload["checkpoints"]], ["graph-storage", "tensor-offsets", "mapping-residency"])

    def test_browser_parser_has_bounds_and_golden_check(self):
        source = (ROOT / "docs/assets/javascripts/gguf-anatomy-lab.js").read_text(encoding="utf-8")
        for required in ["DataView", "getBigUint64", "truncated GGUF", "misaligned tensor offset", "browser parse disagrees with Python golden output"]:
            self.assertIn(required, source)
        self.assertNotIn("WebAssembly", source)

    def test_lab_declares_learning_contract_and_static_fallback(self):
        page = (ROOT / "docs/labs/gguf-anatomy.md").read_text(encoding="utf-8")
        for field in ["Intended learner", "Prerequisite", "Learning objective", "Predicted misconception", "Executable action", "Observable output", "Formative assessment", "Source revision", "Validation method", "Accessibility fallback"]:
            self.assertIn(field, page)
        self.assertIn("Static expected output", page)
        self.assertIn("not native llama.cpp execution", page)


if __name__ == "__main__":
    unittest.main()
