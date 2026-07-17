from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "validate_trace_source_links.py"
SPEC = importlib.util.spec_from_file_location("validate_trace_source_links", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

TRACE_PATH = ROOT / "executable_lectures" / "traces" / "gguf-load-authored-v0.json"
MANIFEST_PATH = ROOT / "executable_lectures" / "source-anchors" / "llama-cpp-e3546c7.json"


class TraceSourceLinkValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.trace = json.loads(TRACE_PATH.read_text(encoding="utf-8"))
        self.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    def test_committed_trace_matches_pinned_source_manifest(self) -> None:
        self.assertEqual(MODULE.validate_source_links(self.trace, self.manifest), [])

    def test_rejects_revision_drift(self) -> None:
        trace = copy.deepcopy(self.trace)
        trace["source"]["revision"] = "0" * 40
        self.assertIn(
            "trace source.revision does not match the pinned manifest",
            MODULE.validate_source_links(trace, self.manifest),
        )

    def test_rejects_wrong_function_even_when_file_exists(self) -> None:
        trace = copy.deepcopy(self.trace)
        trace["steps"][0]["location"]["function"] = "gguf_init_from_file_impl"
        errors = MODULE.validate_source_links(trace, self.manifest)
        self.assertTrue(any("no pinned file/function anchor" in error for error in errors))

    def test_rejects_line_outside_function_range(self) -> None:
        trace = copy.deepcopy(self.trace)
        trace["steps"][1]["location"]["line"] = 1100
        errors = MODULE.validate_source_links(trace, self.manifest)
        self.assertTrue(any("outside the pinned function range" in error for error in errors))

    def test_navigation_clamps_at_boundaries(self) -> None:
        self.assertEqual(MODULE.replay_index(3, 0, "previous"), 0)
        self.assertEqual(MODULE.replay_index(3, 2, "next"), 2)

    def test_navigation_round_trip_for_interior_transition(self) -> None:
        self.assertEqual(MODULE.replay_index(3, MODULE.replay_index(3, 1, "next"), "previous"), 1)
        self.assertEqual(MODULE.replay_index(3, MODULE.replay_index(3, 1, "previous"), "next"), 1)

    def test_missing_optional_runtime_collections_remains_valid(self) -> None:
        trace = copy.deepcopy(self.trace)
        for step in trace["steps"]:
            step.pop("runtime_objects", None)
            step.pop("tensor_shapes", None)
            step.pop("memory_events", None)
            step.pop("figures", None)
        self.assertEqual(MODULE.validate_source_links(trace, self.manifest), [])


if __name__ == "__main__":
    unittest.main()
