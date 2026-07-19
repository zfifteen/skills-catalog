---
name: prompts-presentation
description: >
  Apply the "Presentation" prompt-library workflow: transform the provided material (notes,
  findings, research results, code, arguments, data, or conversation context) into a clean,
  presentation-ready structure suitable for slides, talks, or executive briefings. Preserve
  the core narrative and key evidence while adding logical flow, visual cues, and audience-
  appropriate abstraction.
  Use when the user says "turn this into a presentation", "make slides from this", "presentation
  structure for these findings", "use the presentation prompt", or runs /prompts-presentation.
when-to-use: "Converting raw research, analysis, or meeting output into slide-deck or talk-ready form. Triggers: 'presentation', 'slides', 'deck', 'talk outline', 'executive summary for slides'. Focuses on structure and narrative flow rather than full prose."
argument-hint: "<material, findings, notes, or context to structure as a presentation>"
allowed-tools: ["read_file", "grep", "list_dir"]
metadata:
  short-description: "Convert material into clean, presentation-ready slide structure and narrative"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/prompts-presentation/SKILL.md"
  version: "1.0.0"
---

# Presentation — Grok Port

Turn the current material into a well-structured, audience-ready presentation outline that can be directly turned into slides or a talk.

## Purpose

The original prompt is deliberately minimal ("Turn this into a presentation") because the heavy lifting is in the disciplined extraction of narrative, evidence, and visual logic from messy source material. This Grok port keeps the contract simple while giving the model tools to ground the structure in the actual artifacts.

## Invocation

```
/prompts-presentation <material, notes, findings, paper, meeting transcript, or research artifact>
```

The full user-provided content plus any referenced files become the source.

## Core Task

Transform the input into a presentation:

- Identify the through-line / core story the audience should take away.
- Organize into a logical sequence of sections or slides.
- Surface the strongest evidence, data points, or arguments for each section.
- Add appropriate visual or rhetorical cues (e.g., "show the key plot here", "quote this one sentence", "use a simple diagram of X").
- Balance depth: enough technical substance for experts, clear framing for a broader audience.
- Keep the total scope reasonable for a 10–30 minute talk (or the length implied by the material).

## Recommended Output Structure (Adapt as Needed)

```
# Presentation Title
(One compelling line)

## 1. Opening / Hook
- The single most important question or claim
- Why it matters now (context or stakes)

## 2. Context & Setup (2–4 slides)
- Key background the audience must have
- Current state of the art or prior results (brief)
- The specific gap or problem this work addresses

## 3. Core Contribution / Method (3–6 slides)
- The central idea, algorithm, structure, or finding
- How it works (high-level first, then one level of detail)
- Key evidence or results (tables, figures, numbers, structural proofs)

## 4. Why This Matters / Implications (2–3 slides)
- What changes if this is correct or adopted
- Surprising consequences or new capabilities
- Relation to bigger open questions (especially PGS invariants or laws when relevant)

## 5. Limitations & Open Questions (1–2 slides)
- Honest boundaries of the current result
- What remains unproven or untested
- Natural next experiments or extensions

## 6. Call to Action / Closing
- The one thing the audience should remember or do
- Any concrete ask (review this PR, replicate this experiment, etc.)

## Appendix (optional)
- Detailed data, proofs, code snippets, or references that support the main narrative but would break flow in the live talk
```

For each slide/section, include:
- Suggested title
- 1–3 bullet points of content (keep sparse — slides are not prose)
- Speaker notes or "show X here" cues where helpful
- Any recommended visuals (diagram, plot, table, quote, code fragment)

## Grok Adaptations

- When source material lives in files: use `read_file` and `grep` to extract the actual strongest evidence rather than summarizing from memory.
- For research talks: explicitly surface PGS objects, invariants, and rule applications in the "Core Contribution" section when the work is in this domain (per AGENTS.md).
- Preserve the voice and intellectual honesty of the original material; do not add hype.

## Success Criteria

- A listener who only attends the talk would come away with the correct core message and the key supporting evidence.
- The structure has clear narrative momentum (problem → approach → evidence → implication).
- Slide content is sparse and visual-friendly (not dense paragraphs).
- The outline is immediately usable by the user (or a slide tool) to build the actual deck.
- No important claim in the presentation is weaker in the source material than presented.

## Guardrails

- This skill produces **structure and narrative**, not finished slide files (unless the environment has additional slide-generation tools and the user explicitly asks).
- Do not invent visuals or data points.
- If the source material is weak or incomplete for a good presentation, say so and suggest what is missing rather than papering over gaps with elegant structure.

This minimal but powerful prompt-library skill is now a reliable "narrative extraction + visual logic" tool for Grok.
