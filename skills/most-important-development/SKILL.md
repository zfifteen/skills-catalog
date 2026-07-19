---
name: most-important-development
description: >
  Deeply analyze a Git repository (local working directory or via GitHub URL) by examining
  merged pull requests (titles, descriptions, comments, files touched). Extract themes,
  quantify patterns, and identify the SINGLE most important development activity the
  project owner should focus on next. Output structured with Merged PR Summary, Key
  Themes, Most Important Development Activity, and Detailed Justification with citations.
  Use when the user says "most important development", "what should we work on next based
  on PR history", "/most-important-development", "grok-task-v3-most-important-development",
  or points at a repo for PR-driven prioritization.
when-to-use: Use when the user wants a recommendation for the single highest-leverage next development focus derived from analysis of merged PR history (local git or GitHub).
argument-hint: "[optional GitHub URL or leave blank for current local git repo]"
metadata:
  short-description: "Analyze merged PRs to recommend the single most important next dev focus"
  source: "ported-from-codex/grok-task-v3-most-important-development"
  original_codex: "grok-task-v3-most-important-development"
---

# Most Important Development (PR History Analyst)

## Step 1: Determine Scope & Gather Data
- If the user gave a GitHub URL: use `grok_com_github` MCP tools to list and fetch merged PRs (state=closed, filter merged, paginate, fetch details, comments, files).
- If no URL (default): this is the local working directory. Use `run_terminal_cmd` for:
  - `git log --merges --pretty=format:"%h %an %ad %s" -n 200` (or more)
  - `git log --merges --pretty=fuller` for details
  - For each promising merge commit, use `git show --stat`, `git log -1 --format=%B <sha>`
  - If `gh` CLI is available and repo has remote: `gh pr list --state merged --limit 100 --json ...` and `gh pr view <number> --json comments,files`
- Aim for at least the last 50 merged PRs (or the entire history if the repo is smaller). Note the actual window used (date range or count).

## Step 2: Deep Thematic Analysis
For every merged PR examined:
- Extract title, body summary, comments (especially review threads), files changed, labels.
- Categorize changes: Bug fix, Feature, Refactor, Performance, Docs, Deps, Tests, CI, etc.
- Note recurring pain points, keywords that appear in >15-20% of PRs, long comment threads, repeated revisions.
- Quantify where possible (counts, percentages, median thread length).
- Cross-reference with project goals from README, AGENTS.md, package.json / pyproject.toml, etc.

## Step 3: Synthesize the Single Most Important Focus
From the patterns, identify exactly **one** primary development activity that would have the highest leverage.

Prioritization factors (document your weighting):
- Frequency + severity of the theme in PR history
- Strategic alignment with core project objectives (PGS invariants for this repo)
- Unresolved debates or open questions left in comments
- Potential to reduce future "regret" PRs (the ones that fix the same class of problem repeatedly)

The output must name a specific, actionable focus area (e.g. "Harden error handling and null-check discipline in the divisor-count and gap-walking core" rather than "improve code quality").

## Step 4: Structured Output
```markdown
## Merged PR Summary
- Total analyzed: N (last X days / all history)
- Date range: ...
- Primary sources: local git log + gh / MCP GitHub tools

## Key Themes Extracted (Top 3-5)
1. **Theme Name** (appeared in 37% of merged PRs, median 8 comments)
   - Evidence: PR #12, #19, #27, #41 (quotes + links)
   - ...

## Most Important Development Activity
<One clear sentence naming the single focus area>

## Detailed Justification
3-5 paragraphs with specific citations, metrics, and why this one activity outweighs the others. Explain the chain from observed PR patterns → root cause → why fixing it here has outsized impact on future velocity and correctness.
```

## Step 5: Validation
- Re-read your own analysis against the raw PR data you fetched.
- If data was insufficient (very young repo, private history not accessible), state that plainly and suggest the next best action (e.g. "Scan open issues instead with /most-important-issue").

## Success Criteria
- The recommended activity is the logical synthesis of measurable patterns in the actual merged PR corpus, not generic advice.
- Every claim ("37% of PRs", "median 8 comments") is backed by the counts you performed during the run.
- For this repo: the recommendation explicitly considers the deterministic PGS laws and invariants from AGENTS.md.

## Related Skills
- `/most-important-issue` (focus on open unassigned work instead of history)
- `/highest-priority-issue`
- `/implementation-plan` once the focus area is chosen
