#!/usr/bin/env python3
"""Extract JSON from playwright-cli eval stdout."""
import json
import re
import sys


def main() -> int:
    text = sys.stdin.read()
    match = re.search(r"### Result\s*\n(\{.*?\})\s*\n###", text, re.DOTALL)
    if not match:
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1:
            return 1
        payload = text[start : end + 1]
    else:
        payload = match.group(1)

    try:
        obj = json.loads(payload)
    except json.JSONDecodeError:
        return 1

    if obj.get("error"):
        return 1
    if obj.get("turn_count", 0) < 1:
        return 1

    json.dump(obj, sys.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())