import sys
import argparse
import subprocess
from pathlib import Path
from .core import init_workspace, load_state, save_state, add_learning
from .discovery import get_git_commit_sha, get_git_branch, perform_workspace_save
from .format import format_state_to_markdown

def cmd_init(args):
    cwd = Path(args.cwd)
    msg = init_workspace(cwd)
    print(msg)

def cmd_status(args):
    cwd = Path(args.cwd)
    try:
        state = load_state(cwd)
    except FileNotFoundError as e:
        print(str(e))
        sys.exit(1)

    cached_sha = state.get("project_metadata", {}).get("git_commit_sha", "")
    current_sha = get_git_commit_sha(cwd)

    print(f"Lumos Schema Version: {state.get('schema_version', 'unknown')}")
    print(f"Active Branch: {get_git_branch(cwd)}")
    print(f"Cached commit SHA: {cached_sha or 'None'}")
    print(f"Current commit SHA: {current_sha or 'None'}")

    if not cached_sha:
        print("Warning: No commit SHA is cached yet. Run 'lumos save' to capture current state.")
    elif cached_sha != current_sha:
        print("Warning: Cache is STALE. Workspace HEAD SHA differs from cached SHA. Run 'lumos save' to refresh.")
    else:
        print("Cache Status: Healthy")

def cmd_learn(args):
    cwd = Path(args.cwd)
    learning_arg = args.learning
    if ":" not in learning_arg:
        print("Error: Learning must be formatted as '<path>:<value>', e.g. 'build_invariants.lake: lake build'")
        sys.exit(1)

    path_str, value = learning_arg.split(":", 1)
    try:
        add_learning(cwd, path_str.strip(), value.strip())
        print(f"Added learning insight to '{path_str.strip()}' successfully.")
    except Exception as e:
        print(f"Error adding learning: {str(e)}")
        sys.exit(1)

def cmd_save(args):
    cwd = Path(args.cwd)
    try:
        state = load_state(cwd)
    except FileNotFoundError:
        # Auto-init if directory is clean and git initialized
        init_workspace(cwd)
        state = load_state(cwd)

    try:
        updated_state = perform_workspace_save(cwd, state)
        save_state(cwd, updated_state)
        print("Success: Captured active branch status, modifications, and rules mappings.")
    except Exception as e:
        print(f"Error during workspace state capture: {str(e)}")
        sys.exit(1)

def cmd_load(args):
    cwd = Path(args.cwd)
    try:
        markdown_block = format_state_to_markdown(cwd)
        print(markdown_block)
    except Exception as e:
        print(f"Error loading state: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Lumos: Ephemeral Agent Caching Tool")
    parser.add_argument("--cwd", default=".", help="Workspace target directory (default: current)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Init command
    subparsers.add_parser("init", help="Initialize Lumos workspace cache and update gitignore")

    # Status command
    subparsers.add_parser("status", help="Verify cache integrity and check commit SHA alignments")

    # Learn command
    learn_parser = subparsers.add_parser("learn", help="Save a developer gotcha/learning ledger item")
    learn_parser.add_argument("learning", help="Formatted gotcha string, e.g. 'logical_invariants.port: 3000'")

    # Save command
    subparsers.add_parser("save", help="Serialize active workspace state and logs (Phase 2)")

    # Load command
    subparsers.add_parser("load", help="Format and print clean markdown summaries for prompt ingestion (Phase 3)")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "learn":
        cmd_learn(args)
    elif args.command == "save":
        cmd_save(args)
    elif args.command == "load":
        cmd_load(args)

if __name__ == "__main__":
    main()
