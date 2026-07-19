---
name: prompts-next-step
description: >
  Apply the "Next Step" prompt-library workflow: act as an expert research engineer and software
  architect to deeply analyze a Git-based repository (or provided codebase context), then propose
  **exactly one** concrete, high-leverage "next step" that most effectively advances the core
  research goal. Deliver the answer in a strict 6-part structured format (Research goal, Current
  state, Single best next step, Rationale, Concrete execution plan, Acceptance criteria).
  Use when the user provides a repo URL or is working inside a codebase and says "what is the
  next step", "strongest next step", "use next-step prompt", "recommend the single best action",
  or runs /prompts-next-step.
when-to-use: "Identifying the single highest-leverage, immediately actionable next step in an active research or implementation codebase. Triggers: 'next step', 'what should I do next', 'strongest move', 'one concrete thing', 'prioritize the next action'. Enforces focus on exactly one step with full implementation detail."
argument-hint: "<repository URL or path, plus optional short research goal description and constraints>"
allowed-tools: ["read_file", "grep", "list_dir", "web_fetch", "open_page", "open_page_with_find", "run_terminal_cmd", "git"]
metadata:
  short-description: "Recommend exactly one high-leverage, fully-specified next step for a research codebase (structured 6-part output)"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/prompts-next-step/SKILL.md"
  version: "1.0.0"
---

# Next Step — Grok Port

Produce exactly one concrete, implementation-ready next step that advances the core research goal of the provided repository or codebase, using a rigorous 6-section structured analysis.

## Purpose

The original prompt is one of the most detailed in the library: it forces deep codebase understanding, explicit research-goal alignment, and a single, non-vague, fully-specified recommendation with acceptance criteria. This Grok port adds live tool access to actually inspect the repo instead of hallucinating its state.

## Invocation

```
/prompts-next-step <repo URL or local path> [optional: research goal + constraints]
```

If no explicit goal is supplied, the skill must infer it from README, papers, directory structure, and code.

## Required Structured Output (Contract — Do Not Deviate)

The final answer **must** contain exactly these six sections with the specified internal structure. No more, no less in the primary deliverable.

### Research goal (your understanding)
- One or two sentences summarizing what this repo is fundamentally trying to achieve.

### Current state (high-level)
- Bullet list of 3–6 key points describing:
  - What works
  - What is partially implemented
  - What is clearly missing or uncertain

### Single best next step
- A one-sentence description:
  > "Implement X in order to test/strengthen/extend Y."

### Rationale
- 3–5 bullets explaining:
  - Why this step is higher leverage than other options considered
  - What specific uncertainty or limitation it resolves
  - How success/failure of this step would update the research direction

### Concrete execution plan
- 5–10 bullets, as specific as possible, including:
  - Which files/modules to inspect or modify
  - What new functions/classes/scripts to add
  - What configuration changes, datasets, or hyperparameters to use
  - How to run the relevant experiments or scripts (exact example commands)
  - What metrics, plots, or logs to examine to judge success

### Acceptance criteria
- 3–5 bullets describing clear, falsifiable criteria that indicate whether this next step succeeded (or produced a decisive negative result).

## Grok Workflow (Tool-Augmented)

1. **Establish Research Context**
   - Use tools to read README, any papers/docs in the repo, AGENTS.md, directory tree, key source files, Makefiles, CI configs, experiment runners.
   - Infer (and explicitly state) the project's main research question or objective.
   - If the user's stated goal differs from what the code actually pursues, call the misalignment out before proceeding.

2. **Build Mental Model of the Codebase**
   - Identify core algorithms, models, experimental pipelines, entry points, config systems.
   - Note technical risks, bottlenecks, missing tests, ad-hoc handling, scalability limits.
   - In this workspace (prime-gap-structure): explicitly map any existing PGS objects, invariants, rules, or chamber logic before suggesting changes.

3. **Assess Current Research Progress**
   - Determine implemented vs. experimental vs. incomplete vs. validated.
   - Locate clear open questions or failure modes visible in logs/results.
   - Prioritize gaps that are both high-impact for the research question **and** feasible in a single focused work session (0.5–2 sessions).

4. **Select Exactly One Best Next Step**
   - Choose the single action with the best impact/feasibility ratio.
   - It must be a **specific, actionable task**, not a vague goal ("refactor", "run more experiments", "improve docs").
   - Briefly note (internally) why attractive alternatives were rejected; only surface them if they are strong runners-up that the user might reasonably consider.

5. **Write the Structured Output**
   - Fill every subsection with concrete, implementation-level detail.
   - The execution plan must be narrow enough that a competent engineer or agent can follow it without further high-level decisions.

6. **Ground in Actual Files**
   - Every file reference in the plan must have been confirmed by `read_file`, `grep`, or `list_dir` during the analysis.

## Style & Constraints (Preserved)

- Assume the reader is an experienced researcher-engineer who wants focus and signal, not tutorials.
- Prefer specificity over completeness.
- Propose **exactly one** next step. If multiple are tempting, mark the others as "considered but not chosen" with a one-sentence reason why the selected one wins.
- The step must move the research forward in a measurable way (better evidence, reduced uncertainty, clearer ablation, improved reliability, etc.).

## Success Criteria

- The output contains all six required sections with the exact internal structure specified.
- The "Single best next step" sentence is crisp and names a concrete deliverable.
- The Concrete execution plan is detailed enough to be followed with minimal additional research.
- Acceptance criteria are falsifiable (a later observer can say "yes, this succeeded" or "this produced a clear negative").
- The recommendation is aligned with the actual state of the code (no hallucinated files or capabilities).
- In PGS contexts, the suggested step either strengthens a PGS law application or directly tests a PGS object/invariant.

## Guardrails

- Never propose more than one primary next step in the main output.
- Do not let the plan balloon into a multi-week project; keep it to a focused, completable increment.
- If the repo is in poor shape (no clear goal, broken build, etc.), the "next step" may legitimately be "establish minimal reproducible baseline" — state this clearly.
- Respect AGENTS.md: any suggestion that would cause reasoning to begin from classical methods instead of PGS-native objects must be justified or rejected.

This port converts one of the most valuable prompt-library skills into a live, repo-inspecting strategic advisor that delivers immediately actionable, single-focus recommendations.
