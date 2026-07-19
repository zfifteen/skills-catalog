#!/usr/bin/env python3
"""Convert grok-share JSON payload to Markdown."""
import json
import sys


def main() -> None:
    data = json.load(sys.stdin)
    lines = [
        f"# {data['title']}",
        "",
        f"**Source:** {data['url']}",
        f"**Extracted:** {data['extracted_at']}",
        f"**Turns:** {data['turn_count']}",
        "",
        "---",
        "",
    ]
    for i, turn in enumerate(data["turns"], start=1):
        role = "User" if turn["role"] == "user" else "Grok"
        lines.extend([f"## Turn {i} — {role}", "", turn["text"], ""])
    sys.stdout.write("\n".join(lines).rstrip() + "\n")


if __name__ == "__main__":
    main()