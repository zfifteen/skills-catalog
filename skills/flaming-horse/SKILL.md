---
name: flaming-horse
description: >
  Guide deterministic Flaming Horse video creation from any session while strictly preserving the repository-owned pipeline, contracts, and validation gates. 
  Use /flaming-horse when the user wants assistant-guided concept shaping, review checkpoints, scripted pipeline execution, finalized scene embeds, final video embeds, or Flaming Horse video creation.
when-to-use: "User wants to create a Flaming Horse (Manim + Qwen + ffmpeg) video using the canonical deterministic pipeline from the flaming-horse repo. 'create a flaming horse video about X', 'guide me through a flaming horse project', 'review the flaming horse concept for Y', 'run the flaming horse pipeline'."
allowed-tools: ["run_terminal_cmd", "read_file", "list_dir", "grep", "web_search", "open_page", "ask_user_question", "todo_write"]
argument-hint: "<project_name> --topic '<concept or path to concept.md>' [--phase review]"
metadata:
  short-description: "Strict wrapper around the Flaming Horse deterministic video pipeline and contracts"
  source: "Codex 'flaming-horse' skill (ported 2026-05-24)"
---

# Flaming Horse (Grok Port)

## Purpose

Use this skill to guide creation of a Flaming Horse video from any session while preserving the repository-owned deterministic pipeline.

**The skill is an assistant-mode wrapper around the Flaming Horse runtime. It does not replace the generator, hand-author generated scenes, patch generated project artifacts, skip validation gates, bypass voice caching, or manually assemble videos.**

## Repository Contract

Canonical repo:
`/Users/velocityworks/IdeaProjects/flaming-horse`

**Before command work in the repo, read (via `read_file`):**

1. `docs/policies/USER_PREFERENCES.md`
2. `AGENTS.md`
3. The focused contract document that matches the task:
   - `docs/architecture/PIPELINE_CONTRACT.md`
   - `docs/architecture/HARNESS_CONTRACT.md`
   - `docs/architecture/SCENE_GENERATION_CONTRACT.md`
   - `docs/architecture/VOICE_CONTRACT.md`

If stored repo instructions conflict with the current user request, stop and ask.

## Operating Contract (preserved)

Use the same deterministic pipeline as script mode.

Canonical creation path:
```bash
./scripts/create_video.sh <project_name> --topic "<topic>"
```

For substantial concepts, prefer a concept file and pass its absolute path:
```bash
./scripts/create_video.sh <project_name> --topic /absolute/path/to/concept.md
```

When planning should precede expensive scene generation, run the review checkpoint:
```bash
./scripts/create_video.sh <project_name> --topic /absolute/path/to/concept.md --phase review
```

Inspect the review artifacts and wait for user approval before continuing past the review checkpoint.

## Assistant Duties (strict scope)

1. Clarify or shape the video concept only when needed.
2. Create or inspect a topic/concept artifact only when the user approves.
3. Invoke the Flaming Horse scripted pipeline from the repo (via `run_terminal_cmd`).
4. Read project state, logs, plans, QC reports, and generated artifacts using `read_file` / `list_dir`.
5. Identify the first failing phase when execution fails.
6. Explain failures at the framework level.
7. Embed finalized scene videos inline using absolute local paths in Markdown (Codex Desktop / Grok compatible image/video syntax).
8. Embed the final assembled video inline.
9. Report the project directory and final artifact paths.

## Scene & Final Video Embedding Contract

A scene is finalized only when the pipeline has produced the scene video artifact **and** the required validation or QC phase for that scene has passed.

After each scene is finalized, embed it using an absolute local path:

```markdown
Scene 1: <scene title if known> | finalized | `/absolute/path/to/scene_01.mp4`

![Scene 1](/absolute/path/to/scene_01.mp4)
```

If scenes are rendered as a batch, embed the completed validated scene artifacts immediately after the batch phase, in scene order.

After successful assembly, embed the final video the same way.

## Artifact Discovery

Use deterministic artifact discovery.

Prefer project state, known project directories, and documented artifact paths. Do not guess, glob broadly, search unrelated locations, or treat draft render artifacts as finalized scenes.

If an expected scene artifact or final video is missing, state the expected path and stop.

## Boundaries (non-negotiable — preserved verbatim)

Do not:

1. Hand-author generated scene files.
2. Patch `projects/<project>/scene_*.py` unless explicitly asked.
3. Patch `plan.json`, narration scripts, or other generated artifacts unless explicitly asked.
4. Skip validation gates.
5. Bypass voice caching.
6. Manually assemble the final video.
7. Add fallback generation paths.
8. Retry with alternate methods unless the user explicitly asks.
9. Create broad helper systems or new framework layers.

Generated project artifacts are evidence by default, not fix targets.

## Failure Behavior

On failure, report:

1. The first failing phase.
2. The relevant command.
3. The relevant log, state file, or artifact path.
4. The framework-level interpretation.
5. The exact unresolved condition.

Do not work around the failure.

## Final Response Shape (on success)

1. Embedded finalized scene videos.
2. Embedded final video.
3. A compact artifact manifest:
   - Project directory.
   - Scene video paths.
   - Final video path.
   - QC or report paths when relevant.

Keep the response concise and operational.

## Grok-Specific Adaptations

- All repo reads use the standard Grok tools (`read_file`, `list_dir`, `grep`).
- Pipeline execution uses `run_terminal_cmd` with the exact `./scripts/create_video.sh ...` invocations.
- Embedding uses the same absolute-path Markdown video syntax that works in the Grok / Codex Desktop surfaces.
- `todo_write` is recommended for tracking multi-phase video projects.
- When used inside the prime-gap-structure workspace, combine with the local `AGENTS.md` PGS-first requirements if any number-theoretic content appears in a video concept.

## Success Criteria

- The user experiences the exact same deterministic, contract-respecting pipeline as running the scripts directly.
- All embeds are of *finalized* (validated) artifacts only.
- Failures are reported at the framework level with precise locators.
- No scope creep or invented generation paths.

This port turns the original Codex "assistant-mode wrapper" into a fully tool-instrumented Grok skill while preserving every boundary and contract.
