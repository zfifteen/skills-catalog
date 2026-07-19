---
name: flaming-horse-audit
description: >
  Audit Flaming Horse generator and orchestration behavior for Manim/Qwen/ffmpeg projects. 
  Use /flaming-horse-audit when diagnosing first-pass failures, repeated self-heal loops, scaffold or placeholder drift, Manim API/timing/color issues, voice-cache policy compliance, ffmpeg assembly issues, or phase/state transition bugs.
when-to-use: "User needs a root-cause audit of a Flaming Horse video generation run: 'audit this flaming horse failure', 'why did the self-heal loop happen', 'check the generator against the contracts for this project', 'flaming horse audit'."
allowed-tools: ["run_terminal_cmd", "read_file", "list_dir", "grep", "open_page", "web_search", "todo_write"]
argument-hint: "<path to flaming-horse project run or project_state.json>"
metadata:
  short-description: "Root-cause auditor for the Flaming Horse generator, harness, and contracts (Manim/Qwen/ffmpeg)"
  source: "Codex 'flaming-horse-audit' skill (ported 2026-05-24)"
---

# Flaming Horse Audit (Grok Port)

## Overview

Use this skill to verify that the Flaming Horse generator and harness are producing valid outputs and following project contracts. Keep this skill in an **auditor role**: detect, explain, and recommend minimal fixes at the generator/orchestrator level.

## User Collaboration Preferences (Hard Overrides — preserved)

- Strict scope control: do only what the user explicitly asks; do not add side tasks.
- Explicit execution boundaries: if the user requests draft-only output in chat, do not execute external actions.
- Cost and speed discipline: minimize token usage and command churn; avoid exploratory work not required for the requested deliverable.
- Precision over momentum: do not rush; follow exact wording and constraints.
- No gold-plating: do not add priorities, framing, or content not requested.
- Accountability: on mistakes, acknowledge directly and perform only the requested correction.
- Ambiguity policy: never resolve ambiguity via inference; always ask the user for clarification before proceeding.

## Operating Boundary

- Treat the generator and orchestrator as the source of truth.
- Audit generated artifacts, logs, and state transitions.
- Recommend fixes to generator prompts, templates, deterministic scripts, and phase logic.
- Never act as a replacement generation pipeline.
- Never create full scene files as an alternative to the generator.

## Mandatory Rules (non-negotiable)

- Generated artifacts are evidence, not fix targets.
- Project-level patching is disallowed by default.
- "Fix the project" means fix generator/orchestrator/templates/agent instructions, not generated artifacts.
- Permit project-level edits only with explicit user override, and only as temporary containment or proof-of-cause.
- Any temporary project edit must include the generator-level follow-up fix and explicit removal trigger.
- Treat generated projects as diagnostics; default remediation target is generator/orchestrator/template logic, not one-off project patching.
- Never create scene files when auditing generator behavior.
- Never rewrite immutable scaffold regions as a workaround.
- Never bypass phase/state contracts to force a pass.
- Prefer root-cause fixes over added guardrails.
- If temporary containment is unavoidable, label it temporary and define a removal trigger.

## Audit Workflow

1. **Identify target run artifacts**
   - Read `project_state.json`, generated scene files, and `build.log` (use `read_file` / `list_dir` on the project directory).
   - Capture where divergence first appears.

2. **Run contract audits**
   - Apply the module checks below.
   - Group findings by root cause, not by symptom.
   - Use `todo_write` to track the audit modules.

3. **Produce root-cause report**
   - For each finding: failure origin, causal chain, primary fix, containment status.
   - Keep remediation minimal and generator-focused.

## Audit Modules

### 1) Generation Contract Audit
- Verify required scaffold signatures and slot markers are present.
- Verify placeholders are fully materialized.
- Verify immutable scaffold regions are unchanged by generation steps.
- Flag missing scaffold files as hard failures.

### 2) Manim Color Contract Audit
- Detect invalid color value types (for example numpy scalar leakage).
- Detect invalid `ManimColor.from_rgb`/`from_rgba` usage.
- Detect mixed unsafe color encodings in palettes and style helpers.

### 3) Timing Contract Audit
- Detect forbidden `run_time` usage with slot timing helpers.
- Detect duplicate timing injection into `Scene.play`.
- Detect zero/negative waits or total run time.
- Verify timing logic aligns to beat-plan ownership.

### 4) Manim Compatibility Audit
- Detect version-incompatible API usage.
- Examples: deprecated tracker attributes, invalid kwargs, method-to-play misuse.
- Prefer targeted compatibility fixes in generator output logic/templates.

### 5) Pipeline/Policy Audit
- Verify local cached Qwen voice prerequisites and wiring.
- Verify no fallback/network TTS patterns are introduced.
- Verify ffmpeg assembly assumptions and warning relevance.
- Verify phase transitions and `project_state.json` updates are valid.

### 6) Self-Heal Loop Audit
- Detect repeated identical failure signatures across retries.
- Flag when self-heal becomes primary path instead of fallback.
- Recommend strategy pivots at source (prompt/template/script logic), not extra retries.

## Output Format

Return findings first, ordered by severity.

For each finding include:
- Scope: file/phase/scene
- Failure origin: first diverging step
- Causal chain: how failure propagated
- Primary fix: source-level change
- Containment status: temporary guardrail (if any) and removal condition

Then include:
- Residual risks
- Suggested verification checks

## Non-Goals

- Do not author complete scene content.
- Do not substitute deterministic scaffold generation with ad-hoc scene creation.
- Do not optimize for passing one run at the expense of architectural contracts.

## Grok-Specific Notes

- All reads use `read_file`, `list_dir`, `grep`.
- When the target run lives in the flaming-horse repo, first read the relevant contract documents (see flaming-horse skill) before auditing.
- `todo_write` is excellent for tracking the six audit modules across a large run.
- When used inside prime-gap-structure, apply the local AGENTS.md PGS-first frame if any mathematical content is under audit.

## Success Criteria

- The report identifies the true first point of divergence.
- Every recommendation is a minimal generator/orchestrator/template change, not a patch to generated artifacts.
- The user can act on the primary fix with high confidence that it addresses the root cause.

This port preserves the auditor mindset and the exhaustive contract checklist while making the workflow fully native to Grok's tool surface.
