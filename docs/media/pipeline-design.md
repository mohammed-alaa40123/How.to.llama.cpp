# Media pipeline design

_Last verified against official service documentation: 2026-07-17_

This document converts the official media-service review into implementation constraints. It does not authorize external API use and does not make generated media technical evidence.

## Authority hierarchy

1. **Authoritative technical layer:** deterministic SVG, Mermaid, Graphviz, D3, tables, and trace-derived figures generated from pinned source, fixture, or trace data.
2. **Reviewed explanatory layer:** project-authored text, captions, transcripts, narration scripts, and manually reviewed diagrams.
3. **Optional generative layer:** illustrations, rendered narration, or video used only as supplemental presentation after the authoritative layer is complete.

A generated asset must never be the only representation of a code path, tensor shape, pointer relationship, ownership claim, memory event, benchmark, or timing result.

## Supported optional service classes

| Class | Verified current capability | Allowed project role | Canonical dependency? |
|---|---|---|---|
| OpenAI image generation/editing | API generation/editing and streamed partial images | Supplemental illustration or manually reviewed visual treatment | No |
| OpenAI text-to-speech | Render reviewed scripts; custom voices require consent and eligibility | Optional narration with transcript | No |
| OpenAI Realtime | Low-latency multimodal/speech sessions | Optional live demonstration after static lesson exists | No |
| OpenAI video generation | Asynchronous prompt/reference-based clips | Optional reviewed summary or transition media | No |
| Gemini native image generation | Text/image generation and editing; generated images include SynthID | Supplemental illustration or manually reviewed visual treatment | No |
| NotebookLM | Source-grounded product artifacts; Enterprise preview API verifies notebook management | Instructor-side ideation or manually exported/reviewed supplement | No |

Official capability links and service-specific cautions are maintained in [`../publication/literature-map.md`](../publication/literature-map.md).

## Required artifact lifecycle

```text
structured source / reviewed script
        ↓
manifest + prompt or storyboard
        ↓
manual approval to generate
        ↓
external generation outside ordinary CI
        ↓
cached output + immutable receipt
        ↓
technical, accessibility, licensing and representation review
        ↓
accepted / revised / rejected
        ↓
publish only accepted assets with deterministic/static fallback
```

Ordinary pushes and pull requests may validate manifests, hashes, cached outputs, captions, transcripts, review state, and stale-asset rules. They must not invoke paid generation endpoints or overwrite approved assets.

## Immutable generation receipt

Each external generation requires a repository record with:

- provider;
- endpoint or API surface;
- exact documented model identifier when available;
- model/version label returned by the service, when available;
- generation parameters;
- UTC creation time;
- prompt or storyboard path and SHA-256;
- input-asset paths and SHA-256 values;
- pinned How.to.llama.cpp and upstream source revisions;
- output path, media type, byte size, and SHA-256;
- usage or cost record when the API exposes it;
- provider provenance signal, such as SynthID, when applicable and detectable;
- technical-claim declaration;
- privacy and licensing notes;
- accessibility artifacts;
- human review records;
- final state: `accepted`, `revised`, or `rejected`.

A provider name or friendly model family label alone is insufficient. Hosted model aliases and product capabilities can change.

## Stale-asset rules

An accepted asset becomes stale when any of the following changes:

- relevant project or upstream source revision;
- deterministic input data;
- reviewed narration script;
- prompt or storyboard;
- reference image/audio/video;
- generator model identifier or API surface;
- manifest or validation-schema version;
- technical-claim declaration;
- accessibility fallback.

Stale status does not trigger regeneration. It blocks publication until a human chooses to retain, revise, regenerate, or reject the asset.

## Accessibility contract

| Asset | Required equivalent |
|---|---|
| Image or diagram | Meaningful alt text; long description or data table when the content is complex |
| Narration | Exact reviewed script/transcript; pronunciation and factual review |
| Video | Captions, transcript, static source-linked fallback, reduced-motion path, keyboard-operable controls |
| Realtime demonstration | Equivalent non-realtime lesson; no required microphone; no learner audio retention by default |

Automatic transcription may start a draft but is not reviewed caption evidence.

## Privacy and security boundary

Default external inputs are limited to public repository content, project-authored prompts/scripts, and assets with documented redistribution rights.

Do not send:

- API keys or secrets;
- private repository content;
- restricted model weights;
- learner names, emails, identifiers, prompts, responses, code, voice, or video;
- unpublished participant or evaluation data;
- third-party assets without documented rights.

Provider statements that business/API data is not used for training by default do not imply zero retention. Before any approved generation run, record the applicable account class, endpoint, region, retention setting, and data-sharing configuration.

## Human review rubric

Every asset receives separate dispositions for:

1. **Technical correctness:** no false source, runtime, tensor, memory, timing, or architecture claim.
2. **Accessibility:** equivalent content is complete and usable.
3. **Licensing and redistribution:** inputs and outputs can be stored and published as intended.
4. **Privacy and security:** no disallowed data or credential exposure.
5. **Representation and pedagogy:** imagery and voice choices do not introduce stereotypes, distraction, or misleading anthropomorphism.
6. **Educational necessity:** the asset supports a defined learner objective rather than visual novelty.

An asset cannot be `accepted` while any required review is missing or failed.

## NotebookLM boundary

NotebookLM may be used as an optional companion for source-grounded instructor exploration. As of the verification date, the official NotebookLM Enterprise preview API documents notebook creation, retrieval, listing, deletion, and sharing, but the reviewed documentation does not establish the complete programmatic artifact lifecycle required here: generation, deterministic retrieval/export, model/version provenance, checksums, and review-state integration for every derived artifact.

Therefore NotebookLM is not a canonical CI or build dependency. Manually exported output must enter the same manifest, caching, accessibility, licensing, and human-review process as any other external generation.

## Rejected implementations

- Generative architecture diagrams presented as authoritative.
- Prompt-only provenance without output and input checksums.
- Mutable “latest” model labels treated as reproducible versions.
- Automatic paid generation on push, pull request, or scheduled documentation build.
- Audio or video without reviewed text/static equivalents.
- Public NotebookLM sharing used as a substitute for source-rights and privacy review.
- Realtime voice as a required or sole learning interface.

## Week 1 implementation consequence

The deterministic GGUF-layout figure remains the next media vertical slice. It should be generated from the synthetic fixture manifest, produce a reproducible SVG and text/table equivalent, and validate against the existing media manifest contract without any external generation call.
