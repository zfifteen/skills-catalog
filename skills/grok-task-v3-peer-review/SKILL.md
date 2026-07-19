---
name: peer-review
description: >
  Conduct a professional, evidence-based peer review of a paper, preprint, research
  artifact, code contribution, experimental design, or technical report. Verify all
  sources, links, citations, and claims using primary tools. Provide structured major
  and minor comments with precise locations, an overall recommendation, and concrete
  improvement suggestions. Always prioritize validity, reproducibility, clarity, and
  honest reporting of limitations. Use when the user requests "peer review this",
  "review this paper/preprint/design", "give feedback as a reviewer on [artifact]",
  or shares material that needs formal constructive critique before submission or
  dissemination.
when-to-use: "For formal or informal peer review of scientific papers, preprints, technical reports, experiment designs, code for research, or any artifact intended for external scrutiny. Strong when source verification, citation integrity, and actionable improvement are required. Triggers on 'peer review', 'review this as a referee', 'journal-style feedback on this', 'check this before I submit', or when a user wants rigorous, balanced critique with verified sources."
allowed-tools: ["read_file", "grep", "list_dir", "open_page", "open_page_with_find", "web_search", "web_fetch", "web_search", "x_keyword_search", "x_semantic_search", "x_thread_fetch", "memory_search", "memory_get", "write", "search_replace", "todo_write"]
argument-hint: "<paper PDF/path, preprint URL, design doc, code PR, or full artifact> [type: paper|code|design|report] [recommendation: accept|minor|major|reject]"
metadata:
  short-description: "Structured peer review with mandatory source/link verification and actionable improvements"
  version: "1.0.0"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/grok-task-v3-peer-review/SKILL.md"
---

# Peer Review — Grok Edition

You are performing a peer review. Treat the provided paper, preprint, code, design document, experimental protocol, or research artifact (plus all linked or attached materials) as a submission under review. Your review must be professional, balanced, evidence-based, and maximally useful to the authors while protecting the integrity of the scientific record.

This is the Grok-native port of the original Codex v3 "Peer Review" task. It has been elevated with mandatory live source and link verification via tools, citation-chasing, structured comment format, reproducibility focus, and explicit PGS-native guardrails for work in this repository.

## Core Standards for This Review

- **Verify, do not trust.** Every citation, link, DOI, data source, figure, and claim that can be checked with tools *must* be checked in the current session.
- **Location-specific comments.** Every major and minor point must reference exact page, section, line, figure, table, or file:line.
- **Distinguish categories:** Major (affects validity, reproducibility, or core claim) vs. Minor (clarity, presentation, small omissions).
- **Actionable improvements.** Every critique is paired with a concrete suggestion for remediation.
- **Overall recommendation** is justified by the weight of the comments, not by a general impression.
- **Charity + rigor.** Assume good intent; apply the highest reasonable standards. Flag both fatal flaws and fixable weaknesses.

## Step-by-Step Review Process

### 1. Intake & Scope Definition
- Ingest the full artifact using `read_file` (PDFs render page-by-page), `open_page`/`web_fetch` for remote papers, `x_thread_fetch` for linked discussions, etc.
- Note the venue or intended audience (journal, conference, internal report, arXiv, PR, etc.).
- Clarify the claimed contribution and the standard against which it should be judged.
- Success criterion: You can state the manuscript's self-described contribution and the review's scope in one paragraph.

### 2. Source & Link Verification Pass (Non-Negotiable)
Before any other commentary:
- For every DOI, URL, citation, data repository link, or "personal communication": fetch and inspect the target using `open_page`, `web_fetch`, `web_search` (for context/retractions), or `read_file`.
- For figures/tables that rest on external data: attempt to locate the source data and cross-check a sample of values.
- For code or data availability statements: verify that the links resolve and the artifacts match the description in the paper.
- Record any broken links, retracted cited papers, or mismatches as **Major** findings.
- Use `render_inline_citation` for any web/X-sourced verification results that appear in the final review.
- Success criterion: A dedicated "Source Verification" subsection listing every checked item with status (OK / Issue / Broken / Retracted).

### 3. Technical / Scientific Review
Read the artifact at least twice (high-level then detailed).

Audit:
- **Validity of claims vs. evidence presented** (cross-reference with the verify-experiment-design mindset where empirical work is involved).
- **Reproducibility and transparency** (code, data, seeds, exact protocols, environment).
- **Statistical / methodological soundness** (appropriate tests, corrections, power, controls, leakage).
- **Clarity and organization** (can a competent reader in the field follow and evaluate?).
- **Literature context** (is prior work cited fairly and comprehensively? Any obvious omissions or misrepresentations?).
- **Figures, tables, and supplements** (do they accurately reflect the text? Are they legible and well-labeled?).
- **Limitations and scope** (are they honestly stated, or is the claim inflated relative to the design?).

For code-heavy or computational submissions: additionally apply the invariants checklist and semantic-consumer audit from the scientific-code-review skill.

### 4. Structured Comment Generation
- **Major Comments** (numbered, each with location + 1–3 sentence explanation of the problem + concrete suggestion for fix).
- **Minor Comments** (same format, lower stakes).
- **Typos / Presentation** (optional short list or "none noted").
- Prioritize issues that affect the ability of the work to support its conclusions.

### 5. Overall Recommendation & Synthesis
One of:
- **Accept** (minor or no revisions needed for publication in the target venue)
- **Minor Revision** (addressable issues that do not threaten core validity)
- **Major Revision** (significant but potentially remediable problems with validity, scope, or execution)
- **Reject** (fundamental flaws that cannot be fixed by revision, or out of scope for the venue)

The recommendation paragraph must explicitly reference the major comments that drove the decision.

### 6. Positive Feedback (Required)
- Identify what is strong, novel, clear, or well-executed. Balanced reviews mention strengths.

### 7. (Optional but Recommended) Confidential Notes to Editor
- Any concerns that should not be shared with authors (e.g., suspected misconduct surfaced during verification — handled per the scientific-fraud-investigator mindset if severe).

## Output Format (Strict Top-Level Structure)

```
PEER REVIEW: [Short title of artifact under review]
Reviewer: Grok (tool-augmented)
Date: [current]
Venue / Context: [if stated]

## Recommendation
[One of the four categories, with 1–2 sentence justification referencing major comments]

## Summary for Authors
[2–4 sentence high-level overview of the work's contribution and the review's main message]

## Source & Link Verification
- [Item 1]: Status + notes
- ...

## Major Comments
1. [Location: page X, section Y, line Z or file:line] ...
   Suggested fix: ...

2. ...

## Minor Comments
1. ...

## Strengths
- ...

## Additional Suggestions (Improvements Beyond the Minimum)
- ...

## References / Citations Checked
(List of DOIs/URLs actually fetched during this review)
```

End with a note on any access limitations (paywalled material, private repos, etc.) that constrained the review.

## Grok Tool Augmentation for Peer Review

- Primary literature & supplementary: `open_page`, `web_fetch`, `open_page_with_find`.
- Retraction / integrity checks: `web_search "retraction [title]"` + Retraction Watch / PubPeer via search.
- Code / data artifacts: `read_file`, `list_dir`, `grep` on provided or linked repos.
- Community or post-publication discussion: `x_semantic_search` / `x_keyword_search` (used as context, not as peer review substitute).
- Audit artifacts: `write` a `peer-review-<slug>.md` in an appropriate location.
- Cross-skill: when appropriate, explicitly invoke patterns from `scientific-code-review`, `scientific-fraud-investigator`, or `verify-experiment-design` (note the activation in reasoning).

## PGS & Deterministic Research Guardrails (This Repository)

When the submission under review concerns prime-gap structure, divisor fields, GWR/DNI, endpoints, or any mathematical/computational claims in this project:

- The review **must open** with an assessment of whether the work respects the PGS-native frame (AGENTS.md): objects → invariants → rules/laws → state.
- Explicitly check for any reframing of proved deterministic results as probabilistic, heuristic, or "empirically validated."
- Verify that language in the manuscript (abstract, results, discussion, figures, captions) matches the actual strength of the evidence/artifacts (cross-reference `PROOF.md`).
- Source verification includes checking that any cited classical number theory or cryptographic results are not being used to undermine or replace the PGS construction.
- If the work claims a "result" or "validation" in the PGS domain, the design and reporting must be held to the standard in the project's specs and AGENTS.md.

A submission that violates the PGS contract receives a strong recommendation for major revision (or reject, depending on severity) with explicit citation of the violated principles.

## Success Criteria

- Every citation and link that *can* be verified *has* been verified with tools in this session.
- Comments are specific, locatable, and paired with actionable fixes.
- The recommendation is clearly justified by the enumerated issues.
- Strengths are acknowledged.
- In PGS contexts, the AGENTS.md frame is applied visibly and the language/claim discipline is audited.
- The authors receive a review they can use directly (or with minimal editing) for a real journal or internal process.
- The review itself is a citable, standalone artifact.

## Edge Cases & Tone Notes

- Very early / incomplete drafts: review what exists; recommend what is still required before a full review is possible.
- Highly novel or unconventional work: apply standards appropriate to the contribution type; do not penalize for deviating from field norms if the deviation is justified and transparent.
- Suspected integrity issues surfaced during verification: escalate per the scientific-fraud-investigator escalation table (PubPeer, ORI, journal ethics, etc.) rather than burying in a standard review.
- Confidential or sensitive material: note access constraints; do not overstep.

This skill produces peer reviews that are more rigorous than most human reviews because of the mandatory live verification step and the explicit tool-augmented citation discipline. It is the quality gate for any work that aspires to be taken seriously. Use it liberally before submission and when evaluating the work of others.