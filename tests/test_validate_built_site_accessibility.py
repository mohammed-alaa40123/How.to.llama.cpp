from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from scripts.validate_built_site_accessibility import inspect_page, validate_site


VALID_PAGE = """<!doctype html>
<html lang="en"><body><main><h1>Title</h1>
<img src="diagram.png" alt="Execution flow">
<iframe src="explorer.html" title="Interactive inference explorer"></iframe>
<button aria-label="Open navigation"></button>
</main></body></html>
"""


class BuiltSiteAccessibilityTests(unittest.TestCase):
    def test_valid_page_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "index.html"
            path.write_text(VALID_PAGE, encoding="utf-8")
            self.assertEqual(inspect_page(path), [])

    def test_reports_structural_failures(self) -> None:
        html = """<html><body><h1>A</h1><h1>B</h1>
        <img src="missing.png"><iframe src="x.html"></iframe><button></button>
        </body></html>"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.html"
            path.write_text(html, encoding="utf-8")
            errors = inspect_page(path)
            joined = "\n".join(errors)
            self.assertIn("html[lang]", joined)
            self.assertIn("exactly one <main>", joined)
            self.assertIn("exactly one <h1>", joined)
            self.assertIn("image lacks alt", joined)
            self.assertIn("iframe lacks", joined)
            self.assertIn("button(s) without", joined)

    def test_site_validation_skips_standalone_interactive_assets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "index.html").write_text(VALID_PAGE, encoding="utf-8")
            interactive = root / "assets" / "interactive"
            interactive.mkdir(parents=True)
            (interactive / "standalone.html").write_text("<html></html>", encoding="utf-8")
            self.assertEqual(validate_site(root), [])

    def test_missing_or_empty_site_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertTrue(validate_site(root))
            self.assertTrue(validate_site(root / "missing"))


if __name__ == "__main__":
    unittest.main()
