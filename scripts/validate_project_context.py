#!/usr/bin/env python3
"""Validate the durable context required by scheduled research runs."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    ROOT / "README.md",
    ROOT / "docs/reference/project-state.md",
    ROOT / "docs/reference/research-log.md",
    ROOT / "docs/reference/research-ledger.md",
    ROOT / "docs/roadmap.md",
    ROOT / "scripts/start_scheduled_run.sh",
    ROOT / ".github/workflows/pages.yml",
    ROOT / ".github/workflows/hourly-context-check.yml",
    ROOT / ".github/workflows/refresh-source-index.yml",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def main() -> int:
    errors = 0
    for path in REQUIRED:
        if not path.is_file():
            fail(f"missing required file: {path.relative_to(ROOT)}")
            errors += 1
        elif path.stat().st_size == 0:
            fail(f"empty required file: {path.relative_to(ROOT)}")
            errors += 1

    readme_path = ROOT / "README.md"
    if readme_path.is_file():
        readme = readme_path.read_text(encoding="utf-8")
        start = "<!-- SCHEDULED-RUN-INSTRUCTIONS:START -->"
        end = "<!-- SCHEDULED-RUN-INSTRUCTIONS:END -->"
        if start not in readme or end not in readme:
            fail("README scheduled-run instruction markers are missing")
            errors += 1
        elif readme.index(start) > readme.index(end):
            fail("README scheduled-run instruction markers are reversed")
            errors += 1

        required_mentions = [
            "docs/reference/project-state.md",
            "docs/reference/research-log.md",
            "docs/reference/research-ledger.md",
            "logs/research/",
            "scripts/start_scheduled_run.sh",
        ]
        for mention in required_mentions:
            if mention not in readme:
                fail(f"README does not mention required context location: {mention}")
                errors += 1

    state_path = ROOT / "docs/reference/project-state.md"
    if state_path.is_file():
        state = state_path.read_text(encoding="utf-8")
        for heading in ("Source baseline", "Active milestone", "Immediate next task", "Known blockers and caveats"):
            if not re.search(rf"^## {re.escape(heading)}\s*$", state, re.MULTILINE):
                fail(f"project state is missing heading: {heading}")
                errors += 1

    if errors:
        print(f"Context validation failed with {errors} error(s).", file=sys.stderr)
        return 1

    print("Context validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
