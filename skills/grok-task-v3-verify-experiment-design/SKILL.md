---
name: verify-experiment-design
description: >
  Perform a deep, systematic audit of an experiment's design (code, protocol, parameters,
  controls, analysis plan, data sources, and claimed conclusions) to determine whether the
  design is capable of supporting the intended scientific or engineering conclusion with
  validity. Identify threats to internal validity, external validity, construct validity,
  and statistical conclusion validity. Assess power, reproducibility enablers, pre-specification,
  and alignment between design and claim. Use when the user provides or describes an
  experiment and wants assurance that the conclusions will be (or are) warranted by the
  method. Trigger on "verify this experiment design", "audit the validity of this setup",
  "does this design actually test what it claims?", "design review for [paper/experiment]",
  or before launching expensive/long-running probes.
when-to-use: "For pre-launch or post-hoc review of any experimental, computational, or empirical setup where the validity of the eventual conclusions matters. Especially valuable for high-stakes research, grant proposals, or before interpreting results from complex pipelines. Activates on design audit requests, 'is this experiment well-designed?', 'check for confounds/leakage/power issues', or when a paper/method claims a conclusion and the design details are available for scrutiny."
allowed-tools: ["read_file", "grep", "list_dir", "write", "search_replace", "open_page", "open_page_with_find", "web_search", "web_fetch", "x_keyword_search", "x_semantic_search", "memory_search", "memory_get", "todo_write"]
argument-hint: "<experiment description, code path, paper section, protocol, or design doc> [focus: validity|power|reproducibility|all]"
metadata:
  short-description: "Rigorous audit of experiment design for validity threats, power, controls, and conclusion alignment"
  version: "1.0.0"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/grok-task-v3-verify-experiment-design/SKILL.md"
---

# Verify Experiment Design — Grok Edition

You are executing the "Verify Experiment Design" workflow. Treat all provided material (code, papers, protocols, logs, parameter tables, previous results, images, links) plus workspace context as the subject of a formal design audit. Your goal is to determine, with evidence, whether the experiment's design can credibly support the conclusion(s) the researchers intend to draw.

This is the Grok-native port of the original Codex v3 task. It has been expanded into a comprehensive validity audit framework with tool-augmented inspection, literature grounding, structured checklists, and mandatory PGS-first discipline for work in this repository.

## Core Principles

- **Design, not results.** You are auditing the *plan and implementation of the plan*, not (primarily) the numeric outcomes. Good design can produce null or surprising results; poor design cannot support strong claims even with "good" numbers.
- **Threats to validity are first-class.** Name them specifically (internal, external, construct, statistical conclusion) with concrete examples from the artifact.
- **Alignment of design to claim.** The strongest finding is often "the design tests a related but different question than the one claimed."
- **Reproducibility is a validity dimension.** A design that cannot be replicated by others has limited scientific value regardless of internal logic.
- **No design is perfect.** The output is a balanced assessment of strengths, weaknesses, and residual risks, not a binary pass/fail.

## Step-by-Step Audit Workflow

### 1. Reconstruct the Intended Inference
- From the provided material, state in one or two sentences: "The experiment is intended to support the conclusion that [precise claim]."
- Identify the estimand, the target population/parameter space, and the decision rule or threshold for "support."
- Note any pre-registered or pre-specified hypotheses vs. post-hoc reframing.
- Success criterion: The intended conclusion is captured accurately and can be quoted or tightly paraphrased from the source.

### 2. Map the Actual Design
- Using tools (`read_file`, `grep`, `list_dir`, `open_page`, etc.), extract the complete implemented design:
  - Sampling / search strategy / data generation procedure
  - Treatment / intervention / parameter settings
  - Controls, baselines, and counterfactuals
  - Measurement / outcome variables and their operationalization
  - Analysis plan, statistical tests, correction procedures
  - Exclusion / inclusion / stopping rules
  - Randomization, blinding, or determinism guarantees
  - Environment, seeds, versions, hardware
- Produce a concise "Design Summary" artifact (in reasoning or written to the workspace).
- Success criterion: You can describe what was actually done at a level sufficient for another researcher to attempt replication from your summary alone.

### 3. Validity Threat Analysis (Systematic Checklist)
For each major validity type, explicitly answer:

**Internal Validity**
- Confounding / selection bias / history threats?
- Leakage (train/test, data snooping, peeking at outcomes before design freeze)?
- Implementation fidelity (did the code do what the protocol said?)?
- Attrition / missing data handling?

**Construct Validity**
- Do the measured variables / outputs actually capture the theoretical constructs named in the claim?
- Operationalization drift (e.g., "endpoint" measured in a way that includes or excludes cases the theory cares about)?

**External Validity / Generalizability**
- Scope of the search space, parameter ranges, or sampled population vs. the claimed population?
- Boundary conditions acknowledged or ignored?

**Statistical Conclusion Validity**
- Power / precision for the claimed effects or distinctions?
- Multiple testing / p-hacking / HARKing exposure?
- Appropriate error control and model assumptions?
- Effect size / uncertainty reporting?

**Reproducibility & Transparency**
- Code, data, seeds, exact protocol available and complete?
- Environment pinned?
- Analysis code matches the described procedure (no silent changes)?

Use `todo_write` to track checklist progress for complex designs.

For each threat identified, cite the specific file:line, parameter, or protocol passage that creates the risk.

Success criterion: A structured table or bulleted findings section, each tied to concrete evidence in the artifact.

### 4. Power, Sensitivity & Robustness Review
- Where quantitative: assess (via reasoning + tools or external lookup) whether the design has adequate power or resolution to detect the effects of interest at the claimed scale.
- Sensitivity: how fragile are conclusions to small changes in parameters, seeds, exclusion rules, or analysis choices?
- For computational experiments (especially number-theoretic): verify that boundary selectors, interval definitions, and state representations are exact and free of off-by-one or floating-point artifacts that could invert conclusions.
- Success criterion: Explicit statement of power/sensitivity findings with supporting numbers or qualitative analysis.

### 5. Alignment & Conclusion Warrant Assessment
- Does the design, as implemented, provide a valid test of the *intended* conclusion, or only of a weaker/adjacent claim?
- What is the strongest conclusion the design can actually support?
- What additional design elements (controls, larger N, pre-registration, different operationalization) would be required to support the headline claim?
- Verdict categories: "Design supports the intended conclusion with minor caveats", "Design supports a narrower conclusion than claimed", "Design has critical validity threats that undermine the intended inference", "Design cannot support any strong conclusion on the stated question."

### 6. Recommendations (Actionable, Prioritized)
- High-priority fixes that would materially improve validity.
- Nice-to-have enhancements.
- "Do not change" items (elements that are already strong or required by the research question).
- If in this repository, specific recommendations that respect the PGS object/invariant frame.

## Output Structure (Use This Order)

1. **Experiment Identification** (title, authors/source, date of design, link or path)
2. **Intended Conclusion** (verbatim or tight quote)
3. **Design Summary** (concise 1–2 paragraph reconstruction)
4. **Validity Findings** (by category, with evidence citations: file:line or section)
5. **Power, Sensitivity & Robustness**
6. **Alignment Verdict** (one of the four categories above + 1-sentence rationale)
7. **Recommendations** (prioritized list)
8. **Reproducibility Assessment** (code/data/seed availability and completeness)
9. **Residual Risks** (what remains even after fixes)

Lead with the verdict in plain prose before the structured sections.

## Grok Tool Patterns for This Audit

- Deep code/protocol reading: `read_file` + `grep` (precise patterns for leakage, hard-coded boundaries, etc.).
- External grounding: `web_search` + `open_page` for field-specific best practices, prior critiques of similar designs, or power analysis methods.
- Visual designs (flowcharts, diagrams in papers): `read_file` on images or `open_page_with_find`.
- X discussion of the experiment: `x_semantic_search` for community validity concerns (use as leads, not evidence).
- Artifacting the audit itself: `write` a `design-audit-<slug>.md` in `experiments/` or `docs/audits/`.

## PGS & Deterministic Research Guardrails (This Repository)

When the experiment under review involves prime gaps, divisor normalization, GWR selectors, endpoint classification, search intervals, or any deterministic construction in this project:

- The audit **must begin** from the PGS-native frame (AGENTS.md): ordered prime-gap state, divisor-count field, DNI, Leftmost Minimum-Divisor Rule, selected integer, endpoint, chamber reset, structural certificate, modulus-link closure, etc.
- Check that the experimental design operationalizes these objects and invariants correctly and does not substitute classical or probabilistic proxies.
- Verify that boundary/endpoint handling, excess-DNI accounting, and state-transition rules are implemented exactly as specified in the governing documents (`PROOF.md`, `DIVISOR_NORMALIZATION_IDENTITY.md`, `LEFTMOST_MINIMUM_DIVISOR_RULE.md`, specs).
- Flag any design element that would allow "empirical validation" language around proved results or that mixes classical factoring heuristics into the core logic.
- The design must be capable of producing a structural certificate or explicit invalidation under the PGS rules; otherwise the experiment cannot support deterministic claims.

Any design that violates the PGS contract receives an automatic "critical validity threat" classification.

## Success Criteria

- The audit produces a clear, evidence-based verdict on whether the design warrants the intended conclusion.
- Every validity concern is tied to a specific, locatable element of the provided artifact.
- Recommendations are actionable and prioritized by impact on validity.
- PGS contexts show explicit application of the native object/invariant frame.
- The user can decide with confidence whether to trust, modify, or discard the experimental results on the basis of this review.
- The audit itself is reproducible from the documentation produced.

## Edge Cases

- Purely theoretical or proof-based "experiments": focus on the logical structure and artifact alignment rather than statistical power.
- Under-specified designs (common in early-stage work): verdict "cannot yet support strong conclusions"; list minimal information required to complete the audit.
- Post-hoc design changes: treat them as threats to validity (HARKing, p-hacking via analysis flexibility) unless pre-registered with clear rationale.
- Resource-constrained designs: acknowledge trade-offs but still name the validity cost of the constraint.

This skill is the gatekeeper that prevents "the experiment looked reasonable" from becoming "the conclusion is supported." Use it early, before heavy investment, and whenever a result is surprising or convenient.