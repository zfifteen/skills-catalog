---
name: forensic
description: >
  Perform a detailed, technical forensic analysis of a situation, claim,
  artifact, incident, code behavior, data anomaly, or dispute. Output as a
  title followed by a single, tight list of bullets. Constrained to ~2500
  characters. Use when the user says "forensic", "forensic analysis of this",
  "technical post-mortem", "what actually happened here", "root cause
  analysis", or provides logs, diffs, claims, or events that require precise,
  evidence-based reconstruction of what occurred and why. Valuable for
  debugging mysterious failures, auditing surprising results, or dissecting
  contradictory narratives in research or operations.
when-to-use: "Use for technical forensic / root-cause / post-mortem analysis of incidents, anomalies, surprising results, or disputed claims. Trigger on 'forensic this', 'what really happened', 'debug this anomaly', 'post-mortem the failure'. Produces title + single bullet list, ~2500 char cap."
allowed-tools: ["read_file", "grep", "list_dir", "web_search", "web_fetch", "open_page", "open_page_with_find", "x_keyword_search", "x_semantic_search", "x_thread_fetch", "memory_search", "memory_get", "todo_write"]
metadata:
  short-description: "Detailed technical forensic analysis as title + single bullet list (~2500 chars)"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/grok-task-v3-forensic/SKILL.md"
---

# Forensic

Interpret the current user message, attachments, files, logs, links, images, conversation history, and all context as the complete material for forensic analysis.

**PGS Project Contract (this repository):** If the matter involves prime gap structure research, divisor fields, experimental outputs, or deterministic claims in this workspace, the forensic analysis **must** reconstruct events using the PGS objects → invariants → rules frame (AGENTS.md). It must not introduce probabilistic reinterpretations of proved results, nor default to classical number-theoretic explanations without explicit justification. Every finding must be tied to concrete artifacts, logs, or code.

## Core Instruction (from Codex origin)

Forensic: Perform a detailed technical forensic analysis of this matter. Format as a title followed by a single list of bullets. Use 2500 characters.

## Workflow

1. **Scope the Incident / Matter**
   - Precisely define what is being forensically examined (the "incident").
   - Gather the primary evidence surface: logs, code, diffs, generated artifacts, timestamps, prior session memory, external sources via tools.
   - Identify all actors, processes, data flows, and decision points involved.

2. **Timeline & Causation Reconstruction**
   - Build a strict chronological reconstruction using only verifiable timestamps and artifact states.
   - For each step, note what was true in the environment at that moment.
   - Distinguish observed facts from inferred intent or causes.

3. **Anomaly & Deviation Analysis**
   - Surface every deviation from expected behavior (per specs, previous runs, invariants, or stated claims).
   - For each deviation, record the exact evidence (file:line, log excerpt, metric value, structural mismatch).

4. **Root Cause Hypothesis Formation**
   - Form the minimal set of root-cause hypotheses that explain the observed surface.
   - Test each against the full evidence set; eliminate those that fail to account for any key fact.
   - Prioritize deterministic, reproducible causes over "flaky" or environmental ones.

5. **Evidence Sufficiency & Gaps**
   - Explicitly call out any missing information that would be required for a conclusive determination.
   - Distinguish "strong forensic conclusion" from "most likely explanation given available evidence."

6. **Synthesize & Constrain**
   - Produce the output under the hard character budget (~2500 chars total).
   - Every bullet must be a concrete, evidence-backed statement.

## Output Format (Strict)

**Title**

A single, precise, neutral title that names the matter under forensic examination (e.g., "Forensic Analysis: Unexpected Endpoint Collapse in 10^12 Search at Seed 424242").

Then a single list of bullets (no sub-bullets or nested structures unless absolutely required for clarity). The entire response after the title must fit comfortably within 2500 characters.

Each bullet should address one of:
- A key timeline event with evidence
- An observed anomaly with exact locator
- A causal link supported by multiple independent artifacts
- A ruled-out alternative with the contradicting evidence
- A remaining uncertainty with the precise missing datum

Do not add concluding prose after the bullet list. The bullets are the analysis.

## Execution Rules

- Stay strictly within the character limit; prioritize precision over completeness.
- Use tools to re-verify every claim against primary sources before including it.
- Never speculate about motive or unobservable internal state.
- For code or experiment anomalies in this repo: always re-read the relevant source (AGENTS.md, PROOF.md, specific scripts, output JSONs) with tools.
- If X or web material is involved, fetch full threads/posts before analyzing.
- When evidence is incomplete, the last bullets must explicitly list the exact additional artifacts or commands needed for closure.

## Success Criteria

- A reader can reconstruct the essential sequence of events and the most likely technical cause(s) solely from the title + bullets.
- Every substantive claim is backed by a specific, locatable piece of evidence.
- No probabilistic softening of deterministic facts; no classical framing injected into PGS contexts.
- The analysis is useful for preventing recurrence or for handing off to "advance-my-research" or "logic-check" siblings.

This forensic skill produces the highest-signal, lowest-noise technical reconstruction possible under tight length constraints—ideal for incident response, result auditing, and claim verification in active research programs.
