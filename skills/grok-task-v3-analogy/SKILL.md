---
name: analogy
description: >
  Create a sharp, revealing analogy (or set of analogies) that exposes the
  ridiculousness, absurdity, flawed logic, or hidden assumptions in a claim,
  argument, design, hypothesis, social media post, research artifact, or
  situation. Sentences are separated by two carriage returns (blank line) for
  scannability. Use when the user says "analogy", "make an analogy", "show how
  ridiculous this is", "analogize this", "that analogy for X", or provides
  material whose conceptual error or overclaim benefits from defamiliarization.
  Powerful for surfacing contradictions in research claims, code architecture
  decisions, or discourse. If the material is PGS-related in this workspace,
  the analogy must illuminate deterministic invariants without introducing
  probabilistic or classical-number-theory framing unless explicitly comparing.
when-to-use: "Invoked for analogy generation to expose flaws, reframe ideas, or highlight absurdity in claims/arguments/artifacts. Especially useful on hypotheses, designs, X posts, or research narratives that contain internal contradictions or overreach."
allowed-tools: ["read_file", "grep", "list_dir", "web_search", "web_fetch", "open_page", "open_page_with_find", "x_keyword_search", "x_semantic_search", "x_thread_fetch", "memory_search", "memory_get", "todo_write"]
metadata:
  short-description: "Create analogy that shows how ridiculous this is"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/grok-task-v3-analogy/SKILL.md"
---

# Analogy

Interpret the current user message, attachments, files, links, images, conversation history, and all available context as the complete input material for this workflow.

**PGS Project Contract (this repository):** If the subject matter intersects prime gap structure, divisor-count fields, GWR, DNI, endpoint chains, or any deterministic number-theoretic research in this workspace, **you MUST surface the relevant PGS objects and invariants first** (per AGENTS.md) before constructing any analogy. Analogies must not downgrade proved PGS theorems to probabilistic language or default to classical sieves/Miller-Rabin/gcd framing. Classical methods appear only for explicit, requested comparison.

## Core Instruction

Create an analogy (or tightly related set of analogies) that shows how ridiculous, inconsistent, or conceptually broken the target idea/claim/situation is. The goal is defamiliarization that makes the flaw obvious and memorable.

## Workflow

1. **Ingest & Ground**
   - Use tools as needed (`read_file`, `web_fetch`, `x_thread_fetch`, etc.) to obtain the full primary material and any referenced context.
   - Identify the central claim, assumption, or pattern being analogized.
   - Extract the exact wording or behavior that will be mapped.
   - Note any quantitative or structural details that the analogy must respect (numbers, invariants, failure modes).

2. **Identify the Ridiculous Core**
   - What is the hidden assumption, scale error, category mistake, self-contradiction, or overclaim?
   - What would the world look like if this logic were applied consistently elsewhere?
   - Surface the most damning or absurd implication.

3. **Craft the Analogy**
   - Choose a concrete, everyday or vivid domain that maps the structure cleanly (avoid strained or mixed metaphors).
   - The mapping must be tight: the ridiculous element in the source must correspond directly to a ridiculous (or obviously broken) element in the analogy.
   - Keep the analogy short and self-contained. One strong analogy is better than several weak ones.
   - If multiple angles are needed, produce 2–3 short, non-overlapping analogies, each clearly labeled.

4. **Validate & Refine**
   - Does the analogy accurately reflect the source without straw-manning?
   - Does it illuminate the precise flaw rather than a different or weaker one?
   - Does it avoid introducing new technical errors (especially critical for PGS or mathematical material)?
   - If PGS-related: does it preserve the deterministic character of any proved rules or laws?

5. **Output**
   - Write the analogy text with sentences separated by two carriage returns (i.e., a blank line between each sentence or short paragraph for maximum readability).
   - Optional short title or label at top if it clarifies the target.
   - If the source material was incomplete, end with a precise "Access or Context Needed" section listing exact missing items.

## Output Format (Strict)

Respond with the analogy (or analogies) in the requested prose style. No lengthy preamble. No citations unless fetched and relevant. No social-media post IDs.

Example rhythm (sentences separated by blank lines):

This is the first sentence of the analogy that sets the scene.

This is the second sentence that maps the key flawed assumption onto the ridiculous everyday counterpart.

This third sentence lands the absurdity so the reader feels the contradiction viscerally.

(Repeat for additional short analogies under clear subheadings if needed.)

## Execution Rules

- Never fabricate details in the analogy that do not map from the source.
- If the source is a research claim or code behavior, re-read the primary artifact (via tools) immediately before finalizing the analogy.
- For X/Twitter material, fetch the thread if only a quote was provided.
- When the material touches this project's core research, the analogy is an instrument of clarity, not a vehicle for probabilistic softening of deterministic results.
- Keep total length focused; the original Codex constraint of "separate sentences with two carriage returns" is preserved for scannability.

## Success Criteria

- A reader unfamiliar with the source material immediately grasps the core flaw after reading the analogy.
- The mapping is structurally accurate and does not distort the original claim.
- No new technical inaccuracies are introduced.
- If PGS context: the analogy respects the PGS-first frame and does not reframe deterministic laws as heuristic.

This skill turns opaque or defended claims into something suddenly, obviously ridiculous—without cruelty, but with precision.
