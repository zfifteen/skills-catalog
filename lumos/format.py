from pathlib import Path
from .core import load_state

def format_state_to_markdown(workspace_dir: Path) -> str:
    """Formats the JSON state payload into a dense markdown block."""
    try:
        state = load_state(workspace_dir)
    except Exception as e:
        return f"Error loading state for formatting: {str(e)}"

    metadata = state.get("project_metadata", {})
    w_map = state.get("workspace_map", {})
    history = state.get("operational_history", {})
    ledger = state.get("learnings_ledger", {})
    handoff = state.get("handoff_state", {})

    lines = []
    lines.append("### 🧠 Lumos Workspace Active Memory")
    lines.append(f"- **Project**: `{metadata.get('name', workspace_dir.name)}` (branch: `{metadata.get('active_branch', 'unknown')}`)")
    lines.append(f"- **Git HEAD Commit**: `{metadata.get('git_commit_sha', 'None')}`")
    lines.append(f"- **Last Cached**: {metadata.get('last_updated', 'Never')}")
    lines.append("")

    # Modified Files
    modified = w_map.get("key_paths", {}).get("modified_files", [])
    if modified:
        lines.append("#### 📂 Active Modifications")
        for f in modified:
            lines.append(f"- `{f}`")
        lines.append("")

    # Preferred Commands
    pref_cmds = history.get("preferred_test_commands", {})
    if pref_cmds:
        lines.append("#### 🛠️ resolved Build & Test Commands")
        for path_prefix, cmd in pref_cmds.items():
            lines.append(f"- `{path_prefix}` -> `{cmd}`")
        lines.append("")

    # Learnings Ledger
    has_ledger = False
    for section, gotchas in ledger.items():
        if gotchas:
            if not has_ledger:
                lines.append("#### 📜 Learnings Ledger (Workspace Gotchas)")
                has_ledger = True
            lines.append(f"##### {section.replace('_', ' ').title()}")
            for k, v in gotchas.items():
                lines.append(f"- **{k}**: {v}")
    if has_ledger:
        lines.append("")

    # Handoff
    has_handoff = False
    last_step = handoff.get("last_completed_step", "")
    pending = handoff.get("pending_tasks", [])
    warnings = handoff.get("warnings", [])

    if last_step or pending or warnings:
        lines.append("#### 🏁 Handoff State")
        if last_step:
            lines.append(f"- **Last Completed Step**: {last_step}")
        if pending:
            lines.append("- **Pending Tasks**:")
            for task in pending:
                lines.append(f"  - [ ] {task}")
        if warnings:
            lines.append("- **Warnings / Notes**:")
            for warn in warnings:
                lines.append(f"  - ⚠️ {warn}")
        has_handoff = True

    return "\n".join(lines)
