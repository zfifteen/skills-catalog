#!/usr/bin/env python3
"""
finalize_pet_run.py — Real final assembly, validation, and packaging for hatch-pet (Grok port).

This version actually calls the supporting scripts (compose, validate, contact sheet, etc.)
instead of writing placeholders.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def run_script(script_name: str, args: list[str], cwd: Path) -> dict:
    """Run a helper script and return parsed JSON if possible."""
    script_path = cwd / "scripts" / script_name
    if not script_path.exists():
        return {"ok": False, "error": f"Script not found: {script_path}"}

    cmd = [sys.executable, str(script_path)] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            return {"ok": False, "error": result.stderr.strip() or result.stdout.strip()}
        # Try to parse JSON from last line
        for line in reversed(result.stdout.strip().splitlines()):
            if line.strip().startswith("{"):
                return json.loads(line)
        return {"ok": True, "raw_output": result.stdout.strip()}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    scripts_dir = Path(__file__).parent

    print(f"[hatch-pet] Finalizing run at {run_dir}")

    final_dir = run_dir / "final"
    qa_dir = run_dir / "qa"
    final_dir.mkdir(parents=True, exist_ok=True)
    qa_dir.mkdir(parents=True, exist_ok=True)

    results = {}

    # 1. Compose atlas
    compose_result = run_script("compose_atlas.py", ["--run-dir", str(run_dir)], scripts_dir.parent)
    results["compose"] = compose_result
    if compose_result.get("ok"):
        atlas_path = Path(compose_result.get("atlas", final_dir / "spritesheet.png"))
    else:
        atlas_path = final_dir / "spritesheet.png"

    # 2. Validate
    validate_result = run_script("validate_atlas.py", ["--atlas", str(atlas_path)], scripts_dir.parent)
    results["validate"] = validate_result

    # 3. Contact sheet
    contact_result = run_script("make_contact_sheet.py", ["--run-dir", str(run_dir), "--atlas", str(atlas_path)], scripts_dir.parent)
    results["contact_sheet"] = contact_result

    # 4. Package (basic pet.json for now)
    try:
        pet_request = json.loads((run_dir / "pet_request.json").read_text())
        pet_id = pet_request.get("pet_id", run_dir.name)
    except Exception:
        pet_id = run_dir.name

    package_dir = Path.home() / ".grok-pets" / pet_id
    package_dir.mkdir(parents=True, exist_ok=True)

    # Copy atlas as webp/png
    webp_path = package_dir / "spritesheet.webp"
    try:
        from PIL import Image
        Image.open(atlas_path).save(webp_path, "WEBP", quality=90)
    except Exception:
        import shutil
        shutil.copy2(atlas_path, package_dir / "spritesheet.png")

    (package_dir / "pet.json").write_text(json.dumps({
        "id": pet_id,
        "displayName": pet_id.replace("-", " ").title(),
        "description": "Hatched with Grok + hatch-pet skill",
        "spritesheetPath": "spritesheet.webp"
    }, indent=2), encoding="utf-8")

    results["package"] = {
        "ok": True,
        "package_dir": str(package_dir),
        "pet_json": str(package_dir / "pet.json")
    }

    # Write summary
    summary = {
        "finalized_at": datetime.now(timezone.utc).isoformat(),
        "run_dir": str(run_dir),
        "results": results,
    }
    (qa_dir / "run-summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(json.dumps({
        "ok": True,
        "run_dir": str(run_dir),
        "package_dir": str(package_dir),
        "results_summary": {k: v.get("ok", False) for k, v in results.items()}
    }, indent=2))


if __name__ == "__main__":
    main()
