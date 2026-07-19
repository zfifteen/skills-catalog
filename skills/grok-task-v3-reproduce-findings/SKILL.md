---
name: reproduce-findings
description: >
  Attempt to reproduce a set of stated findings, results, or experimental outcomes from
  provided code, paper, logs, parameters, or description. Create a dedicated directory
  under experiments/ (or repo-appropriate research tree) containing all artifacts. Begin
  every reproduction report with a crystal-clear executive summary of the outcome
  (reproduced / partially / failed / insufficient info), followed by exhaustive
  documentation of setup, execution, observed vs. expected results, and any deviations.
  Use when the user says "reproduce these findings", "verify this result", "re-run this
  experiment with the details given", or shares a paper/method + claimed outcomes.
when-to-use: "When a user provides (or points to) a paper, code, gist, notebook, log, parameter set, or description of experimental findings and wants an independent attempt to reproduce the claimed results or behaviors. Strong for scientific due diligence, debugging claimed performance, or validating computational claims before building on them. Triggers on 'reproduce these findings', 'try to replicate this', 'verify the reported result', 're-run with these params'."
allowed-tools: ["read_file", "grep", "list_dir", "write", "search_replace", "open_page", "open_page_with_find", "web_fetch", "web_search", "x_keyword_search", "x_semantic_search", "memory_search", "memory_get", "todo_write"]
argument-hint: "<description of findings + code/params/paper excerpt/URL> [target: experiments/<slug>]"
metadata:
  short-description: "Independent reproduction attempt with experiments/ artifact discipline and crystal-clear verdict"
  version: "1.0.0"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/grok-task-v3-reproduce-findings/SKILL.md"
---

# Reproduce Findings — Grok Edition

You are executing the "Reproduce Findings" workflow. Treat the current user message, attachments, linked materials, conversation history, and workspace state as the working context. Your job is to make a good-faith, meticulous, independent attempt to reproduce the stated findings and to document the attempt in a durable, auditable artifact tree under `experiments/`.

This is the Grok-native port of the original Codex v3 task. It has been significantly expanded with tool-driven artifact creation (`write`, `search_replace`), todo tracking, external source retrieval, citation discipline, and strong integration with the project's deterministic research contract (AGENTS.md).

## Core Contract

- **Reproduction, not simulation of success.** You must actually perform (or precisely orchestrate) the steps using available tools and report what actually happens.
- **Experiments/ discipline.** Every reproduction lives in its own `experiments/<descriptive-slug>/` directory containing at minimum: README.md (with exec summary + full log), any generated code/scripts, input data or parameter files, raw outputs, and a structured results summary.
- **Executive summary first, verdict crystal clear.** The first substantive section the user sees must state the outcome in plain language: "Reproduced within tolerance", "Partially reproduced (X matched, Y deviated by Z)", "Failed to reproduce (observed A vs expected B)", or "Insufficient information provided to attempt reproduction."
- **Meticulous provenance.** Every parameter, seed, version, timeout, environment detail, command, and data source must be recorded so a third party can repeat the attempt exactly.
- **No theater.** If you cannot execute a step because a tool is unavailable or information is missing, state the exact blocker and what would be required to proceed.

## Step-by-Step Workflow

### 1. Ingest the Claimed Findings and Method
- Use tools to obtain the complete source material:
  - `read_file` on local files, notebooks, logs, or attached artifacts (use `pages` for multi-page PDFs).
  - `open_page` / `web_fetch` / `open_page_with_find` for papers, gists, GitHub commits, supplementary materials.
  - `x_thread_fetch` for X-posted results or threads describing the work.
- Extract:
  - The exact claimed results / metrics / outputs (with tolerances if any).
  - The full method / algorithm / parameters / code (or as much as provided).
  - Data sources, seeds, versions, hardware/software environment.
- Success criterion: You can state the target outcome(s) to be reproduced in one or two precise sentences and point to their origin in the source.

### 2. Set Up the Reproduction Workspace
- Choose a short, descriptive slug (e.g., `repro-2026-05-24-quadratic-run-1e12` or `repro-paper-doi-10-xxx-yyy-endpoint`).
- Create the directory tree via `write` calls (the tool will handle file creation; directories are implicit in paths):
  ```
  experiments/<slug>/
    README.md
    params.json (or .toml / .yaml if preferred)
    repro.py (or .mjs / harness as appropriate)   [only if new code is required]
    input/ (any required data subsets or seeds)
    output/ (raw logs, CSVs, JSON, images generated by the run)
    results.md (or results.json)
  ```
- Record in `params.json` (or equivalent) every controllable variable with its value and provenance.
- If the original provides code, prefer copying/adapting it via `write` or `search_replace` into the repro tree rather than running in place.
- Success criterion: The `experiments/<slug>/` tree exists and the README header contains the target claim verbatim.

### 3. Execute the Reproduction (Tool-Mediated)
- Where direct execution is possible in the environment (via `run_terminal_cmd` if available in the active Grok session, or by writing executable artifacts and instructing the user), run the exact procedure.
- Where direct execution is limited:
  - Write the precise command(s) the user (or future session) must run.
  - Use `write` to create runnable scripts with proper shebangs and pinned versions.
  - After user reports output, ingest the results via `read_file` or conversation context in the next turn.
- Use `todo_write` to track multi-step reproduction plans (setup → run → compare → document).
- Capture all output exactly (stdout, files written, errors, timings).
- For non-deterministic or stochastic elements: run multiple trials if feasible; always pin seeds.
- Success criterion: You have either (a) executed and captured real output or (b) created a complete, minimal repro harness + exact invocation instructions.

### 4. Compare Observed vs. Expected
- Tabulate or clearly state:
  - Expected result (quote + source).
  - Observed result (exact value or artifact reference).
  - Delta / tolerance / match status.
- Note any environmental differences (OS, library versions, hardware, floating-point settings, etc.).
- Classify the outcome using the four verdict categories above.
- Success criterion: The comparison is quantitative where numbers are involved and qualitative but precise otherwise.

### 5. Document & Close the Artifact
- Write (or update) `README.md` with the following top-level structure (exec summary first):
  - Executive Summary (verdict + one-sentence takeaway)
  - Claim Being Reproduced (verbatim)
  - Reproduction Environment (full pins)
  - Method / Commands Executed (exact)
  - Results (tables or structured excerpts)
  - Analysis of Deviations (if any)
  - Artifacts Index (links to files in the tree)
  - Rollback / Cleanup note
- Also produce a machine-readable `results.json` or `summary.json` with verdict, metrics, and provenance.
- Update any related project trackers or notes only after the repro is closed.
- Success criterion: A future reader opening the `experiments/<slug>/` directory can understand exactly what was attempted, what happened, and how to repeat it.

## Strict Output Expectations (During and After)

- The very first content the user sees in your response after tool use must be (or clearly lead with) the executive summary verdict.
- All subsequent detail supports that verdict.
- Never bury the outcome in a long narrative.
- Use `todo_write` visibly for any reproduction that spans more than 3–4 dependent actions.

## Grok Tool Usage Patterns

- Artifact creation: `write` (new files) and `search_replace` (precise edits to repro code).
- Inspection: `read_file` (with offset/limit for large logs), `grep`, `list_dir`.
- External claims/data: `web_search` + `open_page`/`web_fetch`; always cite with `render_inline_citation`.
- X-sourced findings: `x_thread_fetch` + appropriate search tools.
- State tracking: `todo_write`, `memory_*` where multi-session continuity is needed.
- Visual outputs: `read_file` on generated images/PDFs (renders content).

If `run_terminal_cmd` (or equivalent execution tool) is available in the active environment, prefer it for actual runs and capture its output. If not available, the skill still fulfills its contract by producing complete, executable repro artifacts and precise instructions.

## PGS & Deterministic Research Guardrails (This Repository)

When the findings to be reproduced concern prime-gap-structure, GWR, DNI, endpoint chains, divisor fields, or any deterministic mathematical/computational claims in this project:

- **PGS-first frame is mandatory** (AGENTS.md): Begin from ordered prime-gap state, divisor-count field, DNI, Leftmost Minimum-Divisor Rule (GWR), selected integer, endpoint, search interval, chamber reset, structural certificate, etc.
- Do not introduce classical sieves, probabilistic primality tests, or cryptographic heuristics as the reproduction method unless the original claim itself used them *and* you first document the PGS-native alternative.
- Reproduction of a "proved" result must verify the proof artifacts or the exact deterministic construction, not merely sample behavior.
- Any deviation must be analyzed against the invariants in `PROOF.md`, `DIVISOR_NORMALIZATION_IDENTITY.md`, `LEFTMOST_MINIMUM_DIVISOR_RULE.md`, and related specs.
- Language: "Reproduced the deterministic behavior" or "The construction produces the claimed state" — never downgrade to "appears to hold empirically."

Violations of this frame are first-class findings in the reproduction report.

## Success Criteria

- A complete, self-contained `experiments/<slug>/` tree exists with durable artifacts.
- The executive summary delivers an unambiguous verdict in the first paragraph.
- Setup, execution, and comparison are documented at a level that allows exact re-execution by a competent third party.
- All external data or claims are cited with `render_inline_citation` components.
- In PGS contexts, the AGENTS.md contract is followed and documented.
- The user can immediately see whether the original finding holds, and why.

## Edge Cases

- Insufficient information: Verdict = "Insufficient information"; list the exact missing pieces (parameter values, code, seeds, full method) required to proceed.
- Environment mismatch: Reproduce what can be reproduced; clearly separate "reproduced under these constraints" from "not reproducible in this environment."
- Stochastic results: Report distribution or multiple runs with seeds; do not claim reproduction from a single lucky draw.
- The "finding" is a negative result or absence claim: The reproduction attempt must be designed to detect presence; document search effort and coverage.

This skill turns "the paper says it works" or "the log shows X" into "I attempted it; here is exactly what happened and the complete audit trail." It is the foundation of trustworthy scientific work in the repository.