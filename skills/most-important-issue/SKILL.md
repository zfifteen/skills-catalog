---
name: most-important-issue
description: >
  Act as a meticulous repository analyst. Given a GitHub repo or issues URL, enumerate
  ALL open UNASSIGNED issues, read them fully (body + comments), analyze recent merged
  PR history, apply a rigorous 0-10 scoring rubric (Impact, Urgency, Coupling, Effort,
  Recency), and identify the SINGLE highest-priority unassigned issue with full evidence
  and provenance. Output is strict Markdown only (no JSON blocks). Use when the user
  says "find the most important issue", "highest priority unassigned issue in...",
  "/most-important-issue", "grok-task-v3-most-important-issue", or provides a GitHub
  issues URL for prioritization.
when-to-use: Use when the user provides (or the conversation implies) a GitHub repo/issues URL and wants an objective, evidence-based recommendation for the single most important open unassigned issue to tackle next.
argument-hint: "<GitHub repo or issues URL, e.g. https://github.com/org/repo/issues>"
metadata:
  short-description: "GitHub repo analyst: pick highest priority unassigned issue from open list + merged PRs"
  source: "ported-from-codex/grok-task-v3-most-important-issue"
  original_codex: "grok-task-v3-most-important-issue"
---

# Most Important Issue (Repo Analyst)

## Prerequisites
This skill relies heavily on the connected `grok_com_github` MCP server (45 tools). Before starting:
- If you do not know the exact tool names and schemas, first invoke the MCP discovery / list tools (the system will provide the protocol for this).
- Common tools you will need: `list_issues`, `search_issues`, `get_issue` (or equivalent for body/comments), `list_pull_requests`, `get_pull_request`, `get_commit`, `search_repositories`, etc.
- You may also use `run_terminal_cmd` with `gh` CLI if it is installed and authenticated in the environment.

## Step-by-Step Procedure (Follow Exactly)
1. **Resolve OWNER/REPO**
   - Parse the TARGET_URL.
   - Use MCP tools to verify the repo exists and fetch basic metadata (description, stars, open issues count, etc.).
   - If URL is ambiguous, search and disambiguate.

2. **Enumerate Open Unassigned Issues**
   - Use the appropriate list/search tool with filters: state=open, assignee=none (or no assignee), per_page=100.
   - Fully paginate until a page returns fewer results than requested.
   - For every issue collect: number, title, labels, created_at, updated_at, comments_count, author, html_url.
   - Then fetch full body + all comments for each (use get + list comments tools). Extract 1-3 exact quotes per issue that speak to impact, urgency, or coupling.

3. **Analyze Recent Merged PRs**
   - Retrieve merged PRs for the last 90 days (expand to 180 if zero results).
   - For each: number, title, labels, merged_at, author, html_url, files touched (if available), body summary.
   - Identify recurring themes, components, regressions, and follow-up work implied by the merges.

4. **Score Every Open Unassigned Issue (0-10 total)**
   Rubric (document numeric breakdown for each):
   - Impact (0-3): user-visible breakage, security, data loss, blocks critical workflows.
   - Urgency (0-3): active regression, high comment velocity, recent reports, time-sensitive.
   - Coupling (0-2): overlaps hot areas from recent merged PRs or unblocks many pending tasks.
   - Effort (0-1, inverted): small/medium change with large payoff scores higher.
   - Recency (0-1): recently updated scores higher (stale lower unless severe).
   - Total = sum. Ties broken by clearer scope + broader unblock value.

5. **Select and Justify the Single Highest**
   - Choose only one.
   - Provide full evidence table.
   - Cite every claim with exact URL + short verbatim quote + UTC timestamp.

6. **Output Format (Markdown Only — No JSON)**
   See the original Codex skill for the exact detailed table layout (Summary, Why this is top priority, Evidence bullets, full tables for Open & Unassigned Issues, Merged PRs, Scoring & Decision, Appendix with all scored issues, Pagination/Rate-Limit Notes, Next Actions).

   Include at the top:
   - Repo Scan — owner/repo
   - Scan time (UTC): ...
   - Tools used: list of MCP tool names actually called + any gh fallback.

## Constraints
- Output Markdown only. Never emit a ```json block.
- No fabrication. If rate limited or API returns partial data, state exactly what was fetched vs. what is missing.
- Be explicit about pagination counts and rate-limit status.
- Read-only: never create issues, comments, or branches during analysis.

## Success Criteria
- The chosen issue is demonstrably the highest by the published rubric using data that another agent can re-fetch.
- Every number (issue count, PR count, scores) matches the raw tool output.
- The "Next Actions" are concrete and start with the chosen issue.

## For This Repo + PGS Work
When scanning prime-gap-structure or related Z-Framework repos, explicitly note in the analysis whether any high-priority issues align with or threaten the deterministic PGS laws and invariants described in AGENTS.md.

## Related Skills
- `/highest-priority-issue` (variant with slightly different output headings)
- `/most-important-development` (focus on merged PR themes instead of open issues)
- `/second-opinion` after you have a candidate
