---
name: technical-task
description: >
  Convert the current conversation context, files, error logs, or feature request into a
  high-quality technical issue description ready for GitHub (or linear/jira). Includes
  reproduction steps, expected vs actual, scope, acceptance criteria, and links to all
  relevant code and prior work. Use when the user says "turn this into a technical task",
  "write a GitHub issue for...", "/technical-task", "grok-task-v3-technical-task", or
  needs a precise, actionable issue body from loose discussion.
when-to-use: Use when the user wants the current discussion or task turned into a formal GitHub-style technical issue description.
argument-hint: "[optional: target repo or 'for the current bug/feature']"
metadata:
  short-description: "Turn context into GitHub-ready technical issue"
  source: "ported-from-codex/grok-task-v3-technical-task"
  original_codex: "grok-task-v3-technical-task"
---

# Technical Task

Turn the provided material into a complete, copy-paste-ready technical issue description.

## Steps
1. **Gather Context Thoroughly**
   - Read all mentioned or attached files using `read_file`.
   - Use `grep` to find related code, tests, and comments.
   - Use `run_terminal_cmd` for `git log --oneline -10 -- <relevant paths>`, `git diff`, etc.
   - If GitHub context is available, use `grok_com_github` MCP tools to pull exact issue/PR text, comments, and linked code.
   - Capture exact error messages, stack traces, or unexpected outputs verbatim.

2. **Structure the Issue**
   Produce Markdown with these exact top-level sections (adapt headings only if the target tracker uses different conventions):

   ```markdown
   ## Summary
   One or two sentences stating the problem or requested capability.

   ## Background
   Why this matters. Link to project goals, user impact, or technical debt.

   ## Reproduction (if bug) / Current State (if feature)
   Exact steps or current code/behavior. Include file paths + line numbers.

   ## Expected Behavior
   What should happen. Be specific and testable.

   ## Actual Behavior (or Gap)
   What actually happens or what is missing. Include verbatim logs/quotes.

   ## Scope
   - In scope
   - Explicitly out of scope

   ## Acceptance Criteria
   - [ ] Criterion 1 (measurable)
   - [ ] Criterion 2
   ...

   ## Proposed Approach (optional but recommended)
   High-level sketch of how it could be solved. Note any prior art in the repo.

   ## References
   - File: path/to/file.ext:LINE (key excerpts)
   - PR / Issue: links with short quote
   - External: URLs + 1-line relevance
   - Conversation context: (if needed) key quotes from this chat

   ## Labels / Components (suggested)
   - e.g. `bug`, `enhancement`, `performance`, `docs`
   - Affected modules: `src/core/`, `tests/prime_gap/`
   ```

3. **Make It Actionable and Evidence-Based**
   - Every claim about current behavior must be backed by a tool result you performed.
   - Include enough context that a new contributor can start work without asking clarifying questions.
   - If the task involves this repo's PGS work, include the required PGS objects/invariants framing in the Background or Proposed Approach.

4. **Output**
   - Present the full issue body ready to copy into GitHub "New issue".
   - Also output a suggested title (≤ 72 chars, conventional style).
   - Ask: "Shall I create the issue using the GitHub MCP tools, or save this as a local draft file?"

## Success Criteria
- A competent engineer unfamiliar with the conversation can implement from the issue alone.
- All reproduction / current-state details are verifiable from the links and excerpts provided.
- No "TODO: fill in" or placeholder text remains.
- Scope and acceptance criteria are specific enough that "done" is unambiguous.

## Related Skills
- `/user-story` for the product/user-facing version
- `/implementation-plan` if the task is large and needs phasing
- `/technical-design-document` if architecture decisions need capture first
