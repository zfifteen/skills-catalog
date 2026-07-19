---
name: summarize-progress
description: >
  Generate a professional, evidence-grounded executive summary of recent progress
  in a target repository or research program. Audits git history, code, docs, PRs,
  issues, benchmarks, and artifacts to surface real advances, breakthroughs,
  active work, and risks — with zero invention. Use when the user says "summarize
  progress", "executive status update", "repo audit", "what's new in the project",
  "leadership summary of the last 30 days", or provides a repo path/URL + "summarize
  progress on this". Especially strong for technical research programs needing
  honest, source-cited status reports.
when-to-use: "Trigger on requests for repository or project executive summaries, progress audits, 'what have we accomplished recently', or leadership updates. Requires concrete repo context (local path, GitHub URL, or current workspace)."
allowed-tools: ["read_file", "grep", "list_dir", "web_search", "web_fetch", "open_page", "open_page_with_find", "memory_search", "memory_get", "todo_write", "write", "search_replace", "run_terminal_command"]
argument-hint: "<repo path or GitHub URL or 'this workspace'> [--days 30]"
metadata:
  short-description: "Repository executive summary generator — grounded, no invention"
---

# Summarize Progress

## Purpose

Produce a leadership-grade "Executive Status Update" for a repository or active research program. The output must be strictly derived from verifiable artifacts in the repo (commits, PRs, code comments, benchmark logs, issues, docs). No speculation, no invented metrics, no narrative padding.

This skill is the Grok-native port of the Codex "grok-task-v3-summarize-progress" workflow, adapted to Grok's toolset while preserving the original truth constraint and output structure.

## PGS Project Contract (prime-gap-structure and similar)

If the target is this workspace or any PGS-related research:
- Begin from PGS objects, invariants, DNI, GWR, endpoint chains, structural certificates, etc. (per AGENTS.md).
- Never reframe deterministic PGS laws as probabilistic or heuristic.
- Classical methods (sieves, Miller-Rabin, gcd, etc.) appear only for explicit downstream comparison when the artifact itself uses them.
- Every claim must map back to a specific file:line, commit, or artifact.

## Invocation

`/summarize-progress <target> [--days N]`

- `<target>`: local absolute path to repo root, GitHub URL (https://github.com/owner/repo), or "this workspace" / "." for the current project.
- `--days N`: look back window (default ~30 days or last 50 commits).

The skill will ingest the current conversation context plus explicit tool-gathered evidence.

## Workflow (Adapted for Grok Tools)

1. **Repo / Target Ingestion**
   - If local path or current workspace: use `list_dir`, `read_file`, `grep` to inspect structure, key docs (README, AGENTS.md, PROOF.md, RESULTS.md, recent essays), and any provided artifacts.
   - If GitHub URL: use `web_fetch` or `open_page` on the repo root, /commits, /pulls, specific file raw URLs (https://raw.githubusercontent.com/...). For history, fetch recent commit list pages and PR pages.
   - If terminal available (`run_terminal_command` permitted in environment): run `git log --oneline -50`, `git log --since="30 days" --pretty=...`, `git diff` on key ranges, `git branch --show-current`. Capture exact output.
   - Also search conversation attachments, pasted diffs, benchmark CSVs, prior memory entries via `memory_search`.
   - Record exact sources for every fact (file path + line or commit SHA or URL + section).

2. **Repo Baseline**
   - Identify default branch.
   - Most recent commit on it: hash, author, timestamp, one-sentence plain-language description of what the diff actually changed (read the diff or commit page).
   - Note any AGENTS.md / contract files that govern reasoning.

3. **Recent Direction of Work (Timeline / Thematic View)**
   - Gather last ~30 days / ~50 commits or equivalent from web pages / git output.
   - Group into themes (e.g. "endpoint-chain traversal improvements", "DNI reciprocal transport proofs", "GWR leftmost minimum-divisor rule applications").
   - For each theme: problem attacked, concrete changes (files edited, new invariants named), measurable claims only if present in sources (quote exactly: "3.92% → 0.077% offset", "50× closer").

4. **Breakthroughs / Accomplishments**
   - Only items explicitly labeled or strongly evidenced as breakthroughs, firsts, wall removals, large gains in the source material.
   - Include PR/commit pointer + concrete impact statement from the artifact itself.

5. **Active Work / Open Problems**
   - Open issues, in-flight PRs, TODOs, unresolved questions from docs or code.
   - Link to prior breakthroughs where relevant.
   - Note any superseded work.

6. **Risk / Fragility / Unproven Areas**
   - Explicit admissions of uncertainty, missing validation at target scale (e.g. 10^18), hand-tuned constants, lack of proof, etc.
   - Make it obvious what still requires experimental or formal work.

7. **Output Format (Strict)**
   Emit **only** the structured report (no intro, no "Here is the summary"):

   ```
   Executive Summary
   • 3–6 headline bullets of last period's real advances.

   Thematic Progress

   [Theme 1]
   • Goal: ...
   • What changed: ...
   • Impact / evidence: (exact quotes + locators only)
   • Key commits / PRs: ...

   [repeat for each theme]

   Breakthroughs / Milestones
   • ...

   Active Work / Next Steps
   • ...

   Open Risks / Validation Gaps
   • ...
   ```

8. **Truth & Citation Rules**
   - Every numeric or concrete claim must trace to commit message, PR description, code comment, benchmark log, or attached data. Otherwise: "(no quantitative data provided)".
   - Conflicting sources: report both.
   - Web / external facts: use `render_inline_citation` component.
   - For PGS work: surface the exact PGS objects/invariants in play.
   - No URLs unless they appear verbatim in the source artifacts.

## Success Criteria

- Every claim has a direct, locatable source (file:line, SHA, URL+section, or tool output quote).
- Output matches the exact structure above.
- No invented numbers, no "we believe", no future work speculation.
- Reader (external leadership) can act on the status with clear picture of what is proved vs. open.
- In PGS context: the summary respects the deterministic nature of proved laws and correctly identifies unresolved vs. invalidated states.

## Guardrails

- Higher contracts (AGENTS.md PGS-first, safety) always override.
- If insufficient evidence in the target (no git access, no provided artifacts), state the limitation plainly in the "Risks" section rather than guessing.
- Never use this skill to launder low-evidence claims into "executive" language.
- Prefer primary source inspection over secondary summaries.
- When in a prime-gap-structure workspace, the skill must explicitly call out any drift from PGS-native reasoning in the audited artifacts.

## Tool Notes for This Environment

- Local repo inspection: `list_dir`, `read_file` (with offset/limit for large files), `grep` (with context), `open_page_with_find`.
- Git history: `run_terminal_command` with `git ...` when the tool is available in the host environment.
- Remote GitHub: `web_fetch` + `open_page` on raw and HTML commit/PR pages; extract text.
- Cross-session state: `memory_search` / `memory_get` for prior summaries or key artifacts.
- State tracking: `todo_write` for multi-theme analysis.
- New artifacts (e.g. saved summary): `write`.

This produces the highest-fidelity, lowest-regret executive view possible from the actual ground truth in the repository.
