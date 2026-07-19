---
name: never-mentioned
description: >
  Identify and articulate something genuinely alarming or under-appreciated about
  the current matter that is almost never discussed in public or in the
  surrounding conversation. Deliver as a titled investigative-style piece with
  citations in their own section. Use when the user says "never mentioned",
  "what's the alarming thing no one talks about", "the elephant", "the risk
  everyone is ignoring", or wants an expose-style take grounded in the full
  context. Complements new-information and what-haven-t-you-told-me.
when-to-use: "Explicit request for the 'almost no one ever mentions' angle on a technical, scientific, or strategic matter. Requires rigorous non-fabrication and source discipline; high-stakes output."
allowed-tools: ["web_search", "web_fetch", "open_page", "open_page_with_find", "read_file", "grep", "list_dir", "x_keyword_search", "x_semantic_search", "x_thread_fetch", "memory_search", "memory_get", "todo_write"]
argument-hint: "<the matter or claim under discussion>"
metadata:
  short-description: "Alarming / under-appreciated aspect that almost no one mentions — investigative expose style"
---

# Never Mentioned

## Purpose

Surface the specific, concrete, alarming (or strategically critical) thing about the topic that is visible from the evidence but is almost never stated plainly in the literature, on social media, in project discussions, or in the current conversation. The output must feel like a tight investigative expose while remaining strictly non-fabulative.

This is the Grok port of the Codex "grok-task-v3-never-mentioned" task, with added tool power for verification and the citation component.

## Non-Negotiable Constraints

- DO NOT fabricate data, information, or sources.
- DO NOT infer from filler text, absence of evidence, or social-media volume.
- Incorporate the entire current conversation + workspace + memory context.
- No post IDs as sources.
- Do not cite social media as authoritative sources (X tools may be used for signal of what *is* being discussed, not for the alarming fact itself).
- Limit ~2000 characters total.

## Invocation

`/never-mentioned <matter>`

## Workflow

1. **Context Lock**
   - Ingest the full relevant context (conversation, workspace files via `read_file`/`grep`/`list_dir`, memory via `memory_*`, recent X discussion via X tools).
   - In PGS or prime-gap-structure work: explicitly surface the current PGS objects, invariants, and any drift from the AGENTS.md contract.

2. **Signal vs. Silence Scan**
   - What is the dominant public / conversational framing of the matter?
   - What does the primary evidence (papers, code, benchmarks, proofs, logs) actually show that contradicts, complicates, or is simply omitted from that framing?
   - The "alarming" or "never mentioned" item must be a positive, specific observation supported by evidence, not merely "no one is talking about X".

3. **Ground the Claim**
   - Every element must trace to verifiable primary material (exact commit, paper section, benchmark log line, mathematical derivation in PROOF.md, etc.).
   - Use web/X tools to confirm that the observation is indeed rarely stated (search for close variants and note the silence or misdirection).

4. **Output Format (Strict)**

   **Title**  
   (One line, in the style of an investigative expose headline — no "The Alarming Truth About...")

   <blank line>

   Body paragraphs (short, separate sentences with two carriage returns between them as per original constraint where applicable).

   **Citations**  
   - Bulleted list of primary sources with working links or file:line locators.
   - Use `render_inline_citation` for web results.

   Stop. No meta, no "this is rarely discussed because...", no calls to action.

## Success Criteria

- A reader familiar with the domain says "Yes — that is real, it is under-discussed, and the sources are solid."
- The piece does not rely on the phrase "no one mentions this" or similar; the rarity is demonstrated by the contrast with the dominant framing.
- Total length and tone match the "investigative expose" request while staying under the character limit.
- In research contexts (especially PGS): the never-mentioned item directly affects proof strategy, validation scope, or interpretation of results.

## Guardrails

- This is one of the highest-risk skills for hallucination. When in doubt, return a smaller or null result rather than stretch.
- AGENTS.md and PROOF.md contracts are binding: never use this skill to downgrade a proved PGS theorem or to treat deterministic laws as probabilistic.
- If the "alarming" item is actually well-known inside the project but not outside, label the scope of the silence accurately.
- The skill may refuse if the context does not contain sufficient primary evidence for a non-fabulative expose.

## Grok Environment Notes

- The combination of web search, page fetch, X search, local file tools, and memory makes it possible to do a far more rigorous "what is the actual silence" analysis than the original Codex prompt could achieve.
- `render_inline_citation` gives the output immediate credibility and auditability.
- `todo_write` is useful when the scan requires tracking multiple source threads in parallel.

Use this skill when the user wants the sharp, uncomfortable, evidence-based observation that polite or conventional discussion routinely omits.
