# Related-work evidence notes

_Last updated: 2026-07-17_

This is a planning artifact, not manuscript prose. The claimed gap between usage-oriented documentation and source-level systems understanding remains a **hypothesis** until a systematic documentation audit is completed.

## Source comprehension and trace visualization

- Cornelissen, Zaidman, and van Deursen compared an IDE-only condition with IDE plus execution-trace visualization using eight program-comprehension tasks and measured correctness and time. This supports an information-equivalent static baseline, but its historical results cannot be treated as an expected effect size for How.to.llama.cpp. <https://doi.org/10.1109/TSE.2010.47>
- Wyrich, Bogner, and Wagner mapped 95 code-comprehension experiments and documented heterogeneous task and measurement choices. This supports freezing the construct, tasks, answer keys, and scoring before evaluation. <https://arxiv.org/abs/2206.11102>
- Wyrich’s conceptual model warns against defining comprehension only by an unspecified task. The first executable-lecture evaluation therefore targets bounded path reconstruction and evidence classification, not general llama.cpp mastery. <https://arxiv.org/abs/2310.11301>
- Hassan and Zilles found that learner tracing can fail through non-use, incorrect tracing, or uninformative inputs. Prediction-before-reveal and diagnostic distractors should expose those failure modes. <https://sigcse2023.sigcse.org/details/sigcse-ts-2023-papers/21/On-Students-Usage-of-Tracing-for-Understanding-Code>
- Park et al. used correctness questions and confidence alongside eye tracking. Confidence is useful for calibration but is not a substitute for correctness. <https://doi.org/10.1007/s10664-024-10532-x>
- Thilderkvist and Dobslaw reported inadequate consumer-webcam eye-tracking data for their intended remote comparison. Webcam eye tracking is rejected for the first evaluation because it adds privacy and validity risk. <https://doi.org/10.1016/j.infsof.2024.107502>

## Current synthesis

**Verified:** primary program-comprehension work commonly operationalizes outcomes through correctness and task time, sometimes supplemented by confidence, difficulty, gaze, or cognitive-load proxies.

**Interpretation:** the fairest first comparison is synchronized viewer versus an information-equivalent static source/text package. Raw source alone is not a fair control because it removes curated evidence as well as interaction.

**Open question:** whether synchronized source/state/explanation navigation improves bounded tracing for this target audience remains unevidenced.

## Required follow-up

Create a versioned benchmark artifact with identical evidence, tasks, answer keys, source revision, time limits, and accessibility alternatives in both conditions. Obtain independent technical review and evaluation-path approval before participant recruitment.