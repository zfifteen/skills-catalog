#!/usr/bin/env python3
"""Small deterministic helpers for the research-meeting skill (Grok port).

This is a well-adapted port of the original Codex research-meeting/scripts/research_meeting.py.
Key adaptations for Grok environment:
- No hardcoded user-specific paths.
- Optional use of sibling templates/ directory for opening prompt and minutes skeletons (with {{PLACEHOLDER}} substitution).
- Clear documentation of Grok CLI vs. local / subagent / codex-bus usage patterns.
- Same CLI interface for compatibility with existing workflows.
- LF line endings, strict no-overwrite on init.

Usage examples (from workspace root or skill dir):
  python skills/ported-from-codex/research-meeting/scripts/research_meeting.py init \
      --title "Reciprocal Left Gate" \
      --out-dir research-meetings

  python .../research_meeting.py grok-command \
      --cwd /path/to/prime-gap-structure \
      --prompt-file research-meetings/reciprocal-left-gate/transcript/round-00-opening.md
"""

from __future__ import annotations

import argparse
import re
import shlex
from datetime import datetime
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    if not slug:
        raise SystemExit("title produced an empty slug")
    return slug


def write_new(path: Path, text: str) -> None:
    if path.exists():
        raise SystemExit(f"refusing to overwrite existing file: {path}")
    path.write_text(text, encoding="utf-8", newline="\n")


def _load_template(templates_dir: Path, name: str) -> str | None:
    """Load a template file if it exists next to this script."""
    candidate = templates_dir / name
    if candidate.exists():
        return candidate.read_text(encoding="utf-8")
    return None


def _substitute(template: str, mapping: dict[str, str]) -> str:
    result = template
    for key, val in mapping.items():
        result = result.replace("{{" + key + "}}", val)
    return result


def init_meeting(args: argparse.Namespace) -> None:
    slug = args.slug or slugify(args.title)
    root = Path(args.out_dir).expanduser().resolve() / slug
    transcript = root / "transcript"
    if root.exists():
        raise SystemExit(f"meeting directory already exists: {root}")

    transcript.mkdir(parents=True)
    created = datetime.now().isoformat(timespec="seconds")

    # Determine templates directory (sibling to this script in the ported skill)
    script_dir = Path(__file__).resolve().parent
    templates_dir = script_dir.parent / "templates"

    # Try to load templates; fall back to original hardcoded content if missing.
    opening_tpl = _load_template(templates_dir, "opening_prompt.md")
    minutes_tpl = _load_template(templates_dir, "minutes.md")

    if opening_tpl:
        opening_content = _substitute(
            opening_tpl,
            {
                "TITLE": args.title,
                "AGENDA": "TODO: State the meeting agenda in one sentence.",
                "VERBATIM_STARTING_MATERIAL": "Paste the user-supplied starting material verbatim here.",
                "CURRENT_EVIDENCE_AND_BOUNDARIES": "TODO: List exact artifacts, measured status, proof status, invalidated rules, and unresolved questions.",
            },
        )
    else:
        # Original fallback content (slightly modernized)
        opening_content = f"""# Research Meeting Opening Prompt

## Meeting Title

{args.title}

## Created

{created}

## Instructions For Grok

Use your maximum available reasoning for this meeting. Opine freely on the
agenda and starting material first. Then propose a concrete deliverable for the
meeting. After that, ask Codex exactly one question.

## Agenda

TODO: State the meeting agenda in one sentence.

## Starting Material

Paste the user-supplied starting material verbatim here.

## Current Evidence And Boundaries

TODO: List exact artifacts, measured status, proof status, invalidated rules,
and unresolved questions.
"""

    if minutes_tpl:
        minutes_content = _substitute(
            minutes_tpl,
            {
                "TITLE": args.title,
                "CONTEXT": "TODO",
                "COMMAND_CAPABILITY_NOTES": "TODO",
                "AGENDA": "TODO",
                "NEGOTIATED_DELIVERABLE": "TODO",
                "CANDIDATE_INSIGHTS": "TODO",
                "FALSIFICATION_TESTS": "TODO",
                "CONVERGENCES": "TODO",
                "UNRESOLVED_QUESTIONS": "TODO",
                "NEXT_RESEARCH_MOVE": "TODO",
            },
        )
    else:
        minutes_content = f"""# {args.title} Research Meeting Minutes

## Context

TODO

## Participants

- Codex
- Grok CLI (or local subagent / codex-bus peer)

## Command Capability Notes

TODO

## Agenda

TODO

## Negotiated Deliverable

TODO

## Round Log

### Round 1

- Grok focus:
- Grok question:
- Codex answer:
- New object or invariant:
- Open issue:

## Candidate Insights

TODO

## Falsification Tests

TODO

## Convergences

TODO

## Unresolved Questions

TODO

## Next Research Move

TODO
"""

    write_new(transcript / "round-00-opening.md", opening_content)
    write_new(root / "minutes.md", minutes_content)

    print(f"Created meeting directory: {root}")
    print(f"  Opening prompt: {transcript / 'round-00-opening.md'}")
    print(f"  Minutes:        {root / 'minutes.md'}")


def grok_command(args: argparse.Namespace) -> None:
    """Print a ready-to-run Grok CLI (or equivalent) command."""
    command = [
        "grok",
        "--cwd",
        str(Path(args.cwd).expanduser().resolve()),
        "--always-approve",
    ]
    if args.session_id:
        command.extend(["--resume", args.session_id])
    command.extend(
        [
            "--prompt-file",
            str(Path(args.prompt_file).expanduser().resolve()),
            "--output-format",
            "plain",
            "--max-turns",
            str(args.max_turns),
        ]
    )
    if not args.allow_web_search:
        command.append("--disable-web-search")

    print("# Ready-to-paste command (adjust for your Grok environment):")
    print(shlex.join(command))
    print()
    print("# In environments without a direct 'grok' CLI binary, use this as a template")
    print("# for run_terminal_command, or adapt for codex-bus topic + subagent calls.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare research-meeting folders and Grok CLI (or equivalent) commands. Grok port."
    )
    subcommands = parser.add_subparsers(dest="command", required=True)

    init = subcommands.add_parser("init", help="create a meeting folder + transcript/minutes skeleton")
    init.add_argument("--title", required=True, help="Human-readable meeting title")
    init.add_argument("--out-dir", required=True, help="Base directory for meeting folders")
    init.add_argument("--slug", help="Optional explicit slug (defaults to slugified title)")
    init.set_defaults(func=init_meeting)

    grok = subcommands.add_parser("grok-command", help="print a Grok CLI (or equivalent) invocation command")
    grok.add_argument("--cwd", required=True, help="Repository working directory for the grok process")
    grok.add_argument("--prompt-file", required=True, help="Path to the round prompt file to send")
    grok.add_argument("--session-id", help="Existing session ID to resume (instead of new)")
    grok.add_argument("--max-turns", type=int, default=80, help="Max turns for this invocation")
    grok.add_argument("--allow-web-search", action="store_true", help="Permit web search in the invoked Grok")
    grok.set_defaults(func=grok_command)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
