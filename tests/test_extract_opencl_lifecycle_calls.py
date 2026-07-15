from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "extract_opencl_lifecycle_calls.py"
SPEC = importlib.util.spec_from_file_location("extract_opencl_lifecycle_calls", SCRIPT)
assert SPEC and SPEC.loader
extractor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(extractor)


class OpenCLLifecycleCallExtractorTests(unittest.TestCase):
    def test_extracts_completion_and_release_calls_in_source_order(self) -> None:
        source = """\
CL_CHECK(clFinish(queue));
clReleaseKernel(kernel);
clReleaseProgram(program);
clReleaseCommandQueue(queue);
clReleaseContext(context);
"""
        self.assertEqual(
            extractor.extract_opencl_lifecycle_calls(source),
            [
                {"name": "clFinish", "line": 1},
                {"name": "clReleaseKernel", "line": 2},
                {"name": "clReleaseProgram", "line": 3},
                {"name": "clReleaseCommandQueue", "line": 4},
                {"name": "clReleaseContext", "line": 5},
            ],
        )

    def test_ignores_similar_identifiers_without_a_call(self) -> None:
        source = """\
auto clFinishStatus = 0;
const char * name = "clReleaseContext";
release_clReleaseProgram(program);
"""
        self.assertEqual(extractor.extract_opencl_lifecycle_calls(source), [])

    def test_ignores_calls_inside_comments_and_literals(self) -> None:
        source = """\
// clFinish(queue);
/* clReleaseContext(context);
   clReleaseProgram(program); */
const char * text = "clReleaseKernel(kernel)";
const char escaped = '\\'';
clFlush(queue);
"""
        self.assertEqual(
            extractor.extract_opencl_lifecycle_calls(source),
            [{"name": "clFlush", "line": 6}],
        )

    def test_preserves_lines_across_multiline_comments_and_literals(self) -> None:
        source = """\
/* hidden clWaitForEvents(1, &event);
   hidden clReleaseEvent(event); */
const char * text = "ignored clReleaseMemObject(buffer)";
clReleaseMemObject(buffer);
"""
        self.assertEqual(
            extractor.extract_opencl_lifecycle_calls(source),
            [{"name": "clReleaseMemObject", "line": 4}],
        )

    def test_covers_event_buffer_flush_and_wait_calls(self) -> None:
        source = """\
clFlush(queue);
clWaitForEvents(1, &event);
clReleaseEvent(event);
clReleaseMemObject(buffer);
"""
        self.assertEqual(
            extractor.extract_opencl_lifecycle_calls(source),
            [
                {"name": "clFlush", "line": 1},
                {"name": "clWaitForEvents", "line": 2},
                {"name": "clReleaseEvent", "line": 3},
                {"name": "clReleaseMemObject", "line": 4},
            ],
        )


if __name__ == "__main__":
    unittest.main()
