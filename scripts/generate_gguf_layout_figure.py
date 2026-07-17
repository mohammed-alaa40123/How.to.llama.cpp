#!/usr/bin/env python3
"""Generate a deterministic SVG layout from the synthetic GGUF golden record."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


def build_svg(data: dict[str, Any]) -> str:
    total = int(data["file_size"])
    data_offset = int(data["data_offset"])
    alignment = int(data["alignment"])
    tensors = data["tensors"]
    width, height = 960, 540
    x0, bar_width = 48, 864

    def esc(value: Any) -> str:
        return html.escape(str(value), quote=True)

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">Synthetic GGUF v3 layout</title>',
        f'<desc id="desc">A deterministic layout of a {total}-byte synthetic GGUF file: header and metadata, tensor descriptors, alignment padding, and two bounded F32 tensor payloads.</desc>',
        '<style>text{font-family:system-ui,sans-serif;fill:#111}.label{font-size:16px;font-weight:700}.small{font-size:13px}.box{fill:#fff;stroke:#111;stroke-width:2}.muted{fill:#f3f4f6}.payload{fill:#e5e7eb}.guide{stroke:#111;stroke-width:1;stroke-dasharray:5 5}</style>',
        '<rect class="box" x="24" y="24" width="912" height="492" rx="12"/>',
        '<text class="label" x="48" y="58">Project-owned synthetic GGUF fixture</text>',
        f'<text class="small" x="48" y="82">GGUF v{data["version"]} · {total} bytes · {alignment}-byte alignment · non-model teaching fixture</text>',
    ]

    for label, start, end, css_class in (
        ("Header + metadata", 0, data_offset, "muted"),
        ("Tensor data", data_offset, total, "payload"),
    ):
        x = x0 + bar_width * start / total
        section_width = bar_width * (end - start) / total
        lines.extend(
            [
                f'<rect class="box {css_class}" x="{x:.2f}" y="110" width="{section_width:.2f}" height="54"/>',
                f'<text class="small" x="{x + 8:.2f}" y="133">{esc(label)}</text>',
                f'<text class="small" x="{x + 8:.2f}" y="152">bytes {start}–{end - 1}</text>',
            ]
        )

    lines.extend(
        [
            '<text class="label" x="48" y="205">Structured records</text>',
            f'<text class="small" x="48" y="230">Metadata entries: {data["metadata_count"]}</text>',
            f'<text class="small" x="48" y="252">Tensor descriptors: {data["tensor_count"]}</text>',
            f'<text class="small" x="48" y="274">Tensor payload begins at aligned byte {data_offset}</text>',
            '<line class="guide" x1="48" y1="302" x2="912" y2="302"/>',
            '<text class="label" x="48" y="330">Tensor payload ranges</text>',
            '<rect class="box" x="48" y="354" width="864" height="72"/>',
        ]
    )

    payload_size = total - data_offset
    for tensor in tensors:
        start = int(tensor["absolute_offset"])
        end = start + int(tensor["size"])
        x = 48 + 864 * (start - data_offset) / payload_size
        tensor_width = max(2.0, 864 * int(tensor["size"]) / payload_size)
        lines.extend(
            [
                f'<rect class="payload" stroke="#111" stroke-width="2" x="{x:.2f}" y="354" width="{tensor_width:.2f}" height="72"/>',
                f'<text class="small" x="{x + 6:.2f}" y="379">{esc(tensor["name"])}</text>',
                f'<text class="small" x="{x + 6:.2f}" y="401">{esc(tensor["type"])} {esc(tensor["dimensions"])} · bytes {start}–{end - 1}</text>',
            ]
        )

    lines.extend(
        [
            '<text class="small" x="48" y="462">Verified from labs/fixtures/gguf/synthetic-v0.golden.json; no model weights or native inference are represented.</text>',
            '<text class="small" x="48" y="486">Authority boundary: deterministic byte layout only. Runtime graph construction is outside this figure.</text>',
            '</svg>',
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("labs/fixtures/gguf/synthetic-v0.golden.json"))
    parser.add_argument("--output", type=Path, default=Path("media/generated/gguf-layout-deterministic-v0.svg"))
    args = parser.parse_args()

    data = json.loads(args.input.read_text(encoding="utf-8"))
    svg = build_svg(data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(svg, encoding="utf-8", newline="\n")
    print(f"Generated {args.output} ({len(svg.encode('utf-8'))} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
