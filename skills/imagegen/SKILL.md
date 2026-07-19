---
name: imagegen
description: >
  Generate or edit high-quality raster images using Grok's native `image_gen` and `image_edit` tools (preferred), or the explicit OpenAI fallback script when the user specifically requests GPT-Image / DALL·E models. 
  Use for brand-new bitmap assets (photos, illustrations, sprites, mockups, product shots, UI visuals, concept art, transparent cutouts) or transformations of existing images. 
  Do not use when the task is better served by editing SVG/vector/repo-native code, or when a simple icon can be drawn directly in HTML/CSS/SVG.
  Triggers: "generate an image of...", "create a hero banner", "edit this photo", "make a sprite sheet", "product mockup", "illustration for...", "transparent background cutout of this".
when-to-use: "Any request for AI-generated or AI-edited bitmap visuals. Grok's image_gen is first-class and preferred. This skill provides the prompting discipline, taxonomy, iteration patterns, and reference guidance that make the native tools produce production-grade results. The bundled script is strictly for explicit OpenAI fallback requests."
allowed-tools: ["image_gen", "image_edit", "video_gen", "run_terminal_cmd", "read_file", "write", "search_replace", "list_dir"]
argument-hint: "<detailed visual request or edit instruction> [use case: product-mockup | illustration-story | ...] [--refs /path1 /path2]"
---

# Image Generation Skill (Grok Port)

**Primary Rule (Grok-native):** Use the built-in `image_gen` tool for normal generation and `image_edit` for edits on images already visible in context. The bundled `scripts/image_gen.py` is **explicit-fallback-only** — never auto-switch to it.

This port preserves the excellent prompting structure, use-case taxonomy, specificity policy, and iteration discipline from the original Codex imagegen skill while centering Grok's native vision tools.

## Decision Tree (Always Follow)

1. **Intent**
   - New image or major creative transformation → **generate**
   - Modify an existing image while preserving core identity/parts → **edit** (use `image_edit` on context-visible images; for pure filesystem edits, load with appropriate viewer first if required by the environment)

2. **Execution**
   - Single asset or a few variants → repeated native `image_gen` / `image_edit` calls (best quality + provenance).
   - Many assets → script a loop or (only if explicitly requested) the OpenAI batch path.

3. **References**
   - User-provided images for style/composition/subject guidance → treat as **generate** with strong reference role labels.
   - The actual target of an edit → **edit** path.

Assume "generate" unless the user clearly wants to change an existing visible image.

## Prompting Discipline (Core of the Skill)

Use a consistent, labeled structure for every call (even when using the native tool's free-form prompt field — the structure improves results):

```
Use case: <taxonomy slug from below>
Asset type: <where it will live: landing hero, app icon, game sprite, social post, etc.>
Primary request: <user's core ask, verbatim or lightly normalized>
Input images: Image 1 (role: reference / style source / subject); Image 2 ...
Scene/backdrop: <environment or none>
Subject: <main subject description>
Style/medium: <photo / flat illustration / pixel-adjacent sprite / 3D render / etc.>
Composition/framing: <wide / close / top-down / rule-of-thirds placement>
Lighting/mood: <studio / golden hour / dramatic / soft / etc.>
Color palette: <limited / brand colors / vibrant / muted>
Materials/textures: <key surface notes>
Text (verbatim): "exact text to render" or none
Constraints: must keep X, must avoid Y
Avoid: <negative prompt items>
```

**Specificity policy (critical):**
- Already detailed user prompt → normalize/structure only. Do not add unsolicited creative requirements.
- Generic prompt → tasteful, minimal augmentation that materially helps (composition, polish level, intended-use framing). Never invent characters, slogans, or side-specific placements.

**Text in images:** Spell tricky words letter-by-letter. Require verbatim rendering. For logos/branding, quote exactly.

**Input images & references:** Always label roles explicitly in the prompt and in your thinking: "reference image", "edit target", "style source", "layout guide (do not copy visible lines)".

**Iteration:** One targeted change per follow-up. Re-inspect. Preserve invariants aggressively on edits ("change only the background; keep product edges and lighting identical").

## Use-Case Taxonomy (Keep Slugs Consistent)

**Generate:**
- photorealistic-natural
- product-mockup
- ui-mockup
- infographic-diagram
- logo-brand (vector-friendly intent)
- illustration-story
- stylized-concept
- historical-scene
- sprite-pixel-adjacent (for games / pets / mascots — see hatch-pet skill)

**Edit:**
- text-localization
- identity-preserve (try-on, person-in-scene)
- precise-object-edit
- lighting-weather
- background-extraction (transparent cutouts — excellent with native tools)
- style-transfer
- compositing
- sketch-to-render

## Native Grok Tool Usage Patterns

- **Generation:** Call `image_gen(prompt=structured_spec, aspect_ratio=...)`. Review the returned path. For project use, copy the chosen output into `output/assets/` or the consuming location. Never leave a project-referenced asset only at the default Grok generation cache.
- **Edits:** Use `image_edit(prompt=..., image=[visible_image_path_or_dataurl])`. For filesystem-only targets, first ensure the image is described/loaded in context.
- **Variants & batches:** Issue multiple targeted `image_gen` calls rather than one giant batch request when using native tools. This gives better control and intermediate inspection points.
- **Transparent backgrounds:** Explicitly request "perfectly flat pure chroma-key background" or "clean transparent background" and verify with renders.
- **For hatch-pet style sprites:** Combine this skill's sprite-specific rules (chunky silhouette, limited palette, flat cel, thick dark outlines, no detached effects) with the dedicated hatch-pet skill's deterministic atlas/packaging pipeline.

## Fallback OpenAI CLI (Explicit Only)

If the user explicitly says "use the OpenAI fallback" or "I need GPT-image-1.5 for this comparison":
1. Confirm the request.
2. Use `<dirname of this SKILL.md>/scripts/image_gen.py generate ...` (or edit/generate-batch).
3. The script enforces the same prompting contract and will surface the need for `OPENAI_API_KEY`.
4. After generation, still apply the visual inspection + move-to-project rules.

Never auto-route to the CLI. The native Grok tools are higher fidelity for most creative work inside this environment.

## Output & Provenance Rules

- Project-bound assets: move or copy the final chosen file(s) into the workspace (`output/imagegen/`, `output/assets/`, or alongside the consuming code).
- Preview-only: render inline; the cache path is acceptable.
- Always report the final absolute path + the exact prompt used + which path (native vs fallback) was taken.
- For any asset that will be committed or referenced in docs/code, produce a stable, descriptive filename (never rely on auto-generated `ig_*.png` names alone).

## Quality & Inspection

After every meaningful generation or edit:
- Inspect subject, style, composition, text accuracy, and all stated constraints/invariants.
- For transparent or sprite work, verify no chroma-key bleed into the subject and no detached artifacts.
- Iterate with the smallest possible change.

## References (Original Codex — Adapted)

- `references/prompting.md` — full structure & iteration principles (the content above is the distilled Grok-native version).
- `references/sample-prompts.md` — copy/paste recipes by asset type.
- `references/cli.md`, `references/image-api.md` — fallback-only details.
- The original also ships `assets/imagegen.png` and an OpenAI agent config; those are omitted here as they are environment-specific.

When deeper reference material is needed, the source Codex skill tree remains available at `~/.codex/skills/imagegen/`.

## Success Criteria

- The chosen image(s) exactly satisfy the use-case taxonomy, invariants, and visual spec.
- User receives the file path(s), the authoritative prompt, and confirmation of which generation path was used.
- Native Grok tools are used by default; fallback is only on explicit request and is clearly labeled.
- No "it generated something pretty" — every asset is inspected against the stated constraints.

This port makes the outstanding prompting and workflow discipline of the original Codex imagegen skill a first-class citizen inside Grok's native creative tool surface.
