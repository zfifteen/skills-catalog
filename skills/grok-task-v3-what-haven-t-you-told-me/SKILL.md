---
name: what-haven-t-you-told-me
description: >
  Surface anything important about the current work, research program, codebase,
  or conversation that has not yet been communicated explicitly. Use when the
  user invokes /what-haven-t-you-told-me, "what haven't you told me", "what have
  you been holding back", "unsaid implications", "elephant in the room", or
  simply wants the AI to volunteer high-value observations that the explicit
  questions have not yet elicited. Strong for long-running research threads,
  complex codebases, or high-stakes decisions where drift or hidden assumptions
  accumulate.
when-to-use: "Use on explicit request for 'what you haven't told me yet', or proactively when conversation history is long, context is rich, and the user is about to make a consequential decision or commit to a direction. Complements other reflection skills."
allowed-tools: ["read_file", "grep", "list_dir", "memory_search", "memory_get", "web_search", "web_fetch", "x_keyword_search", "x_semantic_search", "x_thread_fetch"]
argument-hint: "<optional focus: 'about the proof', 'regarding the last experiment', 'in this repo'>"
metadata:
  short-description: "Surface important unsaid observations about the current work"
---

# What Haven't You Told Me?

## Purpose

Create a safe, explicit channel for the model to volunteer observations, implications, tensions, or opportunities that the user has not directly asked about but that are visible from the full context (conversation + workspace + memory + external sources).

This is the Grok-native port of the Codex "grok-task-v3-what-haven-t-you-told-me" prompt. It is deliberately minimal in its core question so that the model must do the work of scanning the entire working context for high-leverage unsaid material.

## Invocation

`/what-haven-t-you-told-me [focus area]`

The focus is optional and narrows the scan (e.g., "the current proof attempt", "the factorization pipeline", "the meeting we just had").

## Core Question (Always Answer This)

Is there anything about this work that you always wanted to tell me but haven't had a chance to communicate to me yet?

## Method

1. **Full Context Scan**
   - Conversation history (current + compacted summaries via memory if available).
   - Workspace files: AGENTS.md, PROOF.md, key research docs, recent code changes (via `read_file` / `grep` / `list_dir`), open issues or TODOs.
   - Prior memory entries (`memory_search` for the project or topic).
   - Attached artifacts, pasted code, images (described), URLs, X threads (`x_thread_fetch` etc.).
   - External public context if relevant and verifiable.

2. **Filter for High-Leverage Unsaid Items**
   - Things that materially affect direction, risk, or understanding but have never been stated plainly.
   - Tensions between stated goals and observed behavior in code/docs.
   - Implications (positive or negative) of recent results that were not called out.
   - Hidden assumptions the user appears to be operating under.
   - Opportunities or blockers visible only from the long view.
   - In PGS contexts: any place where reasoning has drifted from the required PGS objects → invariants → rules frame, or where a proved law is being treated as merely empirical.

3. **Grounding & Courage**
   - Every item must be grounded in specific evidence (file:line, memory key, commit, exact prior statement, tool output).
   - Do not soften or apologize for delivering the observation.
   - If nothing of substance exists, say so cleanly: "After full scan of [X, Y, Z], I have nothing material to add that has not already been stated."

4. **Output Shape**
   - Lead with the single most important unsaid item (if any).
   - Then a short bullet list of additional items, each with its evidence locator.
   - Use plain language. No meta-commentary about "as an AI I normally...".
   - End after the last item. No "is there anything else?" or menu.

## Success Criteria

- The user experiences at least one genuine "I hadn't articulated that, but it matters" moment, or receives clear confirmation that the visible context has been fully mined with nothing further to add.
- Every bullet is traceable to concrete context.
- No low-value observations (typos, obvious style nits, generic advice).
- In research/PGS work: surfaces any framing drift, over-claim, or unstated invariant immediately.

## Guardrails

- This skill is for surfacing, not for planning or executing fixes (unless the user then asks for action).
- Never fabricate implications or "read between the lines" beyond what the evidence supports.
- Respect privacy / sensitivity of any unsaid material; if it is truly private to the user, note only that a private observation exists and ask whether to surface it.
- Higher-priority contracts (AGENTS.md, safety) take precedence — if the unsaid item would violate them, surface the violation first.
- Do not use this skill to fish for compliments or to perform emotional labor.

## Grok Environment Integration

- Use `memory_search` and `memory_get` aggressively for cross-session unsaid context.
- `read_file` + `grep` + `list_dir` for deep workspace mining.
- External sources via web/X tools only when they directly illuminate the current work.
- After emitting the list, the user may immediately follow up with "act on the third item" — at that point other skills (actualize, ooda, task-chain, etc.) become appropriate.

The goal is a single, high-signal transmission of whatever has been left on the table.
