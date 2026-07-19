#!/usr/bin/env python3
"""List public GitHub repositories with short Markdown summaries.

Grok port of the Codex "repos" skill supporting script.
Original: ~/.codex/skills/repos/scripts/list_public_repos.py

Functional for Grok: invoked via `run_terminal_cmd` tool.
No Python package dependencies (uses `gh` CLI which must be installed and authenticated).

Usage in Grok skill context:
  python3 "<SKILL_DIR>/scripts/list_public_repos.py"

The script emits one Markdown bullet per public repository for the currently
authenticated `gh` account. Summaries capped at 500 chars, derived from
repo description or cleaned README.

Public forks marked with " _(fork)_".
"""

from __future__ import annotations

import base64
import json
import re
import subprocess
import sys
from typing import Any


MAX_SUMMARY_CHARS = 500
NO_SUMMARY = "No public description or README summary available."


def run_gh(args: list[str]) -> str:
    result = subprocess.run(
        ["gh", *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"gh {' '.join(args)} failed: {detail}")
    return result.stdout


def active_owner() -> str:
    owner = run_gh(["api", "user", "--jq", ".login"]).strip()
    if not owner:
        raise RuntimeError("gh api user returned an empty login")
    return owner


def public_repos(owner: str) -> list[dict[str, Any]]:
    output = run_gh(
        [
            "repo",
            "list",
            owner,
            "--visibility=public",
            "--limit",
            "1000",
            "--json",
            "name,url,description,isFork",
        ]
    )
    return json.loads(output)


def readme_text(owner: str, repo: str) -> str:
    output = run_gh(["api", f"repos/{owner}/{repo}/readme", "--jq", ".content"])
    compact = "".join(output.split())
    if not compact:
        return ""
    decoded = base64.b64decode(compact).decode("utf-8", errors="replace")
    return clean_markdown(decoded)


def clean_markdown(text: str) -> str:
    text = re.sub(r"```.*?```", " ", text, flags=re.DOTALL)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"^#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[ \t]*[-*+]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"[*_`>]+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def normalize_plain_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def first_sentence_window(text: str, *, markdown: bool) -> str:
    cleaned = clean_markdown(text) if markdown else normalize_plain_text(text)
    if len(cleaned) <= MAX_SUMMARY_CHARS:
        return cleaned
    clipped = cleaned[: MAX_SUMMARY_CHARS + 1]
    boundary = max(clipped.rfind(". "), clipped.rfind("! "), clipped.rfind("? "))
    if boundary >= 120:
        return clipped[: boundary + 1].strip()
    return cleaned[:MAX_SUMMARY_CHARS].rstrip()


def summary_for(owner: str, repo: dict[str, Any]) -> str:
    description = (repo.get("description") or "").strip()
    if description:
        return first_sentence_window(description, markdown=False)
    try:
        readme = readme_text(owner, repo["name"])
    except RuntimeError:
        readme = ""
    if readme:
        return first_sentence_window(readme, markdown=True)
    return NO_SUMMARY


def markdown_bullet(owner: str, repo: dict[str, Any]) -> str:
    summary = summary_for(owner, repo)
    if len(summary) > MAX_SUMMARY_CHARS:
        summary = summary[:MAX_SUMMARY_CHARS].rstrip()
    fork_marker = " _(fork)_" if repo.get("isFork") else ""
    return f"- [{repo['name']}]({repo['url']}): {summary}{fork_marker}"


def main() -> int:
    try:
        owner = active_owner()
        repos = public_repos(owner)
        for repo in repos:
            print(markdown_bullet(owner, repo))
    except Exception as exc:
        print(f"repos skill failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
