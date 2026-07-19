---
name: highest-priority-issue
description: >
  Variant of the repo analyst workflow. Given a GitHub URL, fully enumerate open UNASSIGNED
  issues + recent merged PRs, apply the 0-10 rubric, and declare the single highest-priority
  issue with evidence. Uses a slightly different Markdown output structure (more compact
  headings, explicit "Top issue" callout early). Strict Markdown only. Use when the user
  invokes the "Highest Priority Issue" workflow or provides a GitHub URL for prioritization.
when-to-use: Use when the user wants the "highest priority issue" analysis (this specific rubric + output variant) on a GitHub repo or issues page.
argument-hint: "<GitHub repo or issues URL>"
metadata:
  short-description: "Repo analyst (variant output): highest priority unassigned issue"
  source: "ported-from-codex/grok-task-v3-highest-priority-issue"
  original_codex: "grok-task-v3-highest-priority-issue"
---

# Highest Priority Issue (Repo Analyst — Variant Output)

Follow the exact same **Step-by-Step Procedure** as the `most-important-issue` skill (resolve repo, paginate unassigned open issues, read bodies/comments, analyze merged PRs 90-180 days, score with the same 5-factor rubric, select one winner, cite everything with verbatim quotes and timestamps).

The only differences are in the final presentation format.

## Output Format (This Variant)
Use the more compact structure from the original (headings like `## Summary`, early bold `**Top priority:**`, table for Open & Unassigned as a list, "Themes observed", scoring table with "Factor | Score | Rationale", "Assumptions & Limits", "Next Actions" as numbered list, "Appendix: Full Scored List").

Explicitly include a "Scan time (UTC)" and "Tools used" line near the top.

## All Other Rules Identical
- Markdown only, no JSON blocks.
- Full pagination required.
- State rate limits and gaps honestly.
- Read-only analysis.

## Success Criteria
Same as most-important-issue: evidence-based, reproducible by another agent with the same MCP tools, single unambiguous top issue.

## When to Prefer This Variant vs most-important-issue
- Use this one when the user specifically says "highest priority issue" or references the v3 workflow by that name.
- The other variant produces slightly more verbose "Why this is top priority" narrative sections.

Both are valid; the rubric and data gathering are identical.
