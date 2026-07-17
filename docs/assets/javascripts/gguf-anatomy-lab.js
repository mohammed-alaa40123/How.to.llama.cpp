(() => {
  "use strict";
  const UINT32 = 4, STRING = 8, ARRAY = 9, F32 = 0;

  class Reader {
    constructor(bytes) {
      this.bytes = bytes;
      this.view = new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength);
      this.offset = 0;
    }
    require(size) {
      if (!Number.isInteger(size) || size < 0 || this.offset + size > this.bytes.byteLength) {
        throw new Error(`truncated GGUF at byte ${this.offset}: need ${size} bytes`);
      }
    }
    u32() { this.require(4); const v = this.view.getUint32(this.offset, true); this.offset += 4; return v; }
    u64() {
      this.require(8); const v = this.view.getBigUint64(this.offset, true); this.offset += 8;
      if (v > BigInt(Number.MAX_SAFE_INTEGER)) throw new Error("fixture integer exceeds browser-safe range");
      return Number(v);
    }
    string() {
      const length = this.u64(); this.require(length);
      const value = new TextDecoder("utf-8", { fatal: true }).decode(this.bytes.subarray(this.offset, this.offset + length));
      this.offset += length; return value;
    }
  }

  const align = (value, alignment) => value + ((alignment - value % alignment) % alignment);
  const decode = (encoded) => Uint8Array.from(atob(encoded), (char) => char.charCodeAt(0));

  function parseFixture(bytes) {
    const reader = new Reader(bytes);
    const magic = String.fromCharCode(...bytes.subarray(0, 4)); reader.offset = 4;
    if (magic !== "GGUF") throw new Error("invalid GGUF magic");
    const version = reader.u32(), tensorCount = reader.u64(), metadataCount = reader.u64();
    if (version !== 3) throw new Error(`unsupported teaching fixture version: ${version}`);
    if (tensorCount > 16 || metadataCount > 64) throw new Error("fixture collection bound exceeded");

    const metadata = {};
    for (let i = 0; i < metadataCount; i += 1) {
      const key = reader.string(), type = reader.u32();
      if (type === UINT32) metadata[key] = reader.u32();
      else if (type === STRING) metadata[key] = reader.string();
      else if (type === ARRAY) {
        const elementType = reader.u32(), length = reader.u64();
        if (elementType !== STRING || length > 16) throw new Error("unsupported fixture array");
        metadata[key] = Array.from({ length }, () => reader.string());
      } else throw new Error(`unsupported fixture metadata type: ${type}`);
    }

    const alignment = metadata["general.alignment"] ?? 32;
    if (!Number.isInteger(alignment) || alignment < 8 || alignment % 8 !== 0) throw new Error("invalid general.alignment");
    const tensors = [];
    for (let i = 0; i < tensorCount; i += 1) {
      const name = reader.string(), dimensionsCount = reader.u32();
      if (dimensionsCount < 1 || dimensionsCount > 4) throw new Error(`invalid dimensions for ${name}`);
      const dimensions = Array.from({ length: dimensionsCount }, () => reader.u64());
      const type = reader.u32(), relativeOffset = reader.u64();
      if (type !== F32) throw new Error(`unsupported fixture tensor type for ${name}`);
      if (relativeOffset % alignment !== 0) throw new Error(`misaligned tensor offset for ${name}`);
      const size = dimensions.reduce((product, dimension) => product * dimension, 1) * 4;
      tensors.push({ name, dimensions, type: "F32", relative_offset: relativeOffset, size });
    }

    const dataOffset = align(reader.offset, alignment);
    tensors.forEach((tensor) => {
      tensor.absolute_offset = dataOffset + tensor.relative_offset;
      tensor.end_offset = tensor.absolute_offset + tensor.size - 1;
      if (tensor.end_offset >= bytes.byteLength) throw new Error(`tensor range exceeds file for ${tensor.name}`);
    });
    return { format: magic, version, tensor_count: tensorCount, metadata_count: metadataCount, metadata, alignment, data_offset: dataOffset, file_size: bytes.byteLength, tensors };
  }

  function canonical(value) {
    return {
      format: value.format, version: value.version, tensor_count: value.tensor_count,
      metadata_count: value.metadata_count, metadata: value.metadata, alignment: value.alignment,
      data_offset: value.data_offset, file_size: value.file_size,
      tensors: value.tensors.map(({ name, dimensions, type, relative_offset, absolute_offset, size }) => ({ name, dimensions, type, relative_offset, absolute_offset, size }))
    };
  }

  function render(output, result) {
    output.replaceChildren();
    const summary = document.createElement("p");
    summary.textContent = `${result.format} v${result.version}; ${result.metadata_count} metadata records; ${result.tensor_count} tensors; data starts at byte ${result.data_offset}.`;
    output.appendChild(summary);
    const table = document.createElement("table");
    table.innerHTML = "<thead><tr><th scope='col'>Tensor</th><th scope='col'>Shape</th><th scope='col'>Type</th><th scope='col'>Relative offset</th><th scope='col'>Absolute byte range</th></tr></thead>";
    const body = document.createElement("tbody");
    result.tensors.forEach((tensor) => {
      const row = document.createElement("tr");
      [tensor.name, `[${tensor.dimensions.join(", ")}]`, tensor.type, tensor.relative_offset, `${tensor.absolute_offset}–${tensor.end_offset}`].forEach((value) => {
        const cell = document.createElement("td"); cell.textContent = String(value); row.appendChild(cell);
      });
      body.appendChild(row);
    });
    table.appendChild(body); output.appendChild(table);
  }

  document.querySelectorAll(".gguf-lab").forEach((root) => {
    const button = root.querySelector("[data-gguf-run]"), status = root.querySelector("[data-gguf-status]"), output = root.querySelector("[data-gguf-output]");
    if (!button || !status || !output) return;
    button.addEventListener("click", async () => {
      button.disabled = true; status.textContent = "Parsing bounded browser fixture…";
      try {
        const response = await fetch(root.dataset.payload, { cache: "no-store" });
        if (!response.ok) throw new Error(`payload request failed: ${response.status}`);
        const payload = await response.json(), bytes = decode(payload.fixture.data);
        if (bytes.byteLength !== payload.fixture.byte_length) throw new Error("fixture byte length mismatch");
        const result = parseFixture(bytes);
        if (JSON.stringify(canonical(result)) !== JSON.stringify(canonical(payload.golden))) throw new Error("browser parse disagrees with Python golden output");
        render(output, result);
        status.textContent = "Parse complete. Browser-derived result matches the Python golden record.";
      } catch (error) {
        output.replaceChildren(); status.textContent = `Parser failed: ${error.message}`;
      } finally { button.disabled = false; }
    });
  });
})();
