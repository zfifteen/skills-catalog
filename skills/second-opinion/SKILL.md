---
name: second-opinion
description: >
  Before giving a final answer on a technical, architectural, or high-stakes question,
  force a rigorous second opinion. The skill prepares a complete "Second Opinion Request
  Package" (problem + rich context + orientation prompt + technical judgment prompt),
  can invoke a helper script to enrich the package with live repo state (diffs, recent
  files), and then either (a) spawns a fresh subagent for an internal second look or
  (b) outputs the package so it can be fed to another Grok instance / xAI endpoint.
  Use when the user says "/second-opinion", "force a second opinion", "get an xAI/Grok
  second opinion", "before you answer, get a second look", or explicitly wants the
  original second-opinion workflow.
when-to-use: Use when the user wants an external or fresh second technical opinion on the current blocker, proposed answer, code change, or research conclusion before proceeding. Especially valuable for high-stakes or subtle number-theoretic / architectural decisions.
argument-hint: "<the exact question or blocker; optional focus area>"
metadata:
  short-description: "Force a rigorous second opinion via prepared package + subagent or external Grok"
  source: "ported-from-codex/second-opinion"
  original_codex: "second-opinion"
---

# Second Opinion

Activate on explicit request for a second (or xAI/Grok) technical opinion.

## Core Philosophy (Preserved from Original)
- The importance of complete context cannot be overstated.
- Multiple rounds (orientation → technical judgment) are desired behavior when they improve alignment.
- Never hide material disagreement between your initial view and the second opinion.
- Do not pretend a second opinion was obtained if the mechanism fails.

## Step 1: Prepare the Request Package
1. Clearly identify the `problem`: the exact question, blocker, or decision the user wants a second opinion on.
2. Assemble rich `context`:
   - Use `read_file` / `grep` on all relevant code, tests, logs.
   - Use `run_terminal_cmd` for `git diff --cached`, `git diff`, `git log -10`, recent changes.
   - Capture your own proposed answer or current reasoning so far.
   - Include constraints, failed assumptions, unresolved PGS states (if in this repo).
3. (Optional but recommended) Run the helper script to further enrich the package with live workspace state.

## Step 2: Use the Helper Script (Recommended)
From the directory containing this SKILL.md (the system gives you the path), the helper lives at:
`scripts/call_second_opinion.py`

Invoke it via `run_terminal_cmd` (the agent runtime provides `run_terminal_cmd`):

```bash
python3 "<absolute-path-to-this-skill-dir>/scripts/call_second_opinion.py" <<'JSON'
{
  "problem": "Exact question or blocker here",
  "context": "Rich multi-paragraph context with file excerpts, diffs, your current thinking, constraints...",
  "focus": "Optional narrow focus area for the opinion",
  "mode": "package"   # or "local-review"
}
JSON
```

The script will:
- Validate and pretty-print the input.
- Optionally run `git status/diff/log` in the current workspace and append a "Live Workspace Snapshot" section.
- Output a complete, ready-to-paste "Second Opinion Request Package" in Markdown (with clear Orientation Round and Technical Judgment Round prompts).
- For `mode=local-review`: also emit a self-contained verifier prompt you can feed to a `task` subagent right now.

## Step 3: Obtain the Second Opinion
Two primary paths in the Grok environment:

**Path A — Internal Fresh Subagent (fast, same context window limitations)**
- Use the `task` tool (or equivalent subagent spawn) with `run_in_background: false`.
- Seed the subagent with the full Orientation prompt from the package first.
- On completion, resume or start a second task for the Technical Judgment round, passing `previous_response_id` equivalent (the subagent transcript) or simply the orientation result.
- Look for explicit acknowledgment of the big picture before the narrow judgment.

**Path B — External / Another Grok Instance (stronger isolation)**
- Take the complete package emitted by the helper script.
- Paste it into a fresh Grok chat (or another xAI model via API / grok.com).
- Or post relevant parts to X and use the `x-api` MCP tools for community second opinions on public aspects.
- Return the external response verbatim (rendered, not raw JSON).

**Path C — MCP Harness (if you have an equivalent xai_second_opinion MCP configured)**
- The original Codex script called a stdio MCP server defined in `~/.codex/config.toml`.
- In this environment, if an equivalent MCP server exposing a `second_opinion` tool is connected, call it directly using the MCP function calling protocol.
- The helper script can be extended later to support stdio MCP calls the same way the Codex version did (it already contains the structural skeleton).

## Step 4: Integrate and Decide
After receiving the second opinion:
- State it plainly.
- Note whether the orientation round was properly completed (big-picture acknowledgment before narrow judgment).
- Explicitly call out points of agreement and material disagreement with your own initial reasoning.
- Decide (and tell the user) whether the second opinion changes the plan, confirms it, or surfaces new risks.
- Proceed with the stronger combined path.

## Failure Handling
- If the helper script fails: report the exact error and continue only if the task is urgent and non-destructive.
- If no second opinion mechanism is available: say so plainly. Do not fabricate one. Offer to do a structured self-review using the local-review mode of the script instead.

## Output Rule
Never hide the second opinion or the comparison. Display both your query/package and the received opinion as rendered rich text.

## For This Repo (PGS)
When the question touches prime-gap structure, divisor field, GWR, DNI, chamber resets, or any proved PGS law, the second opinion prompt **must** explicitly instruct the reviewer to evaluate against the deterministic PGS frame in AGENTS.md, not classical probabilistic number theory defaults.

## Related Skills
- `/grade-ten` (ask the second opinion to also be delivered in Grade 10 English)
- `/check` (the bundled verifier skill — good complement for code changes)
- The GitHub analysis skills (to give the reviewer full repo context)
