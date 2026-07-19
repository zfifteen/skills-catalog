#!/usr/bin/env python3
"""
install_skill.py — Functional helper for the Grok skill-installer skill.

Subcommands:
  validate <skill-dir>          Check that <skill-dir> looks like a valid Grok skill.
  install <source> <target>     (future) Copy/validate in one shot.
  diff <a> <b>                  Show structural diff between two skill dirs.
  receipt <skill-dir>           Print the install receipt if present.

The script is deliberately self-contained (stdlib only + minimal subprocess for git/chmod).
It is safe to run via the agent's run_terminal_cmd tool.

Exit codes:
  0 success / valid
  1 validation failed (details on stdout)
  2 usage / arg error
  3 I/O or unexpected error
"""

import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
REQUIRED_FRONTMATTER = {"name", "description"}


def load_frontmatter(skill_dir: Path) -> Tuple[Dict[str, Any], str]:
    """Return (parsed_frontmatter_dict, raw_yaml_text) or raise on error."""
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise FileNotFoundError(f"SKILL.md not found in {skill_dir}")

    text = skill_md.read_text(encoding="utf-8", errors="replace")
    m = FRONTMATTER_RE.match(text)
    if not m:
        raise ValueError("No YAML frontmatter (--- ... ---) found at start of SKILL.md")

    raw = m.group(1)
    # Very small YAML parser for the keys we care about (name, description, etc.)
    data: Dict[str, Any] = {}
    current_key = None
    for line in raw.splitlines():
        if ":" in line and not line.strip().startswith("-"):
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            data[key] = val
            current_key = key
        elif current_key and line.strip().startswith((">", "|")):
            # crude multi-line support
            data[current_key] = data.get(current_key, "") + "\n" + line.strip()
    return data, raw


def validate_skill(skill_dir: Path) -> List[str]:
    """Return list of error/warning strings. Empty list = clean."""
    errors: List[str] = []
    warnings: List[str] = []

    if not skill_dir.is_dir():
        errors.append(f"Not a directory: {skill_dir}")
        return errors

    name = skill_dir.name
    if not re.match(r"^[a-z0-9][a-z0-9-]{1,62}[a-z0-9]$", name):
        warnings.append(f"Directory name '{name}' does not look like a recommended skill name (lowercase, hyphens, 3-64 chars)")

    try:
        fm, raw = load_frontmatter(skill_dir)
    except Exception as e:
        errors.append(f"Frontmatter error: {e}")
        return errors

    missing = REQUIRED_FRONTMATTER - set(fm.keys())
    if missing:
        errors.append(f"Missing required frontmatter keys: {missing}")

    if "name" in fm and fm["name"] != name:
        warnings.append(f"frontmatter name: '{fm['name']}' != directory name '{name}' (some loaders are strict)")

    if "description" in fm and len(str(fm["description"]).strip()) < 20:
        warnings.append("description is very short (<20 chars) — auto-invocation may be weak")

    # Check for scripts/ that are declared or present
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists():
        for py in scripts_dir.glob("*.py"):
            if not py.read_text(encoding="utf-8", errors="replace")[:2] == "#!":
                warnings.append(f"Script {py.name} has no shebang — agent may not know how to run it directly")
        for sh in list(scripts_dir.glob("*.sh")) + list(scripts_dir.glob("*.mjs")):
            warnings.append(f"Non-Python script found: {sh.name} (ensure it is executable and agent can invoke it)")

    # Look for obvious dangerous patterns in SKILL.md (very lightweight)
    full_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8", errors="replace").lower()
    if "os.system" in full_text or "subprocess.call" in full_text or "eval(" in full_text:
        warnings.append("SKILL.md contains patterns that look like shell execution — review before installing from untrusted source")

    if warnings:
        errors.extend(["WARNING: " + w for w in warnings])

    return errors


def cmd_validate(args: List[str]) -> int:
    if len(args) != 1:
        print("Usage: install_skill.py validate <skill-directory>", file=sys.stderr)
        return 2
    target = Path(args[0]).expanduser().resolve()
    errs = validate_skill(target)
    if errs:
        for e in errs:
            print(e)
        return 1
    print(f"VALID: {target} looks like a well-formed Grok skill.")
    return 0


def cmd_diff(args: List[str]) -> int:
    if len(args) != 2:
        print("Usage: install_skill.py diff <dir-a> <dir-b>", file=sys.stderr)
        return 2
    a, b = (Path(x).expanduser().resolve() for x in args)
    # Very simple structural diff
    def tree(p: Path) -> List[str]:
        return sorted(str(pp.relative_to(p)) for pp in p.rglob("*") if pp.is_file())

    ta, tb = set(tree(a)), set(tree(b))
    only_a = sorted(ta - tb)
    only_b = sorted(tb - ta)
    common = sorted(ta & tb)

    print(f"Only in {a.name}:")
    for x in only_a:
        print(f"  - {x}")
    print(f"\nOnly in {b.name}:")
    for x in only_b:
        print(f"  - {x}")
    print(f"\nCommon files ({len(common)}):")
    for x in common[:30]:
        print(f"  = {x}")
    if len(common) > 30:
        print(f"  ... and {len(common)-30} more")
    return 0


def cmd_receipt(args: List[str]) -> int:
    if len(args) != 1:
        print("Usage: install_skill.py receipt <installed-skill-dir>", file=sys.stderr)
        return 2
    d = Path(args[0]).expanduser().resolve()
    receipt = d / "installed-from.json"
    if not receipt.exists():
        print("No receipt found (skill was not installed by this helper or receipt was deleted).")
        return 1
    print(receipt.read_text())
    return 0


def cmd_install(args: List[str]) -> int:
    # Placeholder for a full one-shot installer (the SKILL.md orchestrates most of the work via agent tools)
    print("The full install flow is orchestrated by the skill-installer SKILL.md using the agent's write / MCP / run_terminal_cmd tools.")
    print("This subcommand is a stub for future direct CLI use or CI.")
    print("For now, run 'validate' first, then let the skill do the copy.")
    return 0


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        print("Subcommands: validate, diff, receipt, install")
        sys.exit(2)

    sub = sys.argv[1]
    rest = sys.argv[2:]

    if sub == "validate":
        sys.exit(cmd_validate(rest))
    elif sub == "diff":
        sys.exit(cmd_diff(rest))
    elif sub == "receipt":
        sys.exit(cmd_receipt(rest))
    elif sub == "install":
        sys.exit(cmd_install(rest))
    else:
        print(f"Unknown subcommand: {sub}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
