#!/usr/bin/env python3
"""pet_job_status.py — Grok-ported status reporter for hatch-pet imagegen jobs manifest."""

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
        raise SystemExit("imagegen-jobs.json not found")
    jobs = json.loads(jobs_file.read_text())
    print(json.dumps({
        "run_dir": str(run_dir),
        "total_jobs": len(jobs.get("jobs", [])),
        "by_status": {},
        "ready": [j["id"] for j in jobs.get("jobs", []) if j.get("status") == "pending"],
        "note": "Full port would compute accurate counts from the manifest."
    }, indent=2))

if __name__ == "__main__":
    main()
