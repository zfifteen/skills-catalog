---
name: technical-design-document
description: >
  Create a new folder under experiments/ (or equivalent) containing a meticulous Technical
  Design Document that captures the full implementation plan, architecture, decisions,
  risks, and validation approach for the current task. Use when the user says "technical
  design document", "write a TDD", "create design doc for...", "/technical-design-document",
  "grok-task-v3-technical-design-document", or asks to capture the plan in a permanent
  experiments/ artifact.
when-to-use: Use when the user wants a formal technical design document (TDD) or design doc created on disk in an experiments/ folder for the current feature, fix, or research task.
argument-hint: "<description of what to design>"
metadata:
  short-description: "Create experiments/<id>/ design doc capturing the full plan"
  source: "ported-from-codex/grok-task-v3-technical-design-document"
  original_codex: "grok-task-v3-technical-design-document"
---

# Technical Design Document

Create a permanent, reviewable Technical Design Document on disk.

## Step 1: Setup
1. Generate a short unique ID for this design (8 hex chars). Use `run_terminal_cmd`:
   ```bash
   python3 -c "import uuid; print(uuid.uuid4().hex[:8])"
   ```
   Store as `DESIGN_ID`.

2. Create the experiments directory if it does not exist:
   ```bash
   mkdir -p experiments/${DESIGN_ID}
   ```

3. Define the main artifact path:
   - `design_doc_path`: `experiments/${DESIGN_ID}/design.md`
   - Also create `experiments/${DESIGN_ID}/summary.md` for a one-page executive summary.

## Step 2: Gather Full Context
Use all available tools to deeply understand what is being designed:
- Read relevant source files, tests, AGENTS.md, README, existing docs.
- Use `grep` for related patterns, TODOs, prior attempts.
- Use MCP GitHub tools for any linked issues/PRs.
- Use `web_fetch` / `open_page` for external references mentioned.
- If the task builds on prior work, read those files too.

Record a "Context Sources" section with exact paths and 1-2 sentence relevance for each.

## Step 3: Write the Design Document
Write a comprehensive design document to `design_doc_path` (use the `write` tool or `search_replace` with empty old_string for new file).

The document **must** contain at minimum:

- Title and date + DESIGN_ID
- Problem Statement (what is broken or missing, with evidence)
- Goals and Non-Goals (what is in scope vs explicitly out)
- Background / Prior Art (what already exists in the repo + external)
- Proposed Design (architecture, data structures, algorithms, interfaces, file layout)
- Detailed Implementation Phases (link to or embed an Implementation Plan)
- Key Decisions and Trade-offs (with rationale and rejected alternatives)
- Risks, Mitigations, and Unknowns
- Validation & Testing Strategy (unit, integration, benchmarks, statistical tests, charter compliance if in this repo)
- PR / Rollout Plan (ordered, independently reviewable PRs with dependencies)
- Open Questions (explicit list of things that still need user or team input)
- References (all files read, all external sources with URLs and access dates)

For this repo (Prime Gap Structure): the design **must** begin from PGS objects, invariants, and rules per AGENTS.md. Explicitly call out how the design preserves or extends deterministic PGS laws.

## Step 4: Write the Summary
Write a concise 1-2 page `summary.md` that a reviewer can read in <5 minutes. It must include:
- One-paragraph problem + solution
- Top 3 risks
- The PR plan (titles + order)
- Any blocking open questions

## Step 5: Verify and Present
1. Read back the files you just wrote.
2. Confirm the directory structure:
   ```
   experiments/<DESIGN_ID>/
     design.md
     summary.md
   ```
3. Tell the user the exact paths.
4. Offer: "Would you like me to start the first phase implementation, turn the PR plan into GitHub issues via `/technical-task`, or run a design review loop (writer + reviewer subagents)?"

## Success Criteria
- The design doc is written to disk (not just in chat).
- Every major claim about current state is backed by actual file reads performed during this run.
- The PR plan is realistic and incremental (each PR deliverable and reviewable on its own).
- Open Questions section is non-empty if any real decisions remain for the user.
- For PGS work: explicit mapping from design elements back to PGS invariants and the Leftmost Minimum-Divisor Rule / DNI etc.

## Related Skills
- `/implementation-plan` for the phased template (can be embedded or linked)
- `/grade-ten` if the user wants the design rendered accessibly
- `/second-opinion` for an external technical review of the finished design
