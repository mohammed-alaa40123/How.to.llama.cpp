import unittest

from scripts.apply_opencl_event_release_fix import apply_release_fix


class ApplyOpenCLEventReleaseFixTests(unittest.TestCase):
    def test_inserts_release_after_each_unmatched_wait(self):
        source = (
            "void f() {\n"
            "    cl_event first;\n"
            "    CL_CHECK(clWaitForEvents(1, &first));\n"
            "    use();\n"
            "    CL_CHECK(clWaitForEvents(1, &second));\n"
            "}\n"
        )
        report = {
            "simple_waited_events": [
                {"event": "first", "wait_line": 3, "status": "unmatched_in_scope"},
                {"event": "second", "wait_line": 5, "status": "unmatched_in_scope"},
            ]
        }

        patched, count = apply_release_fix(source, report)

        self.assertEqual(count, 2)
        self.assertIn(
            "CL_CHECK(clWaitForEvents(1, &first));\n"
            "    CL_CHECK(clReleaseEvent(first));\n"
            "    use();",
            patched,
        )
        self.assertIn(
            "CL_CHECK(clWaitForEvents(1, &second));\n"
            "    CL_CHECK(clReleaseEvent(second));",
            patched,
        )

    def test_ignores_already_released_records(self):
        source = "CL_CHECK(clWaitForEvents(1, &evt));\n"
        report = {
            "simple_waited_events": [
                {"event": "evt", "wait_line": 1, "status": "released_in_scope"}
            ]
        }

        with self.assertRaisesRegex(ValueError, "no unmatched"):
            apply_release_fix(source, report)

    def test_rejects_stale_wait_line(self):
        source = "CL_CHECK(clWaitForEvents(1, &actual));\n"
        report = {
            "simple_waited_events": [
                {"event": "expected", "wait_line": 1, "status": "unmatched_in_scope"}
            ]
        }

        with self.assertRaisesRegex(ValueError, "does not contain expected call"):
            apply_release_fix(source, report)

    def test_rejects_duplicate_records_for_one_line(self):
        source = "CL_CHECK(clWaitForEvents(1, &evt));\n"
        report = {
            "simple_waited_events": [
                {"event": "evt", "wait_line": 1, "status": "unmatched_in_scope"},
                {"event": "evt", "wait_line": 1, "status": "unmatched_in_scope"},
            ]
        }

        with self.assertRaisesRegex(ValueError, "same wait line"):
            apply_release_fix(source, report)


if __name__ == "__main__":
    unittest.main()
