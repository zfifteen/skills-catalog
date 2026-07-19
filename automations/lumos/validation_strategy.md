# Validation and Testing Strategy: Lumos Workspace Cache

This document provides a detailed, step-by-step validation protocol for verifying the behavior, safety, and performance of **Lumos**. It is designed to be executed by a third-party tester or automated validation agent on a clean macOS/Linux environment.

---

## 1. Prerequisites and Environment Setup

Before starting the test suite, ensure the target testing machine has the following tools and configurations:

- **OS**: macOS (10.15+) or Linux
- **Python**: version 3.8 or higher (`python3 --version`)
- **Git**: version 2.20 or higher (`git --version`)
- **Required Libraries**: Install the validation dependencies:
  ```bash
  pip install pytest
  ```
  *(Note: Lumos runs zero-dependency for core commands, so `jsonschema` must not be a hard requirement to execute standard commands).*

---

## 2. Test Workspace Preparation

To ensure tests do not corrupt production directories, the tester must create a mock workspace:

```bash
# Create a temporary workspace directory
mkdir -p /tmp/lumos-test-repo
cd /tmp/lumos-test-repo

# Initialize Git
git init

# Configure local git user for test commits
git config user.name "Lumos Tester"
git config user.email "tester@lumos.local"

# Create a sample project structure
mkdir -p src/python src/c tests
echo 'print("Hello Lumos")' > src/python/main.py
echo 'int main() { return 0; }' > src/c/main.c
echo "Makefile content" > Makefile
echo "pytest command" > tests/test_main.py

# Commit initial files
git add .
git commit -m "Initial commit of test repository"
```

---

## 3. Step-by-Step Test Cases

### Test Case 1: Initializing Lumos (`lumos init`)
* **Objective**: Verify that Lumos creates the hidden metadata folder, sets up rules templates, and updates ignore rules.
* **Tester Steps**:
  1. Navigate to `/tmp/lumos-test-repo`.
  2. Run the initialization command:
     ```bash
     python3 -m lumos.cli init
     ```
* **Expected Output**:
  - The CLI outputs: `Success: Initialized Lumos workspace cache at .lumos/`
  - A directory named `.lumos` is created.
  - A file named `.lumos/workspace_state.json` exists.
  - A file named `.gitignore` exists and contains `.lumos/`.
* **Failure Condition**: Any exit code other than `0`. Failure to write `.lumos/` to `.gitignore`.

---

### Test Case 2: Workspace State Capture & SHA Checking (`lumos status` and `save`)
* **Objective**: Verify that Git HEAD commit SHA, branch, and status match and are verified by the status command.
* **Tester Steps**:
  1. Run the save command:
     ```bash
     python3 -m lumos.cli save
     ```
  2. Modify a file in the workspace:
     ```bash
     echo '# Test modification' >> src/python/main.py
     ```
  3. Run the status command:
     ```bash
     python3 -m lumos.cli status
     ```
  4. Commit the changes and run status again:
     ```bash
     git add src/python/main.py
     git commit -m "update code"
     python3 -m lumos.cli status
     ```
* **Expected Output**:
  - Step 1 creates a cache with the current Git commit SHA.
  - Step 3 returns `Cache Status: Healthy` (as the active commit SHA has not changed, even with local modifications).
  - Step 4 returns `Warning: Cache is STALE. Workspace HEAD SHA differs from cached SHA. Run 'lumos save' to refresh.`

---

### Test Case 3: Invariant Preservation & CLI Learning (`lumos learn`)
* **Objective**: Ensure the `learn` CLI command appends gotchas correctly and does not wipe them during subsequent saves.
* **Tester Steps**:
  1. Run the learn command:
     ```bash
     python3 -m lumos.cli learn "logical_invariants.test_gotcha: Running C tests requires setting ENV_VAR=1"
     ```
  2. Inspect `.lumos/workspace_state.json` to verify the entry exists.
  3. Modify another workspace file:
     ```bash
     echo '# Another modification' >> src/c/main.c
     ```
  4. Run the save command:
     ```bash
     python3 -m lumos.cli save
     ```
  5. Inspect `.lumos/workspace_state.json`.
* **Expected Output**:
  - The learning `test_gotcha` is written directly to `"learnings_ledger" -> "logical_invariants"`.
  - The manual gotcha remains fully intact after the subsequent auto-save.

---

### Test Case 4: Security and Regex Secret Scrubbing
* **Objective**: Verify that high-risk keys and credentials are automatically scrubbed from history logs, and custom rules are respected.
* **Tester Steps**:
  1. Create a mock secret file:
     ```bash
     echo "AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" > .env
     ```
  2. Add `.env` to `.lumos/.secretsignore` (or configure ignore rules).
  3. Run the save command:
     ```bash
     python3 -m lumos.cli save
     ```
  4. Open `.lumos/workspace_state.json` and search for:
     - `wJalrXUtnFEMI/K7MDENG`
* **Expected Output**:
  - The file `.env` must not be parsed or included in the key path indexes.
  - Any commands containing sensitive key formats must be redacted in the history list.

---

### Test Case 5: State Deserialization & Formatting (`lumos load`)
* **Objective**: Verify that loading the state prints a clean, prompt-ready Markdown block under 200ms.
* **Tester Steps**:
  1. Run the load command:
     ```bash
     time python3 -m lumos.cli load
     ```
* **Expected Output**:
  - The CLI outputs a clean Markdown codeblock summary representing the workspace status, branch, pending tasks, and ledger.
  - The total execution time is under `0.20s` (200ms).

---

## 4. Tester Sign-Off Sheet

| Test ID | Title | Result (Pass/Fail) | Notes / Logs | Verified By (Initials) |
|:---|:---|:---|:---|:---|
| **TC-1** | Initializing Lumos & Ignore Check | | | |
| **TC-2** | SHA Verification (`lumos status`) | | | |
| **TC-3** | CLI Learning Command (`learn`) | | | |
| **TC-4** | Regex Secret Scrubbing | | | |
| **TC-5** | Prompt Markdown Format (`load`) | | | |
