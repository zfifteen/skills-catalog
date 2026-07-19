#!/usr/bin/env python3
"""
record_imagegen_result.py — Grok-ported ingest helper for hatch-pet.

After a successful image_gen (or imagegen skill) call for a job (base or row),
this script copies the selected output PNG into the exact decoded/ path
expected by the rest of the deterministic pipeline and updates imagegen-jobs.json
with source metadata and timestamp.

Grok adaptation: The agent selects the best generated image from the native
image_gen tool output (or the imagegen skill return), then invokes this script
with the absolute path to that chosen file.

Usage:
  python3 <SKILL_DIR>/scripts/record_imagegen_result.py \
    --run-dir /abs/path/to/run \
    --job-id base \
    --source /abs/path/to/chosen/ig_XXXX.png
"""

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--source", required=True)
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    source = Path(args.source).expanduser().resolve()
    jobs_file = run_dir / "imagegen-jobs.json"

    if not jobs_file.exists():
        raise SystemExit(f"imagegen-jobs.json not found in {run_dir}")

    jobs = json.loads(jobs_file.read_text(encoding="utf-8"))
    job = next((j for j in jobs["jobs"] if j["id"] == args.job_id), None)
    if not job:
        raise SystemExit(f"Job {args.job_id} not found in manifest")

    decoded_path = run_dir / job["output_path"]
    decoded_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, decoded_path)

    job["status"] = "recorded"
    job["recorded_at"] = datetime.now(timezone.utc).isoformat()
    job["source_path"] = str(source)
    job["source_size"] = source.stat().st_size

    jobs_file.write_text(json.dumps(jobs, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "ok": True,
        "job_id": args.job_id,
        "decoded": str(decoded_path),
        "source": str(source)
    }, indent=2))


if __name__ == "__main__":
    main()
