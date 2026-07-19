---
name: task-chain
description: >
  Decompose a high-level implementation goal (from a URL, spec, research target,
  or pasted artifact) into a rigorous, numbered chain of small, focused TASK_XXX.md
  files. Each task has a single objective, measurable success criteria, explicit
  validation gates (especially 10^14–10^18 scale for number theory), reproducibility
  pins, and a "proceed to next" handoff. Use when the user provides a URL or goal
  and says "task chain", "break this into tasks", "decompose this spec", "create
  implementation plan with TASK files", or similar. Prevents scope creep and
  ensures every step is auditable and deterministic.
when-to-use: "Invoked for complex implementation or research goals that benefit from explicit decomposition into chained, self-contained micro-tasks with success criteria and next-task pointers. Especially for number-theoretic or systems work requiring scale validation and reproducibility."
allowed-tools: ["read_file", "grep", "list_dir", "web_fetch", "open_page", "open_page_with_find", "web_search", "write", "search_replace", "todo_write", "memory_search", "memory_get", "run_terminal_command"]
argument-hint: "<URL or goal description or pasted spec> [--out-dir .task-chain]"
metadata:
  short-description: "Decompose goal into rigorous chained TASK_*.md files with validation gates"
---

# Task Chain

## Purpose

Convert a large or vague implementation/research goal into a linear (or lightly branched) sequence of tiny, verifiable tasks. Each task is small enough (~500 tokens), deterministic-preferring, and ends with an explicit handoff to the next. The chain is the primary artifact; the plan summary is secondary.

This is the Grok port of the Codex "grok-task-v3-task-chain" workflow, adapted to create real files in the workspace using the `write` tool and to leverage Grok's inspection tools for the analysis phase.

## Core Principles (Non-Negotiable)

- One task = one focused objective.
- Prefer deterministic algorithms and explicit parameters over probabilistic or heuristic approaches.
- Validation at declared real scale (e.g., 10^14–10^18 for prime-gap or RSA work), never toy examples unless the goal explicitly is a toy.
- Every claim, constant, seed, timeout must be pinned for exact reproduction.
- No "future-proofing", no speculative branches, no gold-plating.
- Collapse complexity wherever possible.
- Every task file ends with a precise "Upon completion, proceed to TASK_YYY.md".

## Invocation

`/task-chain <URL | goal text | pasted spec> [--out-dir <path>]`

- The source may be a GitHub URL (commit, PR, file, gist), arXiv, local file, or plain description.
- Output directory defaults to `.task-chain/` (or `research/task-chains/<slug>/` inside a PGS research tree).

## Workflow

1. **Ingest & Extract Core Goal**
   - Fetch the source using `web_fetch` / `open_page` (for URLs) or `read_file` / `grep` (local).
   - Identify the single primary implementation or research goal and all hard constraints (scale, precision, reproducibility, validation targets).
   - Extract or infer measurable success criteria and explicit validation gates from the source (quote them).
   - In PGS context: restate the goal in terms of PGS objects → invariants → rules first.

2. **Analysis & Planning**
   - Produce a short implementation plan summary (goals, scale, validation gates, key risks).
   - Identify natural decomposition points that keep each task ≤ ~500 tokens of instruction.
   - Ensure the chain covers the full goal without gaps or "and then magic" steps.

3. **Decomposition into Task Files**
   - Create one file per task: `TASK_001.md`, `TASK_002.md`, ... (zero-padded).
   - Use the `write` tool (preferred) or `search_replace` for precision.
   - Each file must follow this exact skeleton:

     ```
     # TASK_XXX: [Concise Title]

     ## Objective
     [One sentence: what this single task accomplishes toward the goal]

     ## Context
     [Minimal necessary context carried from prior tasks; reference earlier TASK files]

     ## Requirements
     - [Specific, testable requirement 1]
     - [Include explicit validation gates, scale targets, precision parameters, seeds, timeouts]
     - [Reproducibility pins: library versions, command flags, data sources]

     ## Implementation
     [Step-by-step instructions]
     [Guard clauses and early-exit conditions before any heavy work]
     [Preferred Grok tools or terminal commands if relevant]

     ## Success Criteria
     - [Measurable, binary or quantitative outcome]
     - [Exact artifacts that must be produced (files, log lines, numeric thresholds with tolerance)]
     - [How to verify (exact command or tool sequence)]

     ## Next Task
     Upon completion, proceed to TASK_YYY.md
     ```

4. **Dependency Graph (if non-linear)**
   - If tasks have light dependencies, emit a small `DEPENDENCIES.md` or ASCII graph at the top level.

5. **Handoff & Verification**
   - After writing all files, re-read the first and last task + the plan summary to confirm the chain is closed and every handoff is correct.
   - Use `todo_write` internally if the decomposition itself has many moving parts.
   - Report the location of the generated chain and a one-paragraph summary of the plan.

## Output (Minimal)

1. One-sentence plan summary + key scale/validation gates.
2. The complete set of `TASK_*.md` files created (list their paths).
3. Any `DEPENDENCIES.md` or graph.
4. (Optional) A top-level `README.md` for the chain that points to TASK_001.md as the entry point.

## Success Criteria

- Every task file exists on disk with the exact required sections.
- No task exceeds the spirit of "small and focused".
- All reproducibility pins and validation gates from the original goal are present in at least one task.
- A third party (or future self) can start at TASK_001 and reach the goal by following the chain exactly, using only the pinned parameters.
- In number-theoretic or PGS work: every scale target and gate is explicit and at production-relevant size.

## Guardrails

- Never invent requirements not present in the source.
- If the source is a URL, verify the fetched content before decomposing (use `open_page_with_find` or multiple fetches).
- PGS workspaces: surface PGS objects/invariants in the plan and in relevant task contexts.
- If a goal cannot be decomposed without introducing probabilistic core steps, flag it explicitly in the plan summary and propose a deterministic reformulation if one exists.
- Do not execute the tasks unless the user later explicitly says "run the chain" or "start TASK_001".
- Prefer editing existing files over new ones when the goal is a patch; only create the chain when the goal is genuinely multi-step greenfield or large refactor.

## Grok Environment Notes

- File creation: primary mechanism is the `write` tool (absolute or workspace-relative paths).
- Inspection of existing code: `read_file` (with `pages` for PDFs, `offset`/`limit` for large sources), `grep`.
- External sources: `web_fetch`, `open_page`, `open_page_with_find`.
- Git / shell operations inside tasks: the generated tasks may reference `run_terminal_command` when the host environment exposes it.
- State across long chains: `memory_*` and `todo_write` are available to the executor.

This skill turns "I want to build X at real scale" into an auditable, handoff-complete execution graph that a capable agent or human maintainer can follow without further clarification.
