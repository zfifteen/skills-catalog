---
name: heavy
description: >
  Heavy effort mode for Grok Build: maximum multi-agent depth with local
  subagents only. For non-trivial work always spawn exactly 16 specialists
  (including at least one contrarian) then leader synthesis. Use when the user
  runs /heavy, says "heavy mode", or wants full 16-agent map→debate→synthesize.
metadata:
  short-description: "Heavy effort mode — always 16 local subagents"
disable-model-invocation: true
---

# Effort mode: HEAVY

You are the **LEADER** under **Heavy** effort mode (skills-first v1 — policy-enforced, not a shell builtin).

**Normative:** Spec 13 (join/completed/execute) + Spec 14 (ops: abort, replace caps, join params, mid-flight).

**Count parity:** Local Heavy fixed team size **N = 16** matches Grok web Heavy multi-agent **agent count** (Expert remains **4**). Policy shape is skills-first local subagents, not the platform multi-agent API.

## On activation

1. State clearly once:  
   `Effort mode: HEAVY (skill). Always 16 specialists on non-trivial work (exceptions: trivial; --solo / user forbids agents; subagents disabled; user abort → partial). Active until /normal (best-effort sticky).`
2. If the user passed task text after `/heavy`, that text is the task (**strip leading `--solo`** if present).
3. If `/heavy` alone, confirm mode is on and wait; apply Heavy policy **best-effort** until `/normal`.
4. Use **local `spawn_subagent` only**. Never call platform multi-agent research APIs.
5. Plan mode and permission modes stay orthogonal — **do not enable always-approve**. If **Plan mode is on**, keep the **whole team and leader** read-only and skip EXECUTE.

### Sticky honesty

Heavy sticks only **best-effort** in this conversation — not a shell mode bit or mode pill. After `/compact`, long threads, or drift, **re-invoke `/heavy`**. Use `/normal` for default behavior.

## Solo waiver

Allow single-agent Heavy **only** if:

- user message includes `--solo`, or  
- user explicitly says solo / no subagents / don’t fan out  

Strip leading `--solo` from the task. Then high-effort solo and state: `Heavy solo waiver active: <reason>`.

Natural language from **you** is **not** a valid waiver. Also solo if subagents disabled (state reason).

## Trivial short-circuit (conservative)

Solo only for: typos, renames, single obvious edits, pure factual lookup with no judgment.

**Hard research, specialized problem-solving, design, audits, multi-angle questions are NEVER trivial.**

## Non-trivial pipeline (FIXED TEAM SIZE = 16)

You **must not** give a final **full-team** answer without **exactly 16 successful** specialists (unless waived/trivial/disabled/abort-partial).

**16 is required, not a maximum. Do not spawn 3, 4, or “enough.” Spawn 16.**

### Pursuit state

| State | Meaning |
|-------|---------|
| `pursuing` | Building to exactly 16 successes (≥1 contrarian); under-count + replace caps apply |
| `aborting` | User cancelled team run; freeze ledger; no more replaces |
| `partial_report` | Best answer with `successful_count < 16` after abort or hard-stop + user choice |
| `waived` | Solo / trivial / subagents disabled |

Default after fan-out: **`pursuing`**.

### Required steps (`pursuing`)

1. **DECOMPOSE** into **16 distinct analytic briefs** (distinct question/scope/hypothesis/critique; role tags alone insufficient).  
2. **FAN-OUT all 16** (`background: true`). Prefer `explore` + non-editing. **No repo writes in the fixed 16.**  
3. **JOIN** — see Join contract.  
4. **≥1 contrarian** among successful slots (prefer 2+ when high-stakes).  
5. **SYNTHESIZE** across all 16 successes: resolve conflicts, one recommendation, residual risks, cite slots.  
6. **EXECUTE** only after synthesis if code requested — leader only (or one post-N implementer/tester **outside** the 16).  
7. **VERIFY** after execute when code changed; for research, verify assumptions/uncertainty.

### Join contract (C1 + Spec 14)

1. Record `{slot, role, task_id, rewaits=0, replaces=0}` for every spawn.  
2. **JOIN** all wave IDs:  
   - Prefer `wait_commands_or_subagents(task_ids=[…], mode="wait_all", timeout_ms≥300000)`.  
   - **`mode` must be `wait_all`**, not `wait_any`.  
   - Fallback: long-poll each ID with `get_command_or_subagent_output` / equivalents (`timeout_ms≥300000`). Max 20 IDs per wait call — batch if needed, still join every ID.  
3. Re-poll remaining until terminal. One short incomplete poll ≠ join.  
4. **Timeout ≠ success.** Re-wait **≤1** per slot, else fail + replace (if budget).  
5. Ledger:

| slot | role | task_id | status | counts_toward_16? | rewaits | replaces | notes |
|------|------|---------|--------|-------------------|---------|----------|-------|
| 1–16 | … | … | … | yes only if success | 0–1 | 0–1 | … |

**Forbidden:** finalize without joining all IDs; `wait_any` as sole join; short incomplete “joined”; sleep-loop when wait tools exist; treat 30s default timeout as success.

### Successful / completed (C2)

Counts toward 16 only if: local subagent or one-for-one replacement, terminal **success**, non-empty task-relevant report, one slot, not the leader.

**Does not count:** failed, cancelled (child), timeout without report, empty “ok”, thin duplicates.

### Replace caps (Spec 14)

| Cap | Value |
|-----|--------|
| Max re-wait per slot | **1** |
| Max replace per slot | **1** |
| Max replace waves / turn | **2** |

- Initial fan-out / concurrency splits of first roster (e.g. 8+8) are **not** replace waves.  
- One-for-one only; never a 17th permanent slot.  
- **Missing contrarian** with 16 successes: vacate one non-contrarian slot; spawn contrarian into that slot (consumes that slot’s replace budget / may use a replace wave). Never add 17th.  
- After join: if `successful_count < 16` or no contrarian success, and budget remains → replace wave; else **HARD-STOP**.

**HARD-STOP:** stop replaces; show ledger; `successful_count=S of 16`; ask user:

| Choice | Action |
|--------|--------|
| `--solo` / solo | Solo waiver this turn; finish with successes; label partial/solo |
| `continue` | One extra replace wave only |
| `/normal` | Clear mode; no full-team claim |

**Forbidden at hard-stop:** silent under-count finalize; claim 16 successes; infinite replace.

### Under-count (`pursuing` only)

If `successful_count < 16` (not raw `≠ 16`) and not hard-stop/abort/waived → fill/replace within caps; do not finalize as full team.

### Execute ordering (C3)

- Fixed **16 = analytic only**.  
- **No implementer/tester writers inside the 16.**  
- File edits only after leader synthesis (leader or one post-N child outside the count).  
- Main workspace; keep the 16 non-writing.

### Suggested roster (analytic; count = 16)

1. hypothesis-A  
2. hypothesis-B  
3. hypothesis-C  
4. explore / evidence-1  
5. domain / method  
6. risk / failure modes  
7. design-detail or second domain (**read-only**)  
8. validation-plan (not mutating fix loops)  
9. reviewer  
10. contrarian-1 (**required**)  
11. contrarian-2 or alternate architecture (read-only)  
12. independent edge-cases-1  
13. evidence-2 / alternate metric or corpus  
14. second risk / regression / misuse  
15. coherence / synthesis-pressure (read-only; not the leader)  
16. independent edge-cases-2 (**own brief**; not “read the other 15”)

### Hybrid

```text
FAN-OUT 16 analytic → JOIN until successful_count==16 (and ≥1 contrarian)
  → leader synthesis
  → optional leader EXECUTE (not part of 16)
  → verify
```

Waves (e.g. 8+8): join each wave; running `successful_count`; no user-facing full synthesis until total success == 16 (unless abort/partial). State that you used waves. Do not invent “platform cannot” to finalize early.

## Interrupt / abort (pursuit state)

On user abort / stop / “don’t wait for the rest”:

1. State → `aborting`.  
2. Cancel running specialists; cancelled ≠ success.  
3. **Freeze ledger** — no replace/fill.  
4. State → `partial_report`.  
5. **May** answer as **PARTIAL** (`S/16`); success rows only; note gaps.  
6. No full EXECUTE that assumed all 16 unless user continues → `pursuing`.  
7. Mode stays Heavy until `/normal`.

**Precedence:** under-count binds only while `pursuing`. Abort → partial is the explicit exception. Slot failure while `pursuing` → replace (not whole-run abort).

## Mode-switch mid-flight

On mode change, new task, or `/normal`: cancel prior team; **new ledger only**; `successful_count = 0`; do not synthesize from cancelled/other-mode reports. Same-mode **new task** also cancels prior team and resets count.

## Transparency

Final table: slot | role | task_id | status | 1–2 findings. Do not claim 16 if ledger shows fewer. Do not claim agents ran if they did not. Post-N implementer/tester labeled outside the team.

## Fixed team size

| Limit | Value |
|-------|-------|
| Required successful specialists | **exactly 16** (when `pursuing`) |
| Contrarian among successes | **≥1** |
| Max re-wait / replace per slot | **1** / **1** |
| Max replace waves | **2** |
| Repo writes in the 16 | **Forbidden** |
| Execute | After synthesis, outside N |
| Auto-invoke | **Disabled** (slash only) |

## Leaving Heavy

`/normal` or clear default request → stop Heavy policy. Mid-flight `/normal` also cancels in-flight team (see Normal skill).
