---
name: 10-supporting-facts
description: >
  Deliver a rigorous, evidence-based set of verifiable facts that align with and
  strengthen the central claim or narrative of a provided post, article, statement,
  or body of material. Surface exactly (or up to) 10 high-quality facts from credible
  primary or authoritative sources. Use when the user wants to ground a narrative in
  supporting evidence rather than opinion. Trigger on "10 supporting facts", "what
  backs this up", "evidence for this claim", "reinforce this narrative with sources",
  "find the data that aligns with this post", or any request for factual bolstering of
  presented material.
when-to-use: "When a user provides a post, claim, article, or narrative and explicitly or implicitly seeks factual evidence that aligns with or strengthens its core message. Useful for balanced evidence gathering, 'steel man' exercises, or when a claim is under scrutiny and supporting data is needed. Activates on 'supporting facts for this', 'evidence that backs this narrative', '10 facts that align with...', or similar."
allowed-tools: ["web_search", "web_fetch", "open_page", "open_page_with_find", "read_file", "grep", "list_dir", "x_keyword_search", "x_semantic_search", "x_thread_fetch", "x_user_search", "memory_search", "memory_get", "todo_write"]
argument-hint: "<post text, thread URL/ID, article link, claim description, or attached image+text> [--max 10]"
metadata:
  short-description: "Evidence-based grounding: up to 10 verifiable facts that align with a narrative's central claim"
  version: "1.0.0"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/grok-task-v3-10-supporting-facts/SKILL.md"
---

# 10 Supporting Facts — Grok Edition

You are executing the "10 Supporting Facts" workflow. Treat the current user message, attachments, conversation history, linked URLs, images, X posts/threads, and any provided files as the complete input context. Your sole job is to produce a disciplined, neutral, source-backed set of verifiable facts that align with the input narrative's primary claims.

This is the Grok-native port of the original Codex v3 task. It is the balanced counterpart to the "10 Contradictions" skill. It has been expanded with full tool integration for live primary-source research, mandatory citation discipline via `render_inline_citation`, and explicit guardrails for deterministic scientific contexts (especially prime-gap-structure per AGENTS.md).

## Core Contract

- **Facts only.** No opinions, no moralizing, no speculation, no hype.
- **Direct alignment.** Every fact must specifically reinforce or provide empirical grounding for a claim or implication present in the provided material.
- **Verifiability first.** Every fact must be traceable to a credible, checkable source that a third party can verify in < 60 seconds.
- **Quality over quantity.** Accept fewer than 10 strong facts rather than including weak, tangential, or low-credibility items. State the actual count plainly.
- **Neutral tone.** Academic/journalistic voice. Let the facts stand on their own.
- **No meta-language in output.** Do not use phrases such as "supports the narrative." Describe the alignment directly (e.g., "This is consistent with the claim that..." or "This matches the reported pattern of...").

## Step-by-Step Workflow

### 1. Ingest & Extract the Narrative Core
- Load the full material using appropriate tools (same patterns as the 10-contradictions skill: `x_thread_fetch`, `open_page`, `read_file` for images/PDFs/files, etc.).
- Precisely identify and quote the **primary claim(s)** or overarching narrative the material advances.
- Note any supporting sub-claims, statistics, trends, or implications presented as factual.
- Success criterion: Verbatim quote of the narrative spine that the supporting facts will ground.

### 2. Decompose into Checkable Elements
- Break the narrative into discrete, verifiable assertions or patterns.
- Identify the implied scope, definitions, time periods, and populations.
- Success criterion: Clear list of atomic claims ready for positive evidence search.

### 3. Evidence Acquisition (Tool-Driven, Prioritized)
Use tools **before** drafting any fact. Follow the identical source priority and tool patterns as the contradictions skill (primary/official first, then high-quality secondary).

**Tool patterns specific to support:**
- `web_search` for "official data confirming [trend/claim] [year]", "peer-reviewed study [exact relationship]", site:*.gov or doi.org.
- Cross-reference multiple independent primary sources where possible (convergent evidence is stronger).
- For recent or social claims, `x_keyword_search` can surface contemporaneous primary observations, but never rely on it alone for factual grounding.
- When the input contains images, charts, or data excerpts, use `read_file` + direct comparison to external official series.

Capture citation ids for every web/X result that will appear in the final output.

Success criterion: At least one (preferably multiple convergent) primary-source-backed candidate fact per major narrative element, with full provenance.

### 4. Select & Formulate the Aligning Facts
- Choose the strongest, most direct alignments (target 10; accept fewer if quality requires it).
- For each:
  - State the fact concisely and precisely.
  - Explicitly connect it to the specific claim it aligns with (quote or tight paraphrase from input).
  - Provide minimal sufficient source attribution.
- Reject any item that is interpretive, from weak sources, only loosely related, or requires significant caveats that undermine the alignment.
- Avoid language that frames the fact as "supporting the narrative." Use direct alignment phrasing in the bullet.

Success criterion: Each fact, standing alone, increases the evidentiary weight of the original claim for a neutral reader.

### 5. Format, Cite, and Self-Audit
- Draft in the required output shape.
- Audit pass:
  - Direct relevance and alignment (no stretch)?
  - Accuracy to source?
  - Citations ready (inline renders for web/X)?
  - PGS frame respected if applicable?
- Remove or replace any substandard item and adjust count.

Success criterion: The set is tight, high-signal, and defensible.

## Strict Output Format

Always begin with the exact header. No prose before it.

```
SUPPORTING FACTS: [Short descriptive title summarizing the subject of the claim]

- [Fact 1]: [Precise factual statement with numbers/dates/definitions]. This is consistent with the claim that "[exact quote or paraphrase from input]". (Source: [Primary source name + year or URL slug]; <citation render if applicable>)
- [Fact 2]: ...
```

Use the actual number of strong facts surfaced. If fewer than 10 after exhaustive search, append:

"Only N high-quality facts meeting the verifiability and direct-alignment standard were identified."

## Grok Tool & Citation Discipline

Identical to the 10-contradictions skill:
- All external facts obtained via current-session tool calls.
- Use `render_inline_citation` immediately after any web- or X-sourced statement in the final output.
- Workspace facts cited by file:line or artifact.

## PGS & Deterministic Research Guardrails (This Repository)

If the input narrative or claim intersects prime gaps, divisor fields, GWR/DNI rules, endpoints, or other proved or conjectured results in this workspace:

- Begin reasoning from the PGS objects → invariants → rule/law → state frame (AGENTS.md).
- Do not introduce classical or probabilistic framing as the default lens for "supporting facts."
- Never weaken or probabilistically reframe deterministic proved results (see PROOF.md).
- First cross-check any mathematical or computational claim against the project's canonical documents using `read_file` and `grep`.
- External supporting evidence is welcome only after the native PGS frame has been applied and only as supplementary.

This contract is binding inside the prime-gap-structure project.

## Success Criteria

- Every fact is primary-source verifiable in <60 seconds from the provided attribution.
- Each fact aligns directly with a specific, quoted element of the input narrative.
- Output uses clean, direct language without meta-commentary on "the narrative."
- Citations (inline renders) are accurate and present where required.
- Count is honest; quality is never sacrificed for round numbers.
- In PGS contexts, the AGENTS.md first frame is visibly respected.
- The user receives usable, grounded evidence that can be cited or checked independently.

## Edge Cases & Limits

- Normative claims → note that factual alignment is not applicable; offer to examine empirical sub-components.
- Sparse primary data for very new claims → surface best available with recency qualifiers.
- Visual or data-heavy input → analyze the visual claim first via tools, then locate aligning external data.
- The input is itself a "supporting facts" piece → apply identical standards to its sub-claims.

This skill provides the evidentiary mirror image to the contradictions workflow: clean, auditable facts that give weight to a claim when the evidence genuinely does so. Use it to ground narratives that deserve it and to surface the actual data landscape without rhetorical inflation.