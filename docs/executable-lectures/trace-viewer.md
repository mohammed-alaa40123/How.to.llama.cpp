# Executable Lecture 0: authored GGUF loading trace

## Learning contract

| Field | Declaration |
|---|---|
| Intended learner | A learner who can read C/C++ but struggles to connect source locations, state descriptions, and explanatory claims |
| Prerequisite | Basic C/C++ reading, files versus memory, and the GGUF fixture overview |
| Learning objective | Trace three bounded GGUF-loading steps while distinguishing authored examples from source-derived evidence |
| Predicted misconception | Every displayed object or memory event was captured from a native llama.cpp run |
| Executable action | Predict the evidence type, then move forward and backward through pinned source locations and inspect the revealed state |
| Observable output | Current source anchor, evidence label, prediction prompt, explanation, runtime-object summary, tensor shapes, and memory events |
| Formative assessment | Before revealing each step, state whether the evidence is authored, source-derived, or native-captured and explain why |
| Source revision | `ggml-org/llama.cpp` at `e3546c7948e3af463d0b401e6421d5a4c2faf565` |
| Validation method | Trace schema validation, immutable source-anchor validation, deterministic viewer-data replay, and static shell tests |
| Accessibility fallback | Arrow-key/Home/End navigation, visible buttons, live text status, no motion requirement, and the complete ordered transcript below |

!!! warning "Evidence boundary"
    This is an **authored/source-derived teaching trace**, not a native execution capture. Empty runtime collections mean “not recorded for this authored step,” not that the native runtime contains no such state.

<style>
.trace-viewer { border: 1px solid var(--md-default-fg-color--lightest); border-radius: .4rem; padding: 1rem; }
.trace-viewer:focus { outline: .15rem solid var(--md-accent-fg-color); outline-offset: .15rem; }
.trace-controls { display: flex; gap: .5rem; flex-wrap: wrap; margin: .75rem 0; }
.trace-evidence { display: inline-block; padding: .15rem .45rem; border: 1px solid currentColor; border-radius: 999px; font-weight: 700; }
.trace-grid { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 1rem; }
@media (max-width: 48rem) { .trace-grid { grid-template-columns: 1fr; } }
@media (prefers-reduced-motion: reduce) { .trace-viewer * { scroll-behavior: auto !important; transition: none !important; } }
</style>

<div class="trace-viewer" data-trace-viewer data-trace-url="../../assets/data/gguf-load-authored-v0.viewer.json" tabindex="0" aria-label="Authored GGUF loading trace viewer">
  <p data-trace-status role="status" aria-live="polite">Loading the trace. The ordered transcript remains available below.</p>
  <div data-interactive>
    <div class="trace-controls" aria-label="Trace navigation controls">
      <button type="button" data-action="previous">Previous step</button>
      <button type="button" data-action="next">Next step</button>
      <span data-step-count></span>
    </div>
    <p><strong>Evidence:</strong> <span class="trace-evidence" data-evidence></span></p>
    <p><strong>Pinned source:</strong> <a data-source target="_blank" rel="noopener noreferrer"></a></p>
    <div class="trace-grid">
      <section aria-labelledby="trace-predict-heading">
        <h2 id="trace-predict-heading">Predict</h2>
        <p data-prompt></p>
        <h2>Explain</h2>
        <p data-summary></p>
      </section>
      <section aria-labelledby="trace-state-heading">
        <h2 id="trace-state-heading">Revealed state</h2>
        <div data-details></div>
      </section>
    </div>
  </div>

  <section data-transcript aria-labelledby="trace-transcript-heading">
    <h2 id="trace-transcript-heading">Ordered static transcript</h2>
    <ol>
      <li><strong>Entry — authored-example.</strong> At `ggml/src/gguf.cpp:451`, begin at `gguf_init_from_reader`. The synthetic fixture and bounded read are teaching representations, not captured execution.</li>
      <li><strong>Header — source-derived.</strong> At line 480, inspect fixture-derived header and tensor descriptors. Descriptor parsing does not prove physical page residency or inference readiness.</li>
      <li><strong>Layout — source-derived.</strong> At line 757, derive the 32-byte-aligned tensor-data region beginning at byte 384 and containing 44 payload bytes.</li>
    </ol>
  </section>
</div>

## Keyboard operation

Focus the viewer and use <kbd>Left</kbd>/<kbd>Right</kbd> to step, <kbd>Home</kbd> for the first step, and <kbd>End</kbd> for the last step. Buttons remain available for pointer, touch, switch, and keyboard activation.

## What this prototype does not prove

- It does not execute llama.cpp in the browser.
- It does not claim that the displayed runtime objects were captured natively.
- It does not yet establish that the viewer improves code-tracing accuracy over a static source-and-text baseline.
- It does not replace independent technical review of the selected source anchors.
