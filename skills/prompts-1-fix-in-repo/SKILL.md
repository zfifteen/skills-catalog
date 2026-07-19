---
name: prompts-1-fix-in-repo
description: >
  Apply the focused "1 Fix in Repo" prompt-library workflow: deeply analyze an entire
  repository (or provided repo material), identify logical, documentation, or computational
  errors, create a new branch for the work, then deliver a ruthlessly scoped review on ONLY
  the single highest-severity issue. All other findings are excluded by design.
  Use when the user says "1 fix in this repo", "highest severity issue in the whole repo only",
  "use the 1-fix repo prompt", "find the one thing to fix across this codebase", or runs
  /prompts-1-fix-in-repo. Also when a repo root or broad collection of files is the input.
when-to-use: "Narrow single-issue repository-wide review. Triggers: '1 fix in repo', 'single worst problem in the entire codebase', 'repo audit but only report the top one', 'create branch and fix the highest severity item'. Prevents scope explosion in large codebases."
argument-hint: "<repository path, root URL, or description of the repo material to analyze>"
allowed-tools: ["read_file", "grep", "list_dir", "web_fetch", "open_page", "open_page_with_find", "search_repositories", "search_code", "git", "run_terminal_cmd"]
metadata:
  short-description: "Single highest-severity issue across an entire repository (with branch creation)"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/prompts-1-fix-in-repo/SKILL.md"
  version: "1.0.0"
---

# 1 Fix in Repo — Grok Port

Apply a high-discipline, whole-codebase but single-issue audit. The output is intentionally minimal so the implementer receives one clear target instead of a flood of findings.

## Purpose

The Codex original forces extreme focus: analyze broadly, but report on exactly one issue (the worst), and for that issue the reviewer is expected to create a branch. This Grok port preserves the "one thing only" contract while adding tool-grounded analysis of real repository state.

## Invocation

```
/prompts-1-fix-in-repo <repo root path or URL>
```

Natural triggers as listed in when-to-use. The conversation context, any linked repo, or the current working directory (if inside a git repo) supply the `{input_material}`.

## Input Grounding (Grok Adaptation)

1. **Determine the repository root**:
   - If a path is given: `list_dir` + `read_file` on key files (README, AGENTS.md, package manifests, main source dirs).
   - If a GitHub URL: use web tools or MCP repository tools to explore.
   - If inside a workspace: use `run_terminal_cmd` with `git rev-parse --show-toplevel` (if the runtime exposes terminal) or start from cwd and walk up.

2. **Build architecture map** (lightweight):
   - Use `grep` with glob filters or `list_dir` recursively (respecting reasonable depth) to identify core modules, entry points, critical algorithms, and any AGENTS.md / PGS contracts.
   - Pay special attention to invariants, proved statements, or deterministic structures (per AGENTS.md for this workspace).

3. **Sample for risk**:
   - Focus tool calls on high-churn or high-complexity areas, recent changes (if git history accessible), and anything touching core mathematical/computational claims.

## Core Analysis Contract (Adapted from Original)

Dig deep into this repo, identify any logical, documentation or computational errors.

- Create a new branch (when the environment supports it; otherwise clearly describe the intended branch name and starting point).
- Select the **highest severity issue** and provide a focused review about **that one issue only**.
- For any false positives discovered during analysis, add a code comment explaining why the item is actually correct (so future reviewers are not misled).
- **Do not mention or reference any other issues or concerns** apart from the single selected issue.
- Scope is intentionally limited so the implementer does not get confused or distracted by verbosity.
- If no issues are found, reply with **"Looks good."** followed by any other analysis or comments you deem appropriate and relevant.

## Output Shape (Strict)

**When an issue is selected:**

```
## Highest-Severity Issue (1 Fix in Repo)

**Branch**: `fix/<short-kebab-description>` (create with `git checkout -b ...` or equivalent)
**Location**: `path/to/file.ext:NN` (primary site; note secondary sites if the pattern is systemic but still report as one issue)
**Severity**: bug | security | invariant-violation | doc-error | computational-error | architectural-drift
**Why highest severity**: (1-2 sentences on blast radius or contract violation; in PGS contexts any weakening of invariants is automatically selected)

**Description**:
[Precise technical explanation with direct references to code or docs]

**Recommended Fix**:
[Concrete guidance. If the fix is small, sketch the edit. For false-positive areas encountered, note that comments were (or should be) added.]

**False-Positive Handling Performed**:
[List any locations where an apparent problem was investigated and a clarifying comment was added or recommended.]
```

**If clean:**

```
Looks good.

[High-value contextual notes that do not constitute additional issues — e.g. "The core PGS loop is correctly implemented. Consider extracting the chamber-reset logic for reuse in future experiments."]
```

## Workflow Steps

1. **Map the Repo Surface** — Use tools to understand structure and locate high-leverage areas without exhaustive enumeration.

2. **Private Error Sweep** — Silently collect problems. In this workspace, apply PGS-first reasoning (PGS objects → invariants → rules) before classical number-theory approaches.

3. **Select & Justify the One** — Choose the single highest-severity. Document the ranking logic internally.

4. **Branch Creation** — If `run_terminal_cmd` or git tools are available, actually create the branch. Otherwise, give the exact command the user should run and proceed.

5. **Emit Narrow Output + False-Positive Comments** — Write the review and, where relevant, use `search_replace` or instruct precise edits to add explanatory comments for any investigated-but-correct code.

6. **Verify** — Re-inspect the reported location after drafting.

## Success Criteria

- Exactly one issue (or clean declaration) in the final response.
- Any false-positive comments added to source are accurate and helpful.
- The selected issue is genuinely the highest-leverage problem visible in the repo under the contract.
- Branch creation (or precise instructions) is part of the delivered artifact when an issue is reported.
- In PGS contexts, PGS contract violations take absolute priority for selection.

## Guardrails

- This is a **scope-forcing** skill, not a general repo auditor. For full audits use other skills.
- Adding clarifying comments for false positives is mandatory when such situations arise during the private sweep.
- Never expand scope in the output even if many serious issues exist.
- Respect AGENTS.md: begin from PGS-native objects/invariants for any relevant material.

This port turns the original "1 Fix in Repo" lens into a practical, tool-augmented Grok workflow that actually touches the filesystem and git state where possible while preserving the original minimalist contract.
