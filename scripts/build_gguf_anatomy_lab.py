#!/usr/bin/env python3
"""Build the deterministic browser payload for Lab 1 GGUF Anatomy."""
from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from generate_synthetic_gguf import build_fixture, parse_fixture

COURSE_REVISION = "17d6da2c269df7d1e524cd4f5b94f677d90e9c32"
UPSTREAM_REVISION = "e3546c7948e3af463d0b401e6421d5a4c2faf565"


def build_payload() -> dict:
    data, _ = build_fixture()
    golden = parse_fixture(data)
    return {
        "schema_version": "0.1.0",
        "lesson_id": "lab1-gguf-anatomy-v0",
        "evidence_kind": "browser-derived",
        "source_revision": {
            "repository": "mohammed-alaa40123/How.to.llama.cpp",
            "revision": COURSE_REVISION,
            "fixture_generator": "scripts/generate_synthetic_gguf.py",
            "upstream_parser_revision": UPSTREAM_REVISION,
        },
        "fixture": {
            "encoding": "base64",
            "byte_length": len(data),
            "sha256": golden["file_sha256"],
            "data": base64.b64encode(data).decode("ascii"),
        },
        "golden": golden,
        "checkpoints": [
            {
                "id": "graph-storage",
                "predict": "Does this GGUF contain an executable GGML graph?",
                "discover": "Inspect the parsed sections: header, metadata, tensor descriptors, alignment padding, and tensor payload bytes.",
                "explain": "No. This fixture stores metadata and tensor bytes; graph construction is a later native runtime activity.",
            },
            {
                "id": "tensor-offsets",
                "predict": "Is demo.vector stored immediately after demo.matrix?",
                "discover": "Compare demo.matrix end byte 400 with demo.vector absolute offset 416.",
                "explain": "No. The second tensor begins at the next 32-byte-aligned relative offset, leaving padding bytes.",
            },
            {
                "id": "mapping-residency",
                "predict": "Does parsing or mapping a tensor descriptor prove all tensor pages are physically resident?",
                "discover": "The browser parser reads a 428-byte in-memory teaching fixture and reports file offsets only.",
                "explain": "No. File layout and address mapping do not prove native OS page residency; this browser result is not a native mmap trace.",
            },
        ],
    }


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    output = root / "docs/assets/data/gguf-anatomy-v0.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(build_payload(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
