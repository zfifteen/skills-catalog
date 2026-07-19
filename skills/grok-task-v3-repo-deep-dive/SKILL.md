---
name: repo-deep-dive
description: >
  Perform an ultra-deep, tool-grounded dive into a GitHub repository (clone if necessary), deriving 1-2 non-obvious, high-impact observations about its architecture, algorithms, or emergent behavior — especially those with practical applications. 
  Use when the user provides (or the context contains) a repository URL and asks for a "repo deep dive", "deep analysis of this codebase", "what's surprising in this repo", "architectural insights", or the specific "grok-task-v3-repo-deep-dive" workflow.
when-to-use: "User supplies a GitHub repo URL (or points to one in conversation/attachments) and wants a deep, non-obvious analysis of the actual source: architecture, algorithms, emergent patterns, practical applications, with specific file:line citations. Grounded in checked-out code + verifiable external sources. 1-2 high-impact observations only."
allowed-tools: ["run_terminal_cmd", "read_file", "grep", "list_dir", "web_fetch", "web_search", "open_page", "open_page_with_find", "search_replace", "write", "todo_write", "x_keyword_search", "memory_search", "grok_com_github"]
argument-hint: "<repository URL or local path> [focus area]"
metadata:
  short-description: "Ultra-deep, citation-backed architectural & algorithmic analysis of a codebase"
  source: "Codex 'grok-task-v3-repo-deep-dive' (ported 2026-05-24)"
---

# Repo Deep Dive (Grok Port)

**PGS Project Contract (this repository):** If the target repository concerns prime gap structure, divisor fields, GWR/DNI rules, endpoint chains, or any number-theoretic research, **you MUST begin reasoning from the PGS-native frame per AGENTS.md**:

PGS objects → PGS invariants → PGS rule or law → resolved/unresolved/invalidated PGS state.

Do NOT default to classical number theory, sieves, Miller-Rabin, `isprime`, `gcd`, probabilistic methods, or cryptographic assumptions. Classical tools enter only for explicit comparison when requested by the user. This is non-negotiable for any PGS-related work in this repo.

## Core Instruction (preserved & adapted)

Treat the current user message, attachments, files, links, images, and other task material as the working context.

Perform an ultra–deep dive into the codebase hosted at the repository URL provided (or the local checkout if already present).

If the repository is not already present in the current working directory (or a clearly related subdirectory), clone it first using `run_terminal_cmd` (`git clone <REPO_URL>` into a sensible location such as `/tmp/grok-deep-dives/<slug>` or the user's preferred work area).

Then, based on the actual source files, derive **one or two** non-obvious, high-impact observations about the project’s architecture, algorithms, or emergent behavior, especially those with practical applications (e.g., new compositional patterns, surprising performance/robustness properties, novel abstractions).

## Constraints and Method (strict)

- Treat the local repository contents as primary ground truth; traverse code, tests, docs, and configuration using `list_dir`, `read_file`, `grep`. Reference specific paths (e.g., `src/module/file.ext:42`) when supporting claims.
- You may use public, independently verifiable external sources (e.g., library specs, standards, academic papers) via `web_fetch`, `web_search`, `open_page`. Include at least one working hyperlink for each external source you cite (use `render_inline_citation` where the source came from a web_search result).
- Do not fabricate repository structure, files, or behaviors; if something is not present in the checked-out code, say so. Clearly label any speculative extrapolations and base them on concrete code evidence.
- Treat “groundbreaking / never-before-presented” as: “plausibly novel or under-documented combinations or perspectives,” not as a provable claim of absolute global novelty.
- Use `todo_write` for any multi-stage traversal or cross-file analysis tracking.
- When the repo is large, prioritize high-signal directories (src/, core/, lib/, algorithms/, architecture docs) and use targeted `grep` + `read_file` rather than exhaustive enumeration.

## Output Format (exact structure, terse)

Respond with exactly these sections:

**Title**  
A concise, specific title for the deep-dive report (e.g. "Two Emergent Patterns in the XYZ Engine's State Machine That Enable Zero-Copy Replay").

**Observation(s)** (1–2 only)
- Concise, high-impact point about what the repository uniquely enables, surprising properties, or powerful but non-obvious uses.
- Each observation must be backed by evidence.

**Supporting Data**
- Bullet list tying each observation back to specific code locations (file:line or dir) and, where relevant, external references (with working links or `render_inline_citation`).
- Include short, verbatim or near-verbatim excerpts where they illuminate the point.
- Quantify impact where possible (e.g., "reduces allocation pressure by N% on the hot path", "enables the only O(1) path for Z").

**Methodology & Scope**
- Brief: how the checkout was obtained, key directories traversed, tools used, any limits (e.g., "did not expand submodules", "focused on core/ and ignored vendor/").

**Access or Clarification Needed** (only if relevant)
- Any missing pieces that would materially improve the analysis (private repo access, specific large data files, build logs, etc.).

## Step-by-Step Execution (Grok agent)

1. **Locate or obtain the repository**
   - If a local path is already in context or the user points to a checkout: use it.
   - Otherwise: parse the URL, derive a safe local slug, `git clone` via `run_terminal_cmd` (shallow clone is acceptable unless full history is needed for the question).
   - Record the absolute local path.

2. **Initial reconnaissance**
   - `list_dir` at root.
   - Read README, AGENTS.md / CONTRIBUTING / architecture docs, pyproject / package.json / Cargo.toml etc.
   - Identify the core language(s) and primary entry points.

3. **Deep traversal**
   - Use `grep` for architectural signals: class hierarchies, core state machines, hot loops, extension points, performance annotations, novel data structures.
   - Read the highest-leverage files (the ones that appear in many call graphs or comments).
   - Cross-reference tests and examples for emergent behavior.
   - For external context: fetch library docs, papers, or GitHub issues/PRs that illuminate design decisions.

4. **Synthesis**
   - Look for non-obvious combinations, robustness properties that fall out of the design, or patterns that are powerful precisely because they are not the "standard" approach.
   - Limit to the single best or two best observations. Ruthlessly discard weaker ones.

5. **Citation & verification**
   - Every claim has a locator.
   - External facts are fetched and cited properly.

6. **Produce the report** in the exact format above.

## Grok Tooling Notes

- `grok_com_github` MCP (if connected): excellent for additional context (list_commits, search_issues, get_file_contents on the remote without re-cloning), but the local checkout + `read_file`/`grep` remains the ground truth for deep code analysis.
- For very large repos, combine `run_terminal_cmd` (`find`, `git grep`, `cloc`, etc.) with the native tools for precision.
- `todo_write` is highly recommended for tracking the exploration plan across many files.

## Success Criteria

- The report contains 1–2 genuinely non-obvious, high-leverage insights that a casual reader of the README or top-level files would miss.
- Every statement is traceable to specific code locations or fetched external sources.
- The user feels they now see the "hidden power" or "surprising elegance" of the codebase.
- No hallucinated files or behaviors.

This port turns the original Codex "apply this prompt text" instruction into a fully tool-using, reproducible Grok workflow while preserving the strict output contract and depth expectations.
