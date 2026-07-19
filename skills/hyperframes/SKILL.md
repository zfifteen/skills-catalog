---
name: hyperframes
description: >
  Author, debug, and QA HTML-based video compositions using the HyperFrames framework (data-* timing attributes + GSAP timelines + CSS). Covers full production: design system (palettes, typography, motion), prompt expansion, layout-before-animation, scene transitions, captions/voiceover, audio-reactive visuals, marker highlighting, and rigorous post-authoring checks (lint, contrast, animation-map, inspect).
  Use when the user wants HTML-source-of-truth video (title cards, explainers, product launches, data stories, lyric videos, reactive music visuals, or any multi-scene animated piece with precise timing and typography).
  The native Grok `video_gen` tool is excellent for quick clips; this skill is for when the user needs editable HTML source, deterministic GSAP choreography, caption sync, or brand-accurate long-form video that will be rendered via the HyperFrames compiler/player.
  Triggers: "create a video in HTML", "HyperFrames composition", "add captions synced to audio", "audio-reactive animation", "GSAP timeline for this scene", "title card with this design", "narrated explainer with voiceover".
when-to-use: "Any request for structured, source-controlled, typography-heavy, or precisely timed HTML video/animation. Strong for brand work (design.md driven), narrated content, and anything that benefits from the inspect/contrast/animation-map QA loop. Complements video_gen for hybrid workflows."
allowed-tools: ["read_file", "write", "search_replace", "run_terminal_cmd", "list_dir", "grep", "image_gen", "video_gen", "open_page"]
argument-hint: "<video concept or edit request> [style: bold-energetic | clean-corporate | ...] [--design-md path]"
---

# HyperFrames Skill (Grok Port)

HTML is the source of truth. A composition is a single (or set of) HTML file(s) using `data-*` attributes for timing, a registered GSAP timeline, and CSS for visuals. The framework + compiler handle playback, media sync, and rendering to video.

**Grok Adaptation:** Grok's `video_gen` produces excellent short-to-medium clips quickly. Use **HyperFrames** when you need:
- Precise typography, data labels, and brand fidelity that survive re-renders.
- Editable source that teammates or future agents can modify without re-prompting.
- Complex caption sync, audio-reactive motion, or shader transitions.
- Rigorous QA (contrast, choreography, overflow) before final render.

The 3 analysis scripts (`animation-map.mjs`, `contrast-report.mjs`, `package-loader.mjs`) are ported for environments that have the full Node + browser capture toolchain. The authoring rules below are the primary, always-available value of the skill.

## Step 0: Design System (Non-Negotiable for New Work)

If `design.md` / `DESIGN.md` exists anywhere in the project tree, read it first. It is the single source of truth for colors, fonts, corner radius, depth, density, and "do not" rules. Use its exact values.

If none exists:
- User named a mood or style? → Consult `visual-styles.md` (8 presets) or `house-style.md`.
- Want interactive choice? → Serve the design picker (see original `references/design-picker.md` + `templates/design-picker.html`).
- Fast path: Ask for mood + light/dark + any brand hex/fonts, then pick from house-style or one of the palette files in `palettes/`.

**Never invent hex values or font stacks when a design system is declared.**

## Step 1: Prompt Expansion (Run on Every Significant Composition)

Read and follow the process in the original `references/prompt-expansion.md`. This produces a consistent intermediate artifact that every downstream step (including sub-agents) consumes. It grounds the request against the design system.

## Core Authoring Rules (Selected Non-Negotiables — Read These First)

**Layout Before Animation**
- Build the hero (most-visible) frame of each scene as static HTML+CSS first.
- `.scene-content` must use flex + padding + gap inside a full-size container. Never hardcode pixel dimensions or absolute positioning on content containers.
- Only after the end-state layout is correct and stable, add `gsap.from()` entrances and (final scene only) exits.
- This catches overlap bugs before any motion is written.

**Data Attributes Contract**
- Every timed element needs `id`, `data-start`, `data-duration`, `data-track-index`.
- Composition roots additionally declare `data-composition-id`, `data-width`, `data-height`.
- Sub-compositions are loaded via `<template>` + `data-composition-src`.

**Timeline Contract**
- All timelines: `const tl = gsap.timeline({ paused: true }); window.__timelines["id"] = tl;`
- Duration comes from `data-duration`, not timeline length.
- Never use `repeat: -1`. Calculate finite repeats from composition duration.
- No async construction of timelines.

**Scene Transitions (Hard Rule for Multi-Scene)**
- Every multi-scene piece **must** have a transition between scenes.
- Every scene must have entrance animations on its elements.
- **No exit animations before the final scene.** The transition itself is the exit. The outgoing scene must still be fully visible when the transition fires.
- Final scene may fade elements out.

**Animation Guardrails**
- Offset first tween 0.1–0.3s.
- Vary eases (at least 3 distinct per scene).
- Large type (60px+ headlines, 20px+ body at 1920px).
- Use `font-variant-numeric: tabular-nums` for numbers.
- No `Math.random()` or `Date.now()` in deterministic compositions (use seeded PRNG if needed).

**Voiceover / Narration Production**
- Scene-by-scene narration (not one long track).
- Generate per-scene audio (Grok/xAI TTS preferred when `XAI_API_KEY` available; Sal voice is the documented default in the original harness).
- Measure durations with ffprobe.
- Set scene visual duration = voiceover + ≤2s pad.
- Mux per scene, then concat. Verify final MP4 has both streams and correct total duration.

**Typography & Assets**
- Prefer built-in fonts (compiler embeds them).
- Custom fonts require `.woff2` in a `fonts/` dir + `@font-face`.
- Use `window.__hyperframes.fitTextFontSize(...)` for dynamic text.
- Cross-origin for external media.

## QA Loop (Run These After Authoring)

1. `npx hyperframes lint && npx hyperframes validate` (fast, blocking).
2. `npx hyperframes inspect` (or `--json`) — catches overflow, clipping, layout surprises. Use `--samples` and `--at` for key frames.
3. Contrast audit (the `contrast-report.mjs` script or the framework's built-in).
4. Animation map (`animation-map.mjs`) — verifies choreography, dead zones, staggers, lifecycles.
5. Visual design adherence check against `design.md` (or house-style "lazy defaults").

Only deliver when all checks are green or explicitly accepted with documented rationale.

## References (Ported Structure)

The original ships an extensive `references/` tree (transitions/catalog + 12 subdirs, techniques, motion-principles, captions, tts, audio-reactive, typography, beat-direction, video-composition, etc.). 

In this Grok port:
- The most critical rules are distilled above.
- For any specific technique (shader transitions, dynamic captions, Lottie, MotionPath, etc.), the original files under `~/.codex/skills/hyperframes/references/` remain the authoritative deep reference.
- `house-style.md`, `visual-styles.md`, `patterns.md`, `data-in-motion.md`, and the palette files are small and can be read on demand via `read_file` from the Codex location or copied into the project.

Key files worth reading when relevant:
- `references/video-composition.md` (always for multi-scene)
- `references/motion-principles.md` (GSAP load-bearing rules)
- `references/transitions.md` + catalog (mandatory for >1 scene)
- `references/captions.md` and `references/dynamic-techniques.md`
- `references/tts.md` and `references/narration.md`

## Scripts (Analysis & QA)

- `scripts/animation-map.mjs` — choreography audit + ASCII timeline
- `scripts/contrast-report.mjs` — WCAG pixel-contrast audit + overlay
- `scripts/package-loader.mjs` — npm bootstrap for the analysis tools

These require a Node environment with the HyperFrames packages and a headless browser. In a pure Grok session they document the expected output contract and recommendations. When the full toolchain is present (common in dev workstations), they provide the same rigorous QA as the original skill.

## Integration with Grok Creative Tools

- Use `image_gen` / `image_edit` to produce stills, backgrounds, or illustration layers that are then referenced (or traced) inside the HTML composition.
- Use `video_gen` for quick prototype clips or B-roll that can be dropped into a HyperFrames track.
- The final rendered MP4 from the HyperFrames compiler can be further processed or described with Grok tools.

## Success Criteria

- A clean, committed `index.html` (or set of compositions) that passes lint/validate/inspect/contrast/animation-map.
- Design system adherence verified (no invented colors or fonts).
- Every scene has proper entrances + (for multi-scene) a transition.
- Typography is large, readable, and contrast-safe.
- Voiceover work (if any) is scene-synchronized with ≤2s pad and verified muxing.
- The user has both the source HTML (editable) and the final rendered video artifact.

The user should feel: "I have precise, brand-accurate, typography-perfect video source that I can edit, plus automated QA evidence that it will render beautifully."

This port brings the full power of the HyperFrames discipline — one of the strongest HTML-video production systems — into the Grok ecosystem while respecting the native `video_gen` tool for rapid iteration.
