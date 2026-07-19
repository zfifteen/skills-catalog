---
name: expert
description: >
  Expert effort mode for Grok Build: high-quality work with a fixed specialist
  team of exactly 4 local subagents, then leader synthesis and self-review. Use
  when the user runs /expert, says "expert mode", or wants a full 4-agent team
  without Heavy’s 16-agent depth.
metadata:
  short-description: "Expert effort mode — always 4 local subagents"
disable-model-invocation: true
---

# Effort mode: EXPERT

You are the **leader** under **Expert** effort mode (skills-first v1 — policy-enforced, not a shell builtin).

**Normative:** Spec 13 (join/completed/execute) + Spec 14 (ops: abort, replace caps, solo, join params).

## On activation

1. State clearly once:  
   `Effort mode: EXPERT (skill). Always 4 specialists on non-trivial work (exceptions: trivial; --solo / user forbids agents; subagents disabled; user abort → partial). Active until /normal (best-effort sticky).`
2. Prefer higher reasoning quality over speed.
3. If the user passed task text after `/expert`, that text is the task (**strip leading `--solo`** if present — see Solo).
4. If `/expert` alone, confirm mode is on and wait; apply Expert policy to later work **best-effort** until `/normal`.
5. Use **local `spawn_subagent` only**. Never call platform multi-agent research APIs.
6. Plan mode and permission modes stay orthogonal — **do not enable always-approve**. If **Plan mode is on**, keep the **whole team and leader** read-only and skip EXECUTE.

### Sticky honesty

Expert sticks only **best-effort** in this conversation — not a shell mode bit or mode pill. After `/compact`, long threads, or drift, **re-invoke `/expert`** so the policy is explicit again. Use `/normal` for default Grok Build behavior.

## Solo waiver

Allow single-agent Expert **only** if:

- user message includes `--solo`, or  
- user explicitly says solo / no subagents / don’t fan out  

Strip leading `--solo` from the task text. Then high-effort solo work and state: `Expert solo waiver active: <reason>`.

Natural language from **you** (“I’ll just do it alone”) is **not** a valid waiver.

Also solo when: trivial short-circuit; subagents disabled (state the reason).

## Trivial short-circuit (conservative)

Solo (no team) **only** for: typos, renames, one-line obvious fixes, pure factual lookup with no judgment.

**Never** treat hard research, specialized problem-solving, architecture, audits, or multi-file work as trivial just because there are no edit verbs.

When solo under an exception, state: `Expert solo exception active: <reason>`.

## Non-trivial pipeline (FIXED TEAM SIZE = 4)

You **must not** give a final **full-team** answer without **exactly 4 successful** specialists (unless waived/trivial/disabled/abort-partial).

**4 is required, not a maximum. Do not spawn 1–3 “enough.” Spawn 4.**

### Pursuit state

| State | Meaning |
|-------|---------|
| `pursuing` | Building to exactly 4 successes; under-count + replace caps apply |
| `aborting` | User cancelled the team run; freeze ledger; no more replaces |
| `partial_report` | Delivering best answer with `successful_count < 4` after abort or replace hard-stop + user choice |
| `waived` | Solo / trivial / subagents disabled |

Default after fan-out: **`pursuing`**.

### Required steps (`pursuing`)

1. Orient (constraints, goal, risks).  
2. **DECOMPOSE** into **4 distinct analytic briefs** (differ in question, scope, hypothesis, or critique target; role tags alone insufficient).  
3. **FAN-OUT all 4** (`background: true`). Prefer `explore` / non-editing. **No repo writes in the fixed 4.**  
4. **JOIN** — see Join contract.  
5. **SYNTHESIZE** across all 4 success reports: resolve conflicts, one recommendation, **residual risks**, **cite slots**.  
6. **EXECUTE** only after synthesis if code requested — leader only (or one post-N implementer/tester **outside** the 4).  
7. **VERIFY** after execute when code changed; for research, verify assumptions/uncertainty.  
8. Prefer one coherent solution.

### Join contract (C1 + Spec 14)

1. Record `{slot, role, task_id, rewaits=0, replaces=0}` for each spawn.  
2. **JOIN** all wave IDs with platform tools:  
   - Prefer `wait_commands_or_subagents(task_ids=[…], mode="wait_all", timeout_ms≥300000)` when available.  
   - **`mode` must be `wait_all`**, not `wait_any`, for the fixed team.  
   - If multi-id wait is unavailable, long-poll each ID with `get_command_or_subagent_output` / equivalents (`timeout_ms≥300000`).  
3. **Re-poll until terminal** on remaining IDs. One short incomplete poll ≠ join.  
4. **Timeout ≠ success.** Incomplete → re-wait that ID **at most once** per slot; else mark failed and replace (if budget).  
5. Ledger before synthesis:

| slot | role | task_id | status | counts_toward_4? | rewaits | replaces | notes |
|------|------|---------|--------|------------------|---------|----------|-------|

**Forbidden:** finalize without joining all IDs; `wait_any` as sole join for the full team; claim joined after one short poll; sleep-loop when wait tools exist; treat default 30s timeout as success.

### Successful / completed (C2)

Counts toward 4 only if: local subagent (or slot replacement), terminal **success**, **non-empty** task-relevant report, one slot, not the leader.

**Does not count:** failed, cancelled (child), timeout without report, empty “ok”, thin duplicates.

### Replace caps (Spec 14)

| Cap | Value |
|-----|--------|
| Max re-wait per slot | **1** |
| Max replace per slot | **1** |
| Max replace waves / turn | **2** |

- Initial fan-out (and concurrency splits of first roster) is **not** a replace wave.  
- One-for-one only; never a 5th permanent slot.  
- After each join: if `successful_count < 4` and replace budget remains → one replace wave → join; else if still short → **HARD-STOP**.

**HARD-STOP:** stop replaces; show ledger; state `successful_count=S of 4`; ask user:

| Choice | Action |
|--------|--------|
| `--solo` / solo | Solo waiver for this turn; finish with successes; label partial/solo |
| `continue` | One extra replace wave only; then re-check |
| `/normal` | Clear mode; no full-team claim |

**Forbidden at hard-stop:** silent under-count finalize; claim 4 successes; infinite replace.

### Under-count (`pursuing` only)

If `successful_count < 4` and not hard-stop/abort/waived → fill/replace within caps; do not finalize as full team.

### Execute ordering (C3)

- Fixed **4 = analytic only**.  
- **No implementer/tester writers inside the 4.**  
- Repo writes only after synthesis (leader or one post-N child outside the count).  
- Main workspace; keep the 4 non-writing.

### Suggested roster (analytic; count = 4)

1. explore / hypothesis-A  
2. hypothesis-B / alternate angle  
3. reviewer / validation-plan (read-only)  
4. contrarian (prefer on non-trivial research/design)

## Interrupt / abort (pursuit state)

On user abort / stop / “don’t wait for the rest”:

1. State → `aborting`.  
2. Cancel running specialists; cancelled ≠ success.  
3. **Freeze ledger** — no replace/fill for this task.  
4. State → `partial_report`.  
5. **May** answer with `successful_count < 4` as **PARTIAL** (`S/4`); synthesize only success rows; note gaps.  
6. No full EXECUTE that assumed all 4 unless user explicitly continues → back to `pursuing`.  
7. Mode stays Expert until `/normal`.

**Precedence:** under-count forbids early finish only while `pursuing`. Abort → `partial_report` is the explicit exception.

## Mode-switch mid-flight

On mode change, new task, or `/normal`: cancel prior team; **new ledger only** (never mix); `successful_count = 0`; do not synthesize from cancelled/other-mode reports. Re-invoke same mode with a **new** task also cancels prior team and resets count.

## Transparency

Prefer full ledger table + per-slot findings. Do not claim 4 if ledger shows fewer. Do not claim agents ran if they did not. Post-N implementer/tester labeled outside the team.

## Fixed team size

| Limit | Value |
|-------|-------|
| Required successful specialists | **exactly 4** (when `pursuing`) |
| Max re-wait / replace per slot | **1** / **1** |
| Max replace waves | **2** |
| Repo writes in the 4 | **Forbidden** |
| Execute | After synthesis, outside N |
| Auto-invoke | **Disabled** (slash only) |

## Leaving Expert

`/normal` or clear request for default → stop Expert policy. Mid-flight `/normal` also cancels in-flight team (see Normal skill).
