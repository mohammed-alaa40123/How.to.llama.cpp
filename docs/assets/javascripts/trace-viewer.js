(() => {
  "use strict";

  const root = document.querySelector("[data-trace-viewer]");
  if (!root) return;

  const dataUrl = root.dataset.traceUrl;
  const status = root.querySelector("[data-trace-status]");
  const stepCount = root.querySelector("[data-step-count]");
  const evidence = root.querySelector("[data-evidence]");
  const source = root.querySelector("[data-source]");
  const prompt = root.querySelector("[data-prompt]");
  const summary = root.querySelector("[data-summary]");
  const details = root.querySelector("[data-details]");
  const previous = root.querySelector("[data-action='previous']");
  const next = root.querySelector("[data-action='next']");
  const transcript = root.querySelector("[data-transcript]");

  let trace = null;
  let index = 0;

  const list = (items, renderItem) => {
    if (!items || items.length === 0) return "<p>None recorded for this authored step.</p>";
    return `<ul>${items.map(renderItem).join("")}</ul>`;
  };

  const escapeHtml = (value) => String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  const renderDetails = (step) => {
    const objects = list(step.runtime_objects, (item) =>
      `<li><strong>${escapeHtml(item.object_id)}</strong> (${escapeHtml(item.type)}): ${escapeHtml(item.summary)} <em>${escapeHtml(item.evidence_kind)}</em></li>`);
    const tensors = list(step.tensor_shapes, (item) =>
      `<li><strong>${escapeHtml(item.tensor_id)}</strong>: [${item.dimensions.map(escapeHtml).join(", ")}] ${escapeHtml(item.element_type)} <em>${escapeHtml(item.evidence_kind)}</em></li>`);
    const memory = list(step.memory_events, (item) =>
      `<li><strong>${escapeHtml(item.event)}</strong>${item.bytes ? ` (${escapeHtml(item.bytes)} bytes)` : ""}: ${escapeHtml(item.summary)} <em>${escapeHtml(item.evidence_kind)}</em></li>`);
    details.innerHTML = `<h3>Runtime objects</h3>${objects}<h3>Tensor shapes</h3>${tensors}<h3>Memory events</h3>${memory}`;
  };

  const render = () => {
    const step = trace.steps[index];
    stepCount.textContent = `Step ${index + 1} of ${trace.steps.length}: ${step.phase}`;
    evidence.textContent = step.evidence_kind;
    evidence.dataset.kind = step.evidence_kind;
    source.href = step.source_url;
    source.textContent = `${step.location.file}:${step.location.line} — ${step.location.function}`;
    prompt.textContent = step.prediction_prompt || "No prediction prompt for this step.";
    summary.textContent = step.static_summary;
    renderDetails(step);
    previous.disabled = index === 0;
    next.disabled = index === trace.steps.length - 1;
    status.textContent = `Showing ${step.step_id}. Evidence kind: ${step.evidence_kind}.`;
  };

  const move = (delta) => {
    index = Math.max(0, Math.min(trace.steps.length - 1, index + delta));
    render();
  };

  previous.addEventListener("click", () => move(-1));
  next.addEventListener("click", () => move(1));
  root.addEventListener("keydown", (event) => {
    if (event.key === "ArrowLeft") {
      event.preventDefault();
      move(-1);
    } else if (event.key === "ArrowRight") {
      event.preventDefault();
      move(1);
    } else if (event.key === "Home") {
      event.preventDefault();
      index = 0;
      render();
    } else if (event.key === "End") {
      event.preventDefault();
      index = trace.steps.length - 1;
      render();
    }
  });

  fetch(dataUrl)
    .then((response) => {
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      return response.json();
    })
    .then((payload) => {
      trace = payload;
      transcript.hidden = true;
      render();
      root.focus();
    })
    .catch((error) => {
      status.textContent = `Interactive trace unavailable (${error.message}). Use the ordered transcript below.`;
      root.querySelector("[data-interactive]").hidden = true;
      transcript.hidden = false;
    });
})();
