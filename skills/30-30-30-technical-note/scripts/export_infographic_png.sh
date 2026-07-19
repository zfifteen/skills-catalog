#!/usr/bin/env bash
# Export infographic.svg → infographic.png (same directory, 2× scale).
set -euo pipefail

SVG="${1:?Usage: export_infographic_png.sh <path/to/infographic.svg>}"
DIR="$(dirname "$SVG")"
PNG="${DIR}/infographic.png"

if [[ ! -f "$SVG" ]]; then
  echo "Missing SVG: $SVG" >&2
  exit 1
fi

if command -v rsvg-convert >/dev/null 2>&1; then
  rsvg-convert -w 3200 "$SVG" -o "$PNG"
elif command -v magick >/dev/null 2>&1; then
  magick -density 192 -background none "$SVG" -resize 3200x "$PNG"
elif command -v convert >/dev/null 2>&1; then
  convert -density 192 -background none "$SVG" -resize 3200x "$PNG"
else
  echo "Need rsvg-convert or ImageMagick (magick/convert)." >&2
  exit 1
fi

echo "Wrote $PNG ($(wc -c < "$PNG" | tr -d ' ') bytes)"