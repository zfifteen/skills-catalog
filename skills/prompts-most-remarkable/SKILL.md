---
name: prompts-most-remarkable
description: >
  Apply the "Most Remarkable" prompt-library workflow: analyze a folder, experiment results,
  repository contents, or data artifacts and identify the single most remarkable, data-backed,
  or highly significant finding. Provide a thorough explanation of why the evidence qualifies
  as remarkable or breakthrough-level. Take the time needed for deep analysis.
  Use when the user says "most remarkable finding", "what is the real breakthrough here",
  "surface the mind-shattering result", "most significant data-backed evidence", or runs
  /prompts-most-remarkable.
when-to-use: "Locating the single highest-signal, most surprising or consequential result in a body of experimental or analytical work. Triggers: 'most remarkable', 'breakthrough insight', 'mind-shattering', 'the real finding is', 'what actually matters in all this data'."
argument-hint: "<path to folder, experiment results, repo, or description of the material containing results>"
allowed-tools: ["read_file", "grep", "list_dir", "open_page_with_find", "web_fetch"]
metadata:
  short-description: "Identify and deeply justify the single most remarkable data-backed finding in a body of work"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/prompts-most-remarkable/SKILL.md"
  version: "1.0.0"
---

# Most Remarkable — Grok Port

Surface and rigorously justify the single most consequential, data-supported, or paradigm-challenging finding present in the provided experimental or analytical material.

## Purpose

The original prompt demands that the analyst "develop a mind-shattering, remarkable, breakthrough insight" and "take all the time you need." This Grok port operationalizes that demand with tool access to actually inspect the artifacts (logs, CSVs, plots descriptions, code outputs, notebooks) rather than relying on summary.

## Invocation

```
/prompts-most-remarkable <folder path, experiment directory, or description of results>
```

The skill will use `list_dir`, `read_file`, `grep`, and other tools to explore the actual evidence base.

## Core Contract

- Analyse the folder and all experiment results (logs, data files, plots, code outputs, notes, FINDINGS.md files, etc.).
- Develop a mind-shattering, remarkable, breakthrough insight.
- Find the **most remarkable or highly significant data-backed evidence** in the repository / result set.
- Give a **thorough explanation** why the evidence is considered remarkable or highly significant.
- Take the necessary time and depth; do not rush to a superficial "cool result."

## Grok Execution Approach

1. **Inventory the Evidence Base**
   - Recursively explore the target folder(s) with `list_dir`.
   - Identify all result artifacts (CSVs, JSON, text logs, images, `FINDINGS.md`, notebooks, plot descriptions, etc.).
   - Prioritize files that contain quantitative outcomes, statistical tests, structural discoveries, or explicit "result" sections.

2. **Deep Reading of Key Artifacts**
   - Use `read_file` (with targeted offsets) and `grep` (with context) on the highest-yield files.
   - For each candidate remarkable finding, extract the raw numbers, methodology notes, controls, and any author commentary on its significance.

3. **Significance Evaluation**
   - For each candidate, assess against multiple axes:
     - Effect size / magnitude relative to baseline or prior art
     - Surprise relative to conventional expectations in the domain
     - Generality / implications for other work
     - Quality and completeness of the supporting evidence (reproducibility, controls, statistical rigor or deterministic verification)
     - Connection to core project invariants or open questions (especially PGS objects/rules in this workspace)

4. **Select the Single Most Remarkable**
   - Choose exactly one. If several are close, pick the one with the largest combination of magnitude + surprise + leverage on the research program.
   - Be prepared to defend the choice with explicit comparison to the runners-up (internally; do not list them in the final output unless asked).

5. **Produce the Justification**
   - Write a thorough, evidence-dense explanation.
   - Quote or cite specific data points, file:line locations, statistical values, structural observations, or visual patterns.
   - Explain *why* this finding is more remarkable than other plausible candidates.

## Output Shape

```
## Most Remarkable Finding

**Finding (one sentence)**: 
[Clear statement of the remarkable result]

**Location of Evidence**: 
`experiments/xxx/FINDINGS.md:42` (or specific data file + line / plot description)

**Why This Is Remarkable**:
[2–5 paragraphs of rigorous justification covering magnitude, surprise, evidence quality, and research leverage. Include direct quotes or numbers from the artifacts.]

**Supporting Data** (key excerpts):
- ...
- ...

**Implications** (brief):
- ...
```

## Success Criteria

- The output identifies exactly one finding as "most remarkable."
- The justification is data-backed and cites specific evidence locations that the reader can verify.
- The explanation addresses *why* it qualifies as remarkable (not just "this number is big").
- The chosen item genuinely stands out from the rest of the result set (the skill performed the comparative work even if not all comparisons are shown).
- In a PGS workspace, any finding that directly illuminates or challenges a proved invariant or structural law receives strong consideration.

## Guardrails

- "Data-backed" is non-negotiable. Purely theoretical or speculative claims do not qualify unless they are themselves the output of a rigorous derivation whose result is surprising.
- Do not inflate significance. If the most remarkable thing is modest, say so plainly while still highlighting it.
- The skill may take multiple tool-using turns internally; the final user-facing answer is the distilled report.
- This is not a "highlight reel" skill — it is allowed (and encouraged) to conclude that the most remarkable thing is a *negative* or *null* result if that is what the data actually shows most powerfully.

This port gives Grok a disciplined "find the real signal in the noise" lens with actual file-system and artifact inspection capabilities.
