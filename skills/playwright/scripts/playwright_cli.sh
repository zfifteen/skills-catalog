#!/usr/bin/env bash
# playwright_cli.sh — Grok-ported wrapper for @playwright/cli
# Original from Codex playwright skill. Adapted for general Grok environments.
# Uses npx --yes to run without requiring global install of playwright-cli.
#
# Usage (from Grok via run_terminal_cmd):
#   bash /absolute/path/to/this/skills/ported-from-codex/playwright/scripts/playwright_cli.sh open https://example.com --headed
#   ... or with full session management
#
# The script prefers an explicit --session if provided; otherwise honors PLAYWRIGHT_CLI_SESSION env var.
set -euo pipefail

if ! command -v npx >/dev/null 2>&1; then
  echo "Error: npx is required but not found on PATH." >&2
  echo "Install Node.js/npm first (provides npx), then retry." >&2
  exit 1
fi

has_session_flag="false"
for arg in "$@"; do
  case "$arg" in
    --session|--session=*)
      has_session_flag="true"
      break
      ;;
  esac
done

cmd=(npx --yes --package @playwright/cli playwright-cli)
if [[ "${has_session_flag}" != "true" && -n "${PLAYWRIGHT_CLI_SESSION:-}" ]]; then
  cmd+=(--session "${PLAYWRIGHT_CLI_SESSION}")
fi
cmd+=("$@")

exec "${cmd[@]}"
