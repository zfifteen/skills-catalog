---
name: implementation-plan
description: >
  Produce a structured Implementation Plan for a feature, experiment, refactor, or research
  task. Uses a detailed template covering Overview, Objectives, Success Metrics, Mathematical
  Foundations (if applicable), Phases, Tools, Validation Strategy, Risks, Timeline, and
  References. Gathers real context from the repo using tools. Use when the user says
  "implementation plan", "create an implementation plan for...", "/implementation-plan",
  "grok-task-v3-implementation-plan", or asks for a phased plan with validation.
when-to-use: Use when the user requests a formal implementation plan, phased rollout strategy, or the specific "Implementation Plan" workflow on current task/context/files.
argument-hint: "<short description of the proposed work or feature>"
metadata:
  short-description: "Structured implementation plan with phases, metrics, risks, and validation"
  source: "ported-from-codex/grok-task-v3-implementation-plan"
  original_codex: "grok-task-v3-implementation-plan"
---

# Implementation Plan

You are producing a high-quality, evidence-based Implementation Plan.

## Invocation
User runs:
```
/implementation-plan <description of the work>
```
Or attaches files, links, or refers to "the current task".

## Step 0: Gather Real Context (Mandatory)
Before writing any plan section:
1. Use `list_dir` and `read_file` (and `grep` where useful) on the current workspace to understand the project structure, existing code, docs, AGENTS.md, README, tests, and relevant modules.
2. If GitHub-related or external refs are mentioned, use the connected `grok_com_github` MCP tools (first discover exact tool schemas via the MCP protocol if names are not known; common ones include list_issues, search_issues, get_file_contents, list_pull_requests, get_commit, etc.).
3. Run `run_terminal_cmd` for `git status`, `git log --oneline -20`, `git branch` as needed to understand recent activity.
4. If the task references specific papers, gists, or external sites, use `open_page` or `web_search` (or `web_fetch`) to fetch accurate information.
5. Record key findings (file paths, function names, current limitations, data sources) that the plan must address.

Never invent module names, paths, or metrics. Only document what you actually observed or can measure.

## Step 1: Draft the Plan Using the Template
Fill every section of the template below. Keep the headings exactly as shown. Use plain, precise language (combine with `/grade-ten` if requested).

**Implementation Plan Template**

### Project Title
[Concise title for the proposed feature, experiment, or extension]

### Overview
[Brief description of the core idea or problem. Link to broader project goals. State motivation with evidence from the repo scan in Step 0.]

### Key Themes Alignment
- [List 2-5 themes the work advances, e.g. "Empirical Validation First", "Structural invariants", "Reproducibility"]
- Base these only on actual project documents (AGENTS.md, README, existing code comments).

### Objectives
**Primary Objective**
[One clear sentence describing the main deliverable and success condition.]

**Secondary Objectives**
- [Measurable sub-goals, each with a concrete deliverable]

### Success Metrics
- **Quantitative**: e.g. "Throughput improvement of X% on benchmark Y measured via Z script"
- **Qualitative**: e.g. "All new code passes `ruff check` and existing test suite with 0 new failures"
- **Validation**: Specific statistical or acceptance criteria the work must meet

### Mathematical / Theoretical Foundations (if applicable)
[Core equations, models, or invariants the work rests on. Cite exact sources in the repo or external references fetched in Step 0. Mark any novel hypotheses clearly as such and note the empirical support observed so far.]

### Assumptions and Priors
- [Only list assumptions you can verify or have evidence for from the current codebase/state]

### Novel Hypotheses
[Only if supported by data you gathered. State the hypothesis + the exact observation or correlation that supports it.]

### Implementation Phases
Break into sequential, testable phases. Each phase must produce a minimal viable artifact (code, script, doc, benchmark result) that can be reviewed independently.

**Phase 1: [Name]**
- Tasks: ...
- Deliverables: (specific files or outputs)
- Estimated Effort: (days or story points)
- Validation: (how you will know it succeeded before moving on)

(Repeat for Phase 2, 3, ... 4. Keep total realistic.)

### Tools and Technologies
- Languages:
- Libraries / Frameworks:
- Build / Test / Lint commands (exact, from repo):
- Benchmarking approach:
- Documentation standards:

### Validation and Testing Strategy
**Unit / Integration Tests**
- ...

**Benchmark Suite**
- ...

**Static Analysis / Linters**
- ...

**Manual / Acceptance Checks**
- ...

### Risks and Mitigations
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| ...  | ...        | ...    | ...        |

### Timeline
Use a simple table of milestones with dependencies.

| Milestone | Target | Dependencies | Status |
|-----------|--------|--------------|--------|
| ...       | ...    | ...          | [ ]    |

### References and Resources
- Repo files examined: (list absolute paths + key excerpts)
- External sources fetched: (URLs + 1-sentence summary of what was learned)
- Related issues / PRs: (use MCP tools to list real ones)

## Step 2: Review Your Own Draft
Before presenting:
- Cross-check every claim against the evidence you gathered in Step 0.
- Ensure no fabricated paths, function names, or performance numbers.
- If any section cannot be filled with real data, explicitly mark it "To be determined after Phase 1 exploration" and explain why.

## Step 3: Present and Offer Refinements
Output the complete filled template in Markdown.

Offer next steps:
- "Would you like me to expand any phase into a technical task (`/technical-task`) or user story (`/user-story`)?"
- "Shall I create the experiments/ folder and initial stub files for Phase 1?"
- "Run the plan through a second-opinion review?"

## Success Criteria for This Skill
- Every concrete claim (file names, commands, metrics, current behavior) is backed by tool output you actually performed.
- The plan is actionable by a competent engineer who has never seen the repo before.
- Risks are realistic given the actual state of the codebase.
- Timeline accounts for the need to run real builds/tests/benchmarks (not optimistic guesses).

## For This Repo (Prime Gap Structure)
When the plan touches number-theoretic code, the plan **must** respect the AGENTS.md contract: PGS objects → PGS invariants → PGS rule/law → resolved/unresolved/invalidated state. Classical probabilistic methods are secondary and only enter for explicit comparison or legacy prefilter code.

## Related Skills
- `/technical-design-document` for deeper architecture capture
- `/technical-task` to turn a phase into a GitHub-ready issue
- `/user-story` for product-oriented breakdown
- `/grade-ten` to render the final plan in plain English
