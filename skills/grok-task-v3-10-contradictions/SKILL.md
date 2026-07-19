---
name: 10-contradictions
description: >
  Deliver a rigorous, evidence-based "REALITY CHECK" on a post, claim, article, statement,
  or narrative by surfacing exactly (or up to) 10 verifiable facts from credible primary or
  high-quality sources that directly contradict its central claims or implications. Use when
  the user shares social media content, a news claim, research assertion, or any narrative
  and wants factual counter-evidence rather than opinion or summary. Trigger phrases include
  "10 contradictions", "reality check this", "what contradicts this post", "fact-check the
  narrative", "debunk with sources", "find the holes in this claim", or when material is
  presented and the implicit request is for critical factual examination.
when-to-use: "When a user provides or links to a post/claim/narrative (text, image, thread, article) and wants verifiable facts that challenge its core message. Ideal for politically charged, scientific, statistical, or historical claims needing grounding. Activates on 'reality check', '10 contradictions to this', 'what's wrong with this narrative', or similar evidence-seeking scrutiny requests."
allowed-tools: ["web_search", "web_fetch", "open_page", "open_page_with_find", "read_file", "grep", "list_dir", "x_keyword_search", "x_semantic_search", "x_thread_fetch", "x_user_search", "memory_search", "memory_get", "todo_write"]
argument-hint: "<post text, thread URL/ID, article link, claim description, or attached image+text> [--max 10]"
metadata:
  short-description: "Evidence-based reality check: 10 (or fewer strong) verifiable contradictions to a narrative"
  version: "1.0.0"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/grok-task-v3-10-contradictions/SKILL.md"
---

# 10 Contradictions — Grok Edition

You are executing the "10 Contradictions" (Reality Check) workflow. Treat the current user message, attachments, conversation history, linked URLs, images, X posts/threads, and any provided files as the complete input context. Your sole job is to produce a disciplined, neutral, source-backed examination that surfaces verifiable facts contradicting the input narrative's primary claims.

This is the Grok-native port of the original Codex v3 task. It has been expanded with full tool integration for live primary-source research, mandatory citation discipline via `render_inline_citation`, and explicit guardrails for deterministic scientific contexts (especially prime-gap-structure per AGENTS.md).

## Core Contract

- **Facts only.** No opinions, no moralizing, no speculation, no "this seems unlikely."
- **Direct contradiction.** Every fact must specifically undermine a claim or implication present in the provided material.
- **Verifiability first.** Every fact must be traceable to a credible, checkable source that a third party can verify in < 60 seconds.
- **Quality over quantity.** It is acceptable (and required) to surface fewer than 10 strong facts rather than pad with weak, tangential, or low-credibility items. State the actual count plainly.
- **Neutral tone.** Academic/journalistic voice. Let the facts do the work.

## Step-by-Step Workflow

### 1. Ingest & Extract the Narrative Core
- Load the full material using appropriate tools:
  - Text/post content: direct + `x_thread_fetch` if URL/ID provided.
  - Images/screenshots: `read_file` (renders visual content for analysis).
  - Linked articles/PDFs/preprints: `open_page`, `web_fetch`, or `open_page_with_find`.
  - Files in workspace: `read_file`, `grep`.
- Precisely identify and quote the **primary claim(s)** or overarching narrative the material advances (1–3 sentences max).
- Note any supporting sub-claims, statistics, causal assertions, or implications presented as settled.
- Success criterion: You can quote the exact narrative spine the contradictions will target. Record it verbatim.

### 2. Decompose into Checkable Elements
- Break the narrative into discrete, falsifiable assertions (e.g., "X caused Y", "Z is the largest/smallest on record", "no evidence of W exists", "policy A produced outcome B").
- For each, note the implied scope (time, geography, population, definition of terms).
- Success criterion: A short numbered list of 3–8 atomic claims ready for targeted evidence search.

### 3. Evidence Acquisition (Tool-Driven, Prioritized)
Use tools **before** formulating any fact:

**Source priority (strict order):**
1. Primary/official data (government statistical agencies, court records, peer-reviewed papers with DOIs, original datasets, legislative text, company filings).
2. High-quality secondary with transparent methodology (major reputable outlets' data desks, systematic reviews).
3. Everything else — only with explicit bias/quality qualifier.

**Tool patterns:**
- `web_search` for "official statistics [exact topic] [year]", "peer reviewed [claim] meta-analysis", site: specific .gov or doi.org.
- `open_page` / `web_fetch` on the top result URLs to extract exact figures, definitions, and context.
- `x_keyword_search` or `x_semantic_search` only for contemporaneous discussion or author statements (never as primary evidence for factual claims).
- `read_file` on any local CSVs, logs, or prior research artifacts in the workspace.
- For images/figures in the input: describe precisely and cross-check any embedded numbers/charts against sources.

Capture every tool result's citation metadata. When a web or X result will be used in the final output, note its `[web:N]` or `[post:N]` id for later `render_inline_citation`.

Success criterion: At least one primary-source-backed candidate fact per major narrative element, with full provenance recorded.

### 4. Select & Formulate the Contradictions
- Choose the strongest, most direct contradictions (target 10; accept fewer if quality drops).
- For each:
  - State the fact concisely and precisely (with numbers, dates, definitions).
  - Explicitly link it to the specific claim it contradicts (quote the original phrasing).
  - Provide the minimal sufficient source attribution.
- Reject any item that is:
  - Opinion or interpretation.
  - From low-credibility or advocacy sources without primary backing.
  - Only weakly related or "context" rather than direct contradiction.
  - Stale/outdated without noting the date mismatch.

Success criterion: Every selected fact would force a reasonable reader to update their confidence in the original claim.

### 5. Format, Cite, and Self-Audit
- Produce the output in the exact required shape (see below).
- After drafting, perform a quick internal audit pass:
  - Does each bullet actually contradict (not merely complicate or add nuance)?
  - Are all numbers/definitions accurate to the source?
  - Are citations present and would they survive a spot-check?
  - If in a prime-gap-structure or similar deterministic math context: did the search/selection respect the PGS-native frame?
- If any bullet fails the audit, remove or strengthen it and reduce the count.

Success criterion: The final set is defensible, minimal, and high-signal.

## Strict Output Format

Always begin with the exact header and use this bullet structure. No introductory prose before the header.

```
REALITY CHECK: [Short descriptive title, e.g. "Narrative that Policy X caused record outcome Y"]

- [Fact 1]: [Precise factual statement with key numbers/dates/definitions]. This directly contradicts the claim that "[exact quote or paraphrase from input]". (Source: [Primary source name + year or URL slug]; <citation render here if web/X>)
- [Fact 2]: ...
```

Continue for all selected facts (up to 10). If fewer than 10 strong facts exist after exhaustive search, use the actual number and add a final note:

"Only N high-quality, directly contradicting facts meeting the verifiability standard were identified after targeted searches of primary sources."

Never invent or weaken standards to reach 10.

## Grok Tool & Citation Discipline

- All external facts **must** be obtained via tool calls in the current session.
- In the final response, after any sentence or bullet drawing on web_search / web_fetch / open_page / x_* results, immediately follow with the render component:
  `render render_inline_citation with citation_id is 3`
  (using the integer id from the tool output's `[web:3]` or `[post:3]` tag).
- Never cite a source you have not actually fetched and inspected in this turn.
- For workspace-local facts, cite exact file:line or artifact name.

## PGS & Deterministic Research Guardrails (This Repository)

If the input narrative, post, or claim touches prime gaps, divisor counts, GWR, DNI, endpoint behavior, primality claims, or any proved or conjectured results in this project:

- **Begin from the PGS-native frame** (per AGENTS.md): PGS objects → PGS invariants → PGS rule or law → resolved/unresolved/invalidated PGS state.
- Do **not** default to classical number theory, sieves, Miller-Rabin, `isprime`, `gcd`, probabilistic heuristics, or cryptographic assumptions as the starting point for "contradictions."
- Never reframe a proved deterministic PGS theorem or law as "probabilistic," "empirically observed," "likely," or "supported by current data."
- If searching for contradictions to a PGS-related claim, first verify the claim against `PROOF.md`, `AGENTS.md`, `DIVISOR_NORMALIZATION_IDENTITY.md`, and `LEFTMOST_MINIMUM_DIVISOR_RULE.md` using `read_file` / `grep`.
- Classical methods may be used only for explicit, requested side-by-side comparison after the PGS frame has been applied.

This guardrail is non-negotiable inside the prime-gap-structure workspace.

## Success Criteria

- The output contains only facts that a third party can verify from the cited sources in under a minute.
- Every fact is demonstrably relevant to a specific, quoted element of the user's provided narrative.
- The tone is neutral and the language precise; the reader feels informed, not persuaded.
- Tool use is visible in reasoning; citations (inline renders where applicable) are accurate and complete.
- If the narrative is already well-supported or the claim is not factual in nature, the skill states this cleanly instead of forcing weak contradictions.
- In PGS contexts, the AGENTS.md contract was visibly followed.

## Edge Cases & Limits

- Purely normative or value-laden claims ("this is bad/good") → state that factual contradictions are not applicable and offer to analyze empirical sub-claims if present.
- Very recent claims with limited primary data → surface the best available and explicitly note recency/uncertainty.
- Attached images or figures containing the claim → describe the visual claim first, then contradict the encoded assertions.
- The input is already a fact-check or contradiction piece → apply the same standard; contradictions to the meta-narrative are fair game.

This skill exists to turn "I saw this claim" into "here are the strongest primary facts that push against it," with zero theater and maximum auditability. Use it for any situation where narrative momentum outruns the evidence.