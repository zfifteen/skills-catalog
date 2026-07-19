---
name: logic-check
description: >
  Check code, mathematical derivations, proofs, algorithms, or formal
  arguments for logical consistency and detect mathematical or reasoning
  errors. Output format: headline containing the final conclusion,
  followed by a bulleted list of any errors found, followed by a detailed
  explanation. Use when the user says "logic check", "check for logical
  errors", "verify the math", "does this derivation hold?", "audit this
  proof", or provides code, formulas, or reasoning steps that must be
  sound. Critical for research codebases and formal claims where a single
  hidden contradiction can invalidate downstream results.
when-to-use: "Use for rigorous logical and mathematical consistency audits of code, proofs, derivations, algorithms, or arguments. Trigger on 'logic check this', 'verify the math here', 'find contradictions in this reasoning', 'audit this proof for errors'. Headline conclusion + error bullets + detailed explanation."
allowed-tools: ["read_file", "grep", "list_dir", "web_search", "web_fetch", "open_page", "open_page_with_find", "memory_search", "memory_get", "todo_write"]
metadata:
  short-description: "Check code/derivations for logical consistency and mathematical errors (headline conclusion + bullets + explanation)"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/grok-task-v3-logic-check/SKILL.md"
---

# Logic Check

Interpret the current user message, attached code, mathematical text, derivations, proofs, logs, and all conversation context as the complete subject for logical and mathematical audit.

**PGS Project Contract (this repository):** When the material under review involves prime gap structure, divisor-count arithmetic, GWR selectors, DNI normalization, endpoint chains, or any deterministic number-theoretic reasoning in this workspace, the logic check **must** evaluate against the PGS-native invariants and rules (AGENTS.md and PROOF.md). It must not accept "empirical validation" or probabilistic arguments as substitutes for deterministic structural certificates. Classical number theory or cryptographic methods are relevant only when the artifact itself invokes them for comparison.

## Core Instruction (from Codex origin)

Your job is to check code for logical consistency and detect mathematical errors.

Output: Make the headline your final conclusion, followed by a bulleted list of any errors and finish with detailed explanation.

## Workflow

1. **Full Ingestion**
   - Read every line of provided code or derivation (use `read_file` with appropriate offsets/limits or `open_page_with_find` for large/remote material).
   - Map all variables, functions, invariants, and control flow.
   - Identify the claimed theorem, property, or post-condition.

2. **Invariant Extraction**
   - Explicitly state the governing logical or mathematical invariants that the artifact claims to respect (or that the surrounding context requires it to respect).
   - In PGS contexts, derive these from the official objects/invariants in the project (DIVISOR_NORMALIZATION_IDENTITY.md, LEFTMOST_MINIMUM_DIVISOR_RULE.md, PROOF.md, etc.).

3. **Consistency & Error Audit**
   - Walk the artifact step by step, checking each transformation, assignment, proof step, or control branch against the invariants.
   - Categories of errors to hunt:
     - Algebraic or arithmetic mistakes
     - Off-by-one / boundary errors
     - Invariant violations (a quantity that must always hold is allowed to drift)
     - Type or domain mismatches
     - Circular reasoning or hidden assumptions
     - Incorrect handling of edge cases, zero, infinity, or empty structures
     - Mismatched pre-/post-conditions between caller and callee
     - Use of probabilistic methods where deterministic guarantees are asserted

4. **Counter-Example or Witness Search (when applicable)**
   - For claimed universal properties, search for the smallest counter-example using tools or by proposing a minimal test case.
   - For proofs, locate the first inference that does not logically follow.

5. **Synthesize Verdict**
   - The headline must be the single, strongest, most precise conclusion supported by the audit (e.g., "The derivation contains a critical off-by-one error in the boundary selector that invalidates the claimed zero-excess guarantee.").

## Output Format (Strict)

**<Final Conclusion Headline>**

- Bullet 1: concise description of first error with file:line or derivation step reference
- Bullet 2: ...
(Only include bullets if errors exist. If no errors, the headline states soundness and the bullet list may be empty or contain "No logical or mathematical errors detected under the stated invariants.")

**Detailed Explanation**

A structured, line-by-line or step-by-step walkthrough of the most important findings. Quote the erroneous fragment, show the contradiction with the governing invariant, and (when possible) provide the minimal correction or the correct counter-example.

End after the explanation. No moralizing, no "overall this is good/bad."

## Execution Rules

- Read the actual artifact with tools before concluding; never rely on summaries.
- In this workspace, cross-reference AGENTS.md, PROOF.md, and the core .md files (DNI, GWR) on every PGS-related audit.
- Distinguish "error" (contradicts invariant or math) from "style" or "clarity" issues. Only the former go in the error list.
- When the artifact is a proof or formal claim, the logic check is a proof audit: every inference must be valid.
- Use `todo_write` if the audit surface is large and requires tracking multiple sub-invariants.

## Success Criteria

- The headline alone gives the user the correct high-level verdict.
- Every error bullet is tied to a specific location and a specific violated invariant or mathematical rule.
- The detailed explanation allows the author to reproduce the error and see exactly why it is fatal (or why it is not).
- PGS material is never accepted if it violates the deterministic contract.

This skill is the last line of defense against subtle logical or mathematical rot in research code and formal arguments. It is deliberately terse and conclusion-first so that soundness (or its absence) is impossible to miss.
