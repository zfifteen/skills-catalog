#!/usr/bin/env python3
"""Fast Safari page-text extraction via AppleScript do JavaScript (happy path).

Proven on x.com/i/grok/share/ pages with authenticated Safari:
  open URL -> wait ~12s -> chunk document.body.innerText -> clean text in <2s.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
OPEN_SH = SCRIPT_DIR / "safari_open.sh"
CHUNK_SIZE = 5000
DEFAULT_WAIT = 12


def run_applescript_js(code: str) -> str:
    escaped = code.replace("\\", "\\\\").replace('"', '\\"')
    script = (
        f'tell application "Safari" to return do JavaScript "{escaped}" '
        "in current tab of front window"
    )
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        err = (result.stderr or result.stdout or "unknown AppleScript error").strip()
        if "Allow JavaScript from Apple Events" in err:
            raise RuntimeError(
                "Enable Safari → Developer → 'Allow JavaScript from Apple Events', then retry."
            )
        raise RuntimeError(err)
    return result.stdout


def open_in_safari(url: str) -> None:
    subprocess.run(["bash", str(OPEN_SH), url], check=True)


def extract_text(wait: int = DEFAULT_WAIT, chunk_size: int = CHUNK_SIZE) -> str:
    time.sleep(wait)
    length_raw = run_applescript_js("String(document.body.innerText.length)")
    length = int(float(length_raw.strip()))
    chunks: list[str] = []
    for start in range(0, length, chunk_size):
        end = start + chunk_size
        chunk = run_applescript_js(f"document.body.innerText.slice({start},{end})")
        chunks.append(chunk)
    return "".join(chunks)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fast Safari text extraction (AppleScript innerText, happy path)"
    )
    parser.add_argument("url")
    parser.add_argument("--output", "-o", help="Write text to this file")
    parser.add_argument("--wait", type=int, default=DEFAULT_WAIT, help="Seconds after navigation")
    parser.add_argument(
        "--no-open",
        action="store_true",
        help="Skip navigation; read the current Safari tab",
    )
    args = parser.parse_args()

    try:
        if not args.no_open:
            open_in_safari(args.url)
        text = extract_text(wait=args.wait)
    except Exception as exc:
        print(f"Safari fast extract failed: {exc}", file=sys.stderr)
        return 1

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        print(f"Wrote {len(text)} chars to {out}", file=sys.stderr)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())