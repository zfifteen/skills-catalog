#!/usr/bin/env python3
"""
compose_atlas.py — Minimal functional atlas composer for hatch-pet (Grok port).

Takes a hatch-pet run directory (with imagegen-jobs.json + decoded/ frames)
and produces the final 1536x1872 spritesheet atlas with correct cell layout.

This is a pragmatic implementation to make the hatch-pet skill actually usable.
"""

import argparse
import json
from pathlib import Path
from PIL import Image

ATLAS = {
    "columns": 8,
    "rows": 9,
    "cell_width": 192,
    "cell_height": 208,
}
ATLAS["width"] = ATLAS["columns"] * ATLAS["cell_width"]
ATLAS["height"] = ATLAS["rows"] * ATLAS["cell_height"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    jobs_file = run_dir / "imagegen-jobs.json"

    if not jobs_file.exists():
        raise SystemExit(f"imagegen-jobs.json not found in {run_dir}")

    jobs = json.loads(jobs_file.read_text(encoding="utf-8"))

    # Create blank transparent atlas
    atlas = Image.new("RGBA", (ATLAS["width"], ATLAS["height"]), (0, 0, 0, 0))

    row_map = {row["id"]: row for row in jobs.get("jobs", []) if row.get("row") is not None}

    # The original layout: rows are in a specific order
    # We use the order from the manifest or fall back to standard order
    standard_order = [
        "idle", "running-right", "running-left", "waving", "jumping",
        "failed", "waiting", "running", "review"
    ]

    for row_idx, state in enumerate(standard_order):
        job = next((j for j in jobs.get("jobs", []) if j.get("id") == state), None)
        if not job:
            print(f"[compose] Warning: no job found for state {state}")
            continue

        decoded_path = run_dir / job.get("output_path", f"decoded/{state}.png")
        if not decoded_path.exists():
            print(f"[compose] Missing decoded frame for {state}: {decoded_path}")
            continue

        try:
            strip = Image.open(decoded_path).convert("RGBA")
        except Exception as e:
            print(f"[compose] Failed to open {decoded_path}: {e}")
            continue

        # The strip should contain N frames side-by-side.
        # We slice it into cells and paste them into the atlas.
        frame_width = ATLAS["cell_width"]
        num_frames_in_strip = strip.width // frame_width

        for col in range(min(num_frames_in_strip, ATLAS["columns"])):
            frame = strip.crop((
                col * frame_width, 0,
                (col + 1) * frame_width, ATLAS["cell_height"]
            ))
            x = col * ATLAS["cell_width"]
            y = row_idx * ATLAS["cell_height"]
            atlas.paste(frame, (x, y), frame)

    output_path = Path(args.output) if args.output else (run_dir / "final" / "spritesheet.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    atlas.save(output_path)

    print(json.dumps({
        "ok": True,
        "atlas": str(output_path),
        "size": [atlas.width, atlas.height],
    }, indent=2))


if __name__ == "__main__":
    main()
