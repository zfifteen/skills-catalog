---
name: prompts-check-for-signal
description: >
  Apply the "Check for Signal" prompt-library workflow: given a hypothesis or claim, design
  and execute (or scaffold the execution of) a decisive test that definitively proves or
  falsifies the claim — never artificially. Create a new isolated folder under experiments/
  (or equivalent), document everything in FINDINGS.md that **leads with the conclusion**,
  followed by technical supporting evidence. Do not modify artifacts outside the new folder.
  Use when the user says "check for signal on this claim", "design a decisive test for",
  "falsify this hypothesis", "prove or disprove", "use check-for-signal", or runs
  /prompts-check-for-signal.
when-to-use: "Designing or running a clean, high-leverage experiment or test whose outcome will materially update belief about a specific claim. Strong triggers: 'decisive test', 'falsify', 'prove or disprove', 'check for real signal', 'experiments/ folder'."
argument-hint: "<hypothesis, claim, or research question to design a decisive test for>"
allowed-tools: ["read_file", "grep", "list_dir", "write", "search_replace", "run_terminal_cmd", "web_search"]
metadata:
  short-description: "Design and document a decisive falsifying/proving test for a claim (experiments/ isolation)"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/prompts-check-for-signal/SKILL.md"
  version: "1.0.0"
---

# Check for Signal — Grok Port

Design and document (and where possible execute) a clean, high-power test that can actually move the needle on a hypothesis instead of producing ambiguous or noisy results.

## Purpose

The original prompt insists on **decisive** tests that "definitively prove or falsify (never artificially)" and requires strict workspace isolation plus conclusion-first documentation. This port makes the skill an active experiment designer and documenter inside the Grok tool environment.

## Invocation

```
/prompts-check-for-signal <hypothesis or claim description>
```

Any additional context in the conversation (prior results, existing code, data files) is part of the input material.

## Core Contract (Preserved)

Goal: Design and execute a test that will definitively prove or falsify (never artificially) the following hypothesis/claim.

- Create a **new folder under `experiments/`** (or project-appropriate equivalent) for **all** artifacts and documentation.
- **Do not modify any artifacts outside** of the new folder.
- Meticulously document findings in `FINDINGS.md` that **leads with the conclusion**, followed by technical supporting evidence.

## Grok Workflow

1. **Clarify the Claim**
   - Restate the exact hypothesis in the clearest, most falsifiable form possible.
   - Surface hidden assumptions, scope, and what "definitively" would look like for this claim.

2. **Design the Decisive Test**
   - Choose the smallest, highest-power experiment or analysis that can produce a clear positive or negative result.
   - Prefer deterministic or low-variance designs over statistical ones when both are viable (aligns with project AGENTS.md preference for deterministic reasoning).
   - Define the success/failure criteria in advance (what numbers, what structural property, what invariant violation, etc. would count as proof or falsification).
   - Identify required inputs, controls, and how to make the result auditable.

3. **Scaffold the Experiment Workspace**
   - Target: `experiments/<kebab-case-claim-slug>/` or `experiments/signal-<slug>/`
   - Create inside it (using `write`/`search_replace`):
     - `README.md` (hypothesis, test design, how to run)
     - `FINDINGS.md` (template or initial entry — see format below)
     - Any scripts, config, or small programs needed for the test (keep minimal)
     - `Makefile` or run instructions if compilation/execution is involved

4. **Execute or Guide Execution (when possible)**
   - Use available tools (`run_terminal_cmd`, code via write+exec patterns, web tools for data, etc.) to carry out the test.
   - If full execution is not possible in the current turn, produce a complete, runnable recipe that a follow-up agent or human can execute with zero ambiguity.

5. **Document Conclusion-First**
   - The `FINDINGS.md` **must** open with a clear prose sentence or short paragraph stating the conclusion.
   - Then provide the technical evidence, methodology, raw outputs, statistical or structural results, and any caveats.
   - Example opening:
     > "The test falsifies the claim that chamber resets are uniformly distributed: in the 10,000-sample run, reset events clustered 3.2× more frequently immediately after leftmost-minimum transitions than expected under uniformity (p < 0.001 via exact permutation test)."

6. **Verification & Audit Trail**
   - Record exact commands, seeds (if any), tool calls, file hashes, and timestamps where relevant.
   - Make it possible for a third party to reproduce the exact conclusion from the artifacts.

## FINDINGS.md Required Shape

```markdown
# FINDINGS — <short claim label>

**Conclusion**: [One or two sentences that a reader can quote as the result. Lead with this.]

**Hypothesis under test**: [restatement]

**Test design**: [1-3 paragraphs describing the decisive procedure and why it has power]

**Execution details**:
- Date/time
- Exact commands / scripts run
- Inputs / datasets / parameters
- Environment (if relevant)

**Results**:
[Tables, key numbers, structural observations, logs, images descriptions, etc.]

**Interpretation**:
[How the data supports or refutes the claim. Be quantitative where possible.]

**Limitations & caveats**:
[Honest statement of what the test does not cover]

**Next actions** (optional):
- ...
```

## Success Criteria

- A new isolated `experiments/...` folder exists containing the complete record.
- `FINDINGS.md` literally leads with the conclusion in plain prose.
- The test design is genuinely capable of producing a decisive (non-ambiguous) result.
- No files were touched outside the experiments folder.
- A later reader can understand exactly what was tested and what the outcome means without re-running the entire conversation.

## Guardrails

- "Never artificially" means do not design a test whose outcome is foreordained by construction or by cherry-picked data. If the only honest answer is "this claim is currently untestable with available resources," say so clearly instead of forcing a weak test.
- Prefer tests that can be executed deterministically or with full auditability.
- In PGS contexts: tests should target PGS objects, invariants, or rule applications directly when the hypothesis touches them.
- Workspace isolation is absolute — this skill does not "helpfully" edit files elsewhere in the project.

This port converts the original "Check for Signal" prompt into a disciplined experiment harness creator and conclusion-first reporter that works with Grok's full toolset.
