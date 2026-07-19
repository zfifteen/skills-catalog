---
name: experiment-design
description: >
  Produce a technical design specification (markdown document) for a focused
  experiment whose goal is to attempt to falsify a given hypothesis. The
  document is placed in a new folder under 'experiments/' (named to include
  any relevant PR or identifier) in preparation for later technical
  implementation. Use when the user says "design experiment", "write the
  experiment spec for", "technical design for falsifying this", or provides
  a hypothesis that needs a rigorous, reproducible experimental plan before
  code is written. Critical for high-integrity research programs where
  experiments must be pre-specified, minimal, and directly probative.
when-to-use: "Invoked when a hypothesis requires a written technical design spec before implementation or execution. Trigger phrases: 'design the experiment', 'experiment spec', 'pre-specify the falsification test', 'write the plan for this probe'. Especially valuable before committing code or large compute in deterministic research."
allowed-tools: ["read_file", "grep", "list_dir", "web_search", "web_fetch", "open_page", "open_page_with_find", "memory_search", "memory_get", "search_replace", "write", "todo_write"]
metadata:
  short-description: "Write technical design spec (markdown) for hypothesis-falsifying experiment under experiments/"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/grok-task-v3-experiment-design/SKILL.md"
---

# Experiment Design

Interpret the current user message, attachments, files, links, images, and conversation context as the complete input for this workflow. Produce a complete technical design specification document for an experiment designed to attempt to falsify the referenced hypothesis. Place the document (and any supporting artifacts) inside a new folder under `experiments/` whose name incorporates the PR number or other stable identifier when available.

**PGS Project Contract (this repository):** When the hypothesis or domain is prime gap structure, divisor normalization, GWR rules, endpoint chains, or any deterministic number-theoretic work in this workspace, the design **must** be framed in PGS-native terms (objects → invariants → rules/laws → state). The experiment must target a deterministic structural prediction or counter-example. Probabilistic language, classical sieves as primary method, or cryptographic assumptions are disallowed except for explicit side-by-side comparison requested by the user. See AGENTS.md.

## Core Instruction (from Codex origin)

Create a technical design specification markdown document for an experiment designed to attempt to falsify the hypothesis. Create a new folder that includes the PR number in the name under 'experiments/' for this document in preparation for future technical implementation.

## Workflow

1. **Ingest the Hypothesis & Context**
   - Fully read the hypothesis statement and all surrounding material (use tools for remote or large artifacts).
   - Identify the precise claim under test and the minimal change or observation that would falsify it.
   - Catalog existing code, data, or methods that the experiment will interact with or extend.
   - Note any prior related experiments (search `experiments/`, research/ output trees).

2. **Define the Experimental Objective**
   - One-sentence statement of what the experiment will decide.
   - Explicit falsification condition (the observable that would force rejection or major revision of the hypothesis).
   - Scope boundaries: what is deliberately excluded from this experiment (keeps it minimal).

3. **Specify the Method (Minimal & Reproducible)**
   - Exact algorithm, parameter settings, data sources, and controls.
   - Full reproducibility section: seeds, precision, versions, timeouts, hardware/OS notes, random number generator state, exact commands.
   - Success / failure criteria expressed as concrete, checkable predicates (log patterns, numeric thresholds with tolerances, structural invariants in output files, theorem certificates, etc.).
   - Data provenance: only standard named benchmarks or fully documented real-world datasets.

4. **Risk & Failure Mode Analysis (Dry Run)**
   - Most likely ways the experiment can fail to deliver a clear answer.
   - Mitigations that stay within the minimal scope.
   - Resource estimate (runtime, memory, storage) at realistic scale.

5. **Implementation Plan**
   - High-level steps to realize the design (files to create/edit, new scripts, data prep).
   - Order of implementation that allows early falsification signal.
   - How results will be captured and where they will live (inside the experiment folder).

6. **Write the Design Document**
   - Create the directory `experiments/<pr-or-slug-or-date>/` (include PR number when the context references one).
   - Write the full specification as a well-structured markdown file (e.g., `experiment-design.md` or `README.md`).
   - Include all sections below.

## Required Sections in the Design Document

**Title**
- Clear, specific: "Experiment Design: Falsifying <short hypothesis label> via <minimal method>"

**Hypothesis**
- Verbatim + source locator.

**Objective**
- One sentence: what decision this experiment will enable.

**Method**
- Detailed but minimal description.
- Pseudocode or exact command skeleton where helpful.
- All parameters and their justification (only those required for the falsification test).

**Reproducibility**
- Complete pin list (seed, precision, versions, dates, commands).

**Data & Environment**
- Exact datasets (named, versioned) or generation procedures.
- Environment requirements.

**Success / Falsification Criteria**
- Precise, checkable conditions for each possible outcome (falsified, supported at this scale, inconclusive but informative, etc.).

**Expected Output Artifacts**
- What files will be produced and their key content signatures.

**Failure Modes & Mitigations**
- Table or bullets.

**Implementation Roadmap**
- Numbered steps with file paths.

**Rollback / Reversion**
- How to undo every change the implementation will make.

**References**
- Links or file:line pointers to all source material used.

## Execution Rules

- The design must be the smallest one that can still deliver a decisive falsification signal.
- No "nice to have" measurements or future-proofing.
- Every claim in the design must be traceable to the hypothesis or to explicit prior results in the workspace.
- Use `write` + `search_replace` to create the directory tree and document.
- After writing, immediately `read_file` the document and verify completeness and accuracy.
- If the context mentions a PR, embed the PR number in the folder name.

## Success Criteria

- An engineer unfamiliar with the hypothesis can read the design document and implement the experiment without further clarification.
- The falsification criterion is unambiguous and directly probative.
- The document lives in the correct `experiments/<...>/` location and is ready for implementation handoff to sibling skills (create-experiment, advance-my-research).
- PGS-related designs are framed in the native PGS object/invariant language.

This skill enforces pre-specification discipline: no experiment is run in this research program without a living, version-controlled technical design that makes the falsification logic explicit before any code is written.
