#!/usr/bin/env python3
"""
image_gen.py — Grok-ported fallback CLI for explicit OpenAI image generation/editing.

From the original Codex imagegen skill. 

**Grok Primary Path:** Use the native `image_gen` and `image_edit` tools (and `video_gen`) for almost all work. 
This script is provided **only** for users who explicitly request the OpenAI GPT-Image / DALL·E path (e.g., for model comparison, specific features, or environments without Grok vision tools).

It is intentionally a thin, policy-enforcing wrapper. Full original implementation (with advanced batching, downscaling, etc.) lives in the Codex source if needed.

Subcommands (when used explicitly):
  generate --prompt "..." [--out ...]
  edit --image /path --prompt "..." 
  generate-batch ...

Requires OPENAI_API_KEY for live calls.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Optional

DEFAULT_OUTPUT = "output/imagegen/output.png"

def _die(msg: str, code: int = 1):
    print(f"Error: {msg}", file=sys.stderr)
    raise SystemExit(code)

def _warn(msg: str):
    print(f"Warning: {msg}", file=sys.stderr)

def _check_key():
    if not os.environ.get("OPENAI_API_KEY"):
        _die("OPENAI_API_KEY not set. Export it for OpenAI fallback mode. (Grok native image_gen does not require it.)")

def cmd_generate(args):
    _check_key()
    print("[image_gen fallback] generate mode (OpenAI path)")
    print(f"Prompt: {args.prompt[:120]}..." if len(args.prompt) > 120 else f"Prompt: {args.prompt}")
    print(f"Model: {args.model}")
    print("Note: In a full Grok environment, prefer the built-in image_gen tool instead of this CLI.")
    print(f"Would write to: {args.out or DEFAULT_OUTPUT}")
    # In a real port with openai installed + key, the original client code would go here.
    # For this production Grok port we keep the policy surface and a working entry point.
    print("To execute real calls, install 'openai' and extend this script with the original Codex logic or call the OpenAI Images API directly.")

def cmd_edit(args):
    _check_key()
    print("[image_gen fallback] edit mode")
    print(f"Image: {args.image}")
    print(f"Prompt: {args.prompt[:100]}...")
    print("Prefer Grok image_edit tool for in-conversation edits.")

def cmd_generate_batch(args):
    print("[image_gen fallback] batch mode (see original Codex scripts/image_gen.py for full implementation)")
    _die("Batch not fully wired in this minimal Grok port. Use native image_gen in a loop or the full Codex script.", 2)

def main():
    parser = argparse.ArgumentParser(description="Grok-ported imagegen fallback (OpenAI explicit only)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    g = sub.add_parser("generate")
    g.add_argument("--prompt", required=True)
    g.add_argument("--model", default="gpt-image-1.5")
    g.add_argument("--out", default=None)
    g.add_argument("--force", action="store_true")
    g.set_defaults(func=cmd_generate)

    e = sub.add_parser("edit")
    e.add_argument("--image", required=True)
    e.add_argument("--prompt", required=True)
    e.add_argument("--out", default=None)
    e.set_defaults(func=cmd_edit)

    b = sub.add_parser("generate-batch")
    b.add_argument("--prompts-file")
    b.set_defaults(func=cmd_generate_batch)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
