---
name: gaslight-check
description: >
  Perform a gaslighting analysis on provided material (typically an X post,
  thread, claim, argument, or narrative) and present the findings as a list
  of bullets titled exactly “How [poster_profile_name] Gaslights You”.
  Academic tone. Confident voice. No adjectives. No citations. Hard cap of
  2500 characters. Use when the user says "gaslight check", "gaslight
  analysis", "how is this person gaslighting", "analyze the rhetoric in this
  post", or provides discourse that appears to use manipulation, moving
  goalposts, selective framing, or reality-distortion patterns. Especially
  useful for public technical or scientific claims on social media.
when-to-use: "Invoked for structured gaslighting / rhetorical manipulation analysis of posts, threads, arguments, or claims. Trigger on 'gaslight check this', 'analyze how this gaslights', 'rhetoric audit of this post'. Always outputs 'How <Name> Gaslights You' bullet list, academic/confident tone, no adjectives or citations, <=2500 chars."
allowed-tools: ["read_file", "web_search", "web_fetch", "open_page", "open_page_with_find", "x_keyword_search", "x_semantic_search", "x_thread_fetch", "x_user_search", "memory_search", "memory_get", "todo_write"]
metadata:
  short-description: "Gaslighting analysis as 'How [Name] Gaslights You' bullet list (academic, confident, no adjectives/cites, ~2500 chars)"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/grok-task-v3-gaslight-check/SKILL.md"
---

# Gaslight Check

Interpret the current user message, attachments, X posts/threads, links, and conversation context as the complete input. The goal is a precise, non-emotional dissection of gaslighting patterns present in the material.

**PGS Project Contract (this repository):** When the material under analysis touches prime gap structure, number-theoretic claims, or research in this workspace, the gaslight check must be especially rigorous about any attempt to reframe deterministic results as probabilistic, heuristic, or "not yet proved" when they are in fact proved per PROOF.md and AGENTS.md. Gaslighting in technical discourse often takes the form of smuggling in classical assumptions or demanding classical validation for PGS-native results.

## Core Instruction (from Codex origin)

Gaslight Check: Perform a gaslighting analysis and present it as a list of bullets called “How [poster_profile_name] Gaslights You”. Use an academic tone, limit the response to 2500 characters, and remove all citations. Use a confident voice. No adjectives. No citations.

## Workflow

1. **Identify the Poster / Source**
   - Extract or infer the profile name or handle of the primary author/speaker (use `x_user_search` or thread metadata if only a quote is provided).
   - If multiple voices are present, focus on the dominant or most relevant one; label clearly.
   - Fetch the full primary source (thread, article, comment chain) using X tools or web tools before analysis.

2. **Map the Reality-Distortion Techniques**
   - Systematically identify instances of:
     - Denial of observable facts or prior statements
     - Moving goalposts (changing success criteria after the fact)
     - Selective omission of context or counter-evidence
     - Equivocation on key terms (especially "proof", "deterministic", "heuristic", "empirical")
     - Projection of the analyst's own standards onto the target
     - Creation of false dilemmas or impossible evidentiary burdens
     - Retroactive reframing of the target's position
   - For each technique, collect the exact original wording + the contradictory evidence from the record.

3. **Structure the Bullets**
   - Each bullet names one distinct gaslighting maneuver.
   - The bullet describes the maneuver in plain academic language and shows, with minimal necessary quotation, how it distorts reality.
   - Maintain strict "no adjectives" rule: "This maneuver..." not "This dishonest/sneaky maneuver...".

4. **Enforce Constraints**
   - Remove every citation (no URLs, no @handles in the final bullets, no superscripts).
   - Keep total length ≤ 2500 characters (title + bullets).
   - Confident declarative voice throughout ("X does Y" rather than "X appears to..." or "one might argue...").

5. **Title Construction**
   - Exactly: "How <Poster Profile Name> Gaslights You"
   - Use the cleanest public-facing name available from the source (full name or handle as appropriate).

## Output Format (Strict)

**How <Poster Profile Name> Gaslights You**

- Bullet 1: precise description of the maneuver with direct evidence of the distortion.
- Bullet 2: ...
(Continue until all major patterns are covered or character budget is reached. No trailing prose.)

The entire output after the title is one flat bullet list. No sub-bullets, no bolded categories, no concluding paragraph.

## Execution Rules

- Fetch the complete source material first; never analyze from a partial quote alone.
- "No citations" is absolute in the final output—citations may be used internally during analysis via tools and `render_inline_citation` where required, but stripped from the delivered bullets.
- Academic tone + confident voice = clinical, authoritative, emotionally neutral.
- If the material is technical/research-related in this workspace, pay special attention to any reframing of proved deterministic results as probabilistic or "emerging."
- If the poster name cannot be determined with certainty, use the most specific descriptor available ("the author of the linked thread", "the account posting under @...") but prefer a clean name.

## Success Criteria

- A reader who has never seen the original material can understand exactly which rhetorical maneuvers constitute gaslighting and see the evidence for each.
- The list is exhaustive of the major patterns within the length cap.
- Zero adjectives or loaded language.
- Zero citations or URLs remain in the final text.
- For PGS-adjacent claims, any attempt to gaslight the deterministic status of results is explicitly surfaced.

This skill provides a standardized, high-signal instrument for recognizing and documenting gaslighting in technical and public discourse—without descending into polemic.
