# Implementation Plan: Lumos Workspace Cache

This document outlines the detailed execution plan for implementing **Lumos: The Persistent Cognitive Bridge and Workspace Cache for Ephemeral AI Agents**.

---

### Project Title
Lumos: Persistent Cognitive Bridge & Workspace Cache

### Overview
Lumos is a client-side python automation and shell-integrated daemon designed to capture, serialize, and deserialize workspace states and compounding developer learnings between transient agent sessions. By maintaining a local `.lumos/workspace_state.json` ledger, the tool eliminates cold-start exploration cycles and minimizes agentic token consumption.

---

### Key Themes Alignment
- **Cognitive Continuity**: Shifting agent interactions from isolated, stateless turns into compounding, continuous project lifetimes.
- **Token Economy**: Maximizing the context window available for complex reasoning by minimizing exploratory overhead.
- **Empirical Reproducibility**: Storing structural build rules and compiler quirks to prevent duplicate testing/build failures.

---

### Objectives

**Primary Objective**
- Create a lightweight, zero-dependency Python CLI tool (`lumos`) and JSON schema that automatically generates, updates, and parses `.lumos/workspace_state.json` state caches in under 500ms, injecting them into the agent's context payload.

**Secondary Objectives**
- Implement auto-discovery routines for git status, modified file diffs, active branches, and recent shell command history.
- Design an heuristic path mapper to link source directories with appropriate build tools and test runners (e.g. mapping `src/c/` to `make`).
- Create seamless git hooks (`pre-commit`, `post-merge`) to trigger state serialization transparently.

---

### Success Metrics

- **Quantitative**:
  - Reduce initial workspace exploration token usage from an average of ~5,000 tokens to `< 1,000` tokens per session.
  - Decrease average agent exploration steps (listing directories, finding configs) from 3–5 commands to 1 command.
- **Qualitative**:
  - Ensure 100% of serialized state payloads validate against the schema.
  - Prevent cache staleness by dynamically validating git commits and file modifications.
- **Validation**:
  - All unit/integration tests must pass with 0 warnings.
  - Cache payload must stay below a hard limit of `4KB` (approx. 1,000 tokens).

---

### Mathematical / Theoretical Foundations

Let:
- $C_{total}$ be the agent's total context window size (tokens).
- $C_{discovery}$ be the tokens consumed by exploratory tool calls (e.g., recursive `list_dir`, broad `grep_search`, config files reads) during standard startup.
- $C_{lumos}$ be the tokens consumed by the Lumos state payload.
- $C_{reason}$ be the remaining tokens available for task reasoning and code generation.

The context relationship is modeled as:
$$C_{reason} = C_{total} - (C_{discovery} + C_{payload})$$

Lumos guarantees:
$$C_{lumos} \ll C_{discovery}$$
Maximizing the available reasoning capacity:
$$\lim_{C_{discovery} \to 0} C_{reason} = C_{total} - C_{payload}$$

Additionally, we define the **Idempotency of Ingestion**:
Let $S_t$ be the workspace file state at time $t$. Reading and parsing $L(S_t)$ must be side-effect free:
$$Ingest(L(S_t)) \implies S_t = S_{t+1}$$

---

### Assumptions and Priors
- **Python Runtime**: The host machine has Python 3.8+ available in the shell path.
- **Git Version Control**: All target workspaces are valid git repositories containing a `.git` folder.
- **Write Permissions**: The agent has permission to read and write to the `.lumos` subdirectory in active workspaces.

---

### Novel Hypotheses
- **Hypothesis 1 (Exploration Reduction)**: Initializing an agent session with a pre-parsed `.lumos/workspace_state.json` reduces the time-to-first-relevant-edit by at least 40%.
- **Hypothesis 2 (Repeat Defect Reduction)**: Storing compilation/test gotchas in the `learnings_ledger` reduces redundant build configuration errors in multi-session tasks to exactly 0.

---

### Implementation Phases

#### Phase 1: Core Serialization & Schema Engine
- **Tasks**:
  - Design the official `.lumos/workspace_state.json` schema.
  - Write `lumos/core.py` to handle configuration parsing, JSON serialization, and schema validation.
  - Create the command-line entrypoint (`lumos init` and `lumos validate`).
- **Deliverables**:
  - `lumos/core.py`
  - `lumos/schema.json`
  - `tests/test_core.py`
- **Estimated Effort**: 2 days
- **Validation**: Run pytest checking schema compliance for valid/invalid JSON configurations.

#### Phase 2: Workspace Mapping & Git Integration
- **Tasks**:
  - Implement discovery routines to parse current Git branch, dirty file list, and file diffs using `git` commands.
  - Implement heuristic scanning of build configs (`Makefile`, `pyproject.toml`, `Cargo.toml`, `lakefile.lean`) to map directory branches to target tools.
  - Implement shell history parser to scrape recent successful commands.
- **Deliverables**:
  - `lumos/discovery.py`
  - `tests/test_discovery.py`
- **Estimated Effort**: 3 days
- **Validation**: Verify accurate mapping on mock C, Python, and Lean repository setups.

#### Phase 3: Git Hooks & Shell Aliases
- **Tasks**:
  - Create hook templates (`pre-commit.sh`, `post-merge.sh`) that automatically run `lumos save`.
  - Create a setup command `lumos hook-install` to install hooks locally.
  - Write shell aliases/wrappers to run `lumos load` on agent startup.
- **Deliverables**:
  - `lumos/hooks/`
  - `lumos/install.py`
- **Estimated Effort**: 2 days
- **Validation**: Verify that performing a git checkout or commit automatically triggers update warnings.

#### Phase 4: Integration & Benchmark Run
- **Tasks**:
  - Run the full loop in a dummy project workspace.
  - Benchmark context usage before and after Lumos injection.
  - Generate a user/agent guide showing how to write to `learnings_ledger`.
- **Deliverables**:
  - `lumos_benchmark_report.md`
  - `README.md` (User/Agent Guide)
- **Estimated Effort**: 2 days
- **Validation**: Verify agent context usage drops significantly on startup.

---

### Tools and Technologies
- **Languages**: Python 3
- **Libraries**: `json`, `pathlib`, `subprocess`, `jsonschema`
- **Test Command**: `python3 -m pytest tests/`
- **Doc Standard**: GitHub Flavored Markdown (GFM)

---

### Validation and Testing Strategy

**Unit / Integration Tests**
- `test_core.py`: Checks schema validation, file reading/writing, and error handling.
- `test_discovery.py`: Mocks git subprocesses and shell history files to ensure safe execution outputs.

**Static Analysis / Linters**
- Linting using `ruff check` and formatting using `ruff format`.
- Strict typing checked via `mypy lumos/`.

**Manual / Acceptance Checks**
- Run `lumos init` in the `prime-gap-structure` project, modify a python test file, and run `lumos save`. Inspect the generated `.lumos/workspace_state.json` file for accuracy.

---

### Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|:---|:---|:---|:---|
| **Stale Cache**: Workspace layout changes but local cache is not updated. | Medium | Medium | Validate file timestamps against the cache timestamp; trigger an automatic scan if any tracked file or config is newer than the cache. |
| **Token Bloat**: Excessive history entries or debug logs bloat the JSON file, consuming too much context. | Low | High | Implement strict array limits (max 5 command histories, max 10 learnings) and truncate values exceeding 500 characters. |
| **Security Leak**: Sensitive environment variables or secrets get cached in the ledger. | Low | High | Explicitly exclude files matching `.env`, `.pem`, `.git-credentials`, or lines containing secret keys/tokens. |

---

### Timeline

| Milestone | Target | Dependencies | Status |
|:---|:---|:---|:---|
| Schema definition and core serialization utility | Day 2 | None | [ ] |
| Git status and build engine auto-discovery | Day 5 | Core Engine | [ ] |
| Hooks and setup script installation | Day 7 | Discovery Engine | [ ] |
| End-to-end integration benchmark | Day 9 | Hooks | [ ] |

---

### References and Resources
- **Repo files examined**:
  - `/Users/velocityworks/.gemini/antigravity-cli/settings.json` (analyzed for permission grants and trusted workspaces)
  - `/Users/velocityworks/IdeaProjects/prime-gap-structure` (analyzed for multi-language complexity)
- **Framework documentation**:
  - Antigravity CLI Reference: `https://antigravity.google/docs/cli/reference`
