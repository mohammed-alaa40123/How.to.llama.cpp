# Interactive inference workflow

The prototype below provides a clickable, animated path through a minimal decoder inference loop. Select a node to view its role, representative functions/files, state, and memory implications.

<div class="workflow-frame">
<iframe src="../../assets/interactive/inference-flow.html" title="Interactive llama.cpp inference workflow" loading="lazy"></iframe>
</div>

## Prototype limitations

- It currently presents a minimal decoder-centric flow.
- Exact symbol links are pinned, but the detail text remains an initial architecture summary.
- Backend-specific lanes, microbatch variants, encoder paths, recurrent memory, MoE, speculative decoding, and multi-sequence execution are future states.
- The final implementation will load nodes and edges from versioned JSON so documentation pages and the animation share the same source facts.
