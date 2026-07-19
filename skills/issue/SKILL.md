---
name: issue
description: >
  Create GitHub issues from the user's current request or conversation context. Resolve the target repository from the local checkout or explicit owner/repo, inspect existing labels, infer a suitable issue type label when possible, and create the issue using native GitHub tooling.
  Use when the user invokes /issue or $issue, asks to create/open/file a GitHub issue, or describes work that should be captured as an issue from a local GitHub repository checkout.
when-to-use: "User describes a bug, feature request, documentation task, maintenance item, or research/validation work and wants it turned into a properly labeled GitHub issue in the current repo (or a specified one). 'file an issue for this', 'create a GitHub issue', 'open an issue about the regression in X'."
allowed-tools: ["run_terminal_cmd", "read_file", "grep", "list_dir", "grok_com_github", "ask_user_question", "web_search"]
argument-hint: "[owner/repo or URL] <description of the issue>"
metadata:
  short-description: "Create well-formed GitHub issue from context, using existing repo labels"
  source: "Codex 'issue' skill (ported 2026-05-24)"
---

# GitHub Issue (Grok Port)

## Overview

Create one GitHub issue from the user's description, using the current local checkout to resolve the repository when possible. Use existing repository labels only, infer the issue type when the evidence is clear, and ask before creating the issue when repository or label choice is ambiguous.

Prefer the connected `grok_com_github` MCP tools for all GitHub operations (schema discovery first if tool names are not yet known in the session). Fall back to `gh` CLI via `run_terminal_cmd` only when the MCP is unavailable or insufficient for the required action.

## Workflow

1. **Resolve the repository**
   - If the user provided an explicit `owner/repo` or GitHub repository URL, use it.
   - Otherwise, from the current working directory, run `git rev-parse --show-toplevel` (via `run_terminal_cmd`) to find the repo root.
   - If not inside a Git repository, ask for the target repository in `owner/repo` form using `ask_user_question`.
   - Run `git remote -v` and collect GitHub remotes only.
   - Normalize to `owner/repo` form.
   - If exactly one GitHub repository is present, use it. If multiple, prefer `origin` only when all `origin` GitHub URLs agree; otherwise ask which repository to use via `ask_user_question`.
   - Once resolved, confirm the full name (e.g. "velocityworks/prime-gap-structure").

2. **Draft the issue**
   - Derive a concise title from the user's request.
   - Write a Markdown body that preserves the concrete facts the user supplied.
   - Do not invent reproduction steps, expected behavior, versions, files, screenshots, acceptance criteria, or implementation details.
   - If the request does not contain enough information to identify the issue, ask one direct question before creating it (use `ask_user_question`).

3. **Inspect existing labels (via MCP or gh)**
   - Preferred: use `grok_com_github` tools (after schema discovery if needed) to list labels for the repository.
   - Fallback: `run_terminal_cmd` with `gh label list --repo OWNER/REPO --json name`.
   - If labels cannot be inspected, state that plainly and ask whether to create the issue without labels or provide exact label names.
   - **Never create new labels** unless the user explicitly asks.

4. **Infer the issue type from the request and the existing labels**
   - Bug language: bug, broken behavior, regression, crash, failure, exception, error.
   - Feature language: feature, enhancement, capability, support, add, implement.
   - Documentation language: docs, documentation, README, explanation, guide, tutorial.
   - Maintenance language: refactor, cleanup, internal improvement, maintenance, tech debt.
   - Research language: research, experiment, benchmark, validation, measurement.
   - Apply only existing labels whose names match the inferred type or a clear local synonym.
   - If confidence is low or several label choices are equally plausible, ask the user to choose before creating the issue using `ask_user_question`.

5. **Create the issue**
   - Preferred path: use the appropriate `grok_com_github` MCP tool for issue creation (e.g. `issue_write` or equivalent after discovering the exact schema and parameter names via the MCP discovery step).
   - Fallback: `gh issue create --repo OWNER/REPO --title "..." --body "..." --label "..."` via `run_terminal_cmd`.
   - Do not assign users or set a milestone unless the user explicitly requested it.
   - Do not use update tools to replace labels after creation unless correcting a mistake in the same workflow.

6. **Return the result**
   - Include the issue number, URL, title, and labels applied.
   - Include a short body summary when the body is more than a few lines.
   - If no labels were applied, say `Labels: none`.
   - Use the compact output shape below.

## Label Selection Rules (preserved)

Prefer exact label names already present in the repository. If a repository has both broad and narrow labels that fit, choose the narrow issue-type label only when the request clearly names that category; otherwise ask.

Common mappings:
- `bug`, `regression`, or a clear local equivalent for broken behavior.
- `enhancement`, `feature`, or a clear local equivalent for new capability work.
- `documentation`, `docs`, or a clear local equivalent for documentation work.
- `refactor`, `maintenance`, `tech debt`, or a clear local equivalent for internal cleanup.
- `research`, `experiment`, `benchmark`, or a clear local equivalent for research or validation work.

When the repository has no suitable existing label for the inferred type, create the issue without that label and report that no matching existing label was available.

## Output Format

Use this compact shape:

```
Created issue:
- Repo: OWNER/REPO
- Issue: #NUMBER TITLE
- URL: https://github.com/OWNER/REPO/issues/NUMBER
- Labels: label-a, label-b
```

## Grok-Specific Adaptations

- **MCP First**: The connected `grok_com_github` server (with its 45+ tools including issue_write, list_issues, search_issues, get_label, etc.) is the idiomatic integration point. Always attempt MCP schema discovery (`call tool ...` or the documented MCP bootstrap) before guessing tool names.
- **Local checkout as context**: The git-based repo resolution is preserved because it gives the user a frictionless "just file it for the project I'm in" experience.
- **ask_user_question**: Used for any interactive choice (repo selection, label selection, confirmation of low-confidence inference).
- **No label invention**: Strict.

## Success Criteria

- The created issue URL is returned.
- Labels (if any) are exactly from the repository's existing set.
- The body is a faithful capture of the user's stated facts with zero invention.
- The user sees a clear, copy-pasteable record of what was created.

## Stop Conditions

- No usable GitHub authentication (neither MCP nor `gh`).
- User has not supplied enough information and clarification questions have been exhausted.
- The user explicitly says "don't create the issue yet" or similar.

This port maintains the original's disciplined use of existing labels and faithful capture while routing all GitHub mutations through Grok's native MCP surface where possible.
