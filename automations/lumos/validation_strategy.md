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
  pip install pytest jsonschema
  ```

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
* **Objective**: Verify that Lumos creates the hidden metadata folder and seeds the initial schema files correctly.
* **Tester Steps**:
  1. Navigate to `/tmp/lumos-test-repo`.
  2. Run the initialization command:
     ```bash
     python3 -m lumos.cli init
     ```
* **Expected Output**:
  - The CLI outputs: `Success: Initialized Lumos workspace cache at .lumos/`
  - A directory named `.lumos` is created.
  - A file named `.lumos/workspace_state.json` exists and is populated with base metadata.
  - A file named `.lumos/schema.json` exists.
* **Failure Condition**: Any exit code other than `0`. Failure to create `.lumos` directory.

---

### Test Case 2: Workspace State Capture (`lumos save`)
* **Objective**: Verify that Git branch, modified file lists, and recent history are accurately captured.
* **Tester Steps**:
  1. Create a new branch:
     ```bash
     git checkout -b feature/test-lumos-branch
     ```
  2. Modify a file in the workspace:
     ```bash
     echo '# Test modification' >> src/python/main.py
     ```
  3. Execute a dummy command to populate the local history:
     ```bash
     make test-dummy-command-success
     ```
  4. Run the state save command:
     ```bash
     python3 -m lumos.cli save
     ```
* **Expected Output**:
  - The file `.lumos/workspace_state.json` contains:
    - `"active_branch": "feature/test-lumos-branch"`
    - `"key_paths"` mapping correctly identifying `src/python` and `src/c`.
    - `"recent_successful_commands"` including `make test-dummy-command-success`.
  - The json structure successfully validates against `.lumos/schema.json`.

---

### Test Case 3: Invariant Preservation (The gotcha test)
* **Objective**: Ensure manually added learnings in the `learnings_ledger` are preserved and not overwritten by subsequent auto-saves.
* **Tester Steps**:
  1. Open `.lumos/workspace_state.json` in an editor.
  2. Under `"learnings_ledger" -> "build_invariants"`, append a custom key-value pair:
     ```json
     "test_gotcha": "Running C tests requires setting ENV_VAR=1"
     ```
  3. Save the file.
  4. Modify another workspace file:
     ```bash
     echo '# Another modification' >> src/c/main.c
     ```
  5. Run the save command again:
     ```bash
     python3 -m lumos.cli save
     ```
  6. Inspect `.lumos/workspace_state.json`.
* **Expected Output**:
  - The newly modified file `src/c/main.c` is listed in the workspace metadata change log.
  - The manual gotcha `"test_gotcha": "Running C tests requires setting ENV_VAR=1"` remains fully intact in the ledger.

---

### Test Case 4: Security and Secret Scrubbing
* **Objective**: Verify that secrets, environment files, and credentials are automatically scrubbed from the history cache.
* **Tester Steps**:
  1. Create a mock secret file:
     ```bash
     echo "API_KEY=xoxb-1234567890-abcdef" > .env
     ```
  2. Modify a tracked file with a mock secret:
     ```bash
     echo "admin_password = 'SuperSecretPassword123'" >> src/python/main.py
     ```
  3. Run the save command:
     ```bash
     python3 -m lumos.cli save
     ```
  4. Open `.lumos/workspace_state.json` and search for:
     - `.env`
     - `xoxb-`
     - `SuperSecretPassword123`
* **Expected Output**:
  - The `.env` file must be excluded from the tracked file listings.
  - Any commands containing sensitive strings or strings matching secret patterns must be omitted or redacted in `operational_history`.

---

### Test Case 5: State Deserialization and Injection (`lumos load`)
* **Objective**: Verify that loading the state reads the payload, validates schema, and prints the payload in under 200ms.
* **Tester Steps**:
  1. Run the load command with timing enabled:
     ```bash
     time python3 -m lumos.cli load
     ```
* **Expected Output**:
  - The CLI outputs a clean JSON payload mapping the current state.
  - The `real` execution time measured by the shell must be less than `0.20s` (200ms).
  - The JSON output contains correct handoff states and tasks.

---

### Test Case 6: Edge Cases & Robustness
* **Objective**: Ensure Lumos degrades gracefully when run in incomplete environments.
* **Tester Steps (Detached HEAD)**:
  1. Checkout a detached git state:
     ```bash
     git checkout HEAD~1
     ```
  2. Run `python3 -m lumos.cli save`.
  * **Expected Output**: `"active_branch"` is recorded as `"DETACHED_HEAD"` or the commit hash. No crash occurs.
  
* **Tester Steps (Non-Git Directory)**:
  1. Navigate outside the repository:
     ```bash
     cd /tmp
     ```
  2. Run `python3 -m lumos.cli save`.
  * **Expected Output**: The CLI terminates with code `1` and prints: `Error: Current directory is not a Git repository or initialized Lumos workspace.`

---

## 4. Tester Sign-Off Sheet

| Test ID | Title | Result (Pass/Fail) | Notes / Logs | Verified By (Initials) |
|:---|:---|:---|:---|:---|
| **TC-1** | Initializing Lumos (`lumos init`) | | | |
| **TC-2** | Workspace State Capture (`save`) | | | |
| **TC-3** | Invariant Preservation | | | |
| **TC-4** | Security & Secret Scrubbing | | | |
| **TC-5** | State Deserialization (`load`) | | | |
| **TC-6** | Detached HEAD / Non-Git Errors | | | |
