from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "classify_opencl_set_tensor_waits.py"
SPEC = importlib.util.spec_from_file_location("classify_opencl_set_tensor_waits", SCRIPT)
assert SPEC and SPEC.loader
classifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(classifier)


class ClassifyOpenCLSetTensorWaitsTests(unittest.TestCase):
    def test_classifies_release_and_scope_exit(self) -> None:
        source = """\
static void set_tensor() {
    {
        clWaitForEvents(1, &evt);
        clReleaseMemObject(data_device);
    }
    {
        clWaitForEvents(1, &evt);
    }
}
"""
        report = {
            "source": "fixture.cpp",
            "simple_waited_events": [
                {"event": "evt", "wait_line": 3, "scope_end_line": 5, "status": "unmatched_in_scope", "followed_by_same_queue_blocking_read": False},
                {"event": "evt", "wait_line": 7, "scope_end_line": 8, "status": "unmatched_in_scope", "followed_by_same_queue_blocking_read": False},
            ],
        }
        result = classifier.classify_waits(source, report)
        self.assertEqual(result["classified_wait_count"], 2)
        self.assertEqual(result["counts"], {"nested_scope_exit": 1, "temporary_upload_buffer_release": 1})
        self.assertEqual(result["records"][0]["enclosing_function"], "set_tensor")

    def test_skips_released_and_blocking_read_records(self) -> None:
        source = """\
static void set_tensor() {
    clWaitForEvents(1, &evt);
    clEnqueueReadBuffer(queue, x, CL_TRUE, 0, 1, dst, 0, NULL, NULL);
}
"""
        report = {
            "simple_waited_events": [
                {"event": "evt", "wait_line": 2, "scope_end_line": 4, "status": "released_in_scope", "followed_by_same_queue_blocking_read": False},
                {"event": "evt", "wait_line": 2, "scope_end_line": 4, "status": "unmatched_in_scope", "followed_by_same_queue_blocking_read": True},
            ]
        }
        result = classifier.classify_waits(source, report)
        self.assertEqual(result["classified_wait_count"], 0)
        self.assertEqual(result["counts"], {})

    def test_reports_other_followup(self) -> None:
        source = """\
static void set_tensor() {
    clWaitForEvents(1, &evt);
    tensor->extra = extra;
}
"""
        report = {"simple_waited_events": [{"event": "evt", "wait_line": 2, "scope_end_line": 4, "status": "unmatched_in_scope", "followed_by_same_queue_blocking_read": False}]}
        result = classifier.classify_waits(source, report)
        self.assertEqual(result["counts"], {"other": 1})


if __name__ == "__main__":
    unittest.main()
