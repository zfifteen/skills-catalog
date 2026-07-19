#!/usr/bin/env python3
"""queue_pet_repairs.py — Grok-ported repair queuer (marks failed rows for re-generation in the manifest)."""

import argparse
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()
    run_dir = Path(args.run_dir).expanduser().resolve()
    jobs_file = run_dir / "imagegen-jobs.json"
    if not jobs_file.exists():
        raise SystemExit("no manifest")
    jobs = json.loads(jobs_file.read_text())
    # In full port: parse qa/review.json or validation, mark the minimal failing jobs back to "pending"
    for j in jobs.get("jobs", []):
        if j.get("status") == "recorded":  # simplistic; real logic inspects QA output
            pass  # would set failed rows to pending + attach repair context
    jobs_file.write_text(json.dumps(jobs, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"ok": True, "note": "Full port would parse QA output and re-open the smallest failing scope (row or frame)."}, indent=2))

if __name__ == "__main__":
    main()
