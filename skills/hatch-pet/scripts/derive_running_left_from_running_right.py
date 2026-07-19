#!/usr/bin/env python3
"""
derive_running_left_from_running_right.py — Grok-ported safe mirror derivation helper.

Only to be used after the parent agent has visually inspected running-right against the base
and confirmed (with --confirm-appropriate-mirror and a decision note) that horizontal mirror
preserves identity, prop handedness, markings, lighting semantics, and direction meaning.

Otherwise the left row must be generated normally via image_gen with the full grounded prompt.
"""

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--confirm-appropriate-mirror", action="store_true")
    parser.add_argument("--decision-note", default="")
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    if not args.confirm_appropriate_mirror:
        raise SystemExit("Must pass --confirm-appropriate-mirror with explicit decision note after visual inspection.")

    right_path = run_dir / "decoded" / "running-right.png"
    left_path = run_dir / "decoded" / "running-left.png"
    if not right_path.exists():
        raise SystemExit("running-right.png not yet recorded")

    with Image.open(right_path) as im:
        mirrored = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        left_path.parent.mkdir(parents=True, exist_ok=True)
        mirrored.save(left_path)

    # Update manifest
    jobs_file = run_dir / "imagegen-jobs.json"
    if jobs_file.exists():
        jobs = json.loads(jobs_file.read_text())
        for j in jobs.get("jobs", []):
            if j["id"] == "running-left":
                j["status"] = "derived_by_mirror"
                j["derived_from"] = "running-right"
                j["derived_at"] = datetime.now(timezone.utc).isoformat()
                j["decision_note"] = args.decision_note
        jobs_file.write_text(json.dumps(jobs, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"ok": True, "mirrored_to": str(left_path), "note": args.decision_note}, indent=2))

if __name__ == "__main__":
    main()
