---
name: implications
description: >
  Detail the (technical, scientific, architectural, strategic, or
  philosophical) implications of a development, result, claim, design
  decision, or discovery. Output as a title followed by a list of bullets.
  Constrained to ~2500 characters. Use when the user says "implications",
  "what are the implications of this", "unpack the consequences", "strategic
  implications of X", or provides a result, finding, or change whose
  downstream effects on a research program, codebase, or domain deserve
  explicit mapping. Complements "advance-my-research" by focusing on
  consequence rather than next minimal action.
when-to-use: "Use to surface the broader consequences of a result, change, or claim. Trigger on 'implications of this', 'what does this mean for the program', 'consequences of X', 'strategic impact of this finding'. Produces title + bullet list, ~2500 char limit."
allowed-tools: ["read_file", "grep", "list_dir", "web_search", "web_fetch", "open_page", "open_page_with_find", "x_keyword_search", "x_semantic_search", "x_thread_fetch", "memory_search", "memory_get", "todo_write"]
metadata:
  short-description: "Detail implications of a development as title + bullet list (~2500 chars)"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/grok-task-v3-implications/SKILL.md"
---

# Implications

Interpret the current user message, the referenced development/result/claim, attachments, files, and conversation context as the complete subject whose implications must be mapped.

**PGS Project Contract (this repository):** If the development concerns prime gap structure, divisor fields, GWR/DNI, proved theorems (see PROOF.md), or any deterministic number-theoretic advance in this workspace, the implications analysis **must** be conducted inside the PGS-native frame. It must not dilute proved results into "suggestive" or "empirical" language, nor introduce classical number theory as the default lens. Implications for the deterministic structure of the theory are the primary focus.

## Core Instruction (from Codex origin)

Detail the implications of this development in the format of a title followed by a list of bullets. Use up to 2500 characters.

## Workflow

1. **Precisely Characterize the Development**
   - Use tools to read the primary artifact(s) describing the result, change, or claim.
   - State in one sentence what actually happened or was shown (not the interpretation).
   - Note the exact scope and any explicit limitations stated by the source.

2. **Map Consequence Chains**
   - For each major dimension (technical correctness, architectural invariants, reproducibility, downstream code, experimental program, theoretical status, resource requirements, strategic positioning), trace the direct and second-order effects.
   - Distinguish certain implications (logically entailed) from plausible or contingent ones.
   - In research contexts, pay special attention to effects on open problems, proved theorems, and active experimental lines.

3. **Prioritize & Constrain**
   - Select the most significant, non-obvious implications.
   - Eliminate redundancy.
   - Stay within the ~2500 character budget for the entire output after the title.

4. **Surface Hidden or Counter-Intuitive Implications**
   - Especially valuable: implications that reverse common assumptions, invalidate prior heuristics, or open previously closed research directions.
   - For PGS work: implications for the status of specific invariants, selectors, or endpoint classifications.

5. **Verify Grounding**
   - Every bullet must be traceable to evidence in the source development plus the surrounding program state (use memory and file tools).

## Output Format (Strict)

**<Precise, Neutral Title Naming the Development and Its Domain>**

- Bullet 1: first major implication with grounding.
- Bullet 2: ...
(Flat list only. No sub-bullets unless required for a single complex point. No trailing summary paragraph.)

Title examples:
- "Implications of the Zero-Excess DNI Certificate at 10^12"
- "Implications of Replacing the Shadow Selector with the Square-Fiber Variant"

## Execution Rules

- Read the actual development artifact first; do not reason from secondary summaries.
- In this workspace, cross-check against AGENTS.md, PROOF.md, and current experimental status before asserting theoretical implications.
- Distinguish "this changes the research program because..." from "this might be useful for...".
- When implications touch proved results, preserve their exact status.
- If the development is external (paper, post, library release), fetch primary sources.

## Success Criteria

- A reader understands the most important downstream effects on the relevant program or domain after reading the title + bullets.
- Every implication is non-trivial and evidence-based.
- No inflation or dilution of certainty.
- PGS implications correctly reflect the deterministic nature of the underlying theory.

This skill forces explicit consequence mapping so that research developments are not left as isolated facts but are immediately integrated into the living strategic picture of the program.
