---
name: prompts-hidden-insights
description: >
  Apply the "Hidden Insights" prompt-library workflow: surface non-obvious insights, patterns,
  and testable syntheses from the provided material using a four-phase structured process
  (Constraint Violation Analysis → Cross-Domain Pattern Matching → Predictive Synthesis →
  Source Grounding). Produce 2-3 testable predictions in table form and ground every claim
  with explicit evidence/citation distinctions and confidence levels. No fabricated citations.
  Use when the user says "hidden insights", "non-obvious patterns", "surface the real insights",
  "what are we missing here", "use hidden-insights prompt", or runs /prompts-hidden-insights.
when-to-use: "Deep, structured insight extraction that goes beyond surface summary. Triggers: 'hidden insights', 'non-obvious', 'what are we really seeing', 'constraint violations', 'cross-domain analogs', 'testable predictions from this'. Ideal after data, papers, or experimental results are on the table."
argument-hint: "<material, conversation context, paper, data, or research artifact to analyze for hidden insights>"
allowed-tools: ["read_file", "grep", "list_dir", "web_search", "web_fetch", "open_page", "open_page_with_find", "memory_search"]
metadata:
  short-description: "Four-phase structured extraction of non-obvious, testable insights with source grounding"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/prompts-hidden-insights/SKILL.md"
  version: "1.0.0"
---

# Hidden Insights — Grok Port

Execute a rigorous, four-phase insight engine that forces the discovery of non-obvious, cross-domain, and testable understandings rather than restating the obvious.

## Purpose

The original prompt provides a precise cognitive scaffold (constraint violations → analogs → predictions → grounding) that reliably produces higher-quality insights than free-form "think deeper." This Grok port makes the phases explicit, tool-augmented, and auditable.

## Invocation

```
/prompts-hidden-insights <material or context>
```

The current conversation, attached files, referenced papers, data, code, or prior analysis become the input. The skill will use tools to deepen grounding where URLs, files, or memory entries are present.

## The Four Phases (Core Contract — Execute All)

### Phase 1: Constraint Violation Analysis
Identify 3 assumptions in this domain that are:
- Widely held but empirically undertested
- Contradicted by edge-case data
- Inherited from older paradigms without re-examination

For each, state the assumption, the contradicting evidence or logical tension, and why it has survived.

### Phase 2: Cross-Domain Pattern Matching
Find structural analogs in unrelated fields (physics, economics, ecology, biology, engineering, etc.) that share mathematical, causal, or topological similarity with mechanisms in the source material.

Specifically answer:
- What systems exhibit the same periodicity, phase relationships, resonance dynamics, or feedback structures?
- Where else does [specific mechanism, object, or invariant from the project] appear in nature or engineered systems?

Name the source domain and the target domain for each analog. Explain the mapping at the level of structure, not surface metaphor.

### Phase 3: Predictive Synthesis
Generate 2-3 **testable predictions** that would be true if the emerging synthesis is correct but false (or much less likely) under conventional understanding.

Present in this exact table format:

| Prediction | Conventional Expectation | Your Synthesis Expects | Test Method |
|------------|---------------------------|-------------------------|-------------|
| ...        | ...                       | ...                     | ...         |

Each prediction must be specific enough that a clear experimental, observational, or analytical procedure could falsify it.

### Phase 4: Source Grounding
For each insight, prediction, or claim above, provide a short grounding block that clearly distinguishes:

- **Reported fact**: [citation or direct reference with URL / file:line / memory entry]
- **Inferred connection**: [your reasoning chain from the facts]
- **Open question**: [what remains unverified or requires further test]

**Requirements**: No fabricated citations. Prefer primary literature, raw data, or direct source material over secondary summaries. Flag confidence for each major claim (high / medium / low) with a one-sentence justification.

## Grok-Specific Execution Notes

- Use `read_file`, `grep`, `open_page_with_find`, `web_fetch` etc. to actually load and quote the source material rather than relying on conversation summary.
- Use `web_search` + `open_page` for cross-domain analogs and primary citations.
- Use `memory_search` / `memory_get` when prior sessions in the same workspace contain relevant patterns or data.
- When the material is a codebase or experiment log, combine structural grep results with the four phases.

## Output Shape (Recommended)

```
## Hidden Insights Report

### Phase 1: Constraint Violations
1. ...
2. ...
3. ...

### Phase 2: Cross-Domain Analogs
1. ...
2. ...

### Phase 3: Testable Predictions
| Prediction | ... |

### Phase 4: Grounding & Confidence
For each item above...

## Summary of Strongest Novel Insight
[One paragraph distillation]
```

## Success Criteria

- All four phases are visibly executed (even if some yield fewer than the nominal 3 items).
- At least two concrete, falsifiable predictions with test methods are produced.
- Every non-trivial claim has an explicit grounding block separating fact from inference.
- No citations are invented; every external reference can be verified by the reader using the provided links or file paths.
- The output feels like a genuine "aha" rather than a rephrasing of the input.

## Guardrails

- This is an insight **engine**, not a summarizer. If the material is thin, the phases will surface that honestly (e.g., "only one weak constraint violation surfaced because...").
- Do not force cross-domain analogs that are superficial. Structural isomorphism is required.
- In PGS or deterministic contexts: Phase 1 must explicitly consider whether classical probabilistic or heuristic assumptions are being smuggled in where PGS objects/invariants should be primary (per AGENTS.md).
- Confidence flags are mandatory and must be honest.

This port makes the original four-phase Hidden Insights prompt a repeatable, tool-augmented, and citation-disciplined workflow for Grok.
