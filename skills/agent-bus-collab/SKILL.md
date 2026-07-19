---
name: agent-bus-collab
description: Use when the user asks Codex to coordinate with Grok or another local peer agent through Agent Bus MCP, mentions agent-bus, bus topics, readiness handshakes, shared MCP coordination, peer handoffs, or asks to send/read messages through the bus.
---

# Agent Bus Collab

Use this skill when Codex needs to coordinate with Grok or another local agent through Agent Bus MCP.

## Session Persistence

When the user invokes this skill, continue using it for the rest of the current session unless the user explicitly turns it off or redirects away from bus coordination.

While active:

- check the relevant bus topic before making shared-area claims or edits;
- post meaningful status, handoffs, and blockers to the bus;
- read peer replies from the bus before treating them as durable coordination state;
- keep using the repository, not the bus, for durable artifacts.

## Contract

Agent Bus is a coordination ledger. The repository remains the source of truth for durable research artifacts, code, evidence, and claims.

Use the bus for:

- status;
- task claims;
- handoffs;
- objections;
- readiness checks;
- coordination questions;
- paths to repo artifacts.

Do not use the bus as the durable location for research evidence, proofs, experiment output, or final reports. Put those in the repo and link the path from the bus.

## Identities

Use stable agent names:

- Codex: `codex`
- Grok: `grok`

Runtime and model details belong inside the message body when relevant, not in the bus identity.

## Message Shape

Use this lightweight structure unless the message is genuinely tiny:

```markdown
agent: codex
runtime: Codex Desktop
model: GPT-5

## Status
...

## Claim / Observation
...

## Evidence
...

## Request / Handoff
...

## Boundary
...
```

For questions and replies, use Agent Bus `message_type='question'` and `message_type='answer'` when the tool exposes that field. Use `reply_to` when answering a specific bus message.

## Start Of Session

Before claiming or editing work in an active shared area:

1. Resolve or create the relevant topic.
2. Join as `codex`.
3. Replay from sequence 0 or from the last known cursor.
4. Check for recent claims, blockers, or handoffs.
5. Post a short claim/status before making overlapping edits.

For the standing readiness topic:

```text
topic name: agent-bus-readiness
topic id: 2f6aae70cd
```

## Tool Use

Prefer native Agent Bus MCP tools when they are exposed in the current Codex session:

- `ping`
- `topic_create`
- `topic_list`
- `topic_resolve`
- `topic_join`
- `cursor_reset`
- `sync`
- `topic_presence`
- `messages_search`

If the native Agent Bus tools are not surfaced but the local server is installed, use the bundled helper script as the explicit transport to the same MCP server. This is not a substitute protocol; it calls the installed Agent Bus MCP server over stdio.

Helper:

```bash
python /Users/velocityworks/.codex/skills/agent-bus-collab/scripts/agent_bus.py --help
```

The helper uses:

```text
uvx --from agent-bus-mcp==0.5.0 agent-bus
AGENT_BUS_DB=/Users/velocityworks/.agent_bus/agent_bus.sqlite
```

## Common Commands

Replay a topic:

```bash
python /Users/velocityworks/.codex/skills/agent-bus-collab/scripts/agent_bus.py history agent-bus-readiness
```

Post a message from a Markdown file:

```bash
python /Users/velocityworks/.codex/skills/agent-bus-collab/scripts/agent_bus.py post agent-bus-readiness /tmp/message.md --type status
```

Check health:

```bash
python /Users/velocityworks/.codex/skills/agent-bus-collab/scripts/agent_bus.py ping
```

## Readiness Sign-Off

For a new peer setup, require a real handoff simulation:

1. Codex posts first if Codex installed the bus.
2. Grok reads Codex's message from the bus and acknowledges on the bus.
3. Grok posts a formal readiness message with one repo path and one coordination claim.
4. Codex replays the topic, confirms ordering and identities, and replies on the bus.
5. Both agents post exactly:

```text
READY: Agent Bus MCP usable for peer coordination.
```

## Failure Rule

If the bus is unavailable, say exactly what failed:

- missing MCP config;
- server not surfaced in the current toolset;
- different `AGENT_BUS_DB`;
- topic not found;
- agent name already reserved and no reclaim token;
- sync returned no peer message.

Do not pretend a chat-transcribed draft was posted to the bus. Only persisted bus messages count.
