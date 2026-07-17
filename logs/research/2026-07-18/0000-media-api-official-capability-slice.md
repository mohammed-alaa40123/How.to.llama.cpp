# Official generative-media capability slice

**Run date:** 2026-07-18 00:00 Africa/Cairo  
**Starting commit:** `b2a39213615e39852cbfd90f23296a493c8e63a2`  
**Assignment:** Literature and Venue Scout — verify the next distinct media-pipeline dependency using current official sources.  
**Learner outcome protected:** technical diagrams and runtime explanations remain source-linked and deterministic even when optional generated illustrations, narration or video are added.

## Scope

Reviewed current official documentation for:

- OpenAI image generation/editing, text-to-speech, Realtime, video generation and endpoint data controls;
- Gemini/Nano Banana image generation;
- NotebookLM Enterprise notebook and source-management APIs.

No API was called and no generated asset, learner data, credential or paid service was used.

## Verified

- OpenAI exposes image, speech, realtime and asynchronous video APIs. API keys are secrets and must not be exposed in browser code.
- Speech generation supports model/voice/format/speed selection; custom voices require a consent recording and are restricted to eligible customers.
- Realtime instructions are guidance rather than guaranteed deterministic behavior.
- OpenAI endpoint data-control documentation distinguishes retention and Zero Data Retention eligibility by endpoint.
- Gemini exposes multiple named Nano Banana image models; generated images include SynthID, and model capabilities/lifecycle differ.
- NotebookLM Enterprise now exposes preview APIs for notebook and source management, requiring Enterprise setup/licensing and Pre-GA acceptance.

## Interpretation

These APIs can support optional reviewed media, but none satisfies the authoritative technical-asset requirements by itself. Prompt retention and watermarking do not establish deterministic replay, source-level correctness, accessibility, licensing clearance or human approval.

## Design requirement

All optional generation adapters must default to dry-run manifest mode and require an explicit manual trigger before network execution. Accepted records must retain provider, exact model/version, generator version, prompt/storyboard and input hashes, source revision, parameters, usage/cost, output checksum, captions/transcript, licensing/privacy notes and human-review status. Ordinary pushes validate cached artifacts only.

## Rejected alternative

Do not use generated images or video as the canonical representation of llama.cpp/GGML architecture, call graphs, tensor layouts, memory transitions or benchmark results. Deterministic SVG/Mermaid/D3/Graphviz or trace-derived figures remain authoritative.

## EAAI implication

The defensible contribution is not the use of fashionable media APIs. It is the explicit separation between deterministic technical evidence and optional human-reviewed multimodal support, with retained failures, costs, provenance and accessibility decisions.

## Files changed

- `docs/publication/literature-map.md`
- this run record

## Sources

- OpenAI API references for images, audio, realtime, videos and data controls
- Google AI for Developers image-generation documentation
- Google Cloud NotebookLM Enterprise notebook/source API documentation

All sources are linked directly in `docs/publication/literature-map.md` and were checked on 2026-07-18.

## Limitations

- This was a documentation review, not a quality, factuality, latency, cost or accessibility experiment.
- Product names, availability, retention, pricing and preview status can change and require revalidation before a generation batch.
- No claim of educational benefit is supported.
- The source-level documentation-gap hypothesis remains open pending `DOC-AUDIT-01` retained search results, independent double-coding and adjudication.

## Validation and next dependency

The branch must receive commit-scoped Documentation CI. The next Literature Scout dependency is to retain the predefined documentation-audit search-result frame; the gap claim must not be strengthened before independent coding.
