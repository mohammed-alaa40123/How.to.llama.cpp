import copy
import json
import unittest
from pathlib import Path

from scripts.validate_trace_source_replay import (
    replay_step_index,
    static_replay,
    validate_source_lock,
)


ROOT = Path(__file__).resolve().parents[1]
TRACE_PATH = ROOT / "executable_lectures" / "traces" / "gguf-load-authored-v0.json"
LOCK_PATH = ROOT / "executable_lectures" / "source-locks" / "gguf-load-e3546c7.json"


class TraceSourceReplayValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trace = json.loads(TRACE_PATH.read_text(encoding="utf-8"))
        cls.lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))

    def test_trace_resolves_against_pinned_source_lock(self):
        self.assertEqual(validate_source_lock(self.trace, self.lock), [])

    def test_wrong_line_is_rejected(self):
        trace = copy.deepcopy(self.trace)
        trace["steps"][1]["location"]["line"] = 457
        self.assertTrue(any("is not locked" in error for error in validate_source_lock(trace, self.lock)))

    def test_wrong_function_is_rejected(self):
        trace = copy.deepcopy(self.trace)
        trace["steps"][0]["location"]["function"] = "gguf_init_from_file"
        self.assertTrue(any("is not locked" in error for error in validate_source_lock(trace, self.lock)))

    def test_lock_line_hash_is_recomputed(self):
        lock = copy.deepcopy(self.lock)
        lock["files"][0]["anchors"][0]["line_text"] += " "
        self.assertTrue(any("hash mismatch" in error for error in validate_source_lock(self.trace, lock)))

    def test_call_stack_frames_must_also_resolve(self):
        trace = copy.deepcopy(self.trace)
        trace["steps"][2]["call_stack"][0]["line"] = 452
        self.assertTrue(any("call_stack[0] is not locked" in error for error in validate_source_lock(trace, self.lock)))

    def test_navigation_is_bounded_and_reversible(self):
        self.assertEqual(replay_step_index(0, "previous", 3), 0)
        self.assertEqual(replay_step_index(0, "next", 3), 1)
        self.assertEqual(replay_step_index(1, "previous", 3), 0)
        self.assertEqual(replay_step_index(2, "next", 3), 2)
        self.assertEqual(replay_step_index(1, "first", 3), 0)
        self.assertEqual(replay_step_index(1, "last", 3), 2)

    def test_static_replay_is_deterministic_with_missing_optional_arrays(self):
        trace = copy.deepcopy(self.trace)
        for step in trace["steps"]:
            step.pop("runtime_objects", None)
            step.pop("tensor_shapes", None)
            step.pop("memory_events", None)
            step.pop("figures", None)
        first = static_replay(trace)
        second = static_replay(trace)
        self.assertEqual(first, second)
        self.assertEqual([item["sequence"] for item in first], [0, 1, 2])
        self.assertEqual(validate_source_lock(trace, self.lock), [])


if __name__ == "__main__":
    unittest.main()
