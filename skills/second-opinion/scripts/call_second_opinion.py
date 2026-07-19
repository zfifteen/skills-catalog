#!/usr/bin/env python3
"""
call_second_opinion.py — Grok-port helper for the second-opinion skill.

Usage (from agent via run_terminal_cmd):
    python3 /path/to/this/script.py <<'JSON'
    {"problem": "...", "context": "...", "focus": "optional", "mode": "package" | "local-review"}
    JSON

It enriches the request with live git/workspace snapshot (best-effort) and emits
a ready-to-use Second Opinion Request Package (Markdown) plus, for local-review
mode, a self-contained verifier prompt.

This is the Grok-adapted equivalent of the original Codex script that called
the xai_harness MCP over stdio. Here we produce high-quality input packages
that work with Grok's task/subagent tools, external Grok chats, or (if
configured) a future MCP second_opinion tool.
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


def run_git(cmd: list[str], cwd: Path | None = None) -> str:
    """Best-effort git command. Returns stdout or short error."""
    try:
        result = subprocess.run(
            ["git"] + cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=8,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return f"(git {cmd[0]} failed: {result.stderr.strip()[:200]})"
    except Exception as e:
        return f"(git unavailable: {e})"


def gather_workspace_snapshot(cwd: Path) -> Dict[str, str]:
    """Collect useful live context from the current git workspace."""
    snap: Dict[str, str] = {}
    snap["timestamp_utc"] = datetime.now(timezone.utc).isoformat()

    # Basic repo identity
    snap["git_remote"] = run_git(["config", "--get", "remote.origin.url"], cwd)
    snap["git_branch"] = run_git(["rev-parse", "--abbrev-ref", "HEAD"], cwd)
    snap["git_head"] = run_git(["rev-parse", "--short", "HEAD"], cwd)

    # Working tree state
    snap["git_status"] = run_git(["status", "--porcelain", "-b"], cwd)
    snap["git_diff_cached"] = run_git(["diff", "--cached", "--stat", "-U0"], cwd)[:4000]
    snap["git_diff"] = run_git(["diff", "--stat", "-U0"], cwd)[:4000]
    snap["recent_commits"] = run_git(["log", "--oneline", "-8"], cwd)

    # Try to find the skill dir (for provenance)
    snap["cwd"] = str(cwd)
    return snap


def build_package(data: Dict[str, Any], snapshot: Dict[str, str] | None) -> str:
    """Return the full Second Opinion Request Package as Markdown."""
    problem = data.get("problem", "").strip()
    context = data.get("context", "").strip()
    focus = data.get("focus", "").strip()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    lines = []
    lines.append("# Second Opinion Request Package")
    lines.append(f"**Generated**: {now}")
    lines.append(f"**Mode**: {data.get('mode', 'package')}")
    lines.append("")

    lines.append("## Problem")
    lines.append(problem or "(no problem statement provided)")
    lines.append("")

    if focus:
        lines.append("## Focus Area")
        lines.append(focus)
        lines.append("")

    lines.append("## Rich Context (provided by caller)")
    lines.append(context or "(no additional context)")
    lines.append("")

    if snapshot:
        lines.append("## Live Workspace Snapshot (captured at generation time)")
        lines.append("```")
        for k, v in snapshot.items():
            if v:
                lines.append(f"### {k}")
                lines.append(v[:3000] if len(v) > 3000 else v)
                lines.append("")
        lines.append("```")
        lines.append("")

    # Orientation Round prompt (critical — do not skip)
    lines.append("## Orientation Round Prompt (send this first)")
    lines.append("```")
    lines.append("You are receiving a Second Opinion Request Package.")
    lines.append("")
    lines.append("FIRST: Confirm or correct your understanding of the big-picture project and goal.")
    lines.append("Identify any missing context you need before giving a narrow technical judgment.")
    lines.append("Acknowledge explicitly when you are ready for the technical-opinion round.")
    lines.append("Do NOT jump to the narrow judgment until you have done the above.")
    lines.append("")
    lines.append("Project / task context is in the sections above (Problem + Rich Context + Workspace Snapshot).")
    if focus:
        lines.append(f"Pay special attention to the Focus Area: {focus}")
    lines.append("```")
    lines.append("")

    # Technical Judgment Round prompt
    lines.append("## Technical Judgment Round Prompt (send only after orientation succeeds)")
    lines.append("```")
    desired = data.get("desired_output") or (
        "Direct technical second opinion with assumptions, risks, and one concrete next action. "
        "Be explicit about whether you agree with the caller's proposed direction and why. "
        "If in a PGS-related repo, evaluate against deterministic PGS objects/invariants first."
    )
    lines.append(f"Desired output: {desired}")
    lines.append("")
    lines.append("Now give your narrow technical judgment on the Problem, using all context above.")
    lines.append("State your assumptions. Highlight risks. End with one concrete recommended next action.")
    lines.append("If this is a code or math claim, point to specific evidence or counter-examples.")
    lines.append("```")
    lines.append("")

    lines.append("## How to Use This Package in Grok")
    lines.append("1. Paste the entire package (or the two round prompts + context) into a fresh chat.")
    lines.append("2. Or feed the Orientation prompt to a `task` subagent first, then the Judgment round on resume.")
    lines.append("3. For even stronger isolation, send to a different model or another Grok session.")
    lines.append("")

    lines.append("---")
    lines.append("*This package was generated by the Grok port of the second-opinion skill.*")
    return "\n".join(lines)


def build_local_review_prompt(data: Dict[str, Any], snapshot: Dict[str, str] | None) -> str:
    """Return a prompt suitable for feeding directly to a verifier subagent right now."""
    problem = data.get("problem", "")
    context = data.get("context", "")
    focus = data.get("focus", "")

    prompt = f"""You are an expert technical reviewer acting as a second opinion.

The user has asked for a rigorous second look before the main agent proceeds.

PROBLEM / QUESTION:
{problem}

FOCUS (if any):
{focus or "(none specified)"}

CALLER-PROVIDED CONTEXT:
{context or "(none)"}
"""
    if snapshot:
        prompt += f"\n\nLIVE WORKSPACE SNAPSHOT (captured moments ago):\n{json.dumps(snapshot, indent=2)[:6000]}"

    prompt += """

INSTRUCTIONS:
1. First acknowledge the big picture (project goals, stakes, where we are).
2. Identify any missing context that would materially change your judgment.
3. Only after the above, give a direct technical second opinion.
4. Explicitly state: assumptions, risks, points of agreement/disagreement with the caller's current thinking, and one concrete next action.
5. If this touches prime-gap-structure or deterministic number theory, evaluate against PGS objects and invariants before classical probabilistic defaults.
6. End with a clear VERDICT line: VERDICT: AGREE | VERDICT: PARTIAL | VERDICT: DISAGREE | VERDICT: NEEDS_MORE_CONTEXT

Be precise, cite specific evidence from the supplied material, and do not hedge.
"""
    return prompt


def main() -> None:
    raw = sys.stdin.read()
    if not raw.strip():
        print("ERROR: No JSON input on stdin", file=sys.stderr)
        sys.exit(1)

    try:
        data: Dict[str, Any] = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}", file=sys.stderr)
        sys.exit(2)

    # Determine cwd for git snapshot (the workspace root the agent is in)
    cwd = Path.cwd()

    snapshot = None
    if data.get("include_snapshot", True):
        snapshot = gather_workspace_snapshot(cwd)

    mode = data.get("mode", "package").lower()

    if mode == "local-review":
        output = build_local_review_prompt(data, snapshot)
        print("=== LOCAL REVIEW PROMPT (feed this to a task subagent or fresh context) ===\n")
        print(output)
    else:
        # Default: full package for external or multi-round use
        package = build_package(data, snapshot)
        print(package)

    # Also emit a machine-readable summary on stderr for the agent to parse if desired
    summary = {
        "ok": True,
        "mode": mode,
        "problem_len": len(data.get("problem", "")),
        "context_len": len(data.get("context", "")),
        "snapshot_captured": snapshot is not None,
        "git_head": snapshot.get("git_head") if snapshot else None,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
    print(json.dumps(summary), file=sys.stderr)


if __name__ == "__main__":
    main()
