---
name: ooda
description: >
  Execute goal-directed work using an Observe → Orient → Decide → Act loop with
  visible tokens. Use when the user invokes /ooda, says "$ooda" or "use OODA",
  or needs structured evidence gathering, context orientation, direct decision
  making, and immediate tool-backed execution against code, research artifacts,
  logs, files, web data, or project state. Strong for iterative debugging,
  research probes, implementation under uncertainty, or any task requiring
  "gather facts then act" discipline.
when-to-use: "Invoked via /ooda or when the task requires repeated evidence-driven cycles rather than one-shot answers. Especially useful for work that risks drift or benefits from explicit Observe/Orient checkpoints."
allowed-tools: ["read_file", "grep", "list_dir", "web_search", "web_fetch", "open_page", "open_page_with_find", "x_keyword_search", "x_semantic_search", "x_thread_fetch", "memory_search", "memory_get", "task", "search_replace", "write", "image_gen", "video_gen"]
argument-hint: "<goal or task description> [--rounds N]"
metadata:
  short-description: "Disciplined Observe → Orient → Decide → Act execution loop with mandatory visible tokens"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/ooda/SKILL.md"
---

# OODA Loop

## Purpose

Run a disciplined Observe → Orient → Decide → Act execution loop. OODA is an **execution engine**, not a planning document. Move through all four phases, produce a visible token update, then loop only while the goal remains unresolved and another pass is warranted.

The loop continues until:
- The goal is resolved (strongest supported result achieved and verified).
- A hard, unresolvable blocker is identified.
- The user explicitly stops or redirects.
- A configured round limit is reached (default: no hard cap; user may pass `--rounds N`).

## Invocation

`/ooda <goal description>`

Optional: `--rounds 5` to bound the number of full cycles.

The goal should be stated in the user's actual scope. OODA will preserve that scope.

## Observe

Gather only the evidence required to understand the current surface relative to the goal. Do not perform broad inventory.

**Preferred Grok tools for local evidence:**
- `read_file`, `grep` (with context), `list_dir`, `open_page_with_find`
- `memory_search` / `memory_get` for cross-session or workspace memory
- Project files: AGENTS.md, SKILL.md, specs, logs, test outputs, prior artifacts

**For external / web / X evidence:**
- `web_search`, `web_fetch`, `open_page`, `open_page_with_find`
- `x_keyword_search`, `x_semantic_search`, `x_thread_fetch`, `x_user_search`

Capture concrete, quotable facts: file paths + line ranges, exact command outputs, measured values, timestamps, diff hunks, error messages, memory entries, API responses, post text, etc.

Prefer primary sources over summaries. When reading code or docs, read the minimal sufficient window (use offset/limit or pattern search).

Record what you examined and the key facts extracted.

## Orient

Relate the observed evidence to the locked goal.

- Restate the goal in the user's exact words (or the tightest faithful restatement).
- Assess current status relative to goal: solved, partially solved, misaligned, blocked (with precise blocker), or unresolved.
- Identify what the evidence implies about progress, missing state, and drift risk.
- Enumerate the immediate, narrow actions that would move the work forward.
- For each candidate action, note the most likely blocker and the narrowest contingency that would overcome it.
- Keep orientation operational and short. The purpose is to expose the direct path, not to produce narrative.

If in a PGS workspace or task, explicitly surface any relevant PGS objects, invariants, or rules before considering classical approaches (per AGENTS.md).

## Decide

Select the single action (or tightly-scoped sequence) that most directly advances the goal under known constraints.

- Choose from the actions surfaced in Orient.
- Prefer the path with the shortest deterministic route to a verifiable result.
- For high-stakes, ambiguous, adversarial, or research-sensitive decisions, consider launching a `task` subagent with a focused prompt (or the second-opinion pattern if available in the environment).
- When using subagents for Decide support, pass the full Observe + Orient context.
- If the chosen action has a known likely blocker, pre-plan the contingency from Orient.
- If no deterministic path exists that can satisfy the contract, stop and state the exact limitation plainly.

## Act

Execute the chosen action using the appropriate tools.

- File changes: `search_replace` (preferred for precision) or `write`.
- Commands / probes: not directly available; synthesize via edits + subsequent Observe (or describe the exact command the user should run and verify output in next Observe).
- External research: web and X tools.
- Visuals or media: `image_gen`, `video_gen` when they serve the goal.
- Complex sub-work: `task` tool (subagent) with clear description and prompt that includes the OODA context.
- After execution, immediately verify with the smallest sufficient check (re-read the edited region, run a targeted grep, fetch the new artifact, inspect output).

Report the strongest supported result first, followed by exact limits, validation performed, and any remaining unresolved state.

## Visible OODA Tokens (Mandatory)

For every full cycle (or major step within a long Act), emit a compact update in this shape:

```
Observe: <concrete evidence examined — files, queries, outputs, facts>
Orient: <goal restatement; current status; key implications; action options + blockers/contingencies>
Decide: <chosen action and rationale; any second-opinion or subagent result>
Act: <execution performed; verification result; strongest supported outcome; limits; unresolved state>
```

Do not leave a turn inside Observe, Orient, or Decide unless the user explicitly requested analysis-only or the next step is blocked by information that cannot be obtained locally with the available tools.

## Looping Discipline

After each Act + token:
- If the goal is now resolved to the required standard and verified, stop and summarize the final state.
- If unresolved and another pass would help, immediately begin the next Observe using the new state.
- Preserve continuity of the goal and key facts across rounds.
- For long-running loops, consider writing durable state (round number, key facts, current goal, blockers) to a workspace temp file (e.g. `/tmp/ooda-<id>.md` or project-local `.ooda-state.md`) via `write` so that future turns or new sessions can resume cleanly.

## State Preservation (Durable Cases)

When the loop spans multiple user turns or sessions, maintain at minimum:
- round_number (and optional round_limit)
- current_goal (user's original or faithfully tightened)
- key_observed_facts (bullet list or references to files)
- current_status (from last Orient)
- last_decision
- unresolved_points
- stop_reason (when terminating)

Use a small Markdown artifact or memory entry for this.

## Guardrails

- OODA is for execution. Do not turn it into open-ended brainstorming or framework theater.
- Never Act without a prior Decide that was justified by Observe + Orient.
- Do not silently widen the goal.
- In code changes, keep every edit narrow and verifiable. Use search_replace with unique context.
- Respect all higher-priority contracts (AGENTS.md PGS-first rule, safety, explicit user constraints).
- For PGS tasks: always surface PGS objects/invariants first in Observe/Orient.
- Stop cleanly on hard blockers; do not invent workarounds that violate contracts.
- Prefer deterministic, auditable actions over resilient or probabilistic ones unless the goal explicitly requires the latter.

## Success Criteria

- Every cycle produces a visible OODA token.
- Progress toward the goal is measurable and documented in the Act phase.
- The loop terminates with either a resolved, verified result or a precise statement of the remaining blocker/unresolved state.
- No drift from the original user goal has occurred.

The user should feel: "We gathered what was needed, decided clearly, acted, verified, and either finished or know exactly what is left."
