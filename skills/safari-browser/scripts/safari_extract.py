#!/usr/bin/env python3
"""Extract visible page text from Safari (authenticated session).

Default: fast AppleScript innerText path (~13s total on Grok shares).
Fallback: Safari WebDriver when --method webdriver is requested.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
FAST = SCRIPT_DIR / "safari_extract_fast.py"


def extract_webdriver(url: str, wait: int, scroll_rounds: int, port: int) -> str:
    import time

    subprocess.run(["pkill", "-f", f"safaridriver --port {port}"], stderr=subprocess.DEVNULL)
    time.sleep(0.3)
    proc = subprocess.Popen(
        ["safaridriver", "--port", str(port)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(1.5)
    try:
        from selenium import webdriver
        from selenium.webdriver.safari.options import Options

        opts = Options()
        opts.port = port
        driver = webdriver.Safari(options=opts)
        driver.set_page_load_timeout(90)
        driver.get(url)
        time.sleep(wait)
        for _ in range(scroll_rounds):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.2)
        return driver.execute_script("return document.body.innerText")
    finally:
        try:
            driver.quit()
        except Exception:
            pass
        proc.terminate()


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract page text via Safari")
    parser.add_argument("url")
    parser.add_argument("--output", "-o")
    parser.add_argument("--wait", type=int, default=12)
    parser.add_argument("--scroll-rounds", type=int, default=6)
    parser.add_argument("--port", type=int, default=4445)
    parser.add_argument(
        "--method",
        choices=("fast", "webdriver"),
        default="fast",
        help="fast=AppleScript innerText (default); webdriver=safaridriver+Selenium",
    )
    args = parser.parse_args()

    if args.method == "fast":
        cmd = [sys.executable, str(FAST), args.url, "--wait", str(args.wait)]
        if args.output:
            cmd.extend(["--output", args.output])
        return subprocess.call(cmd)

    try:
        text = extract_webdriver(args.url, args.wait, args.scroll_rounds, args.port)
    except Exception as exc:
        print(
            "Safari WebDriver failed. Enable Safari → Developer → "
            "'Allow remote automation', or use default --method fast.\n"
            f"Error: {exc}",
            file=sys.stderr,
        )
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