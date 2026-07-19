#!/usr/bin/env python3
"""Call the local Antigravity CLI (agy) for Grok Build collaboration."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_CWD = "/Users/velocityworks/IdeaProjects/prime-gap-structure"
DEFAULT_AGY = "/Users/velocityworks/.local/bin/agy"
DEFAULT_TIMEOUT = "10m"
CONVERSATION_RE = re.compile(
    r"Created conversation ([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})",
    re.IGNORECASE,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Call agy CLI for Grok collaboration.")
    parser.add_argument("--cwd", default=DEFAULT_CWD)
    parser.add_argument("--agy", default=DEFAULT_AGY)
    parser.add_argument("--prompt-file", type=Path)
    parser.add_argument(
        "--mode",
        choices=("start", "continue", "conversation", "clean"),
        default="start",
    )
    parser.add_argument("--conversation")
    parser.add_argument("--project")
    parser.add_argument("--new-project", action="store_true")
    parser.add_argument("--add-dir", action="append", default=[])
    parser.add_argument("--print-timeout", default=DEFAULT_TIMEOUT)
    parser.add_argument("--log-file", type=Path)
    parser.add_argument("--state-file", type=Path)
    return parser.parse_args()


def prompt_text(args: argparse.Namespace) -> tuple[str, Path | None]:
    if args.prompt_file is not None:
        text = args.prompt_file.read_text(encoding="utf-8")
        return text, None

    body = sys.stdin.read()
    if not body.strip():
        raise SystemExit("missing prompt on stdin and no --prompt-file was provided")

    handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        suffix=".md",
        prefix="agy-cli-collab-",
        delete=False,
    )
    with handle:
        handle.write(body)
        if not body.endswith("\n"):
            handle.write("\n")
    return body, Path(handle.name)


def validate_prompt(prompt: str) -> None:
    if not prompt.strip():
        raise SystemExit("empty prompt: agy rejects -p with no content")


def build_command(args: argparse.Namespace, prompt: str) -> list[str]:
    if args.mode == "conversation" and not args.conversation:
        raise SystemExit("--mode conversation requires --conversation <uuid>")

    command = [args.agy]
    add_dirs = args.add_dir or [args.cwd]
    for directory in add_dirs:
        command.extend(["--add-dir", directory])

    if args.mode == "continue":
        command.append("--continue")
    elif args.mode == "conversation":
        command.extend(["--conversation", args.conversation])

    if args.new_project:
        command.append("--new-project")
    if args.project:
        command.extend(["--project", args.project])

    command.append("--dangerously-skip-permissions")

    if args.log_file is not None:
        command.extend(["--log-file", str(args.log_file)])

    command.extend(["--print-timeout", args.print_timeout, "-p", prompt])
    return command


def capture_conversation_id(log_file: Path | None) -> str | None:
    if log_file is None or not log_file.exists():
        return None
    match = CONVERSATION_RE.search(log_file.read_text(encoding="utf-8", errors="replace"))
    return match.group(1) if match else None


def write_state_file(state_file: Path, conversation_id: str) -> None:
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state_file.write_text(conversation_id + "\n", encoding="utf-8")


def default_project_name() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"agy-collab-{stamp}"


def main() -> int:
    args = parse_args()
    prompt, temporary_prompt = prompt_text(args)
    validate_prompt(prompt)

    if args.mode == "start" and args.new_project and not args.project:
        args.project = default_project_name()

    command = build_command(args, prompt)
    cwd = Path(args.cwd)
    if not cwd.is_dir():
        raise SystemExit(f"cwd does not exist: {cwd}")

    try:
        result = subprocess.run(
            command,
            cwd=str(cwd),
            check=False,
            text=True,
            capture_output=True,
        )
        if result.stdout:
            sys.stdout.write(result.stdout)
            if not result.stdout.endswith("\n"):
                sys.stdout.write("\n")
        if result.stderr:
            sys.stderr.write(result.stderr)
            if not result.stderr.endswith("\n"):
                sys.stderr.write("\n")

        if args.mode == "start" and args.state_file is not None:
            conversation_id = capture_conversation_id(args.log_file)
            if conversation_id is None:
                raise SystemExit(
                    "could not parse conversation id from log file; "
                    "pass --log-file on start mode"
                )
            write_state_file(args.state_file, conversation_id)

        return int(result.returncode)
    finally:
        if temporary_prompt is not None:
            temporary_prompt.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())