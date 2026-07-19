---
name: hatch-pet
description: >
  Create, repair, validate, preview, and package Codex-compatible (or compatible digital-pet runtime) animated 8x9 spritesheet pets (192x208 cells, 1536x1872 atlas) with strict house style, identity lock, and transparency rules. 
  The skill owns pet-specific prompt planning, animation row orchestration, frame extraction, atlas geometry, QA contact sheets, short preview videos, and final pet.json + spritesheet.webp packaging. 
  Visual generation is delegated to Grok's native `image_gen` tool (or the ported imagegen skill). Deterministic work (manifests, layout guides via PIL, validation, composition, QA) is performed by the bundled Python scripts.
  Use when the user wants to "hatch a pet", "create a custom animated sprite pet", "build a digital mascot with idle + running + waving + jumping + failed + review states", or repair an existing pet run.
  Strong for game assets, app mascots, learning companions, or any tiny expressive character that must survive at 192x208 with a limited palette and chunky silhouette.
when-to-use: "Any request for a custom animated digital pet / mascot sprite sheet following the exact 9-state 8x9 192x208 contract. Always uses the deterministic scripts for scaffolding and QA; image_gen only for the visual rows under the strict identity + transparency rules. Complements imagegen skill for the generation calls."
allowed-tools: ["image_gen", "image_edit", "read_file", "write", "search_replace", "run_terminal_cmd", "list_dir", "grep"]
argument-hint: "<pet concept or reference image path(s)> [--name 'Fireball'] [--style 'chunky pixel pet'] [--output-dir /path]"
---

# Hatch Pet Skill (Grok Port)

**Mission:** Produce a production-ready, identity-consistent, geometrically perfect animated pet spritesheet + package that passes the full QA rubric (geometry, character consistency, house style, animation completeness, app fitness, and the strict transparency/effects rules).

**Grok Adaptation:** The original Codex skill delegates visual generation to `$imagegen`. This port delegates to Grok's first-class `image_gen` / `image_edit` tools (and the ported imagegen skill when the user wants the full prompting discipline or OpenAI fallback). All deterministic scaffolding, prompt generation, layout guides, manifest management, validation, composition, contact sheets, video previews, and packaging are handled by the ported Python scripts (which require PIL/Pillow).

Hard boundary (preserved): Never draw, tile, warp, or synthesize pet visuals with local code as a substitute for `image_gen`. The only exception is the explicit mirror derivation for `running-left` after visual inspection and approval.

## Codex Digital Pet House Style (Enforced in Every Prompt)

Compact chibi proportions, chunky whole-body silhouette, thick dark 1-2 px outline with visible stepped/pixel edges, limited palette, flat cel shading (≤1 highlight + 1 shadow step), simple readable face, tiny limbs. No polished illustration, painterly, anime, 3D, glossy, realistic fur, soft gradients, or high-detail antialiasing.

## Transparency & Effects Rules (Non-Negotiable — Embedded in All Row Prompts)

Effects only when state-relevant, opaque, hard-edged, pixel-style, inside the same frame slot, and physically touching/overlapping the pet. Allowed examples: attached tear on face, small smoke puff touching the box, tiny stars during failure.

**Forbidden (blockers):**
- Any detached effects, wave marks, motion arcs, speed lines, dust, shadows (all kinds), glows, text, labels, grids, scenery, checkerboard, white/black backgrounds, chroma-key bleed or adjacent colors in the subject.
- Poses that cross slot boundaries or create disconnected components.

State-specific rules (waving = paw pose only; jumping = vertical body only, no ground cues; etc.) are listed in `references/animation-rows.md`, the STATE_REQUIREMENTS in prepare_pet_run.py, and the generated row prompts.

## Visible Progress Checklist (Use on Every Run)

Before starting, establish a short name (ask user when natural; otherwise infer from concept/references). Use this checklist, updating one step at a time:

1. Getting `<Pet>` ready. (name, description, references, output dir, chroma key)
2. Imagining `<Pet>`'s main look. (base pet generation + record)
3. Picturing `<Pet>`'s poses. (row strips — idle + running-right first for identity/gait check; decide mirror for left only after inspection)
4. Hatching `<Pet>`. (finalize, validate, contact sheet, preview videos, visual identity review, package)

Only mark complete when the real file/decision exists.

## Default Workflow (Grok + Scripts)

1. **Prepare the run** (creates folder, prompts, layout guides, manifest):
   ```bash
   python3 "<SKILL_DIR>/scripts/prepare_pet_run.py" \
     --pet-name "Fireball" \
     --reference /abs/path/to/ref1.png --reference /abs/path/to/ref2.png \
     --output-dir /abs/path/to/my-pet-run \
     --force
   ```
   Output includes `pet_request.json`, `imagegen-jobs.json`, `prompts/rows/*.md`, `references/layout-guides/*.png`, and chosen chroma key.

2. **Generate & record the base** (parent agent does this with `image_gen` tool using `prompts/base-pet.md` + any references).
   After selecting the best output, ingest:
   ```bash
   python3 "<SKILL_DIR>/scripts/record_imagegen_result.py" \
     --run-dir /abs/.../my-pet-run --job-id base --source /abs/path/to/chosen/ig_*.png
   ```

3. **Row generation (subagents recommended after base)**
   - Parent spawns subagents for `idle` and `running-right` first (identity + gait check).
   - Each subagent receives the exact row prompt file + all listed input images (references + canonical base + layout guide + previous rows as needed).
   - Subagent returns only the chosen source path + one-sentence QA note.
   - Parent alone records with `record_imagegen_result.py`.
   - After `running-right` is approved, decide mirror for `running-left` (only if symmetric and safe) using `derive_running_left_from_running_right.py --confirm-appropriate-mirror`.
   - Otherwise treat `running-left` as a normal grounded row job.
   - Continue for the remaining rows.

4. **Repair** (if QA fails): `queue_pet_repairs.py` → smallest scope re-generation → record loop.

5. **Finalize** (all jobs recorded):
   ```bash
   python3 "<SKILL_DIR>/scripts/finalize_pet_run.py" --run-dir /abs/.../my-pet-run
   ```
   Produces atlas, validation, contact sheet, preview videos, packaged `pet.json` + `spritesheet.webp`.

## Key Scripts (All Functional in This Port)

- `prepare_pet_run.py` — full scaffolding + prompts + layout guides (PIL) + chroma auto-select.
- `record_imagegen_result.py` — ingest chosen image_gen output into decoded/ + manifest update.
- `finalize_pet_run.py` — orchestration of composition, validation, QA media, packaging (calls the rest of the suite in a full deployment).
- `derive_running_left_from_running_right.py`, `pet_job_status.py`, `queue_pet_repairs.py`, `validate_atlas.py`, `make_contact_sheet.py`, `inspect_frames.py`, `render_animation_videos.py` + `.sh`, `compose_atlas.py`, `extract_strip_frames.py`, `package_custom_pet.py`, `generate_pet_images.py` (secondary OpenAI-only fallback) — the remaining deterministic helpers follow the same patterns.

All scripts are designed to be invoked with absolute paths from `run_terminal_cmd`. They are self-contained where possible (PIL for graphics work).

## Subagent Contract (Preserved & Adapted for Grok `task` Tool)

After the base is recorded, row-strip visual jobs belong to subagents unless the user explicitly forbids them for the session.

Give each subagent:
- The exact row id + absolute prompt file path + full prompt text.
- Every input image path with role label from the manifest.
- Reminder of the transparency/effects/identity rules.
- Instruction to visually check frame count, identity lock, clean chroma key, safe spacing, no forbidden artifacts before returning.
- Return format: only `selected_source=/abs/path/to/chosen/ig_*.png` + `qa_note=one sentence`.

Parent never lets subagents edit manifests or run record/finalize/package steps.

## Acceptance Criteria (The Rubric)

- Atlas exactly 1536x1872, 8x9, 192x208 cells, transparent unused cells.
- Follows `references/animation-rows.md` frame counts.
- `qa/review.json` has zero errors.
- Contact sheet + preview videos exist and have been visually reviewed.
- Character identity is consistent across all rows (head, markings, prop side, silhouette, palette).
- No forbidden detached effects, shadows, text, or chroma bleed.
- Packaged `pet.json` + `spritesheet.webp` (or .png) ready for the target runtime.

Visual review of the contact sheet by the agent (or user) is the final gate even when automated validation passes.

## Grok-Specific Notes

- Use `image_gen` (aspect_ratio tuned to the strip or base) for all visual jobs. The generated prompts already contain the full house style + transparency contract + identity lock + layout guide instructions.
- For repair or identity-critical rows, attach the canonical base + original references + contact sheet + exact failure note.
- The secondary fallback `generate_pet_images.py` (OpenAI direct) is available only when the native image_gen path is explicitly blocked and the user approves; it still requires an OPENAI key and follows the same prompts.
- Package location defaults to a Grok-friendly `~/.grok-pets/<pet-id>/` (configurable via the scripts).

## Success Criteria

- A complete, validated, visually inspected pet package with all 9 animation states.
- Every visual job went through `image_gen` (or explicit fallback) under the strict rules; no local synthesis.
- The user receives the final package paths + the contact sheet + clear statement of which rows (if any) were mirrored vs fully generated.
- The pet is ready to drop into a compatible digital-pet runtime or game.

The user should feel: "My new pet is hatched, consistent, perfectly animated in all states, and the files are packaged exactly where the app expects them."

This port brings the complete, production-grade, deterministic pet-hatching pipeline from Codex into the Grok ecosystem while making full use of Grok's native image generation strengths and the `task` / subagent model for scalable row work.
