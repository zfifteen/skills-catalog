import subprocess
import json
from pathlib import Path
from .scrub import filter_dirty_files

def run_git_cmd(cwd: Path, args: list) -> str:
    """Helper to safely run a git command in the target directory (preserves leading spaces)."""
    try:
        res = subprocess.run(
            ["git"] + args,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=True
        )
        return res.stdout.rstrip()
    except subprocess.CalledProcessError:
        return ""

def get_git_info(cwd: Path) -> dict:
    """Gathers commit SHA, branch, and lists of staged/unstaged changes."""
    sha = run_git_cmd(cwd, ["rev-parse", "HEAD"])
    branch = run_git_cmd(cwd, ["rev-parse", "--abbrev-ref", "HEAD"]) or "DETACHED_HEAD"
    
    # Git status parsing with -u to show individual files in untracked dirs
    status_raw = run_git_cmd(cwd, ["status", "--porcelain", "-u"])
    dirty_files = []
    if status_raw:
        for line in status_raw.splitlines():
            if len(line) > 3:
                # Format: XY filename (XY contains status codes, index 2 is space)
                file_path = line[3:].strip()
                dirty_files.append(file_path)

    return {
        "git_commit_sha": sha,
        "active_branch": branch,
        "dirty_files": filter_dirty_files(dirty_files)
    }

def load_rules(cwd: Path) -> dict:
    """Loads path command mappings from .lumos/rules.json if present."""
    rules_file = cwd / ".lumos" / "rules.json"
    if not rules_file.exists():
        # Return default configurations fallback
        return {
            "path_mappings": {
                "tests": {
                    "test_command": "pytest"
                },
                "src": {
                    "build_command": "make"
                }
            }
        }
    
    try:
        with open(rules_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"path_mappings": {}}

def match_path_rules(cwd: Path, dirty_files: list) -> dict:
    """Iterates through modified paths and resolves target build/test runners."""
    rules = load_rules(cwd)
    mappings = rules.get("path_mappings", {})
    
    resolved_tests = {}
    
    # Guard against O(N*M) lookups on huge changesets
    if len(dirty_files) > 100:
        return resolved_tests

    for file_path in dirty_files:
        path_obj = Path(file_path)
        for match_prefix, commands in mappings.items():
            prefix_path = Path(match_prefix)
            
            # Verify directory hierarchy containment safely
            try:
                # relative_to raises ValueError if path is not a child of prefix
                path_obj.relative_to(prefix_path)
                is_match = True
            except ValueError:
                is_match = False

            if is_match:
                for cmd_type, cmd in commands.items():
                    if cmd_type == "test_command":
                        resolved_tests[match_prefix] = cmd
                    elif cmd_type == "build_command":
                        # We could also track preferred build commands
                        pass

    return resolved_tests

def perform_workspace_save(cwd: Path, state: dict) -> dict:
    """Runs git discovery, updates rules command maps, and packages state updates."""
    git_info = get_git_info(cwd)
    
    state["project_metadata"]["git_commit_sha"] = git_info["git_commit_sha"]
    state["project_metadata"]["active_branch"] = git_info["active_branch"]
    
    # Auto-update workspace map with currently modified files
    state["workspace_map"]["key_paths"]["modified_files"] = git_info["dirty_files"]

    # Match rules command runner
    resolved_commands = match_path_rules(cwd, git_info["dirty_files"])
    if resolved_commands:
        state["operational_history"]["preferred_test_commands"] = resolved_commands

    import datetime
    state["project_metadata"]["last_updated"] = datetime.datetime.now().isoformat()

    return state
