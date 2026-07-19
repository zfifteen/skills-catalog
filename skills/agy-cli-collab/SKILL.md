---
name: agy-cli-collab
description: >
  Sticky Grok→Gemini collaboration via direct local Antigravity CLI (`agy`) subprocess calls only.
  Use when the user invokes /agy-cli-collab, $agy-cli-collab, says "antigravity collab", or asks Grok
  to consult Gemini through the agy CLI. Never use MCP agy_* tools when this skill is active.
  Multi-turn sessions resume with --conversation (pinned UUID) or --continue fallback.
metadata:
  short-description: "Grok→Gemini via agy CLI (no MCP)"
---

# Antigravity CLI Collab

Activate when the user invokes `/agy-cli-collab`, `$agy-cli-collab`, `antigravity collab`, or asks to consult Gemini through the local Antigravity CLI.

Invoking `/agy-cli-collab` enters **Collab Mode** for the rest of the session until the user says to leave it or the session ends. Proactively call `agy` when Gemini input would help — do not wait for the user to say "ask Gemini" each turn.

## CLI-Only Rule

When this skill is active:

- Use **direct `agy` subprocess calls** or the bundled helper script only.
- **Never** call MCP tools `agy_ask`, `agy_ping`, `agy_models`, or `agy_version`.
- Do not silently fall back to MCP if a CLI call fails.

## Contract

`agy` is the live collaboration channel to Gemini (Lead Scientist role per `AGENTS.md`).

Use `agy` for:

- PGS architecture and invariant synthesis
- Large-context file analysis
- Formalization and Lean strategy
- Experiment design feedback
- Strongest objection and falsification criteria

The repository remains the source of truth for durable artifacts, code, evidence, and documentation.

Serialize `agy` calls — never run parallel subprocesses.

## Helper Script

Prefer the bundled helper for repeatable calls:

```bash
python /Users/velocityworks/.grok/skills/agy-cli-collab/scripts/agy_cli.py \
  --cwd /Users/velocityworks/IdeaProjects/prime-gap-structure \
  --mode start \
  --new-project \
  --log-file /tmp/agy-collab.log \
  --state-file /tmp/agy-conv-id.txt \
  --prompt-file /tmp/agy-task.md
```

Turn 2+ with pinned conversation:

```bash
python /Users/velocityworks/.grok/skills/agy-cli-collab/scripts/agy_cli.py \
  --cwd /Users/velocityworks/IdeaProjects/prime-gap-structure \
  --mode conversation \
  --conversation "$(cat /tmp/agy-conv-id.txt)" \
  --prompt-file /tmp/agy-task.md
```

Fallback when UUID is lost (same `cwd` only):

```bash
python ... --mode continue --prompt-file /tmp/agy-task.md
```

## Command Modes

Always `cd` to a **fixed repo root** before every call. Session resume is keyed by shell `cwd`, not `--add-dir`.

### Turn 1 — Start

```bash
cd /absolute/path/to/repo
agy --dangerously-skip-permissions \
  --add-dir /absolute/path/to/repo \
  --new-project \
  --project agy-collab-<timestamp> \
  --log-file /tmp/agy-collab.log \
  --print-timeout 10m \
  -p "$(cat /tmp/agy-task.md)"
```

Capture conversation UUID from log line `Created conversation <uuid>` into a state file.

### Turn 2+ — Pinned Resume (preferred)

```bash
cd /absolute/path/to/repo
agy --dangerously-skip-permissions \
  --add-dir /absolute/path/to/repo \
  --conversation <pinned-uuid> \
  --print-timeout 10m \
  -p "$(cat /tmp/agy-task.md)"
```

### Turn 2+ — Continue Fallback

```bash
agy --dangerously-skip-permissions --add-dir <repo> --continue -p "..." --print-timeout 10m
```

### One-Shot — Clean

```bash
agy --dangerously-skip-permissions --add-dir <repo> -p "..." --print-timeout 10m
```

No `--continue` or `--conversation`.

## Prompt Style

Write focused task briefs for Gemini (Lead Scientist).

Include:

- collaboration role and PGS-native frame first
- whether Gemini may edit files (default: read-only)
- exact repository paths
- current evidence or measured result summaries
- the precise question or design request
- required output shape

Do not send Grok's hidden reasoning. Send evidence and the question.

Default to non-mutating prompts unless the user explicitly authorizes file edits. State exact write scope when edits are allowed.

## Output Handling

After `agy` returns:

- summarize the useful contribution
- preserve material disagreement
- continue work without asking the user to mediate
- cite repo paths when Gemini's answer changes the work
- optionally include a compact **Gemini contribution** section
- integrate into one answer — do not paste Gemini's output as the final response
- do not pretend Gemini participated if the CLI call failed

## Hazards

- `--dangerously-skip-permissions` auto-approves tool execution — scope prompts carefully
- Invalid `--conversation` UUID may silently start a new thread — always capture UUID from turn-1 log
- `agy version` fails in non-TTY — use print-mode smoke for health checks
- Print mode model follows CLI settings; explicit `--model` may not apply in `-p` mode
- Long tasks need adequate `--print-timeout` (default 10m in helper)

## Failure Rule

If the `agy` CLI call fails:

- report the exact command shape and error
- do not fall back to MCP
- do not pretend Gemini participated
- continue locally only if the user explicitly asked to proceed without Gemini

## Known Good Validation

Validated on `prime-gap-structure`:

```text
agy at ~/.local/bin/agy (1.0.16)
--dangerously-skip-permissions + -p works headless
--continue preserves session per cwd
--conversation <uuid> pins exact thread
helper returns AGY_HELPER_NORMAL_OK, AGY_HELPER_CONV_OK, AGY_HELPER_CONTINUE_OK
```