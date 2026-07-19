---
name: prompts-transcribe
description: >
  Apply the "transcribe" prompt-library workflow: produce a complete, clean, timestamp-free
  transcription of the provided video, audio, or media content. The output is pure spoken
  words (and important non-verbal cues if relevant) with no timestamps, no speaker labels
  unless essential, and no editorial commentary.
  Use when the user shares a video link, uploaded media, or says "transcribe this video",
  "full transcript without timestamps", "use the transcribe prompt", or runs
  /prompts-transcribe.
when-to-use: "Obtaining a clean, readable, timestamp-free transcript of spoken video or audio content. Triggers: 'transcribe', 'full transcript', 'no timestamps', 'clean transcript of this video'. Simple but high-utility focused task."
argument-hint: "<video URL, link to audio, or description of the media to transcribe>"
allowed-tools: ["web_fetch", "open_page", "web_search", "read_file"]
metadata:
  short-description: "Produce clean, complete, timestamp-free transcription of video/audio content"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/prompts-transcribe/SKILL.md"
  version: "1.0.0"
---

# transcribe — Grok Port

Generate a high-fidelity, timestamp-free, readable transcript of the provided video or audio material.

## Purpose

The original prompt is intentionally minimal and strict: "Transcribe this video completely. Do not include timestamps." The value lies in the discipline — delivering pure, flowing text that can be read, searched, or fed into other analysis skills without the distraction of timing data. This Grok port preserves that contract while noting modern tool realities for media ingestion.

## Invocation

```
/prompts-transcribe <video URL or reference to media>
```

Or natural language: "transcribe this video without timestamps", "full clean transcript of the attached talk".

## Core Contract (Strict)

- Transcribe the **entire** spoken content.
- **Do not include timestamps** of any kind (no [00:12:34], no "at 3 minutes", no chapter markers).
- Produce clean, readable prose that preserves the original spoken flow, including natural restarts, filler if meaningful, and important emphasis.
- Include non-verbal information only when it is essential for understanding (e.g., "[laughter]", "[long pause]", "[shows diagram]") and only sparingly.
- No speaker identification labels unless the video has clearly distinct, named speakers and the distinction is important to the content.
- No summaries, no commentary, no "here is the transcript" framing in the body — the transcript itself is the output.

## Grok Execution Notes

1. **Media Access**
   - If a public video URL (YouTube, etc.) is provided: use `web_fetch` or `open_page` on the page, then look for available transcripts, captions, or descriptions. Many platforms expose timed text; the skill must strip all timing information.
   - If the environment has dedicated media tools (YouTube skill, local audio upload handling, etc.), prefer the highest-fidelity source.
   - If only a link and no direct transcript API is available, the skill may need to describe the limitation and ask the user to paste key sections or use an external transcription service first, then offer to clean the result.

2. **Post-Processing Discipline**
   - If raw timed captions or ASR output is obtained, **remove every timestamp** and reassemble into continuous paragraphs or natural spoken sentences.
   - Preserve paragraph breaks where the speaker changes topic or there is a clear rhetorical pause.
   - Correct obvious ASR errors only when context makes the intended word certain; otherwise leave as spoken or flag lightly.

3. **Output Purity**
   - The delivered text should be immediately usable as source material for other prompt-library skills (Hidden Insights, Presentation, etc.) or for human reading.
   - If the video contains substantial visual-only content (slides, code, diagrams shown without narration), note the visual sequence in minimal bracketed form only when it carries independent meaning.

## Output Shape (Example)

```
The speaker opens by describing the core problem: large prime gaps exhibit unexpected structure that standard random models fail to capture. They then walk through the definition of the divisor-count field and introduce the Divisor Normalization Identity...

[three paragraphs of continuous transcript...]

In the final segment the speaker shows a plot of leftmost minimum divisor positions across 50,000 candidates and notes that the pattern is inconsistent with uniform random expectation under the classical model.
```

## Success Criteria

- The transcript is complete (covers the entire duration of the spoken content).
- Zero timestamps or timing artifacts remain in the output.
- The text is pleasant and accurate to read as continuous prose.
- Non-verbal or visual notes are minimal and only present when they materially affect meaning.
- The result can be directly fed into downstream analysis skills without cleanup.

## Guardrails

- Do not summarize or editorialize. The contract is transcription, not condensation.
- If the media is inaccessible or the environment lacks transcription capability, state the limitation clearly rather than producing a partial or hallucinated transcript.
- For very long videos, the skill may produce the transcript in chunks with clear continuation markers, but the "no timestamps" rule still applies inside each chunk.

This simple but strictly scoped prompt-library skill is now available as a reliable clean-transcription lens for Grok.
