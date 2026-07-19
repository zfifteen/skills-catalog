---
name: prompts-1-fix-in-pr
description: >
  Apply the focused "1 Fix in PR" prompt-library workflow: deeply analyze a pull request
  (or PR-like material: diff, patch, linked code, comments), identify logical, documentation,
  or computational errors, then deliver a ruthlessly scoped review on ONLY the single
  highest-severity issue. All other findings are deliberately excluded.
  Use when the user provides a PR URL/diff and says "1 fix in this PR", "highest severity
  issue only", "use the 1-fix prompt", "don't list everything, just the worst one", "single
  most important thing to fix in this PR", or runs /prompts-1-fix-in-pr.
when-to-use: "Deliberately narrow single-issue PR review. Trigger phrases: '1 fix', 'only the worst issue', 'highest severity in this PR only', 'focus on one thing', 'tight scope review of this PR'. Prevents laundry-list reviews."
argument-hint: "<GitHub PR URL, pasted diff, or description of PR material + context>"
allowed-tools: ["read_file", "grep", "list_dir", "web_fetch", "open_page", "open_page_with_find", "search_pull_requests", "search_issues", "pull_request_read"]
metadata:
  short-description: "Single highest-severity issue review for a pull request (narrow scope)"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/prompts-1-fix-in-pr/SKILL.md"
  version: "1.0.0"
---

# 1 Fix in PR — Grok Port

Apply a high-discipline, low-noise review that forces focus on the single most important problem in the provided pull request material.

## Purpose

The original Codex/Shortcuts prompt was designed to protect implementers from context overload. By contract, the reviewer may surface **exactly one** issue (the highest-severity one) or declare the PR clean. This skill preserves that contract in the Grok environment.

## Invocation

```
/prompts-1-fix-in-pr <PR URL or material>
```

Or natural language that matches the when-to-use triggers above. The current user message, any attached diffs, linked GitHub PRs, local file paths mentioned, or pasted code become the `{input_material}`.

## Input Grounding (Grok Adaptation)

1. If a GitHub PR URL is present (e.g. `https://github.com/.../pull/NNN`):
   - Prefer MCP `pull_request_read` or `search_pull_requests` + follow-ups if available in the active environment.
   - Fall back to `web_fetch` or `open_page` on the PR URL + `.diff` or `.patch` suffix.
   - Fetch comments and linked files.

2. If local paths or diffs are referenced:
   - Use `read_file` (with offset/limit for large files) and `grep` to inspect the actual changed code.

3. If the material is purely conversational or pasted text:
   - Treat the full user-provided content as the primary artifact. Still use tools to resolve any mentioned files/URLs for ground truth.

4. Build a precise mental model of the changes: what files touched, nature of the diff (bugfix, refactor, feature, docs), risk surface.

Record the exact sources examined.

## Core Analysis Contract (Adapted from Original)

Dig deep into the pull request material. Identify any logical, documentation, or computational errors.

Then:

- Select the **single highest-severity issue**.
- Provide a **focused review about that one issue only**.
- **Do not mention or reference any other issues or concerns** apart from the one selected.
- The scope is intentionally limited so the implementer does not get confused or distracted by verbosity.
- If no issues are found, reply with **"Approved"** followed by any other high-level analysis or comments you deem appropriate and relevant.
- Target output under ~8000 characters.

Severity is judged by: potential for incorrect behavior, data corruption, security impact, maintainability destruction, or violation of invariants (in PGS contexts, any weakening of proved laws or objects is automatically highest severity).

## Output Shape (Strict)

**If issues exist (the common case for this skill):**

```
## Highest-Severity Issue (1 Fix in PR)

**Location**: `path/to/file.ext:NN` (or PR description / comment N)
**Severity**: bug | security | invariant-violation | doc-error | computational-error
**Why this is the single highest-severity**: (1-2 sentences tying to blast radius or contract violation)

**Description**:
[Precise technical explanation of the problem, with evidence from the diff or code]

**Recommended Fix**:
[Concrete, minimal suggestion or patch sketch. Include why it resolves the root cause without introducing new scope.]

(End. No other issues listed.)
```

**If clean:**

```
Approved

[Any brief, high-value contextual comments that do not constitute additional "issues" — e.g. "This is a clean refactoring that improves X. Consider adding a test for the edge case at line 87 in a follow-up."]
```

Never produce a list, never say "the main issues are... but I'm only reporting one", never hedge the "only one" rule.

## Workflow Steps

1. **Ground & Summarize Changes** (Observe)
   - Load the PR material and key files using tools.
   - Produce a 3-6 bullet internal summary of what the PR actually does.

2. **Error Enumeration (Private)**
   - Silently enumerate all problems you can find (logical, docs, computational, style that affects correctness, missing tests for risky changes, etc.).
   - In a PGS workspace, explicitly check against AGENTS.md: any reframing of deterministic laws, classical methods used as primary instead of PGS objects first, etc.

3. **Severity Ranking & Selection (Decide)**
   - Rank the private list by impact.
   - Pick exactly one. If tie, prefer the one with largest blast radius or that touches core invariants.

4. **Write the Focused Output (Act)**
   - Emit only the approved shape above.
   - Use precise file:line references where possible (re-read the file with `read_file` to confirm lines).

5. **Verification**
   - Re-read the key file region after drafting to ensure the reported location and description are accurate.

## Success Criteria

- The emitted review contains **at most one** technical issue.
- Every claim in the review is traceable to specific evidence in the PR material or fetched artifacts.
- If the PR is clean, "Approved" appears prominently and the tone is appropriately affirmative without false praise.
- The implementer (human or agent) can act on the single finding without being distracted.
- In deterministic/PGS contexts, any violation of PGS invariants is automatically surfaced as the selected issue (per AGENTS.md).

## Guardrails

- This skill is **not** a general PR reviewer. It is a scope-forcing lens. If the user wants a full review, they should use a different skill (e.g. a review or peer-review skill).
- Never "leak" other findings into the response even as hints.
- When material is ambiguous, state the ambiguity as part of the single issue rather than listing multiple.
- Respect higher-priority contracts (AGENTS.md PGS-first reasoning for any number-theoretic or structural claims in the PR).

This port keeps the original "1 Fix" discipline while giving Grok the tools to actually fetch and ground the analysis in real repository state.
