---
name: user-story
description: >
  Convert the current context, task, bug, or feature request into a detailed User Story
  following a structured format that includes: As a [role], I want [goal] so that [benefit],
  detailed acceptance criteria, links to all GitHub work (issues, PRs, commits), citations
  for every external reference, and a dedicated "Reasoning & Reproducibility for LLMs"
  section. Use when the user says "turn this into a user story", "write a user story for...",
  "/user-story", "grok-task-v3-user-story", or needs traceable product requirements.
when-to-use: Use when the user wants the current work item expressed as a formal User Story with full traceability and an LLM-reproducibility section.
argument-hint: "<short goal or feature name>"
metadata:
  short-description: "Detailed User Story with GitHub links, citations, and LLM reasoning section"
  source: "ported-from-codex/grok-task-v3-user-story"
  original_codex: "grok-task-v3-user-story"
---

# User Story

Produce a complete, traceable User Story from the provided material.

## Step 1: Research & Link Everything
Before writing:
- Use `grok_com_github` MCP tools (or `run_terminal_cmd` + `gh` if available) to find and link all related GitHub issues, PRs, commits, and discussions. Quote the most relevant snippets.
- Use `read_file` + `grep` on the local repo for code, tests, docs that implement or relate to the story.
- Use `web_search` / `web_fetch` / `open_page` for any external standards, papers, or prior art mentioned. Capture exact titles, authors, URLs, and 1-2 sentence relevance + access date.
- If images, logs, or attachments were provided, describe their content precisely and link or embed references.

## Step 2: Write the User Story
Use this exact structure (Markdown):

```markdown
# User Story: <Short Title>

**As a** [specific role, e.g. "researcher analyzing prime gaps > 10^18" or "maintainer of the Z5D predictor"],
**I want** [clear goal],
**so that** [business or research benefit / outcome].

## Acceptance Criteria
- [ ] AC1: ...
- [ ] AC2: ... (each must be testable / demonstrable)
...

## Detailed Requirements
- Functional
- Non-functional (performance, accuracy, reproducibility)
- Edge cases / error handling

## References & Provenance
### GitHub Work
- Issue #123: "..." (link) — relevant quote
- PR #456 (merged): "..." (link) — files changed summary
- Commit abc1234: "..."

### External Citations
- Paper: "Title" by Author (Year) — URL — "Exact quote or finding used"
- Standard / Spec: ...

### Local Code & Docs
- `path/to/file.py:42` — "key function or comment"
- `AGENTS.md` — "PGS-first requirement"

## Reasoning & Reproducibility for LLMs
**Context captured at time of writing:** [UTC timestamp]

**Key observations from tools:**
1. ...
2. ...

**Why this story is prioritized now:**
- ...

**Potential implementation notes (non-binding):**
- ...

**How another LLM can reproduce this analysis:**
1. Clone repo at <commit or branch>.
2. Run `grep -r "..."` for ...
3. Read the exact files listed above.
4. ...

## Out of Scope
- ...
```

## Step 3: Validate Traceability
- Every acceptance criterion must be derivable from the "References & Provenance" section.
- The "Reasoning & Reproducibility for LLMs" section must contain enough concrete commands, file paths, and quotes that a fresh model with the same tools can arrive at the same story.

## Step 4: Present
Show the full story. Offer:
- "Save this to a local file under docs/user-stories/ ?"
- "Convert one or more ACs into `/technical-task` GitHub issues?"
- "Create an `/implementation-plan` from this story?"

## Success Criteria
- A product manager or new engineer can understand the "why" and "what done looks like" without reading the entire conversation.
- Every external or GitHub claim has a working link + verbatim supporting quote captured at the time of writing.
- The reproducibility section is genuinely useful to another LLM (not generic advice).

## For This Repo
User stories involving prime-gap or number-theoretic work must explicitly reference the AGENTS.md PGS objects → invariants frame in the Requirements or Reasoning section.
