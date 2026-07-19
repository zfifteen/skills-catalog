---
name: research-meeting
description: >
  Convene a structured, bounded research meeting (agenda, verbatim starting
  material, negotiated deliverable, one-question-at-a-time dialogue, raw
  transcript, and formal minutes) especially across Grok CLI instances or with
  external agents. Use when the user wants a "research meeting", "structured
  deep dive with transcript", "meeting minutes on this thesis", or needs
  rigorous, recorded multi-round exploration of a proof target, experiment,
  artifact, or high-stakes decision. Produces auditable artifacts suitable for
  later capture by research-continuity.
when-to-use: "Requests for formal research meetings with agenda, rounds, deliverable negotiation, and minutes. Strong for proof strategy, experiment design reviews, or cross-agent handoffs where a durable record is required. Complements codex-bus for ledger-backed versions and research-continuity for post-meeting state capture."
allowed-tools: ["read_file", "grep", "list_dir", "write", "search_replace", "todo_write", "memory_search", "memory_get", "web_fetch", "open_page", "run_terminal_command"]
argument-hint: "<thesis / artifact / question> [--rounds 5] [--out-dir research-meetings]"
metadata:
  short-description: "Structured research meeting with transcript and minutes (Grok CLI or local)"
---

# Research Meeting

## Purpose

Run a disciplined, time-bounded research meeting that produces a negotiated deliverable, a verbatim transcript, and formal minutes. The meeting is not ordinary chat, not sticky collaboration, and not second-opinion. It has a clear opening protocol, round discipline (one question at a time), and explicit close conditions.

This is the Grok port of the Codex "research-meeting" skill. The port adapts the Grok-CLI-centric workflow for environments that may have direct terminal access (`run_terminal_command`), the agent-bus MCP, or local subagent patterns, while preserving the original rigor and artifact shapes.

## Core Contract

The meeting starts from the user's research object (thesis, insight, proof target, experimental result, artifact, or question) and preserves that object verbatim in the opening prompt.

The meeting must produce a negotiated deliverable. Round count is only a floor, never the stop condition. Examples of good deliverables:
- Proof obligation map
- Falsification test design
- Compressed invariant candidate
- Research decision with rationale
- Clean statement of unresolved blockers + next move
- Implementation plan tied to exact artifacts

## Opening Protocol (Always Follow)

Before any "Grok" (or subagent / CLI) participation:

1. Identify the meeting agenda in one sentence.
2. Preserve the supplied starting material verbatim.
3. State current evidence, file paths, and boundaries.
4. Ask the participant to opine first on the agenda and material.
5. Ask the participant to propose or negotiate one concrete deliverable.
6. Instruct the participant to ask exactly one question after its opening opinion.

## Round Protocol (One Question at a Time)

A round = (participant response containing one question) + (your or Codex answer to that question).

For each round:
- Answer the current question directly.
- Preserve disagreement instead of smoothing.
- If multiple questions appear, answer the first substantive one and ask the participant to hold the rest.
- If no question, ask for the single most important next question.
- Classify any new invariant, experiment, or proof move proposed as: hypothesis, measured result, proof target, invalidated, or unresolved.
- Do not mutate repo files during the meeting unless the user explicitly asked for implementation as part of the deliverable.

## Completion Rule

Do not stop at the minimum round count. Close only when one of:
- The negotiated deliverable is complete and recorded.
- Both sides agree the discussion has saturated.
- A contradiction or hard blocker has been isolated sharply.
- The user-provided hard cap is reached.

## Transcript and Minutes (Mandatory Artifacts)

Before the first participation, create a meeting folder (recommended: `research-meetings/<slug>/` or `/tmp` for scratch).

Structure:
```
research-meetings/<slug>/
  transcript/
    round-00-opening.md
    round-01-participant.md
    round-01-you.md
    ...
  minutes.md
```

Minutes must record the actual path of the meeting (not a polished replacement). Include:
- Context and agenda
- Participants and command capability notes
- Negotiated deliverable
- Round log (focus, question, answer, new objects, open issues per round)
- Candidate insights
- Falsification tests
- Convergences
- Unresolved questions
- Next research move

## Helper Script (Strongly Recommended)

The ported skill ships with a deterministic Python helper:

```bash
python skills/ported-from-codex/research-meeting/scripts/research_meeting.py \
  init \
  --title "Reciprocal Left Gate" \
  --out-dir research-meetings
```

This creates the folder, `minutes.md`, and the opening prompt file using the templates in the skill.

Generate the exact CLI / invocation command:

```bash
python skills/ported-from-codex/research-meeting/scripts/research_meeting.py \
  grok-command \
  --cwd /absolute/path/to/repo \
  --prompt-file /absolute/path/to/round-00-opening.md \
  [--session-id <ID>] \
  [--max-turns 80]
```

The script will print a ready-to-paste `grok ...` command (or equivalent for your environment).

## Grok Environment Adaptations

- **Local terminal available**: Use `run_terminal_command` to execute the helper script and, if desired, to launch or resume external `grok` CLI sessions for true cross-instance meetings.
- **No external Grok CLI / pure single instance**: The skill can still be used to structure an internal multi-round dialogue with the user playing the "Codex" side, writing every round to the transcript files via `write`, and maintaining the one-question discipline manually. The resulting minutes and transcript remain first-class artifacts for `research-continuity`.
- **Agent-bus / codex-bus synergy**: For fully persisted, multi-agent (Grok ↔ Codex) meetings across restarts, prefer or combine with the `codex-bus` skill on a dedicated topic. The research-meeting artifacts can later be posted to the bus as the canonical record.
- **Subagent / task tool**: In environments that expose a `task` tool, the "other participant" can be a focused subagent prompt that receives the current round prompt file and returns one question + opinion.

## Failure Rules

- If an external Grok CLI invocation fails: record the exact command and error in the minutes. Retry once only for operational failures. Do not invent participation. Do not silently fall back to non-meeting chat.
- If the helper script is unavailable or the environment has no Python, fall back to manual creation of the meeting folder and files using `write` + the templates in this skill as guides.

## Verification

Before declaring the meeting setup complete:

```bash
python -m py_compile skills/ported-from-codex/research-meeting/scripts/research_meeting.py
```

After the meeting, confirm that `minutes.md` + transcript/ directory exist with the expected round files and that the negotiated deliverable is recorded in the minutes.

## Success Criteria

- A complete, auditable meeting folder exists with opening prompt, per-round transcript fragments, and a minutes.md that a third party can read and understand exactly what was discussed and decided.
- The one-question-at-a-time discipline was maintained.
- The deliverable is explicit and tied to concrete artifacts or decisions.
- The artifacts are suitable for immediate ingestion by `research-continuity` or posting to `codex-bus`.

## Guardrails

- This skill is for recorded, high-signal research work. It is not a general "chat in rounds" tool.
- Respect the AGENTS.md PGS-first contract in every participant prompt and in the minutes.
- Never let the meeting become an excuse for progress theater; the deliverable must be real.
- The skill itself does not execute code changes or long-running experiments unless the negotiated deliverable explicitly includes them as a final step.

This port preserves the original meeting discipline while making it practical in modern Grok environments that may mix terminal access, subagents, the agent-bus MCP, and direct file operations.
