#!/usr/bin/env bash
# read_share.sh — Extract conversation text from a public Grok share URL.
# Requires: Node.js/npx (uses @playwright/cli via npx --yes).
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: read_share.sh <grok-share-url> [--json] [--output PATH]

Read a public Grok shared conversation (grok.com/share/... or x.com/i/grok/share/...).

Options:
  --json          Emit structured JSON instead of Markdown
  --output PATH   Write output to PATH (default: stdout)
  -h, --help      Show this help

Examples:
  read_share.sh 'https://grok.com/share/bGVnYWN5_...'
  read_share.sh 'https://x.com/i/grok/share/...' --output transcript.md
EOF
}

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Error: '$1' is required but not found on PATH." >&2
    exit 1
  fi
}

URL=""
FORMAT="markdown"
OUTPUT=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      usage
      exit 0
      ;;
    --json)
      FORMAT="json"
      shift
      ;;
    --output)
      OUTPUT="${2:-}"
      if [[ -z "$OUTPUT" ]]; then
        echo "Error: --output requires a path." >&2
        exit 1
      fi
      shift 2
      ;;
    http*)
      URL="$1"
      shift
      ;;
    *)
      echo "Error: unknown argument '$1'" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "$URL" ]]; then
  echo "Error: grok share URL is required." >&2
  usage >&2
  exit 1
fi

if [[ ! "$URL" =~ ^https://(grok\.com/share/|x\.com/i/grok/share/) ]]; then
  echo "Error: URL must be https://grok.com/share/... or https://x.com/i/grok/share/..." >&2
  exit 1
fi

require_cmd npx
require_cmd python3

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
EXTRACT_JS="$(tr '\n' ' ' <"$SCRIPT_DIR/extract.js" | sed 's/  */ /g')"
SESSION="grok-share-$$"
WAIT_SECONDS="${GROK_SHARE_WAIT_SECONDS:-8}"
POLL_ATTEMPTS="${GROK_SHARE_POLL_ATTEMPTS:-15}"

playwright_cli() {
  if [[ -n "${PWCLI:-}" && -x "$PWCLI" ]]; then
    "$PWCLI" --session "$SESSION" "$@"
  else
    npx --yes --package @playwright/cli playwright-cli --session "$SESSION" "$@"
  fi
}

cleanup() {
  playwright_cli close >/dev/null 2>&1 || true
}
trap cleanup EXIT

playwright_cli open "$URL" >/dev/null
sleep "$WAIT_SECONDS"

RAW_JSON=""
for _ in $(seq 1 "$POLL_ATTEMPTS"); do
  if RAW_JSON="$(
    playwright_cli eval "$EXTRACT_JS" 2>/dev/null \
      | python3 "$SCRIPT_DIR/parse_playwright_result.py"
  )"; then
    break
  fi
  RAW_JSON=""
  sleep 1
done

if [[ -z "$RAW_JSON" ]]; then
  echo "Error: failed to extract conversation content from $URL" >&2
  echo "Hint: retry with GROK_SHARE_WAIT_SECONDS=12 GROK_SHARE_POLL_ATTEMPTS=20" >&2
  exit 1
fi

if [[ "$FORMAT" == "json" ]]; then
  FINAL="$RAW_JSON"
else
  FINAL="$(printf '%s' "$RAW_JSON" | python3 "$SCRIPT_DIR/to_markdown.py")"
fi

if [[ -n "$OUTPUT" ]]; then
  mkdir -p "$(dirname "$OUTPUT")"
  printf '%s' "$FINAL" >"$OUTPUT"
  echo "Wrote ${FORMAT} to $OUTPUT" >&2
else
  printf '%s' "$FINAL"
fi