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
    def test_extracts_creation_retention_completion_and_release_in_source_order(self) -> None:
        source = """\
cl_context = clCreateContext(properties, 1, &device, nullptr, nullptr, &error);
queue = clCreateCommandQueue(cl_context, device, 0, &error);
queue2 = clCreateCommandQueueWithProperties(cl_context, device, properties, &error);
clRetainContext(cl_context);
clRetainCommandQueue(queue);
CL_CHECK(clFinish(queue));
clReleaseKernel(kernel);
clReleaseProgram(program);
clReleaseCommandQueue(queue);
clReleaseContext(cl_context);
"""
        self.assertEqual(
            extractor.extract_opencl_lifecycle_calls(source),
            [
                {"name": "clCreateContext", "line": 1},
                {"name": "clCreateCommandQueue", "line": 2},
                {"name": "clCreateCommandQueueWithProperties", "line": 3},
                {"name": "clRetainContext", "line": 4},
                {"name": "clRetainCommandQueue", "line": 5},
                {"name": "clFinish", "line": 6},
                {"name": "clReleaseKernel", "line": 7},
                {"name": "clReleaseProgram", "line": 8},
                {"name": "clReleaseCommandQueue", "line": 9},
                {"name": "clReleaseContext", "line": 10},
            ],
        )

    def test_extracts_context_from_type(self) -> None:
        source = "context = clCreateContextFromType(properties, CL_DEVICE_TYPE_GPU, nullptr, nullptr, &error);\n"
        self.assertEqual(
            extractor.extract_opencl_lifecycle_calls(source),
            [{"name": "clCreateContextFromType", "line": 1}],
        )

    def test_ignores_similar_identifiers_without_a_call(self) -> None:
        source = """\
auto clFinishStatus = 0;
const char * name = "clReleaseContext";
release_clReleaseProgram(program);
create_clCreateContext(properties);
"""
        self.assertEqual(extractor.extract_opencl_lifecycle_calls(source), [])

    def test_ignores_calls_inside_comments_and_literals(self) -> None:
        source = """\
// clCreateCommandQueue(context, device, 0, &error);
/* clReleaseContext(context);
   clReleaseProgram(program); */
const char * text = "clRetainContext(context)";
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

    def test_includes_bounded_original_source_context(self) -> None:
        source = """\
void teardown() {
    // completion before releases
    CL_CHECK(clFinish(queue));
    clReleaseCommandQueue(queue);
    clReleaseContext(context);
}
"""
        self.assertEqual(
            extractor.extract_opencl_lifecycle_calls(source, context_lines=1),
            [
                {
                    "name": "clFinish",
                    "line": 3,
                    "context": {
                        "start_line": 2,
                        "end_line": 4,
                        "text": "    // completion before releases\n"
                        "    CL_CHECK(clFinish(queue));\n"
                        "    clReleaseCommandQueue(queue);",
                    },
                },
                {
                    "name": "clReleaseCommandQueue",
                    "line": 4,
                    "context": {
                        "start_line": 3,
                        "end_line": 5,
                        "text": "    CL_CHECK(clFinish(queue));\n"
                        "    clReleaseCommandQueue(queue);\n"
                        "    clReleaseContext(context);",
                    },
                },
                {
                    "name": "clReleaseContext",
                    "line": 5,
                    "context": {
                        "start_line": 4,
                        "end_line": 6,
                        "text": "    clReleaseCommandQueue(queue);\n"
                        "    clReleaseContext(context);\n}",
                    },
                },
            ],
        )

    def test_context_is_clamped_at_file_boundaries(self) -> None:
        source = "clFlush(queue);\nclReleaseContext(context);\n"
        calls = extractor.extract_opencl_lifecycle_calls(source, context_lines=3)
        expected_context = {
            "start_line": 1,
            "end_line": 2,
            "text": "clFlush(queue);\nclReleaseContext(context);",
        }
        self.assertEqual(calls[0]["context"], expected_context)
        self.assertEqual(calls[1]["context"], expected_context)

    def test_rejects_negative_context_radius(self) -> None:
        with self.assertRaisesRegex(ValueError, "non-negative"):
            extractor.extract_opencl_lifecycle_calls("clFinish(queue);", context_lines=-1)


if __name__ == "__main__":
    unittest.main()
