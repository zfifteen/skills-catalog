# Agent Guidelines & Contract: skills-catalog

Welcome, AI Agent! To maximize context efficiency, reduce token usage, and maintain development continuity on this repository, please adhere to the following startup contract.

---

## 🧠 Startup Protocol: Lumos Cache Ingestion

Before running any exploratory commands (such as recursive directory listings, wide grep searches, or reading multiple source files):

1.  **Check for Lumos Cache**: Look for the `.lumos/workspace_state.json` file in the root directory.
2.  **Ingest State**: If it exists, read it first using `view_file`.
3.  **Synchronize Context**:
    *   Inspect `"project_metadata"` and `"workspace_map"` to identify the active branch and dirty/modified files.
    *   Read the `"learnings_ledger"` to load established build invariants, gotchas, and design preferences for this workspace.
    *   Consult the `"handoff_state"` to read the checklist of pending tasks and warnings left by the previous session.
4.  **Confirm Alignment**: Declare in your first response that you have successfully loaded the Lumos cache and list the pending tasks you are resuming.
