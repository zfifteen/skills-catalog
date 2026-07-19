---
name: new-information
description: >
  From the current matter under discussion, produce a high-leverage, novel
  synthesis or reinterpretation grounded exclusively in publicly verifiable
  sources. Present as Title, Observation, Supporting Data (with real working
  hyperlinks). Originality lives in the framing and connections, never in
  invented facts. Use when the user says "new information", "novel synthesis",
  "what fresh angle", "high-leverage reinterpretation", or provides context and
  asks for new insight with practical applications. Complements research-
  continuity and never-mentioned skills.
when-to-use: "Trigger for requests that explicitly want novel but grounded synthesis, fresh angles on known material, or practical implications derived from public sources. Requires the output to be citable and non-fabulative."
allowed-tools: ["web_search", "web_fetch", "open_page", "open_page_with_find", "read_file", "grep", "list_dir", "x_keyword_search", "x_semantic_search", "x_thread_fetch", "memory_search", "memory_get", "todo_write"]
argument-hint: "<topic, claim, or research context> [--sources N]"
metadata:
  short-description: "Grounded novel synthesis / reinterpretation with practical applications"
---

# New Information

## Purpose

Deliver one piece of high-leverage new information: a synthesis or reinterpretation that was not obvious from the raw inputs, but that is 100% supported by independently verifiable public sources. The value is in the connections and framing, not in new "facts" invented by the model.

This is the Grok port of the Codex "grok-task-v3-new-information" task, upgraded with full tool support for source verification and the `render_inline_citation` component for clean citations.

## Non-Negotiable Rules

- All factual claims must come from publicly verifiable, independently checkable sources.
- Originality is allowed only in the interpretation, connections, and suggested practical applications.
- Never fabricate sources, numbers, quotes, or events.
- Provide real working hyperlinks (or exact file:line locators for local artifacts).
- If a claim cannot be verified in the time available, label it or omit it.

## Invocation

`/new-information <context or question>`

The context may be a research hypothesis, a codebase pattern, a public claim, a set of prior results, or a broad domain ("prime gap structure divisor normalization", "recent RSA-2048 records", etc.).

## Workflow

1. **Scope the Matter**
   - Use conversation + `memory_search` + workspace files (`read_file`, `grep`) to lock the exact claim or open question under discussion.
   - In PGS workspaces: explicitly restate the current PGS objects, invariants, and rules in play before looking outward.

2. **Source Acquisition & Verification**
   - Use `web_search` + `web_fetch` + `open_page` / `open_page_with_find` to locate primary sources (papers, datasets, commit histories, official announcements, benchmark logs).
   - Use X tools for recent technical discussion when relevant.
   - Cross-check at least two independent sources for any non-trivial fact.
   - For local code or docs: treat them as primary sources with precise locators.

3. **Synthesis Construction**
   - Identify the novel angle or reinterpretation that has high leverage (changes how one should think about or act on the matter).
   - Keep the synthesis narrow — one strong idea, not a survey.
   - Derive practical applications that follow directly from the synthesis (again, grounded).

4. **Output Format (Strict)**
   Emit exactly:

   **Title**  
   (One crisp line naming the synthesis or reinterpretation)

   **Observation**  
   (2–6 sentences of the core new framing or connection. Lead with the strongest statement supported.)

   **Supporting Data**  
   - Bullet list. Each bullet:
     - The concrete fact or source excerpt
     - Working hyperlink or exact locator (file:line, commit SHA, arXiv:xxxx, etc.)
     - Optional: `render_inline_citation` for web results

   (No other sections, no "Conclusion", no "Further reading" unless it is part of the synthesis.)

## Success Criteria

- A knowledgeable reader says "I hadn't connected those dots, and the sources check out."
- Every factual assertion has a verifiable pointer that a third party can follow in <30 seconds.
- The practical applications section (if present) is a direct, low-speculation consequence of the synthesis.
- No source is cited that the model did not actually fetch and inspect in this turn or via explicit prior memory.

## Guardrails

- Higher contracts win: AGENTS.md PGS-first frame must be used when the matter is in-scope for this workspace.
- If the search returns weak or contradictory sources, say so plainly in the Supporting Data rather than forcing a synthesis.
- This skill is not a license for speculation; it is a disciplined "connect public dots" engine.
- Limit to one synthesis per invocation. Breadth is the enemy of leverage.

## Grok Environment Advantages

- Full web + X tool suite + citation rendering component lets the skill produce immediately usable, citable artifacts.
- `memory_search` / `memory_get` allow the synthesis to incorporate durable project state without hallucinating prior results.
- `todo_write` can be used internally when the source-gathering phase has many parallel queries.
- Output is designed to be dropped straight into research notes, papers, or the prompt-library-catalog.

When the user wants "something new but real", this skill delivers it with an audit trail.
