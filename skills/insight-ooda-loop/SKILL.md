---
name: insight-ooda-loop
description: >
  Run a closed iterative research loop: Novel Insight Engine produces a novel
  falsifiable prediction → OODA turns it into an execution goal with Observe/
  Orient/ Decide/ Act → finding feeds the next NIE round. Use when the user
  invokes /insight-ooda-loop or wants repeated cycles of insight generation +
  operational testing for hard research, debugging, theorem hunting, invention,
  or strategy. Hard stop at 20 rounds or solution_found.
when-to-use: "For sustained, closed-loop research or problem-solving where insight generation and falsification testing must alternate automatically. Trigger on 'run the insight ooda loop', 'insight-ooda', 'iterate insight and test', or any request for a multi-round engine that stops only on solution or round limit. Composes /novel-insight-engine + /ooda."
allowed-tools: ["read_file", "grep", "list_dir", "search_replace", "write", "web_search", "web_fetch", "open_page", "open_page_with_find", "x_keyword_search", "x_semantic_search", "memory_search", "memory_get", "todo_write", "image_gen"]
argument-hint: "<overall research goal or problem context> [--rounds N (default 20)] [--stop-on-solution]"
metadata:
  short-description: "Closed-loop research engine: Novel Insight Engine → OODA execution → next context (max 20 rounds)"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/insight-ooda-loop/SKILL.md"
---

# Insight OODA Loop — Grok Edition

## Purpose

Run a closed research loop:

```text
Novel Insight Engine -> prediction -> goal -> OODA -> finding -> next context
```

Use this for hard research, debugging, theorem hunting, invention, or strategy work where the user wants repeated insight generation and operational testing rather than one-off advice.

## Required Composition

This skill composes two ported skills (once installed and discoverable via `/skills` or direct `/novel-insight-engine` and `/ooda`):

- **Novel Insight Engine** (`/novel-insight-engine`): produces one novel, falsifiable insight with a prediction or decision rule (see its full contract).
- **OODA** (`/ooda`): turns that prediction into action through Observe → Orient → Decide → Act with visible tokens (see its full contract).

When this skill runs, follow their core contracts. Do not paste their full text unless the user needs a reminder.

## Loop Contract

Run exactly until one of these stop conditions is reached:

```text
solution_found = true
round_number = 20   (or user-provided --rounds N)
user explicitly stops or redirects the loop
```

Do not stop because an intermediate artifact was created, a partial result was found, a useful reframing appeared, a commit landed, or the current round feels like a natural stopping point. Those are findings, not stop conditions.

If no solution is found, complete all rounds (up to the limit).

Each round has this shape:

```text
Round N Context
  current problem context
  prior OODA finding, if any
  unresolved state

NIE
  one core insight
  falsifiable prediction or decision rule
  disconfirmation condition

Goal
  set or restate the OODA goal as the NIE prediction

OODA
  Observe: inspect evidence relevant to the prediction
  Orient: classify status relative to the goal
  Decide: choose the narrowest action that tests or advances the prediction
  Act: execute and verify

Finding
  supported, weakened, falsified, unresolved, or solution_found
  evidence
  next context for the following NIE round
```

Do not skip the prediction-to-goal handoff. Do not run OODA on the original vague problem if the NIE produced a sharper testable prediction.

## Hard Execution Discipline

Before any tool call in a round, emit the round header and contract:

```text
Round N / <limit>
NIE: <one insight and falsifiable prediction>
OODA Goal: <prediction converted into the round goal>
Disconfirmation: <what would weaken or falsify this prediction>
Planned Observe: <the exact evidence or artifact to inspect>
```

After the tool call or action, emit the finding block:

```text
Finding: <supported/weakened/falsified/unresolved/solution_found>
Evidence: <concrete file, command, output, or observation>
Next Context: <input to the next NIE round>
Continue: <yes/no, with stop condition if no>
```

Do not compress multiple rounds into one explanation.
Do not silently continue a round in the background.
Do not decide on your own that a partial result is enough.
Do not make exploratory tool calls before the current round has a visible NIE prediction, OODA goal, and disconfirmation condition.

## State To Preserve

Maintain these fields in the working response or a durable artifact (use `write` to `.insight-ooda-state.md` or similar when the loop spans turns or sessions):

```text
round_number
round_limit = 20 (or user value)
current_context
nie_core_insight
nie_prediction
nie_disconfirmation
ooda_goal
ooda_observe
ooda_orient
ooda_decide
ooda_act
finding_status
finding_evidence
next_context
solution_found
stop_reason
```

For code or research repositories, preserve durable artifacts when the loop creates evidence that future turns must inspect. Keep proof status, measured status, implementation status, and unresolved status separate.

## Stop Rules

Stop immediately when one of these is true:

- `solution_found = true` (the OODA evidence verifies the original user objective, **not** merely a smaller intermediate result)
- `round_number` reaches the configured limit
- user stops or redirects the loop

Blocked work is not a normal stop condition. If a round is blocked by missing information that cannot be discovered locally with the available tools, mark the round unresolved, state the exact missing information, and continue to the next round unless the user stops or redirects. Only stop for a blocker if the blocker makes every remaining round impossible.

When stopping, state:

```text
stop_reason
rounds_completed
strongest_supported_finding
remaining_unresolved_point
next_best_action, if not solved
```

Do not use these as stop reasons:
- tactical artifact landed
- partial certificate found
- interesting reframing found
- commit completed
- enough for now
- natural checkpoint

## Goal Tool Behavior

If the user explicitly asks to set a goal for the loop, use any available goal-tracking mechanism.

Inside the loop, treat each NIE prediction as the active OODA goal for that round. Do not create a new external goal every round unless the user explicitly asks for persistent goal tracking. A round-local OODA goal is enough.

If an existing persistent goal is active, keep the full goal intact and use the round prediction as a subgoal.

## Output Shape (Active Run)

For an active run, use compact round blocks as shown in the Hard Execution Discipline section above.

Keep the output direct. The loop is for progress, not ceremony.

After each full round, consider writing a compact state snapshot with `write` so a future session or new context window can resume cleanly using `read_file`.

## Guardrails

- Do not turn the loop into brainstorming without action.
- Do not run action (Act) without a falsifiable prediction from NIE.
- Do not let a falsified prediction quietly become a weaker claim in the next round.
- Do not add premises, fallback paths, generalized frameworks, or broad side quests unless the OODA evidence requires them for the current prediction.
- Do not claim completion from indirect evidence.
- For mathematical or scientific work (especially in this PGS workspace), never collapse measured evidence into proof language. Preserve the distinction between supported, unresolved, and invalidated states.
- For factorization or PGS work, keep structure discovery separate from any `factor_found` style claims.
- Always surface relevant PGS objects, invariants, DNI, GWR, etc. in the first Observe/Orient of any round that touches this domain (per AGENTS.md).
- Respect the 20-round (or configured) hard cap. The engine is designed to be bounded.

## Success Criteria

- Every round produces the required visible header + finding blocks.
- The loop terminates only on a true stop condition with a precise statement of outcome.
- Progress (or explicit lack of progress) is documented such that a new session can resume without loss of context.
- The final strongest_supported_finding is directly traceable to the original user objective via the chain of NIE predictions and OODA verifications.
- No drift from the locked goal occurs across rounds.

## Invocation Example

`/insight-ooda-loop Close the toy-scale RSA-v2 PGS certificate using only deterministic structural invariants --rounds 12`

The loop will generate the first NIE insight/prediction, convert it to an OODA goal, execute one disciplined cycle, feed the finding back, and continue until solution or limit.

This skill turns two powerful primitives (novel falsifiable insight + disciplined execution) into a persistent research engine.
