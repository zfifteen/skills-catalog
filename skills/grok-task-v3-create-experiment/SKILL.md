---
name: create-experiment
description: >
  Design and execute a focused experiment whose explicit purpose is to attempt
  to falsify a stated hypothesis. Create a dedicated directory under
  'experiments/' (or repo-appropriate research tree) containing all artifacts.
  All findings must open with a crystal-clear executive summary of the
  outcome, followed by meticulous setup, execution, and reproducibility
  details. Use when the user provides or references a hypothesis and says
  "create experiment", "falsify this", "test this hypothesis", "run an
  experiment to...", or similar. Especially valuable in deterministic
  research programs (e.g. prime-gap-structure) where every experiment must be
  minimal, fully pinned, and directly probative of a sharp prediction.
when-to-use: "Use to turn a hypothesis into a concrete, reproducible falsification experiment with artifacts under experiments/. Trigger on 'falsify', 'create experiment to test', 'design a minimal probe for this claim', or when a research artifact contains an explicit or implicit hypothesis needing direct experimental confrontation."
allowed-tools: ["read_file", "grep", "list_dir", "web_search", "web_fetch", "open_page", "open_page_with_find", "x_keyword_search", "x_semantic_search", "memory_search", "memory_get", "search_replace", "write", "todo_write"]
metadata:
  short-description: "Create falsification experiment under experiments/ with executive summary first"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/grok-task-v3-create-experiment/SKILL.md"
---

# Create Experiment

Interpret the current user message, attachments, files, links, images, conversation history, and workspace state as the complete input context. Your job is to turn the referenced hypothesis into the smallest practical experiment that can realistically falsify it (or sharply support it), with all artifacts created under a new `experiments/<slug>/` directory.

**PGS Project Contract (this repository):** If the hypothesis concerns prime gap structure, divisor fields, GWR/DNI, endpoint behavior, or any deterministic number-theoretic claim in this workspace, **you MUST begin from the PGS objects → invariants → rule/law → state frame** (per AGENTS.md). The experiment design must target a deterministic prediction. Do not default to probabilistic language, classical sieves, or cryptographic heuristics unless the explicit goal is a controlled comparison against a legacy method. Never downgrade proved PGS theorems.

## Core Instruction (from Codex origin)

Attempt to falsify the hypothesis (see the More Context link or attached material for the hypothesis details). Create a new directory under 'experiments/' for all your artifacts. Ensure your findings begin with an executive summary that makes the results of the experiment crystal clear, then provide meticulous details on your experiment setup and execution.

## Workflow

1. **Extract & Formalize the Hypothesis**
   - Read all provided material and use tools to fetch any referenced sources.
   - State the hypothesis as a single, precise, testable sentence (quote source location).
   - Identify the exact prediction that would falsify it (the "sharp edge").
   - Note all relevant parameters, ranges, seeds, precision requirements, and controls already present or implied.

2. **Design the Minimal Falsifying Experiment**
   - Choose the smallest intervention or measurement that can deliver a clear pass/fail against the hypothesis.
   - Prefer re-using or minimally extending existing code/artifacts over new greenfield work.
   - Define:
     - Exact command(s) or tool sequence to run.
     - Full reproducibility pins (seed, floating-point precision, timeouts, library versions, date context, hardware notes if relevant).
     - Expected output signature (exact log pattern, numeric threshold with tolerance, structural invariant in generated files).
     - Pass criterion that directly maps to "hypothesis falsified / not falsified / sharpened".
   - If new code or scripts are required, keep them minimal and place them inside the experiment directory with clear comments tying back to the hypothesis.

3. **Create the Experiment Directory & Artifacts**
   - Use `list_dir` + `write` (or `search_replace` for edits) to create `experiments/<hypothesis-slug-or-pr-or-date>/` (choose a stable, descriptive slug).
   - Inside it, produce at minimum:
     - `README.md` or `experiment.md` containing the full report (see Output Format).
     - Any scripts, parameter files, or notebooks needed to reproduce.
     - Captured raw outputs (logs, CSVs, JSON, images) or instructions for generating them.
   - Record exact git commands or `search_replace` recipes for any workspace changes made during setup.

4. **Execute & Capture**
   - Run the experiment using the prescribed commands (describe them precisely for the user if direct execution tooling is limited in the current turn; otherwise use available execution paths).
   - Capture full stdout/stderr, generated files, and any intermediate artifacts.
   - Re-ingest the results with tools (`read_file` on outputs, `grep` for signatures).

5. **Analyze Against Hypothesis**
   - Did the outcome falsify, support, or leave the hypothesis unresolved?
   - Quantify the strength (effect size, confidence bounds if appropriate, or deterministic match/mismatch).
   - Note any unexpected behaviors or required follow-on minimal steps (these may become inputs to sibling "advance-my-research" or "experiment-design" skills).

## Strict Output Format

All findings **must begin with an executive summary** that makes the result of the experiment crystal clear to a reader who will only read the first paragraph.

Then provide:

**Executive Summary**
- One or two sentences: "The experiment falsified / did not falsify / sharpened the hypothesis because [exact observed signature vs. predicted]."

**Hypothesis**
- Verbatim statement + source locator.

**Experiment Design**
- Purpose (falsification target)
- Method (minimal description)
- Reproducibility pins (full list)
- Expected signature & pass criterion

**Execution**
- Exact commands run (or to be run by user)
- Environment details
- Raw output excerpts or links to generated files in the experiment dir

**Results**
- Quantitative or structural findings
- Direct comparison to pass/fail criterion

**Interpretation**
- Implication for the hypothesis (falsified / supported / requires refinement)
- One-sentence statement of what the result updates in the research program

**Provenance & Rollback**
- All files created or modified
- Exact commands to reproduce or revert

**Next Minimal Step (optional but encouraged)**
- The smallest follow-up that would further sharpen or close the line of inquiry.

## Execution Rules

- The experiment directory name must be unique and descriptive (include date or PR reference when relevant).
- Every numeric claim or threshold must have an explicit tolerance or exact-match rule.
- No undocumented fallbacks or "if this fails, try..." paths in the experimental logic.
- Use `todo_write` for any multi-step tracking inside the experiment design.
- After creating artifacts, immediately verify them with `read_file` / `grep`.
- If the hypothesis is PGS-related, the experiment must be capable of producing a deterministic structural certificate or counter-example, not a statistical sample.

## Success Criteria

- A third party can read the executive summary, understand the outcome unambiguously, then follow the reproducibility section and obtain the identical result.
- The experiment is the smallest one that could have falsified the hypothesis.
- All artifacts live under a single clean `experiments/<slug>/` tree.
- No over-claiming: "falsified" is used only when the pass criterion for falsification was met; otherwise "did not falsify" or "sharpened."

This skill ensures hypotheses in active research programs are confronted with direct, minimal, fully documented experimental evidence rather than left as unfalsified assertions.
