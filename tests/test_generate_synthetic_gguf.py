import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "generate_synthetic_gguf.py"
SPEC = importlib.util.spec_from_file_location("synthetic_gguf", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class SyntheticGgufTests(unittest.TestCase):
    def test_regeneration_matches_golden_output(self):
        data, details = MODULE.build_fixture()
        parsed = MODULE.parse_fixture(data)
        golden = json.loads(
            (ROOT / "labs/fixtures/gguf/synthetic-v0.golden.json").read_text(encoding="utf-8")
        )
        manifest = json.loads(
            (ROOT / "labs/fixtures/gguf/synthetic-v0.manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(parsed, golden)
        self.assertEqual(parsed["file_sha256"], manifest["expected_sha256"])
        self.assertEqual(parsed["alignment"], 32)
        self.assertEqual(parsed["tensor_count"], 2)
        self.assertEqual(parsed["metadata"]["fixture.tags"], ["synthetic", "non-model"])
        self.assertEqual(details["tensor_ranges"][0]["relative_offset"], 0)
        self.assertEqual(details["tensor_ranges"][1]["relative_offset"], 32)

    def test_tensor_ranges_are_aligned_and_bounded(self):
        data, _ = MODULE.build_fixture()
        parsed = MODULE.parse_fixture(data)
        for tensor in parsed["tensors"]:
            self.assertEqual(tensor["relative_offset"] % parsed["alignment"], 0)
            self.assertLessEqual(tensor["absolute_offset"] + tensor["size"], len(data))

    def test_bounded_corruptions_are_rejected(self):
        data, details = MODULE.build_fixture()
        for name, variant in MODULE.corruption_variants(data, details).items():
            with self.subTest(name=name):
                with self.assertRaises(ValueError):
                    MODULE.parse_fixture(variant)


if __name__ == "__main__":
    unittest.main()
