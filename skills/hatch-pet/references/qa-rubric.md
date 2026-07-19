# QA Rubric (Grok Port)

Do not accept a hatched pet atlas until **all** checks pass.

## Geometry
- Exact `1536x1872` dimensions.
- 8×9 grid of `192x208` cells.
- Every frame fully contained inside its cell.
- Unused cells 100% transparent (no stray pixels).
- `qa/review.json` (produced by validate_atlas.py) has zero errors.
- `frames/frames-manifest.json` present unless slot extraction was intentionally accepted after visual review.

## Character Consistency (Identity Lock)
- Same silhouette, proportions, head shape, face language, markings, palette, prop design, and outline weight across **every** row and frame.
- No frame introduces a new species, body type, or unrelated object.
- Running-left (when mirrored) must preserve all semantics and markings after flip.

## Sprite Style (Codex Digital Pet House Style)
- Compact chibi, chunky readable silhouette at 192x208.
- Thick dark 1-2 px outline with visible stepped/pixel edges.
- Limited palette, flat cel shading (at most one small highlight + one shadow step).
- Simple expressive face, tiny limbs.
- **No** polished illustration, painterly texture, anime key art, 3D render, glossy app-icon treatment, realistic fur/material, soft gradients, high-detail antialiasing, or complex tiny accessories that vanish at size.

## Animation Completeness & Readability
- Exact frame counts per `references/animation-rows.md`.
- First/last frames loop without obvious pop.
- Directional rows read correctly as left or right.
- State actions (wave, jump, failure, review focus) are legible at pet size.
- Poses are distinct animation variants, not repeated copies or simple transforms of the base.

## App Fitness & Transparency Rules (Critical)
- First idle frame works as a static reduced-motion pet.
- No important detail too small or clipped by the cell.
- Contact sheet shows whole sprites inside cells (not cropped tiles from a larger reference).
- No white/opaque rectangular backgrounds behind the pet unless the design intentionally fills the cell and the user has accepted the tradeoff.
- Chroma key must be cleanly absent from the character and all attached effects. If extraction eats character pixels, choose a different key and regenerate.
- No edge slivers, partial neighboring sprites, or neighboring cell bleed.
- **Forbidden (always blockers unless explicitly accepted for a repair):**
  - Detached effects (floating stars, loose sparkles, falling tears, separated smoke, loose dust, stray pixels, disconnected outline bits).
  - Wave marks, motion arcs, speed lines, action streaks, afterimages, blur, smears, halos, glows, auras.
  - All shadows (cast, contact, drop, oval floor, landing marks, impact bursts).
  - Text, labels, frame numbers, visible grids, guide marks, speech/thought bubbles, UI, code, scenery, checkerboard.
  - Chroma-key-adjacent colors anywhere in the pet, props, effects, or highlights.
  - Poses that cross slot boundaries or create separate disconnected components.

State-specific (in addition to the general rules):
- Waving: paw pose only — no arcs or sparkles around the paw.
- Jumping: vertical body position only — no ground shadows, dust, landing marks, or bounce pads.
- Failed: slumped pose + attached tears/smoke/stars only; no red X, floating symbols, or detached elements.
- Review: lean, blink, head tilt, paw position; no new magnifying glasses, papers, or UI unless they already exist in the base identity.
- All running rows: locomotion through body/limb/prop movement only — no speed lines, dust clouds, or motion trails.

## Repair Policy
Repair the smallest failing scope:
1. Single bad frame (rare).
2. One entire row.
3. Full atlas only when identity or layout is broadly broken.

Use `queue_pet_repairs.py`, re-generate only the affected row(s) with the canonical base + original references + exact failure note as grounding, then re-validate.

**Visual review of the contact sheet is the final gate even when JSON validation passes.** Identity drift or forbidden detached effects are blockers regardless of automated scores.

This rubric is enforced by the deterministic scripts and must be respected in every prompt given to `image_gen`.
