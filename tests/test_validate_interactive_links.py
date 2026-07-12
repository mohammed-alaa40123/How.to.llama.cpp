from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_interactive_links.py"
SPEC = importlib.util.spec_from_file_location("validate_interactive_links", SCRIPT)
assert SPEC and SPEC.loader
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


class InteractiveLinkValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.docs = self.root / "docs"
        self.assets = self.docs / "assets" / "interactive"
        self.assets.mkdir(parents=True)
        self.original_root = validator.ROOT
        self.original_docs = validator.DOCS
        self.original_interactive = validator.INTERACTIVE
        validator.ROOT = self.root
        validator.DOCS = self.docs
        validator.INTERACTIVE = self.assets

    def tearDown(self) -> None:
        validator.ROOT = self.original_root
        validator.DOCS = self.original_docs
        validator.INTERACTIVE = self.original_interactive
        self.tempdir.cleanup()

    def write(self, relative: str, content: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_accepts_valid_href_page_and_anchor(self) -> None:
        self.write("docs/objects/llama-model.md", "# llama_model\n\n## Ownership and teardown\n")
        self.write(
            "docs/foundations/memory-lifetimes.md",
            "# Memory lifetimes\n\n## Page faults and page cache\n",
        )
        asset = self.write(
            "docs/assets/interactive/llama-foundations-explorer.html",
            """<a href=\"../../objects/llama-model/#ownership-and-teardown\">Model</a>
<script>
const layers=[{page:'objects/llama-model/'}];
const memory=[{anchor:'#page-faults-and-page-cache'}];
</script>
""",
        )
        self.assertEqual([], validator.validate_assets([asset]))

    def test_reports_missing_route_with_asset_and_expected_path(self) -> None:
        asset = self.write(
            "docs/assets/interactive/example.html",
            '<a href="../../objects/missing/">Missing</a>',
        )
        problems = validator.validate_assets([asset])
        self.assertEqual(1, len(problems))
        self.assertIn("route does not resolve", problems[0].message)
        self.assertIn("docs/objects/missing.md", problems[0].message)
        self.assertEqual("../../objects/missing/", problems[0].reference)

    def test_reports_missing_anchor(self) -> None:
        self.write("docs/topic.md", "# Topic\n\n## Existing section\n")
        asset = self.write(
            "docs/assets/interactive/example.html",
            '<a href="../../topic/#missing-section">Missing anchor</a>',
        )
        problems = validator.validate_assets([asset])
        self.assertEqual(1, len(problems))
        self.assertIn("anchor '#missing-section' not found", problems[0].message)

    def test_ignores_external_and_non_document_asset_links(self) -> None:
        self.write("docs/assets/diagram.svg", "<svg></svg>")
        asset = self.write(
            "docs/assets/interactive/example.html",
            '<a href="https://example.com/x">External</a><img src="../diagram.svg">',
        )
        self.assertEqual([], validator.validate_assets([asset]))

    def test_heading_slug_handles_code_links_and_explicit_ids(self) -> None:
        markdown = """# Title
## `llama_model` and [context](other.md)
## Custom heading {#stable-id}
"""
        self.assertEqual(
            {"title", "llama_model-and-context", "stable-id"},
            validator.heading_ids(markdown),
        )


if __name__ == "__main__":
    unittest.main()
