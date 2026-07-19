---
name: method-simplification
description: >
  Audit a plan, experiment design, algorithm, probe, analysis script, test
  code, workflow, or research artifact for unnecessary complexity. Use when
  the user asks to "simplify the method", "reduce complexity", "remove
  unnecessary parts", "tighten this experiment", "find the minimal
  deterministic path", or wants an audit that preserves the exact research or
  implementation contract while eliminating avoidable moving parts.
when-to-use: "Before accepting a method as good enough; when reviewing or designing experiments, algorithms, workflows, or code for methodological compression (not generic cleanup). Trigger phrases include 'simplify', 'minimal version', 'too much branching', 'overbuilt'."
allowed-tools: ["read_file", "grep", "list_dir", "search_replace", "write", "grep", "task"]
argument-hint: "<description or path to the method/plan/artifact to audit> [optional: the exact contract it must preserve]"
metadata:
  short-description: "Methodological compression audit: remove avoidable complexity while strictly preserving the research/implementation contract"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/method-simplification/SKILL.md"
---

# Method Simplification

## Purpose

Before accepting any method (plan, algorithm, probe, experiment, test, analysis script, or workflow) as "good enough," audit it for avoidable complexity. The goal is **methodological compression** while preserving the exact contract the method is supposed to satisfy.

A valid simplification must keep the same:
- Hypothesis or question being answered
- Observable or invariant being measured
- Input regime and acceptance/failure conditions
- Validity boundaries

Simplification by weakening the claim, dropping a necessary control, hiding uncertainty, or replacing a precise contract with a vague one is forbidden.

## Core Contract

Prefer the smallest deterministic method that answers the exact question with:
- Fewer moving parts
- Less branching and state
- Fewer repeated computations (compute once, reuse)
- Clearer auditability and reproducibility
- Explicit failure modes instead of silent fallback or resilient degradation

## Audit Workflow

1. **Identify the target**
   - The artifact under review (plan text, algorithm description, pseudocode, source files, experiment protocol, script, etc.).
   - Use `read_file`, `grep`, `list_dir` to load it precisely.

2. **State the contract (one or two sentences)**
   - What exact question or invariant must the method answer or protect?
   - What are the input regime, success condition, and failure condition?
   - If the user provided a contract statement, use it verbatim; otherwise derive the tightest faithful version from the artifact and context and confirm.

3. **Separate necessary vs. avoidable complexity**
   - Trace every branch, helper, repeated computation, abstraction, fallback, config surface, or extra measurement back to the contract.
   - Keep only if removing it would change the answer, the measured object, or the validity boundary.

4. **Propose the minimal replacement**
   - Give the smaller method as concrete steps, pseudocode, edit plan (using search_replace targets), or a narrow script.
   - The replacement must be narrow enough that another agent can implement it without inventing new modes or abstractions.

5. **Name what must not change**
   - Explicitly list any complexity that protects the contract and must remain.

6. **State residual risk**
   - Any limits, assumptions, or checks still required after simplification.
   - If none material, state: "No material residual risk identified under the stated contract."

## What to Look For (Common Targets)

- Unnecessary branching, mode flags, or "if this then that" logic
- Repeated computations that can be hoisted or memoized once
- Helpers, base classes, or frameworks that do not reduce current complexity for this specific contract
- Broad workflows where a straight-line script or single-pass analysis would suffice
- Hidden fallback logic, retries, alternate paths, or silent degradation
- Non-determinism where a deterministic construction is possible
- Measurements, probes, or tests that do not affect the conclusion or decision
- Output artifacts that make the result harder (rather than easier) to audit or reproduce

## Output Shape (Use This Structure)

1. **Contract Preserved**
   - One or two sentences stating the exact question/invariant the simplified method must protect.

2. **Complexity Findings**
   - Bulleted list of only the avoidable complexity that impacts auditability, runtime, reproducibility, or semantic clarity.
   - For each: "This X is unnecessary because <trace to contract>; removing it does not change Y."

3. **Simplified Method**
   - Concrete replacement: numbered steps, pseudocode block, or precise edit plan with file:line anchors.
   - Narrow enough for direct implementation.

4. **What Not To Change**
   - Explicit list of retained complexity and why it is required by the contract.

5. **Residual Risk**
   - "No material residual risk identified under the stated contract." (or the precise remaining items).

## Stop Conditions

- **No simplification recommended**: Every apparent complexity is required by the contract or its removal would alter the measured object, validity boundary, acceptance condition, or failure condition. State this clearly.

- **Shape feels wrong**: The current method is answering a different question than the user asked. Surface the contract mismatch first, before any simplification proposal.

## Guardrails

- This is **not** a generic code-style or lint review. Focus exclusively on methodological / contract fidelity.
- Do not optimize for future extensibility unless extensibility is part of the user's stated contract.
- Never introduce new frameworks, config surfaces, fallback paths, extra modes, or helper subsystems as part of the "simplification."
- Shorter is not automatically better if it obscures the method or weakens reviewability.
- Controls, checks, and explicit failure cases that protect the conclusion must stay.
- Never present a simplification as valid unless you have verified the original contract is fully preserved.
- In PGS or deterministic research contexts, treat the PGS rule/law and invariant set as part of the contract that must not be weakened.

## Success Criteria

- The auditor can point to a specific, smaller method that still satisfies the identical contract.
- Any retained complexity is explicitly justified by the contract.
- The output is immediately actionable by an implementer or experimenter.
- If no simplification is possible, the user receives a crisp explanation rather than a vague "it looks okay."

Use this skill early in experiment or algorithm design and before large implementation efforts.
