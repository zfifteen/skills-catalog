# Antigravity CLI Collab — Integration Test Plan

## Scope

**In scope:** direct `agy` CLI, headless print mode, session resume, helper script, skill contract.

**Out of scope:** MCP `agy_*` tools, interactive TUI, model selection in print mode.

## Prerequisites

- `agy` at `/Users/velocityworks/.local/bin/agy`
- Authenticated keyring session
- Test repo: `/Users/velocityworks/IdeaProjects/prime-gap-structure`

## Phase 1 — Gate (12 cases)

| ID | Test | Expected |
|----|------|----------|
| A-01 | `which agy` | `/Users/velocityworks/.local/bin/agy` |
| A-04 | Direct print smoke | `AGY_SMOKE_OK`, exit 0 |
| A-PY | `py_compile agy_cli.py` | exit 0 |
| H-NORMAL | Helper mode=start | `AGY_HELPER_NORMAL_OK` |
| H-CONV | Helper mode=conversation | `AGY_HELPER_CONV_OK` |
| H-CONTINUE | Helper start+continue | `AGY_HELPER_CONTINUE_OK` |
| C-02 | Empty prompt | exit 1, `empty prompt` |
| G-01 | 1s timeout | `timeout waiting for response` |
| D-07 | Log captures UUID | `Created conversation <uuid>` in log |
| D-08 | Continue logs resume | `resuming conversation` in log |
| D-09 | Pinned T3 recall | T3 stdout = T1 marker |
| D-05 | cwd isolation | different cwd → different thread |

## Phase 2 — Collab Contract (7 cases)

| ID | Test | Expected |
|----|------|----------|
| E-01 | `--add-dir` repo read | reads `PROOF.md` line 1 |
| E-03 | `--new-project` T1 | new conversation |
| E-04 | same project T2 `--continue` | continues thread |
| H-01 | 3-turn sticky collab | T3 recalls T1 |
| I-01 | SKILL forbids MCP | grep MCP exclusion in SKILL.md |
| I-08 | Read-only default | SKILL.md states default |
| K-02 | Skill tree complete | all files on disk |

## Phase 3 — Hardening (manual, post-ship)

C-03–C-06 prompt edge cases, F-02–F-05 permissions, J-01–J-10 hazards.

## Phase 4 — Regression

K-01 after `agy update`.

## Acceptance

Phase 1: 12/12 PASS. Phase 2: 7/7 PASS. H-01 live recall on turn 3.