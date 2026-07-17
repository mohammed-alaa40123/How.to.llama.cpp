from __future__ import annotations

import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "generate_gguf_layout_figure.py"
SPEC = importlib.util.spec_from_file_location("generate_gguf_layout_figure", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class GgufLayoutFigureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.golden_path = ROOT / "labs" / "fixtures" / "gguf" / "synthetic-v0.golden.json"
        self.svg_path = ROOT / "media" / "generated" / "gguf-layout-deterministic-v0.svg"
        self.manifest_path = ROOT / "media" / "manifests" / "gguf-layout-deterministic-v0.json"

    def test_checked_in_svg_is_exact_generator_output(self) -> None:
        data = json.loads(self.golden_path.read_text(encoding="utf-8"))
        generated = MODULE.build_svg(data)
        self.assertEqual(generated, self.svg_path.read_text(encoding="utf-8"))

    def test_manifest_hashes_and_size_match_files(self) -> None:
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        input_bytes = self.golden_path.read_bytes()
        output_bytes = self.svg_path.read_bytes()
        self.assertEqual(hashlib.sha256(input_bytes).hexdigest(), manifest["source"]["input_sha256"][0])
        self.assertEqual(hashlib.sha256(output_bytes).hexdigest(), manifest["output"]["sha256"])
        self.assertEqual(len(output_bytes), manifest["output"]["bytes"])

    def test_svg_exposes_accessible_title_and_evidence_boundary(self) -> None:
        svg = self.svg_path.read_text(encoding="utf-8")
        self.assertIn('role="img" aria-labelledby="title desc"', svg)
        self.assertIn("<title id=\"title\">Synthetic GGUF v3 layout</title>", svg)
        self.assertIn("no model weights or native inference are represented", svg)
        self.assertIn("Runtime graph construction is outside this figure", svg)


if __name__ == "__main__":
    unittest.main()
