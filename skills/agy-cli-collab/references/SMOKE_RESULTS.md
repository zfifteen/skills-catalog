# Smoke Results — `/agy-cli-collab`

**Date:** 2026-07-06  
**Evidence dir:** `/var/folders/k_/spz3zlj566sc4qh29g0tk6jh0000gn/T/grok-goal-2d8517bd7dc9/implementer`  
**agy version:** 1.0.16 at `/Users/velocityworks/.local/bin/agy`

## Summary

| Phase | Cases | Pass | Fail |
|-------|-------|------|------|
| Phase 1 (gate) | 12 | 12 | 0 |
| Phase 2 (collab contract) | 7 | 7 | 0 |
| Live H-01 | 1 | 1 | 0 |

**Ship verdict:** PASS

## Phase 1 — Gate

| ID | Status | Notes |
|----|--------|-------|
| A-01 | PASS | `which agy` → `/Users/velocityworks/.local/bin/agy` |
| A-04 | PASS | Direct smoke `AGY_SMOKE_OK` |
| A-PY | PASS | `py_compile` exit 0 |
| H-NORMAL | PASS | Helper start → `AGY_HELPER_NORMAL_OK` |
| H-CONV | PASS | Pinned conversation → `AGY_HELPER_CONV_OK` |
| H-CONTINUE | PASS | Start+continue → `AGY_HELPER_CONTINUE_OK` |
| C-02 | PASS | Empty prompt rejected by helper guard |
| G-01 | PASS | 1s timeout → `timeout waiting for response` |
| D-07 | PASS | `Created conversation <uuid>` in log |
| D-08 | PASS | `resuming conversation` in continue log |
| D-09 | PASS | T3 pinned recall returned T1 marker |
| D-05 | PASS | Different `cwd` resumes different thread |

## Phase 2 — Collab Contract

| ID | Status | Notes |
|----|--------|-------|
| E-01 | PASS | Read `PROOF.md` line 1 → `# Proof` |
| E-03 | PASS | `--new-project` created conversation |
| E-04 | PASS | `--continue` in same project → `E03_T2` |
| H-01 | PASS | 3-turn collab; T3 recalled `H01_MARKER_7742` |
| I-01 | PASS | SKILL.md forbids MCP `agy_*` when active |
| I-08 | PASS | SKILL.md read-only default documented |
| K-02 | PASS | Skill tree complete on disk |

## cwd vs --add-dir finding

Session resume is keyed by shell **`cwd`**, not `--add-dir`. Evidence: D-05 — start from `/tmp/...` workspace with `--add-dir` pointing at repo, then `--continue` from repo `cwd` returned `CWD_REPO_PROBE` (new repo thread), not the `/tmp` thread.

## Live H-01 transcript (abbreviated)

- **T1:** `The H01 research focus is chamber reset at marker H01_MARKER_7742.`
- **T2:** Strongest objection to chamber reset as inference gate (substantive one-sentence reply).
- **T3:** `H01_MARKER_7742` (exact marker recall)

Captured in `{SCRATCH}/agy-h01.log`.

## Helper smoke evidence

See `{SCRATCH}/agy-helper-smokes.log`, `{SCRATCH}/agy-pinned-recall.log`, `{SCRATCH}/run_smoke_tests-r2.log`.

## MCP usage during build

Zero MCP `agy_*` invocations — CLI-only path per skill contract.