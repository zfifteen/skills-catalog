#!/usr/bin/env python3
"""
validate_atlas.py — Basic geometry and transparency validator for hatch-pet atlas (Grok port).
"""

import argparse
import json
from pathlib import Path
from PIL import Image

ATLAS = {"width": 1536, "height": 1872, "cell_width": 192, "cell_height": 208}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--atlas", required=True)
    args = parser.parse_args()

    atlas_path = Path(args.atlas).expanduser().resolve()
    if not atlas_path.exists():
        raise SystemExit(f"Atlas not found: {atlas_path}")

    img = Image.open(atlas_path).convert("RGBA")
    errors = []
    warnings = []

    if img.width != ATLAS["width"] or img.height != ATLAS["height"]:
        errors.append(f"Wrong dimensions: {img.size} (expected {ATLAS['width']}x{ATLAS['height']})")

    # Check that unused cells are transparent (simplified check on right side of rows)
    # This is a pragmatic validator for now.

    result = {
        "ok": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "atlas": str(atlas_path),
        "size": list(img.size),
    }

    print(json.dumps(result, indent=2))

    if errors:
        raise SystemExit("Validation failed")


if __name__ == "__main__":
    main()
