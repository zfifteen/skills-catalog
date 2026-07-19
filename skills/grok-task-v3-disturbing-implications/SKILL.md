---
name: disturbing-implications
description: >
  Detail the disturbing, uncomfortable, or high-stakes implications of a
  development, result, claim, design decision, or discovery—those that
  create new risks, invalidate comfortable assumptions, force difficult
  choices, or reveal previously unacknowledged vulnerabilities. Output as a
  title followed by a list of bullets. ~2500 character limit. Use when the
  user says "disturbing implications", "uncomfortable consequences of this",
  "the dark side of X", "what keeps you up at night about this result", or
  provides a finding whose negative, risky, or paradigm-shifting downsides
  deserve explicit, unsentimental examination. Complements the standard
  "implications" skill by focusing on the hard or alarming angles.
when-to-use: "Use specifically when the user wants the uncomfortable, risky, or paradigm-threatening consequences surfaced (as opposed to neutral or positive implications). Trigger on 'disturbing implications', 'the scary part of this', 'what this actually threatens', 'uncomfortable consequences'. Title + bullet list, ~2500 chars, unsentimental."
allowed-tools: ["read_file", "grep", "list_dir", "web_search", "web_fetch", "open_page", "open_page_with_find", "x_keyword_search", "x_semantic_search", "x_thread_fetch", "memory_search", "memory_get", "todo_write"]
metadata:
  short-description: "Detail the disturbing implications of a development as title + bullet list (~2500 chars)"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/grok-task-v3-disturbing-implications/SKILL.md"
---

# Disturbing Implications

Interpret the current user message, the referenced development, attachments, and full context as the subject whose most alarming or paradigm-threatening implications must be mapped with clinical precision.

**PGS Project Contract (this repository):** When the subject is prime gap structure research, proved deterministic results (PROOF.md), or experimental claims in this workspace, the disturbing-implications analysis must highlight any developments that risk (a) diluting the deterministic status of proved theorems, (b) re-introducing classical or probabilistic framing as authoritative, (c) creating experimental or archival debt that could later be used to cast doubt on structural results, or (d) opening attack surfaces (cryptanalytic, social, or funding) against the research program. The analysis stays inside the PGS-native frame at all times.

## Core Instruction (from Codex origin)

Detail the disturbing implications of this development in the format of a title followed by a list of bullets. Use up to 2500 characters.

## Workflow

1. **Characterize the Development Accurately**
   - Read the primary source material with tools.
   - State what was actually shown or decided, including its explicit scope and limitations.

2. **Surface the Uncomfortable Angles**
   - Systematically examine:
     - What comfortable prior assumption is now untenable?
     - What new attack surface, failure mode, or evidentiary burden has been created?
     - Which downstream systems, claims, or narratives are now at risk of retroactive invalidation?
     - What does this force the program (or the field) to confront that it has been able to avoid until now?
     - For external claims: what does widespread acceptance of this result enable that would be harmful or misleading?
   - Prioritize implications that are logically entailed or strongly evidenced, not speculative worst-cases.

3. **Maintain Clinical Tone**
   - No sensationalism. "This creates a vector for..." rather than "This is terrifying because...".
   - The disturbance comes from the substance, not the rhetoric.

4. **Constrain to Signal**
   - Select only the highest-leverage disturbing implications.
   - Fit the entire output (title + bullets) within ~2500 characters.
   - Every bullet must be traceable to the development plus program context.

5. **Verify Against Program State**
   - Cross-check with AGENTS.md, PROOF.md, current experimental status, and open questions before asserting any implication for this research program.

## Output Format (Strict)

**<Neutral Title That Names the Development and Signals the Disturbing Domain>**

- Bullet 1: first disturbing implication, grounded.
- Bullet 2: ...
(Flat bullet list. No substructure or concluding paragraph.)

Title examples:
- "Disturbing Implications of Framing the GWR Selector as 'Heuristic'"
- "Disturbing Implications of the 10^12 Endpoint Data Release Without Structural Certificates"

## Execution Rules

- Read the source development directly; do not rely on secondary interpretations.
- In PGS contexts, the most disturbing implications are usually those that erode the deterministic/structural character of the results or create conditions for future gaslighting of the program's claims.
- Distinguish "this is disturbing because it logically entails Y" from "this could be spun badly."
- If the development is external, fetch primary sources and note the difference between the claim and the evidence that actually supports it.
- Use `todo_write` internally if multiple consequence chains must be tracked.

## Success Criteria

- A reader finishes the list with a clear, evidence-based understanding of the new risks or forced confrontations created by the development.
- The analysis is unsentimental and precise; alarmism is absent.
- For material in this workspace: any threat to the proved status of PGS theorems or to the integrity of the experimental record is explicitly called out.
- The output complements (rather than duplicates) a standard implications analysis.

This skill ensures that the hard, risky, or paradigm-upsetting consequences of developments are not left unexamined—precisely the angles that comfortable analysis tends to soft-pedal or omit.
