#!/usr/bin/env python3
"""Generate and validate the project-owned synthetic GGUF v3 teaching fixture."""
from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path
from typing import Any

MAGIC = b"GGUF"
VERSION = 3
ALIGNMENT = 32
GGUF_TYPE_UINT32 = 4
GGUF_TYPE_STRING = 8
GGUF_TYPE_ARRAY = 9
GGML_TYPE_F32 = 0


def align(value: int, alignment: int = ALIGNMENT) -> int:
    return value + (-value % alignment)


def pack_string(value: str) -> bytes:
    encoded = value.encode("utf-8")
    return struct.pack("<Q", len(encoded)) + encoded


def pack_metadata(key: str, value_type: int, value: Any) -> bytes:
    out = bytearray(pack_string(key))
    out.extend(struct.pack("<I", value_type))
    if value_type == GGUF_TYPE_UINT32:
        out.extend(struct.pack("<I", value))
    elif value_type == GGUF_TYPE_STRING:
        out.extend(pack_string(value))
    elif value_type == GGUF_TYPE_ARRAY:
        element_type, values = value
        out.extend(struct.pack("<IQ", element_type, len(values)))
        if element_type != GGUF_TYPE_STRING:
            raise ValueError("fixture arrays support strings only")
        for item in values:
            out.extend(pack_string(item))
    else:
        raise ValueError(f"unsupported metadata type: {value_type}")
    return bytes(out)


def build_fixture() -> tuple[bytes, dict[str, Any]]:
    metadata = [
        ("general.architecture", GGUF_TYPE_STRING, "educational"),
        ("general.alignment", GGUF_TYPE_UINT32, ALIGNMENT),
        ("fixture.title", GGUF_TYPE_STRING, "How.to.llama.cpp GGUF anatomy"),
        ("fixture.version", GGUF_TYPE_UINT32, 1),
        ("fixture.tags", GGUF_TYPE_ARRAY, (GGUF_TYPE_STRING, ["synthetic", "non-model"])),
    ]
    tensors = [
        {"name": "demo.matrix", "dimensions": [2, 2], "type": GGML_TYPE_F32, "values": [1.0, 2.0, 3.0, 4.0]},
        {"name": "demo.vector", "dimensions": [3], "type": GGML_TYPE_F32, "values": [10.0, 20.0, 30.0]},
    ]

    tensor_offset = 0
    for tensor in tensors:
        tensor["offset"] = tensor_offset
        tensor["payload"] = struct.pack(f"<{len(tensor['values'])}f", *tensor["values"])
        tensor_offset = align(tensor_offset + len(tensor["payload"]))

    out = bytearray(MAGIC)
    out.extend(struct.pack("<IQQ", VERSION, len(tensors), len(metadata)))
    for item in metadata:
        out.extend(pack_metadata(*item))

    descriptor_offset_positions: list[int] = []
    for tensor in tensors:
        out.extend(pack_string(tensor["name"]))
        out.extend(struct.pack("<I", len(tensor["dimensions"])))
        out.extend(struct.pack(f"<{len(tensor['dimensions'])}Q", *tensor["dimensions"]))
        out.extend(struct.pack("<I", tensor["type"]))
        descriptor_offset_positions.append(len(out))
        out.extend(struct.pack("<Q", tensor["offset"]))

    data_offset = align(len(out))
    out.extend(b"\x00" * (data_offset - len(out)))
    for tensor in tensors:
        absolute = data_offset + tensor["offset"]
        if len(out) < absolute:
            out.extend(b"\x00" * (absolute - len(out)))
        out.extend(tensor["payload"])

    details = {
        "data_offset": data_offset,
        "descriptor_offset_positions": descriptor_offset_positions,
        "tensor_ranges": [
            {
                "name": tensor["name"],
                "relative_offset": tensor["offset"],
                "absolute_offset": data_offset + tensor["offset"],
                "size": len(tensor["payload"]),
            }
            for tensor in tensors
        ],
    }
    return bytes(out), details


class Reader:
    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0

    def read(self, size: int) -> bytes:
        end = self.pos + size
        if end > len(self.data):
            raise ValueError(f"truncated GGUF at byte {self.pos}: need {size} bytes")
        value = self.data[self.pos:end]
        self.pos = end
        return value

    def unpack(self, fmt: str) -> tuple[Any, ...]:
        size = struct.calcsize(fmt)
        return struct.unpack(fmt, self.read(size))

    def string(self) -> str:
        (length,) = self.unpack("<Q")
        return self.read(length).decode("utf-8")


def parse_fixture(data: bytes) -> dict[str, Any]:
    r = Reader(data)
    if r.read(4) != MAGIC:
        raise ValueError("invalid GGUF magic")
    version, tensor_count, kv_count = r.unpack("<IQQ")
    if version != VERSION:
        raise ValueError(f"unsupported fixture GGUF version: {version}")

    metadata: dict[str, Any] = {}
    for _ in range(kv_count):
        key = r.string()
        (value_type,) = r.unpack("<I")
        if value_type == GGUF_TYPE_UINT32:
            value = r.unpack("<I")[0]
        elif value_type == GGUF_TYPE_STRING:
            value = r.string()
        elif value_type == GGUF_TYPE_ARRAY:
            element_type, length = r.unpack("<IQ")
            if element_type != GGUF_TYPE_STRING:
                raise ValueError("unsupported fixture array element type")
            value = [r.string() for _ in range(length)]
        else:
            raise ValueError(f"unsupported fixture metadata type: {value_type}")
        metadata[key] = value

    alignment = metadata.get("general.alignment", 32)
    if not isinstance(alignment, int) or alignment < 8 or alignment % 8:
        raise ValueError("invalid general.alignment")

    tensors = []
    for _ in range(tensor_count):
        name = r.string()
        (n_dimensions,) = r.unpack("<I")
        if n_dimensions == 0 or n_dimensions > 4:
            raise ValueError(f"invalid dimension count for {name}: {n_dimensions}")
        dimensions = list(r.unpack(f"<{n_dimensions}Q"))
        tensor_type, offset = r.unpack("<IQ")
        if tensor_type != GGML_TYPE_F32:
            raise ValueError(f"unsupported fixture tensor type for {name}: {tensor_type}")
        if offset % alignment:
            raise ValueError(f"misaligned tensor offset for {name}: {offset}")
        element_count = 1
        for dimension in dimensions:
            element_count *= dimension
        size = element_count * 4
        tensors.append({
            "name": name,
            "dimensions": dimensions,
            "type": "F32",
            "relative_offset": offset,
            "size": size,
        })

    data_offset = align(r.pos, alignment)
    if data_offset > len(data):
        raise ValueError("tensor data begins beyond end of file")
    for tensor in tensors:
        absolute_offset = data_offset + tensor["relative_offset"]
        end = absolute_offset + tensor["size"]
        if end > len(data):
            raise ValueError(f"tensor range exceeds file for {tensor['name']}")
        tensor["absolute_offset"] = absolute_offset
        tensor["sha256"] = hashlib.sha256(data[absolute_offset:end]).hexdigest()

    return {
        "format": "GGUF",
        "version": version,
        "alignment": alignment,
        "tensor_count": tensor_count,
        "metadata_count": kv_count,
        "metadata": metadata,
        "data_offset": data_offset,
        "file_size": len(data),
        "file_sha256": hashlib.sha256(data).hexdigest(),
        "tensors": tensors,
    }


def corruption_variants(data: bytes, details: dict[str, Any]) -> dict[str, bytes]:
    bad_magic = bytearray(data)
    bad_magic[0:4] = b"NOPE"

    misaligned = bytearray(data)
    offset_position = details["descriptor_offset_positions"][1]
    struct.pack_into("<Q", misaligned, offset_position, 1)

    last_range = details["tensor_ranges"][-1]
    truncated_payload = data[: last_range["absolute_offset"] + last_range["size"] - 1]

    return {
        "bad-magic.gguf": bytes(bad_magic),
        "misaligned-offset.gguf": bytes(misaligned),
        "truncated-payload.gguf": truncated_payload,
    }


def write_outputs(root: Path) -> None:
    data, details = build_fixture()
    output_dir = root / "labs" / "fixtures" / "gguf"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "synthetic-v0.gguf").write_bytes(data)
    parsed = parse_fixture(data)
    (output_dir / "synthetic-v0.golden.json").write_text(
        json.dumps(parsed, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    corruption_dir = output_dir / "corruptions"
    corruption_dir.mkdir(exist_ok=True)
    for name, variant in corruption_variants(data, details).items():
        (corruption_dir / name).write_bytes(variant)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    data, details = build_fixture()
    parsed = parse_fixture(data)
    if args.check:
        output_dir = args.root / "labs" / "fixtures" / "gguf"
        expected = json.loads((output_dir / "synthetic-v0.golden.json").read_text(encoding="utf-8"))
        manifest = json.loads((output_dir / "synthetic-v0.manifest.json").read_text(encoding="utf-8"))
        if parsed != expected:
            raise SystemExit("synthetic GGUF golden output is stale")
        if parsed["file_sha256"] != manifest["expected_sha256"]:
            raise SystemExit("synthetic GGUF manifest checksum is stale")
        for name, variant in corruption_variants(data, details).items():
            try:
                parse_fixture(variant)
            except ValueError:
                continue
            raise SystemExit(f"corruption variant unexpectedly parsed: {name}")
        print(parsed["file_sha256"])
        return 0

    write_outputs(args.root)
    print(parsed["file_sha256"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
