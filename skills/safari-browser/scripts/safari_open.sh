#!/usr/bin/env bash
# safari_open.sh — Open a URL in the user's authenticated Safari session.
set -euo pipefail

URL="${1:-}"
if [[ -z "$URL" ]]; then
  echo "Usage: safari_open.sh <url>" >&2
  exit 1
fi

osascript <<APPLESCRIPT
tell application "Safari"
    activate
    if (count of windows) = 0 then
        make new document
    end if
    set URL of current tab of front window to "$URL"
end tell
APPLESCRIPT

echo "Opened in Safari: $URL" >&2