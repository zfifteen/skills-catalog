import os
import json
import tempfile
import copy
import shutil
from pathlib import Path

SCHEMA_VERSION = "1.0.0"

DEFAULT_STATE = {
    "schema_version": SCHEMA_VERSION,
    "project_metadata": {
        "name": "",
        "last_updated": "",
        "active_branch": "",
        "git_commit_sha": ""
    },
    "workspace_map": {
        "key_paths": {},
        "entrypoints": []
    },
    "operational_history": {
        "preferred_test_commands": {},
        "recent_successful_commands": [],
        "flaky_commands_to_avoid": []
    },
    "learnings_ledger": {
        "build_invariants": {},
        "logical_invariants": {},
        "design_preferences": {}
    },
    "handoff_state": {
        "last_completed_step": "",
        "pending_tasks": [],
        "warnings": []
    }
}

def get_lumos_dir(workspace_dir: Path) -> Path:
    return workspace_dir / ".lumos"

def get_state_file(workspace_dir: Path) -> Path:
    return get_lumos_dir(workspace_dir) / "workspace_state.json"

def init_workspace(workspace_dir: Path) -> str:
    """Initializes the .lumos directory and default workspace state."""
    lumos_dir = get_lumos_dir(workspace_dir)
    lumos_dir.mkdir(parents=True, exist_ok=True)

    state_file = get_state_file(workspace_dir)
    if not state_file.exists():
        state = copy.deepcopy(DEFAULT_STATE)
        state["project_metadata"]["name"] = workspace_dir.resolve().name
        save_state(workspace_dir, state)

    # Auto-ignore .lumos/ in .gitignore
    gitignore = workspace_dir / ".gitignore"
    ignore_rule = ".lumos/"
    
    ignore_exists = False
    if gitignore.exists():
        try:
            content = gitignore.read_text(encoding="utf-8")
            if any(line.strip() == ignore_rule for line in content.splitlines()):
                ignore_exists = True
        except Exception:
            pass

    if not ignore_exists:
        try:
            with open(gitignore, "a", encoding="utf-8") as f:
                # Add a newline if it doesn't end with one
                if gitignore.exists() and gitignore.stat().st_size > 0:
                    f.write("\n")
                    f.write(ignore_rule + "\n")
                else:
                    f.write(ignore_rule + "\n")
        except Exception as e:
            return f"Initialized workspace at .lumos/ but failed to update .gitignore: {str(e)}"

    return "Successfully initialized Lumos workspace cache at .lumos/"

def load_state(workspace_dir: Path) -> dict:
    """Loads the workspace state from JSON."""
    state_file = get_state_file(workspace_dir)
    if not state_file.exists():
        raise FileNotFoundError(f"Lumos workspace state not found in {workspace_dir}. Run 'lumos init' first.")
    
    with open(state_file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_state(workspace_dir: Path, state_data: dict) -> None:
    """Atomic write of workspace state to JSON with cross-device link safety."""
    lumos_dir = get_lumos_dir(workspace_dir)
    lumos_dir.mkdir(parents=True, exist_ok=True)
    state_file = get_state_file(workspace_dir)

    # Write to a temp file in the same directory, then rename atomically
    with tempfile.NamedTemporaryFile("w", dir=str(lumos_dir), delete=False, suffix=".json", encoding="utf-8") as tf:
        json.dump(state_data, tf, indent=2, ensure_ascii=False)
        temp_name = tf.name

    try:
        os.replace(temp_name, str(state_file))
    except OSError:
        # Fallback to shutil.move in case of cross-device link exceptions (EXDEV)
        try:
            shutil.move(temp_name, str(state_file))
        except Exception:
            if os.path.exists(temp_name):
                os.remove(temp_name)
            raise
    except Exception:
        # Cleanup temp file on general failure
        if os.path.exists(temp_name):
            os.remove(temp_name)
        raise
    
def add_learning(workspace_dir: Path, path_str: str, value: str) -> dict:
    """Adds a key-value insight directly to learnings_ledger.
    path_str can look like 'logical_invariants.test_gotcha' or 'build_invariants.make'
    """
    state = load_state(workspace_dir)
    ledger = state.setdefault("learnings_ledger", {})

    parts = path_str.split(".", 1)
    if len(parts) == 2:
        section, key = parts
    else:
        # Default to logical_invariants if section unspecified
        section, key = "logical_invariants", parts[0]

    # Ensure section dictionary exists
    section_dict = ledger.setdefault(section, {})
    section_dict[key] = value

    save_state(workspace_dir, state)
    return state
