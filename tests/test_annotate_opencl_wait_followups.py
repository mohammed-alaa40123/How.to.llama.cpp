from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "annotate_opencl_wait_followups.py"
SPEC = importlib.util.spec_from_file_location("annotate_opencl_wait_followups", SCRIPT)
assert SPEC and SPEC.loader
annotator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(annotator)


class OpenCLWaitFollowupTests(unittest.TestCase):
    def test_marks_immediate_same_queue_blocking_read(self) -> None:
        source = """\
void readback() {
    CL_CHECK(clWaitForEvents(1, &evt));
    CL_CHECK(clEnqueueReadBuffer(queue, buffer, CL_TRUE, 0, size, dst, 0, nullptr, nullptr));
}
"""
        self.assertEqual(
            annotator.classify_wait_followups(source),
            [
                {
                    "event": "evt",
                    "wait_line": 2,
                    "followed_by_same_queue_blocking_read": True,
                    "read_line": 3,
                }
            ],
        )

    def test_rejects_nonblocking_or_other_queue_read(self) -> None:
        source = """\
clWaitForEvents(1, &first);
clEnqueueReadBuffer(queue, buffer, CL_FALSE, 0, size, dst, 0, nullptr, nullptr);
clWaitForEvents(1, &second);
clEnqueueReadBuffer(peer_queue, buffer, CL_TRUE, 0, size, dst, 0, nullptr, nullptr);
"""
        records = annotator.classify_wait_followups(source)
        self.assertEqual(
            [item["followed_by_same_queue_blocking_read"] for item in records],
            [False, False],
        )

    def test_requires_immediate_following_statement(self) -> None:
        source = """\
clWaitForEvents(1, &evt);
clReleaseMemObject(temp);
clEnqueueReadBuffer(queue, buffer, CL_TRUE, 0, size, dst, 0, nullptr, nullptr);
"""
        record = annotator.classify_wait_followups(source)[0]
        self.assertFalse(record["followed_by_same_queue_blocking_read"])
        self.assertNotIn("read_line", record)

    def test_ignores_comments_and_literals(self) -> None:
        source = """\
clWaitForEvents(1, &evt);
// clEnqueueReadBuffer(queue, buffer, CL_TRUE, 0, size, dst, 0, nullptr, nullptr);
const char * text = "clEnqueueReadBuffer(queue, buffer, CL_TRUE, 0, size, dst, 0, nullptr, nullptr)";
"""
        record = annotator.classify_wait_followups(source)[0]
        self.assertFalse(record["followed_by_same_queue_blocking_read"])

    def test_annotates_only_unmatched_followup_counts(self) -> None:
        source = """\
clWaitForEvents(1, &released);
clReleaseEvent(released);
clWaitForEvents(1, &readback);
clEnqueueReadBuffer(queue, buffer, CL_TRUE, 0, size, dst, 0, nullptr, nullptr);
clWaitForEvents(1, &other);
clReleaseMemObject(temp);
"""
        report = {
            "simple_waited_events": [
                {"event": "released", "wait_line": 1, "status": "released_in_scope"},
                {"event": "readback", "wait_line": 3, "status": "unmatched_in_scope"},
                {"event": "other", "wait_line": 5, "status": "unmatched_in_scope"},
            ]
        }
        annotated = annotator.annotate_report(report, source)
        self.assertEqual(
            annotated["simple_waited_event_followup_counts"],
            {
                "unmatched_followed_by_same_queue_blocking_read": 1,
                "other_unmatched": 1,
            },
        )
        self.assertTrue(annotated["simple_waited_events"][1]["followed_by_same_queue_blocking_read"])
        self.assertFalse(annotated["simple_waited_events"][2]["followed_by_same_queue_blocking_read"])


if __name__ == "__main__":
    unittest.main()
