---
name: grok-cli-collab
description: Use when the user invokes /grok-cli-collab, $grok-cli-collab, asks Codex to collaborate with Grok through the local Grok CLI, says to call Grok directly, or wants sticky Grok CLI collaboration for the rest of the session.
---

# Grok CLI Collab

Use this skill when Codex should collaborate with Grok through the local Grok CLI.

## Sticky Session Behavior

When the user invokes this skill, keep using Grok CLI collaboration for the rest
of the current Codex session unless the user explicitly says to stop, disable
it, or switch collaboration modes.

Do not wait for the user to say "check Grok" or "ask Grok" during an active
collaboration loop. When Grok input is useful, call Grok directly.

## Contract

Grok CLI is the live collaboration channel.

Use Grok CLI for:

- peer reasoning;
- second-pass pressure;
- research objections;
- experiment design feedback;
- repo-aware technical judgment;
- follow-up questions that would otherwise require the user to relay messages.

Do not use Agent Bus MCP as the live back-and-forth channel when this skill is
active. Do not use the xAI API Grok path for this mode.

The repository remains the source of truth for durable artifacts, code,
evidence, outputs, and documentation.

## Command Modes

Always pass the working directory explicitly.

### Normal Mode

Use normal mode for live collaboration, follow-up questions, and repo-aware
discussion that should preserve the current Grok session:

```bash
grok \
  --cwd /absolute/path/to/repo \
  --always-approve \
  --continue \
  --prompt-file /tmp/grok-task.md \
  --output-format plain \
  --max-turns 3
```

Use the current repository root as `--cwd`. For the prime-gap-structure repo,
that is:

```text
/Users/velocityworks/IdeaProjects/prime-gap-structure
```

Use `--continue` by default to preserve the most recent Grok session for the
working directory. Use `--resume <SESSION_ID>` only when the user or prior
evidence identifies a specific Grok session to continue.

Use `--always-approve` every time. The local Grok project may be untrusted, and
this flag prevents approval prompts from stalling collaboration.

Use `--output-format plain` by default. Grok's JSON output includes extra
metadata and may expose fields that are noisy for ordinary collaboration.

### Parallel Reasoning Mode

Use parallel reasoning mode when the next Grok call should pressure a result
from multiple attempts without carrying prior session state:

```bash
grok \
  --cwd /absolute/path/to/repo \
  --always-approve \
  --best-of-n 2 \
  --prompt-file /tmp/grok-task.md \
  --output-format plain \
  --max-turns 10 \
  --disable-web-search
```

Do not use `--continue` in parallel reasoning mode. The clean prompt and the
repository state are the intended context.

### Role-Agent Mode

Use role-agent mode when the research needs explicit lenses, such as boundary
critic, experiment designer, grammar compressor, or evidence auditor:

```bash
grok \
  --cwd /absolute/path/to/repo \
  --always-approve \
  --best-of-n 3 \
  --agents '{"boundary_critic":{"description":"Pressure-test candidate PEDK rules","instructions":"Find falsification risks and public-state boundary failures."}}' \
  --prompt-file /tmp/grok-task.md \
  --output-format plain \
  --max-turns 10 \
  --disable-web-search
```

Do not use `--continue` in role-agent mode until clean isolation from old bus
context has been revalidated.

## Helper Script

Prefer the bundled helper for repeatable CLI calls:

```bash
python /Users/velocityworks/.codex/skills/grok-cli-collab/scripts/grok_cli.py \
  --cwd /Users/velocityworks/IdeaProjects/prime-gap-structure \
  --max-turns 3 \
  --prompt-file /tmp/grok-task.md
```

Normal helper mode invokes:

```text
grok --cwd <cwd> --always-approve --continue --prompt-file <file> --output-format plain
```

Parallel helper mode starts a clean Grok run:

```bash
python /Users/velocityworks/.codex/skills/grok-cli-collab/scripts/grok_cli.py \
  --mode parallel \
  --best-of-n 2 \
  --cwd /Users/velocityworks/IdeaProjects/prime-gap-structure \
  --prompt-file /tmp/grok-task.md
```

Role-agent helper mode reads the JSON agent map from a file:

```bash
python /Users/velocityworks/.codex/skills/grok-cli-collab/scripts/grok_cli.py \
  --mode roles \
  --best-of-n 3 \
  --agents-file /tmp/grok-agents.json \
  --cwd /Users/velocityworks/IdeaProjects/prime-gap-structure \
  --prompt-file /tmp/grok-task.md
```

It also avoids zsh's read-only `status` variable issue by managing exit codes
inside Python.

## Prompt Style

Write Grok prompts as focused task briefs.

Include:

- the collaboration role;
- whether Grok may edit files;
- exact repository paths when relevant;
- current evidence or result summaries;
- the precise question or objection requested;
- required output shape.

Default to non-mutating prompts unless the user explicitly asks Grok to edit
or implement. If Grok may edit files, state the exact write scope.

For research work, ask Grok for:

- strongest objection;
- falsification criterion;
- next measurable object;
- interpretation of a measured result;
- one concrete experiment design.

For parallel and role-agent calls, make the prompt self-contained. Include the
measured result, exact paths, candidate rule, falsification boundary, and
requested output shape because those modes do not inherit the live session.

Do not send Grok Codex's hidden reasoning. Send the evidence and the question.

## Output Handling

After Grok returns:

- summarize the useful contribution;
- preserve material disagreement;
- continue the work without asking the user to mediate;
- cite repo paths and measured outputs when Grok's answer changes the work;
- do not pretend Grok participated if the CLI call failed.

If Grok proposes an experiment or code change, Codex remains responsible for
reviewing, implementing, and validating it in the shared repo.

## Known Good Validation

This command shape has been validated in `prime-gap-structure`:

```text
--cwd set the repo root correctly
--always-approve allowed read-only tool execution
--continue preserved session continuity
--prompt-file worked for task transport
plain stdout capture worked
normal helper mode returned GROK_HELPER_NORMAL_CHECK_OK
parallel helper mode returned GROK_HELPER_PARALLEL_OK
role-agent helper mode returned GROK_HELPER_ROLES_OK
```

The Grok CLI `--check` flag is not a lightweight dry run in this workflow. It
can consume internal turns and fail with `max_turns exceeded`; validate helper
changes with real plain-output smoke prompts instead.

The active tested Grok session id was:

```text
019e2e0b-ca71-7a22-a28e-b7ca6d0b4400
```

## Failure Rule

If the Grok CLI call fails:

- report the exact command shape and error;
- do not silently fall back to Agent Bus or xAI API;
- do not pretend Grok participated;
- continue locally only if the user has asked Codex to proceed despite Grok
  being unavailable.
