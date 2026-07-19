#!/usr/bin/env python3
"""
make_contact_sheet.py — Simple contact sheet generator for hatch-pet (Grok port).
"""

import argparse
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ATLAS = {"columns": 8, "rows": 9, "cell_width": 192, "cell_height": 208}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--atlas", default=None)
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    atlas_path = Path(args.atlas) if args.atlas else (run_dir / "final" / "spritesheet.png")

    if not atlas_path.exists():
        raise SystemExit(f"Atlas not found: {atlas_path}")

    atlas = Image.open(atlas_path).convert("RGBA")

    # Create a downscaled contact sheet (2x2 grid of the atlas for overview + rows)
    # For simplicity, create a clean tiled overview
    scale = 0.5
    small = atlas.resize(
        (int(atlas.width * scale), int(atlas.height * scale)),
        Image.Resampling.LANCZOS
    )

    contact = Image.new("RGBA", (small.width + 40, small.height + 80), (255, 255, 255, 255))
    contact.paste(small, (20, 60))

    draw = ImageDraw.Draw(contact)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
    except Exception:
        font = ImageFont.load_default()

    draw.text((20, 10), f"Hatch Pet Contact Sheet — {run_dir.name}", fill=(30, 30, 30), font=font)

    out_path = run_dir / "qa" / "contact-sheet.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    contact.save(out_path)

    print(json.dumps({
        "ok": True,
        "contact_sheet": str(out_path)
    }, indent=2))


if __name__ == "__main__":
    main()
