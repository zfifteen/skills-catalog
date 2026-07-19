# Codex Pet Contract (Grok Port)

## Sprite Atlas Requirements

- Format: PNG or WebP (WebP preferred for size).
- Dimensions: exactly `1536 x 1872`.
- Grid: 8 columns × 9 rows.
- Cell size: `192 × 208`.
- Background: fully transparent.
- Unused cells (after the last used frame in each row): fully transparent (no residual pixels, no anti-aliased edges from the chroma key).

The consuming app/webview uses CSS background-position based on the fixed row/column counts. Do not add labels, gutters, borders, grid lines, outer shadows, or extra frames.

## Local Custom Pet Package

Standard location (adapted for any environment):
```
${PET_HOME:-$HOME/.codex-or-grok-pets}/<pet-id>/
├── pet.json
└── spritesheet.webp
```

`pet.json` shape (minimal):
```json
{
  "id": "pet-id-slug",
  "displayName": "Pet Display Name",
  "description": "One short sentence suitable for UI.",
  "spritesheetPath": "spritesheet.webp"
}
```

The folder name under the pets root is the stable id. The app loads custom pets from this structure.

## Grok Adaptation

When packaging for a Grok project or demo, place the final `spritesheet.webp` and `pet.json` in `output/pets/<pet-id>/` or a user-specified location and document the absolute paths. The deterministic scripts (finalize_pet_run.py, package_custom_pet.py) enforce the geometry and manifest.

Visual identity, transparency rules, and effects restrictions are enforced at generation time (see SKILL.md and the row prompts produced by prepare_pet_run.py).
