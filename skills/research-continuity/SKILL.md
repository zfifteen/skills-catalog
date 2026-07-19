---
name: research-continuity
description: >
  Preserve durable research state, detect drift in reasoning or framing, and
  produce artifacts that let a future session (or different agent) continue
  high-stakes work without loss of context or accidental revival of invalidated
  ideas. Use when the user says "preserve continuity", "capture project memory",
  "shape feels wrong", "what should the next session do first", "hand off this
  research", or when ending a long thread and wanting explicit state. Works
  especially well with memory tools, todo_write, and the research-meeting skill.
when-to-use: "Any time continuity, durable memory, or early warning about conceptual drift is part of the request. Strong for multi-session research programs, handoffs between agents, or before compaction / context loss."
allowed-tools: ["read_file", "grep", "list_dir", "write", "search_replace", "memory_search", "memory_get", "todo_write", "web_search", "web_fetch", "open_page", "x_keyword_search", "x_semantic_search"]
argument-hint: "<optional: specific thread, hypothesis, or 'full project state'>"
metadata:
  short-description: "Durable research memory, drift detection, and clean handoff artifacts"
---

# Research Continuity

## Purpose

Ensure that the critical distinctions, proved results, invalidated paths, and next actions survive across sessions, agents, compactions, or handoffs. The skill forces explicit capture of state in a form that is machine- and human-readable and that actively resists common failure modes (drift, revival of dead ideas, loss of epistemic status).

This is a direct Grok port and enhancement of the Codex "research-continuity" skill, deeply integrated with Grok's `memory_*` tools, `todo_write`, and the workspace's AGENTS.md / PROOF.md contracts.

## When the Skill Is Active

The following distinctions must be made explicit in every continuity artifact:

- hypothesis
- measured result
- audit result
- proof result (or structural certificate)
- unresolved state
- invalidated rule / law / selector

## Required Behavior on Invocation

1. **Identify the Minimal Durable Set**
   - Scan current conversation, workspace (AGENTS.md, PROOF.md, key research files via `read_file`/`grep`/`list_dir`), and cross-session memory (`memory_search`).
   - Extract the smallest set of facts, files, and contracts that would allow a fresh session to continue correctly.

2. **Write Durable Artifacts**
   - Prefer repo-local files under `research/continuity/`, `docs/`, or a slug-named handoff directory.
   - Use `write` or `search_replace` with LF endings.
   - Also write or update relevant memory entries via the memory tools when appropriate for cross-project knowledge.
   - Produce or update:
     - A `STATE.md` or `HANDOFF.md` answering the five questions below.
     - Explicit test or reproduction commands.
     - Updates to TODO lists or `todo_write` entries.

3. **Early Drift Detection (Mandatory Language)**
   - If the work's shape is starting to drift, say so immediately and plainly:
     - "Shape feels wrong: ..."
     - "This is starting to look like progress theater."
     - "This is unresolved; the wording should not imply solved."
     - "The code is using a classical gate before the named PGS rule."
     - "PGS-first frame violated — classical selector used as inference engine."
   - Name the concrete drift and the exact corrective action.

4. **PGS / Prime-Gap-Structure Contract**
   - In this workspace (or any PGS research): the continuity artifact must begin with the current ordered prime-gap state, divisor-count field, DNI status, GWR application, endpoint chains, chamber resets, etc.
   - Never allow a continuity artifact to treat a proved PGS law as probabilistic or "empirically supported so far."

5. **Second-Opinion / Pressure Integration**
   - For high-stakes decisions, explicitly recommend or invoke the `second-opinion` skill (or equivalent via `task` subagent or codex-bus) with:
     - The exact question
     - Relevant code excerpts / outputs / stats
     - Known failed rules
     - Current proposed plan
   - Ask for critique, hidden assumptions, falsification paths, and one concrete next action. Follow up on material uncertainty.

## Output Shape (The Five Questions)

A good continuity artifact always answers, in order:

1. What is the current strongest supported claim? (With locator to proof / certificate / benchmark.)
2. What is explicitly not proved or not solved? (Unresolved state, open chambers, missing invariants.)
3. What failed and must not be revived? (Invalidated selectors, rules, assumptions, with dates and reasons.)
4. What should the next session (or next agent) do first? (Smallest high-leverage action with exact command or file to edit.)
5. What command or test reproduces the current state? (Reproducible one-liner or tool sequence.)

## Success Criteria

- A new session or different agent can read the artifact(s) and pick up the work at the correct epistemic level without re-deriving or accidentally reviving dead paths.
- Drift warnings are issued early enough to be actionable.
- All five questions have crisp, locatable answers.
- In PGS work: the artifact itself demonstrates PGS-first reasoning.

## Guardrails

- Avoid broad frameworks or ceremonial process documents. The artifact must be lean and actionable.
- Use LF line endings.
- Prefer writing state into existing contracts (AGENTS.md updates, PROOF.md addenda, spec/ files) over new ceremonial files.
- This skill does not execute the next action; it only captures the state for later execution.
- Higher-priority instructions (safety, explicit user contracts) always win.

## Grok Environment Integration

- `memory_search` + `memory_get` are first-class tools for both reading prior continuity state and writing new durable knowledge.
- `todo_write` is the natural companion for tracking the "what next session should do" items.
- `write` / `search_replace` create the on-disk handoff files.
- Synergy with `research-meeting` (structured deep dives that produce minutes to be captured here) and `codex-bus` (when the handoff must be persisted across truly separate agent instances via the ledger).
- `ooda` or `actualize` can be used after a continuity artifact is written if immediate action is also required.

## Example Minimal Artifact (for a PGS thread)

```markdown
# Continuity Handoff — Reciprocal Transport Closure (2026-05-24)

**Strongest supported claim**: The Divisor Normalization Identity plus GWR leftmost minimum-divisor rule yields a unique structural certificate for every chamber reset in the 10^12–10^14 regime (see PROOF.md:1423 and research/02-gwr-dni/endpoint-01234.json).

**Explicitly not proved**: Closure of the modulus-link for all endpoint chains beyond 10^14; behavior under simultaneous multi-chamber resets.

**Failed and must not be revived**: Shadow selector (invalidated 2026-05-10, see research/02-gwr-dni/invalidation-log.md).

**Next session first action**: Run the boundary-drop admissibility probe on the new 10^14–10^15 slice using the pinned seed and the exact command in research/00-index/continuity/next-command.txt.

**Reproduce current state**: `python research/02-gwr-dni/validate_dni.py --slice 1e14-1e15 --seed 0xfeedface`
```

This skill is the immune system for long-running, high-precision research programs.
