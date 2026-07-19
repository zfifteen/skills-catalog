---
name: self-prompt-and-answer
description: >
  From a post, article, research note, X thread, or other source material, first
  synthesize a sharp, self-contained prompt that captures the core question or
  claim, then answer that prompt directly in the form of a clean title followed
  by a bulleted list. Output only the title + bullets. Use when the user says
  "self prompt and answer", "turn this into Q&A", "prompt from this post then
  answer it", or pastes content and wants the essence extracted and responded to
  without the intermediate prompt being shown.
when-to-use: "Use on requests to distill source material (posts, notes, threads, specs) into a self-contained question and its direct answer in title+bullets form. Common for X content, research fragments, or meeting notes that need to become crisp, standalone artifacts."
allowed-tools: ["read_file", "open_page", "open_page_with_find", "web_fetch", "x_thread_fetch", "x_semantic_search", "x_keyword_search", "memory_search", "grep"]
argument-hint: "<URL or pasted post/text or X thread ID>"
metadata:
  short-description: "Distill source into prompt then answer as title + bullets only"
---

# Self Prompt & Answer

## Purpose

Transform raw, contextual, or conversational source material into a clean, reusable, self-contained knowledge artifact: a precise prompt (synthesized internally) whose answer is delivered as a title followed by bullets, with the prompt itself never shown in the final output.

This is the Grok port of the Codex "grok-task-v3-self-prompt-and-answer" workflow. The port adds tool-based ingestion for URLs, X threads, and local files while preserving the strict "title + bullets only" output discipline.

## Invocation

`/self-prompt-and-answer <source>`

Source may be:
- A URL (article, GitHub gist, blog, arXiv abstract)
- An X post or thread ID / URL (use X tools)
- Pasted text or research note
- Local file path (read via `read_file`)
- "the last post" or reference to recent conversation material

## Workflow

1. **Ingest the Source**
   - For URLs: `web_fetch` or `open_page` + `open_page_with_find` to extract the core claim or question.
   - For X content: `x_thread_fetch` or `x_semantic_search` + `x_keyword_search`.
   - For local/pasted: `read_file` or direct context.
   - For conversation: `memory_search` if needed for full thread.
   - Capture the essential claim, question, or tension in the material.

2. **Synthesize the Hidden Prompt (Internal Only)**
   - Internally formulate the sharpest, most faithful prompt that the source is implicitly asking or that best tests the claim.
   - The prompt should be specific enough that a strong answer is possible in title + bullets.
   - Do **not** output this prompt.

3. **Answer in Required Format**
   - Title (concise, informative, captures the essence)
   - Bulleted list (the direct answer)
   - Nothing else. No exposition, no "The prompt was...", no preamble, no closing.

## Output Rules (Strict)

- First line: the Title
- Then blank line
- Then bullets
- Stop.

Example shape (for illustration only):

```
The Core Tension in Endpoint-Chain Traversal

- The leftmost minimum-divisor rule forces a unique structural certificate at each chamber reset.
- Reciprocal transport across the modulus link is deterministic once the divisor-count field is normalized.
- Any apparent gap in the 10^14–10^18 regime is an artifact of classical selector assumptions, not of the underlying PGS invariants.
```

## Success Criteria

- A reader who never saw the original source can understand the distilled question and the answer from the title + bullets alone.
- The bullets are substantive, not generic.
- No trace of the internal prompt or meta-process appears.
- When the source is an X post or public claim, the answer respects verifiability (use citations where external facts are asserted).

## Guardrails

- Do not fabricate a stronger or weaker claim than the source supports.
- If the source is low-signal or purely social, the synthesized prompt may legitimately be "What is the actual technical content here?" and the answer may be minimal or point out the absence.
- For research claims: preserve epistemic status (hypothesis vs. measured result vs. proved vs. unresolved).
- PGS contexts: the internal prompt and answer must respect AGENTS.md framing; classical methods are not the default lens.
- Never use this skill to generate clickbait or sensationalized versions of serious technical material.

## Grok-Specific Adaptations

- Rich ingestion via the full suite of web, open_page, and X tools allows the skill to work on live public sources the original Codex prompt could not reach.
- `memory_search` lets the skill pull in long-running project context when the "post" is actually a fragment of an ongoing research conversation.
- The output discipline (title + bullets only) makes the result immediately copy-pasteable into notes, papers, prompt libraries, or the prompt-library-catalog skill.

This skill turns noisy or embedded material into crisp, standalone, high-density knowledge units.
