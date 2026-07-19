#!/usr/bin/env bash
# safari_read_page.sh — Happy path: open URL in Safari, extract clean innerText.
# Usage: safari_read_page.sh <url> [--output PATH] [--wait SECONDS]
set -euo pipefail

URL=""
OUTPUT=""
WAIT=12

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output|-o)
      OUTPUT="${2:-}"
      shift 2
      ;;
    --wait)
      WAIT="${2:-12}"
      shift 2
      ;;
    http*)
      URL="$1"
      shift
      ;;
    *)
      echo "Unknown arg: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$URL" ]]; then
  echo "Usage: safari_read_page.sh <url> [--output PATH] [--wait SECONDS]" >&2
  exit 1
fi

FAST="$HOME/.grok/skills/safari-browser/scripts/safari_extract_fast.py"
ARGS=( "$URL" "--wait" "$WAIT" )
if [[ -n "$OUTPUT" ]]; then
  ARGS+=( "--output" "$OUTPUT" )
fi

exec python3 "$FAST" "${ARGS[@]}"