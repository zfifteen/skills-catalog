#!/usr/bin/env python3
"""Call the local Grok CLI with the standard sticky-collaboration flags."""

from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path


DEFAULT_CWD = "/Users/velocityworks/IdeaProjects/prime-gap-structure"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Call Grok CLI for Codex collaboration.")
    parser.add_argument("--cwd", default=DEFAULT_CWD)
    parser.add_argument("--prompt-file", type=Path)
    parser.add_argument("--max-turns", type=int)
    parser.add_argument("--mode", choices=("normal", "parallel", "roles"), default="normal")
    parser.add_argument("--best-of-n", type=int)
    parser.add_argument("--agents-file", type=Path)
    parser.add_argument("--resume")
    parser.add_argument("--no-continue", action="store_true")
    parser.add_argument("--disable-web-search", action="store_true")
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def prompt_path_from_stdin() -> Path:
    body = sys.stdin.read()
    if not body.strip():
        raise SystemExit("missing prompt on stdin and no --prompt-file was provided")
    handle = tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        suffix=".md",
        prefix="grok-cli-collab-",
        delete=False,
    )
    with handle:
        handle.write(body)
        if not body.endswith("\n"):
            handle.write("\n")
    return Path(handle.name)


def main() -> int:
    args = parse_args()
    if args.mode == "roles" and args.agents_file is None:
        raise SystemExit("--mode roles requires --agents-file")
    if args.mode != "roles" and args.agents_file is not None:
        raise SystemExit("--agents-file is only valid with --mode roles")
    if args.mode != "normal" and args.resume:
        raise SystemExit("--resume is only valid with --mode normal")
    if args.mode != "normal" and args.no_continue:
        raise SystemExit("--no-continue is only valid with --mode normal")

    prompt_file = args.prompt_file
    temporary_prompt = False
    if prompt_file is None:
        prompt_file = prompt_path_from_stdin()
        temporary_prompt = True

    max_turns = args.max_turns
    if max_turns is None:
        max_turns = 3 if args.mode == "normal" else 10

    command = [
        "grok",
        "--cwd",
        args.cwd,
        "--always-approve",
        "--prompt-file",
        str(prompt_file),
        "--output-format",
        "plain",
        "--max-turns",
        str(max_turns),
    ]
    if args.mode == "normal" and args.resume:
        command[4:4] = ["--resume", args.resume]
    elif args.mode == "normal" and not args.no_continue:
        command[4:4] = ["--continue"]
    elif args.mode == "parallel":
        best_of_n = args.best_of_n if args.best_of_n is not None else 2
        command.extend(["--best-of-n", str(best_of_n), "--disable-web-search"])
    elif args.mode == "roles":
        best_of_n = args.best_of_n if args.best_of_n is not None else 3
        command.extend(
            [
                "--best-of-n",
                str(best_of_n),
                "--agents",
                args.agents_file.read_text(encoding="utf-8"),
                "--disable-web-search",
            ]
        )
    if args.mode == "normal" and args.disable_web_search:
        command.append("--disable-web-search")
    if args.check:
        command.append("--check")

    try:
        result = subprocess.run(command, check=False)
        return int(result.returncode)
    finally:
        if temporary_prompt:
            prompt_file.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
