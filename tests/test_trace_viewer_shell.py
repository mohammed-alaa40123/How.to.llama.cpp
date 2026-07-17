import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRACE = ROOT / "executable_lectures/traces/gguf-load-authored-v0.json"
PAYLOAD = ROOT / "docs/assets/data/gguf-load-authored-v0.viewer.json"
PAGE = ROOT / "docs/executable-lectures/trace-viewer.md"
SCRIPT = ROOT / "docs/assets/javascripts/trace-viewer.js"
BUILDER = ROOT / "scripts/build_trace_viewer_data.py"


def load_builder():
    spec = importlib.util.spec_from_file_location("trace_viewer_builder", BUILDER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class TraceViewerShellTests(unittest.TestCase):
    def test_generated_payload_matches_validated_trace(self):
        builder = load_builder()
        trace = json.loads(TRACE.read_text(encoding="utf-8"))
        committed = PAYLOAD.read_text(encoding="utf-8")
        self.assertEqual(committed, builder.render(builder.build_payload(trace)))

    def test_payload_preserves_order_and_evidence_boundary(self):
        payload = json.loads(PAYLOAD.read_text(encoding="utf-8"))
        self.assertEqual([0, 1, 2], [step["sequence"] for step in payload["steps"]])
        self.assertEqual(
            ["authored-example", "source-derived", "source-derived"],
            [step["evidence_kind"] for step in payload["steps"]],
        )
        self.assertTrue(all("/blob/e3546c7948e3af463d0b401e6421d5a4c2faf565/" in step["source_url"] for step in payload["steps"]))

    def test_page_declares_learning_and_accessibility_contract(self):
        page = PAGE.read_text(encoding="utf-8")
        required = [
            "Intended learner",
            "Prerequisite",
            "Learning objective",
            "Predicted misconception",
            "Executable action",
            "Observable output",
            "Formative assessment",
            "Source revision",
            "Validation method",
            "Accessibility fallback",
            'aria-live="polite"',
            'data-action="previous"',
            'data-action="next"',
            "Ordered static transcript",
            "prefers-reduced-motion",
        ]
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, page)

    def test_script_has_bounded_keyboard_navigation_and_fallback(self):
        script = SCRIPT.read_text(encoding="utf-8")
        for key in ["ArrowLeft", "ArrowRight", "Home", "End"]:
            self.assertIn(key, script)
        self.assertIn("Math.max(0, Math.min(trace.steps.length - 1", script)
        self.assertIn("Use the ordered transcript below", script)
        self.assertNotIn("eval(", script)
        self.assertNotIn("innerHTML = step", script)


if __name__ == "__main__":
    unittest.main()
