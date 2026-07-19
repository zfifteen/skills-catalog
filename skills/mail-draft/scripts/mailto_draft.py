#!/usr/bin/env python3
"""Open a prefilled email draft in the user's default mail client (macOS).

Grok port of the Codex mail-draft helper (originally at ~/.codex/tools/mailto_draft.py
and invoked via the thin mail-draft zsh wrapper).

This is the preferred implementation for the "mail-draft" skill in Grok environments.
It produces a mailto: URL and uses AppleScript (osascript) to tell the default Mail
app to open a draft window pre-filled with the provided fields.

No external Python dependencies. macOS only (uses osascript + open location).

Usage (via Grok run_terminal_cmd):
  python3 "<SKILL_DIR>/scripts/mailto_draft.py" --to "user@example.com" --subject "Hello" --body "Body here..."
  python3 ... --body-file /tmp/message.txt --to "..." --subject "..."

  --dry-run : print the mailto URL only, do not open Mail.

Supports --cc, --bcc, multiline bodies via --body or --body-file (or stdin).

Original behavior preserved exactly.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlencode, quote


def read_body(args: argparse.Namespace) -> str:
    if args.body_file:
        return Path(args.body_file).read_text(encoding="utf-8")
    if args.body is not None:
        return args.body
    if not sys.stdin.isatty():
        return sys.stdin.read()
    return ""


def build_mailto(
    recipient: str = "",
    subject: str = "",
    body: str = "",
    cc: str = "",
    bcc: str = "",
) -> str:
    query_params = {
        key: value
        for key, value in {
            "subject": subject,
            "body": body,
            "cc": cc,
            "bcc": bcc,
        }.items()
        if value
    }
    query = urlencode(query_params, quote_via=quote)
    if query:
        return f"mailto:{recipient}?{query}"
    return f"mailto:{recipient}"


def open_mailto(url: str) -> None:
    # Use AppleScript to open the mailto: URL in the default handler (Mail.app)
    script = f'open location "{url}"'
    subprocess.run(["osascript", "-e", script], check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Open a Mail draft with recipient, subject, and body (macOS)."
    )
    parser.add_argument("--to", default="", help="Recipient email address")
    parser.add_argument("--cc", default="", help="CC recipient list")
    parser.add_argument("--bcc", default="", help="BCC recipient list")
    parser.add_argument("--subject", default="", help="Email subject")
    parser.add_argument("--body", help="Email body text")
    parser.add_argument(
        "--body-file",
        help="Read the email body from a UTF-8 text file instead of --body",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the mailto URL without opening a draft window",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    body = read_body(args)
    url = build_mailto(
        recipient=args.to,
        subject=args.subject,
        body=body,
        cc=args.cc,
        bcc=args.bcc,
    )
    if not args.dry_run:
        try:
            open_mailto(url)
        except subprocess.CalledProcessError as e:
            print(f"Failed to open mailto URL via osascript: {e}", file=sys.stderr)
            print(f"mailto URL was: {url}", file=sys.stderr)
            return 1
    print(url)
    return 0


if __name__ == "__main__":
    sys.exit(main())
