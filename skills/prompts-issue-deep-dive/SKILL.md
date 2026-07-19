---
name: prompts-issue-deep-dive
description: >
  Apply the "Issue Deep Dive" prompt-library workflow: perform an expert-level technical
  investigation of a GitHub issue (or issue-like material). Comprehend full context including
  all comments, code references, and links; analyze sub-issues and hidden dependencies;
  generate deep reasoning for assumptions, patterns, and implications; synthesize structured
  findings with concrete next actions. Maintain transparent, methodical reasoning suitable
  for expert research collaboration.
  Use when the user pastes or links a GitHub issue and says "deep dive this issue", "full
  technical investigation of this GH issue", "issue deep dive", or runs /prompts-issue-deep-dive.
when-to-use: "Thorough, multi-step investigation of a GitHub issue or complex problem report. Triggers: 'deep dive', 'full technical investigation', 'analyze the whole thread', 'issue deep dive', 'research assistant mode on this issue'. Goes far beyond a quick summary."
argument-hint: "<GitHub issue URL or pasted issue text + comments>"
allowed-tools: ["read_file", "grep", "list_dir", "web_fetch", "open_page", "open_page_with_find", "search_issues", "issue_read", "pull_request_read"]
metadata:
  short-description: "Expert technical deep-dive investigation of a GitHub issue with sub-issue tracing and synthesis"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/prompts-issue-deep-dive/SKILL.md"
  version: "1.0.0"
---

# Issue Deep Dive — Grok Port

Act as an expert technical research assistant that performs a methodical, multi-layer investigation of a GitHub issue, producing transparent reasoning and actionable synthesis.

## Purpose

The original prompt gives a clear four-stage research process that prevents shallow or surface-only treatment of complex issues. This Grok port augments it with direct tool access to fetch the actual issue thread, linked PRs, code, and related artifacts.

## Invocation

```
/prompts-issue-deep-dive <issue URL or full pasted issue>
```

The skill will treat the provided URL or text (plus conversation context) as the primary material and use tools to expand it.

## Four-Stage Investigation Process (Execute in Order)

### 1. Comprehend the Issue Context
- Fetch the full GitHub issue (title, body, all comments, labels, linked PRs/commits, attachments, author history on the thread).
- Identify the main question, problem, or feature request.
- Determine the underlying technical and conceptual intent of the original author.
- Note any explicit or implicit success criteria mentioned.

Use `issue_read` (MCP), `web_fetch`/`open_page` on the issue URL, and follow links to comments or referenced discussions.

### 2. Analyze Sub-Issues and Dependencies
- Trace every linked or referenced issue, pull request, commit, or external resource.
- Map implicit relationships, hidden bottlenecks, and dependency chains.
- Surface any emerging research-relevant themes or hypotheses that connect the nodes.
- Identify "issue clusters" — groups of related tickets that are really one underlying problem.

### 3. Deep Reasoning and Insight Generation
- Go beyond the surface text: infer unstated assumptions, missing variables, or unspoken constraints.
- Explore alternative interpretations of the problem statement.
- Highlight non-obvious patterns, opportunities for generalization, or mathematical/computational insights.
- When relevant, propose experimental, geometric, or structural reformulations that could advance the underlying research (especially valuable in PGS or deterministic work).
- Explicitly apply domain-appropriate frames (in this workspace: PGS objects → invariants → rules before classical methods).

### 4. Synthesize and Recommend
Produce a structured deliverable containing at minimum:

- **Observed Themes** (bullet list)
- **Hidden Insights** (the non-obvious ones surfaced in stage 3)
- **Next Steps** (concrete, prioritized, with rationale and estimated effort)
- **Potential Research Threads** (longer-term directions opened or clarified by the issue)

For each recommendation, include:
- Why it matters
- What artifact or state change would constitute success
- Any blocking dependencies

## Output Contract

The final response should feel like a high-quality research memo written for a technical collaborator who already understands the project:

- Transparent reasoning (show the evidence → inference steps).
- Precise references (issue comment numbers, file:line, commit hashes, external URLs).
- Actionable next steps rather than vague advice.
- Tone: expert, collaborative, intellectually honest, free of both hype and undue hedging.

## Grok Tool Augmentation

- Primary: MCP GitHub tools (`issue_read`, `search_issues`, `pull_request_read`) when available.
- Fallback / supplement: `web_fetch`, `open_page`, `open_page_with_find` on the issue URL and any linked resources.
- Code context: `read_file` + `grep` on any files referenced in the issue or its linked PRs.
- Cross-session: `memory_search` for prior related work in the workspace.

## Success Criteria

- The investigation demonstrably read and incorporated the full comment history and all linked artifacts (not just the opening post).
- Sub-issue/dependency mapping is explicit and accurate.
- At least 2-3 non-obvious insights or reformulations are offered that are not present in the original thread.
- Recommended next steps are specific enough that an engineer could start work immediately.
- Reasoning is traceable: every claim points back to a concrete piece of evidence from the issue or fetched material.

## Guardrails

- Stay within the issue's actual scope unless the deep reasoning legitimately opens a clearly labeled "adjacent but important" thread.
- Do not invent facts or overclaim certainty about author intent.
- When the issue touches proved results or deterministic structures (PGS context), surface any tension with AGENTS.md invariants explicitly in the Hidden Insights or Next Steps section.
- Distinguish "what the issue author wants" from "what would most advance the underlying research goal."

This port turns the original detailed research-assistant prompt into a tool-augmented, traceable deep-dive workflow that produces collaboration-grade output.
