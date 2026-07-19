---
name: codex-bus
description: >
  Full-lifecycle persisted collaboration with Codex over the agent-bus-mcp.
  Manages health checks, the canonical readiness handshake on `agent-bus-readiness`,
  creation of named research topics, threaded question/answer/message exchange with
  proper reply_to and client_message_id, cursor-aware delta sync, FTS/semantic
  history search, peer presence, and reclaim tokens. Enforces durable ledger-only
  coordination and PGS-first reasoning when working inside prime-gap-structure.
  Triggered by phrases like "use the bus with Codex", "post on the agent bus",
  "check Codex's reply", "start a codex thread", or running /codex-bus.
metadata:
  short-description: "Collaborate with Codex via the durable agent-bus MCP"
  version: "0.1.0"
  created: "2026-05-15"
---

# codex-bus — Grok + Codex Collaboration Skill

This skill gives you reliable, auditable, persisted communication with Codex (and other agents) over the shared `agent-bus-mcp` SQLite ledger.

**Core principle:** Everything that matters for coordination must be written to the bus via real MCP tool calls. Chat memory is ephemeral; the bus is the source of truth.

## Persistent Session Mode (Sticky Invocation)

**When the user invokes this skill** (by typing `/codex-bus`, running the skill from the menu, or using any trigger phrase that matches the description), the following contract takes effect for the **remainder of the session**:

- This skill becomes the active, governing frame. All subsequent agent-bus operations, all messages to or from Codex, all topic management, and any research coordination that belongs on the ledger **must** be performed through the patterns, tool-call discipline, and guardrails defined in this document.
- The mandatory `search_tool` → `use_tool` discovery rule, PGS-first reasoning (when context is prime-gap-structure), "persisted ledger only" rule, reclaim-token hygiene, small-max-items sync loops, reply_to threading, and all shape warnings are **automatically active**.
- I will not fall back to one-off ad-hoc MCP calls, forget the current readiness state (e.g., "we are waiting for Message 2"), lose track of active topic_ids and reclaim_tokens, or relax the AGENTS.md / PROOF.md boundaries.
- The skill stays loaded and in control until the user explicitly exits it with a clear command such as:
  - "exit codex-bus"
  - "/codex-bus off"
  - "end bus session"
  - "deactivate codex-bus"
  - "return to normal mode"

This "sticky" behavior exists to prevent the recurring failure where an agent correctly uses the bus for one round and then reverts to chat-only reasoning or non-persisted coordination in the next turn.

If the user has not yet invoked the skill in the current session, I operate normally. Once invoked, the above rules bind until explicit exit.

## 1. Mandatory First Step — Tool Discovery

**Never** call an `agent-bus__*` tool without first calling `search_tool` to retrieve its current input schema.

Always do:

1. `search_tool` with a precise query for the tool you need (e.g. "agent-bus sync outbox", "agent-bus topic_create").
2. Inspect the returned `tool_name` (it will be `agent-bus__ping`, `agent-bus__sync`, etc.) and the exact `input_schema`.
3. Only then call `use_tool` with the exact `tool_name` and a `tool_input` object that matches the schema.

This pattern is non-negotiable because the MCP server can evolve.

## 2. Health & Connection

```text
search_tool → "agent-bus ping"
use_tool agent-bus__ping with {}
```

Expected: `pong (0.5.0)` (or newer).

Then list open topics:

```text
search_tool → "agent-bus topic_list"
use_tool agent-bus__topic_list with {"status": "open"}
```

## 3. The Canonical Readiness Topic

The well-known coordination channel is:

- Name: `agent-bus-readiness`
- Current topic_id: `2f6aae70cd` (as of 2026-05-15)

**Current state (as of this skill creation):**
- seq 1: codex — installer/readiness status + claim
- seq 2: codex — handoff requesting Grok's durable Message 1
- seq 3: grok — pointer to test topic
- seq 4: grok — Message 1 (full acknowledgement + evidence)
- seq 5: codex — answer confirming receipt of Message 1 + request for Message 2

**Message 2 request from Codex:**
Post the formal readiness message referencing the corrected path:
`research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/design/NEIGHBORHOOD_CORPUS_SCHEMA.md`

When you see this skill loaded in a new session, first action on the bus should usually be:

1. Join `agent-bus-readiness` as agent_name `grok` (supply reclaim_token if you have one from a prior successful join).
2. `sync` with `max_items=10`, `include_self=true`, modest `wait_seconds`.
3. Determine the next expected sequence number from the returned messages.
4. Proceed with the next message in the readiness protocol or start a new research thread.

## 4. Joining Topics & Identity

You must join before you can `sync` or post.

```text
search_tool → "agent-bus topic_join"
use_tool agent-bus__topic_join with {
  "agent_name": "grok",
  "topic_id": "2f6aae70cd",           // or "name": "agent-bus-readiness"
  "reclaim_token": "<opaque token from previous successful join>"
}
```

**Important:**
- `agent_name` is reserved for the life of the topic once claimed. "grok" (or "grok-4.3") is conventional for you.
- Always store the `reclaim_token` returned on successful join. It lets you reclaim the same identity after a restart or new MCP session.
- Duplicate agent names on the same topic are rejected.

For new workstreams, prefer descriptive named topics:
- `feature/endpoint-chain-traversal`
- `research/modulus-link-probes`
- `pgs-cryptology/rsa-v2`
- `test/grok-to-codex`

Create with:

```text
search_tool → "agent-bus topic_create"
use_tool agent-bus__topic_create with {
  "name": "research/modulus-link-probes",
  "mode": "new"          // or "reuse" to get the newest open topic with that name
}
```

Then immediately join the returned `topic_id` as "grok".

## 5. Sending Messages (The Outbox)

All writes happen through `sync` with a non-null `outbox`.

Example — sending a threaded answer:

```text
search_tool → "agent-bus sync"
use_tool agent-bus__sync with {
  "topic_id": "2f6aae70cd",
  "outbox": [
    {
      "client_message_id": "grok-readiness-msg2-001",
      "content_markdown": "## Message 2 — Formal Readiness Acknowledgement\n\n...",
      "message_type": "answer",
      "reply_to": "884abc18ac",     // the codex message id you are replying to
      "metadata": {
        "sequence": "2",
        "purpose": "readiness-complete",
        "repo_path": "research/06-cryptology-rsa/experiments/pedk/rsa-v2/gap-compatibility/design/NEIGHBORHOOD_CORPUS_SCHEMA.md"
      }
    }
  ],
  "max_items": 5,
  "wait_seconds": 5
}
```

**Message type conventions:**
- `message` — general post, status, pointer
- `question` — when you are asking Codex something that requires a response
- `answer` — when replying to a question or explicit handoff

Always include a `client_message_id` (idempotency key) when the send must not be duplicated.

## 6. Reading — The Correct Sync Pattern

```text
search_tool → "agent-bus sync"
use_tool agent-bus__sync with {
  "topic_id": "<id>",
  "outbox": null,
  "max_items": 10,           // hard cap 20 — never exceed
  "include_self": true,
  "wait_seconds": 15,
  "auto_advance": true
}
```

**Rules:**
- Keep `max_items` small (≤ 10 is ideal). If `has_more` is true, loop calling sync again until `has_more=false`.
- `status=timeout` is normal when there is no new activity within `wait_seconds`.
- The response will contain the new messages in `received` (or in the text output if the client doesn't surface structuredContent).
- After a successful sync your server-side cursor for this (agent_name, topic) pair is advanced.

To replay full history (e.g. in a brand new session):

```text
search_tool → "agent-bus cursor_reset"
use_tool agent-bus__cursor_reset with {
  "topic_id": "2f6aae70cd",
  "last_seq": 0
}
```

Then call `sync` — you will receive everything from the beginning.

## 7. Searching History

```text
search_tool → "agent-bus messages_search"
use_tool agent-bus__messages_search with {
  "query": "NEIGHBORHOOD_CORPUS_SCHEMA or Message 2",
  "topic_id": "2f6aae70cd",
  "mode": "fts",           // or "semantic" or "hybrid"
  "limit": 10,
  "include_content": true
}
```

Excellent for finding specific handoffs, repo paths, or prior decisions.

## 8. Presence & Liveness

```text
search_tool → "agent-bus topic_presence"
use_tool agent-bus__topic_presence with {
  "topic_id": "2f6aae70cd",
  "window_seconds": 600,
  "limit": 50
}
```

Returns recently active peers and their `last_seq`. Use this to know whether Codex has seen your latest posts.

## 9. PGS / prime-gap-structure Guardrails (When Active Context Is This Repo)

When the working directory or research target is inside `prime-gap-structure`, the following are **non-negotiable** on any bus message you author or forward:

- Begin reasoning from PGS objects → invariants → rules → resolved/unresolved state (see AGENTS.md).
- Never downgrade proved theorems in PROOF.md to "empirical", "heuristic", "validated so far", etc.
- Classical methods (Miller-Rabin, gcd, trial division, etc.) are only for downstream audit or explicit comparison — never for choosing PGS outputs or guiding inference.
- Every coordination claim that affects research direction must be backed by a real persisted bus message, not chat memory.
- When posting research updates, always include the exact repo path(s) of the artifact(s) being discussed.

The skill must refuse or warn loudly if a proposed bus post would violate the PGS-first contract.

## 10. Recommended Research Thread Lifecycle

1. **Readiness** — Complete (or update) the handshake on `agent-bus-readiness` so both agents know the other is real and the ledger is being used.
2. **New topic** — `topic_create` with a descriptive name + `mode: "new"`.
3. **Join** as `grok` and store the reclaim_token.
4. **Post initial context** — a `message` containing:
   - The research question or invariant under study
   - Links / repo paths to the relevant files
   - The PGS objects and current state
   - A clear handoff (question or request for specific analysis)
5. **Work in threads** — use `reply_to` liberally. Keep each topic focused.
6. **Periodic sync + presence** — before important decisions, verify Codex has seen the latest seq.
7. **Search + audit** — before claiming "we decided X", search the bus for the actual decision record.
8. **Close** when the thread is resolved (optional — use `topic_close` with a reason).

## 11. Current Known Topics (as of skill creation)

- `agent-bus-readiness` (2f6aae70cd) — canonical handshake channel. Next action: post Message 2.
- `test/grok-to-codex` (dd74438893) — initial connectivity test topic (may be archived later).

Always call `topic_list` and `topic_presence` at the start of a collaboration session to discover fresh topics.

## 12. Reclaim Token Storage

After every successful `topic_join`, the returned `reclaim_token` should be stored in this session's memory or in a local file the agent can read on restart. The skill should prompt the user (or look in a conventional location) for previously captured reclaim tokens when re-joining a long-lived topic.

## 13. Example Full Flow — Posting Message 2

(See the exact Codex request in section 3. When the user says "post Message 2 on the bus", the skill should:

1. Confirm current cursor/seq via sync on readiness topic.
2. Draft a high-quality Message 2 that:
   - Acknowledges Codex's confirmation
   - Includes the exact `NEIGHBORHOOD_CORPUS_SCHEMA.md` path
   - States the current research focus (endpoint-chain, modulus-link, floor transport, etc.)
   - Proposes the next concrete step with a clear question or handoff
   - Uses `message_type: "answer"`, `reply_to` = the codex message id
   - Includes rich `metadata`
3. Show the draft to the user for approval.
4. On approval: `search_tool` → `use_tool` with the outbox.
5. Immediately `sync` again to confirm the message was accepted and to see any instant reply.

## 14. Error & Shape Warnings

If any of the following feel true, stop and surface the warning:

- "Shape feels wrong: we are about to post something that should have been a real MCP call but was only discussed in chat."
- "Shape feels wrong: the proposed message treats a classical method as the inference engine for a PGS result."
- "Shape feels wrong: we are claiming a research conclusion that is not yet written to the bus."
- "Shape feels wrong: the topic name is vague or the message lacks a concrete repo path."

Corrective action is always: make the post smaller, more specific, more fully backed by persisted evidence, and PGS-native.

## 15. Quick Reference Commands (for the agent)

- Health: `ping`
- Discover: `topic_list`, `topic_resolve "agent-bus-readiness"`
- Join: `topic_join agent_name="grok"`
- Write: `sync` with `outbox`
- Read delta: `sync` (no outbox)
- Replay: `cursor_reset last_seq=0` then `sync`
- Search: `messages_search`
- See who's there: `topic_presence`
- Finish thread: `topic_close`

Use this skill whenever the user mentions the bus, Codex, readiness, handoff, or cross-agent coordination. It exists so that future Grok instances (and Codex) inherit a correct, durable collaboration protocol instead of having to rediscover it each time.
