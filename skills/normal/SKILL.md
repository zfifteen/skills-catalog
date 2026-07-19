---
name: normal
description: >
  Leave Expert/Heavy effort modes and return to default Grok Build behavior.
  Use when the user runs /normal, says "normal mode", "exit heavy", "exit expert",
  or wants to clear multi-agent effort policy overlays.
metadata:
  short-description: "Clear Expert/Heavy — back to normal"
disable-model-invocation: true
---

# Effort mode: NORMAL

Clear **Expert** and **Heavy** skill policies.

## On activation

1. State clearly: `Effort mode: NORMAL. Expert/Heavy policy overlays cleared.`
2. Resume default Grok Build behavior for this conversation:
   - No Expert/Heavy multi-agent gates or team size targets from those skills  
   - No requirement to fan out specialists  
   - Normal single-agent (or ad-hoc subagent) judgment  
3. Do **not** change the user’s permission mode, Plan mode, or model unless they ask.
4. If they had a pending task in the same message after `/normal`, handle it with default behavior.

## Mid-flight clear (Expert/Heavy team in progress)

If `/normal` arrives while an Expert/Heavy fixed team is still running, incomplete, or mid-join:

1. **Mode off first** — stop applying Expert/Heavy policy immediately (no fixed-N fill/replace, no contrarian repair, no “must reach N successes”).
2. **Cancel running specialists (best-effort)** — for every known running effort-mode task ID, call `kill_command_or_subagent` (or session equivalent). Prefer kill-all from the current ledger. If kill is unavailable, say so; do **not** keep joining to finish the team.
3. **Abandon the incomplete team** — no replacements, no waves to 4/16, cancelled ≠ success, do not claim Expert/Heavy completion.
4. **State partial counts** — e.g.  
   `Effort mode: NORMAL. Abandoned in-flight <Expert|Heavy> team: successful=K of N; running/cancelled=R; failed=F. Fixed-N gates dropped.`  
   (N=4 Expert, N=16 Heavy.)
5. **Partial context only if useful** — may use already-successful reports as ordinary Normal context; label as abandoned-team findings, **not** a completed Expert/Heavy synthesis.
6. **Same-message task** — handle with default Normal behavior; not bound to abandoned N.

**Contrast:** User stop/Ctrl+C **without** `/normal` cancels children but **keeps** Expert/Heavy sticky. **`/normal` mid-flight** cancels **and** clears the mode.

**Forbidden after mid-flight `/normal`:** re-entering Expert/Heavy gates “to finish cleanly”; waiting out full join for N; claiming N specialists completed.

## Mode-switch mid-flight

On `/normal` (or leaving Expert/Heavy): cancel prior team; discard their ledger; do not mix prior specialist results into Normal work as if a full team finished.

## Notes

- This skill cannot reset shell “mode pills” or product builtins (skills-first v1).  
- It **does** instruct you to stop following Expert/Heavy skill contracts.  
- If the user later runs `/expert` or `/heavy`, those policies apply again.  
- Slash-only entry: model auto-invoke is disabled (`disable-model-invocation: true`).
