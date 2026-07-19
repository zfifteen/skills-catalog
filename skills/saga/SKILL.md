---
name: saga
description: >
  Query the full LLM consortium (same seven models/settings as Massive) but with
  freshly invented comic-book superhero personas for each model on every run.
  Each model receives a distinct fantastical hero persona (supernatural powers,
  non-literal cognitive scaffold) wrapped around the identical ordinary task.
  Collects responses and produces a structured Markdown synthesis that also
  evaluates which hero framings produced the most useful postures. In automation
  environments uses Comet + Computer Use; in standard Grok, prepares the seven
  distinct atomic prompts, tracks the run, and synthesizes on user-provided
  responses. Use when the user invokes /saga or wants deliberately varied
  cognitive scaffolds for the same hard task.
when-to-use: "When the same task benefits from highly divergent reasoning postures via fresh, fantastical comic-book hero framing (not occupational metaphors). Trigger on '/saga <task>', 'run saga on this', 'hero-framed consortium', or any request for model diversity through imaginative persona scaffolding rather than plain prompts."
allowed-tools: ["read_file", "grep", "list_dir", "write", "web_search", "web_fetch", "open_page", "open_page_with_find", "memory_search", "memory_get", "todo_write", "x_keyword_search"]
argument-hint: "<the ordinary task or question> [context files] [--rounds or continuity note]"
metadata:
  short-description: "LLM consortium with freshly invented comic-book superhero personas for cognitive diversity (Massive variant)"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/saga/SKILL.md"
---

# Saga — Grok Edition

## Contract

`Saga` is derived from `Massive`, but its invariant is different:

- `Massive` sends the same canonical prompt to every model.
- `Saga` sends **model-specific prompts** built from the same ordinary user objective wrapped in a **freshly invented comic-book superhero persona**.
- Each `Saga` prompt must preserve the identical ordinary task objective.
- The superhero persona is a **cognitive scaffold** for posture, agency, attention, imagination, and search behavior. It is **not** a domain tool or role-play request.
- Hero personas must be **invented fresh for every Saga run**. Never reuse a standing roster or previous run's heroes unless the user explicitly asks for continuity.
- Hero personas must be **fantastical enough to read as comic-book superheroes**, not as ordinary consultants, analysts, engineers, reviewers, strategists, etc. wearing dramatic names.

Valid hero design examples: cosmic anomalies, impossible physics, mythic transformations, reality-bending perception, living storms, memory-forged armor, time-fracture sight, spectral duplication, gravity command, dream metallurgy, starfire regeneration, and comparable comic-book-scale abilities.

Invalid: any merely occupational or practical framing (even with a cool name).

Query every configured model with its required conversation setting (identical table to Massive) plus one freshly invented hero persona.

## Required Conversation Settings (Exact — Verify Before Submit)

| Model              | URL                              | Required setting   |
|--------------------|----------------------------------|--------------------|
| Gemini             | https://gemini.google.com/app    | `Thinking`         |
| Grok               | https://grok.com/                | `Expert`           |
| Meta AI            | https://meta.ai/                 | `Contemplating`    |
| Deepseek           | https://chat.deepseek.com/       | `Expert`           |
| Microsoft Copilot  | https://copilot.microsoft.com/   | `Think Deeper`     |
| Claude             | https://claude.ai/new            | `Sonnet 4.6`       |
| ChatGPT            | https://chatgpt.com/             | `Heavy`            |

## Hero Generation (Mandatory Fresh Each Run)

After ingesting the user's task (via `read_file` etc. for local context) and **before** building any prompts:

Invent a new seven-hero roster.

Each hero entry must contain:
1. A new superhero name (e.g., "Aetherweave", "Singularity Cant", "Chronofract").
2. Supernatural comic-book powers (2–4 vivid abilities).
3. A task posture translated from the powers into a reasoning style (how the hero approaches hard problems).
4. A one-sentence reminder that the powers are imaginative framing only, not literal tools or domain evidence.

The seven heroes must be distinct from each other in power source, personality, and reasoning posture.

The assignment table (which hero to which model) belongs in the final output artifact.

## Prompt Shape (Atomic — One Message Per Model)

Every model-specific Saga prompt is an **atomic payload**. It must contain in the same user message:

```text
You are [freshly invented comic-book superhero name].

Your supernatural comic-book powers are: [powers].

Those abilities are not literal tools for this task. They define your posture: [task posture].

Ordinary task:
[base task statement — identical across all seven prompts]

Return:
[requested output shape, or a concise task-appropriate answer if the user did not specify one]
```

Before any submission (manual or automated), verify that the draft input visibly contains the required section labels (or exact equivalents):
- hero name
- supernatural comic-book powers
- non-literal-tools sentence
- ordinary task
- return shape

Do not submit a hero-only setup turn, persona-only turn, etc. One complete message per model.

Do not make the task about the hero's powers. Do not ask the hero to roleplay scenes, lore, combat, dialogue, or fictional worldbuilding unless the user's ordinary task is actually creative writing.

## Execution Modes (Same as Massive)

**Prompt-pack + synthesis mode** (primary for this Grok port):
- Ingest context with tools.
- Invent the seven fresh heroes.
- Build and emit seven atomic, ready-to-paste prompts (one per model + setting).
- Write a run tracker (`.saga-run-...`).
- On user paste-back of the seven labeled responses → perform synthesis and write `saga-YYYY-MM-DD-HHMM.md`.

**Full automation mode** (when browser/Computer Use + Comet available):
- Same tab discipline as Massive.
- For each model: verify setting, then submit its unique atomic hero-wrapped prompt exactly once.
- Harvest, synthesize, write the document.

## Prompt Handling & Sensitive Data

- Build one base task statement.
- Wrap it in the assigned freshly invented hero for each model.
- Differences between the seven prompts come **only** from the hero definition and derived posture — never from secretly changing the user's objective.
- Sensitive-data confirmation (listing all seven destinations) is mandatory before any external submission.

## Collection Rules

For each model response:
- model name
- selected setting
- Saga hero persona (name + powers + posture)
- prompt submitted (reference ok)
- response text
- completeness flag

If truncated or incomplete, record plainly.

## Markdown Output Document

Create (via `write`) `saga-YYYY-MM-DD-HHMM.md` containing:

1. Title and timestamp.
2. Original user request.
3. Base task statement.
4. Fresh hero assignment table (model → hero name + one-line power summary).
5. One summary per model (~500 chars) + which hero it received.
6. Synthesis:
   - Where the models agree
   - Where they disagree
   - Unique responses split by model **and** invented hero
   - Which hero framing(s) appeared to produce the most useful posture for the task (with evidence)
7. Grok/Codex analysis: strongest supported conclusion first, then exact bounds, limits, unresolved questions.
   - Include PGS contract considerations if the workspace AGENTS.md applies.

## Guardrails (Additional to Massive)

- Hero invention must be genuinely fresh and fantastical on every run. Do not fall back to a cached or occupational roster.
- The ordinary task objective must be literally identical in all seven prompts.
- Never let the persona framing leak into changing the task itself.
- In the final synthesis, evaluate the *framing effect* of the heroes separately from the raw model capability.
- In this repository: any Saga run touching prime-gap-structure work must ensure the base task statement and all hero postures respect the PGS-native deterministic frame. The synthesis must not reframe proved laws as probabilistic.

## Success Criteria

- User receives either a complete automated run or a clean, atomic prompt pack (7 distinct hero-wrapped messages) + tracker + synthesis on demand.
- The hero roster is new, vivid, comic-book scale, and the assignment table is present.
- Synthesis explicitly calls out framing effects of the invented personas.
- The final document is named and structured exactly as specified.
- No contamination of the ordinary task by the scaffolding.

## Usage in This Environment

`/saga <ordinary hard task or question>`

The skill will:
- Read relevant files for minimal context
- Invent a fresh seven-hero roster
- Emit seven atomic, copy-paste-ready prompts (one per model+setting+hero)
- Create run state
- On paste-back of responses, write the full synthesis including hero-effectiveness notes

This gives the cognitive diversity benefit of Saga even when full browser automation is not available in the current client.
