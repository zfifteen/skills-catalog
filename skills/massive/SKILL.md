---
name: massive
description: >
  Query Grok Heavy and Gemini on a hard engineering or research problem using the
  identical prompt and verified conversation settings for each model. Runs through
  Safari (authenticated sessions on this Mac) — never Playwright, Chromium, or
  Comet. Collects both responses and produces a structured Markdown synthesis.
  If Safari submit cannot be completed automatically, falls back to a two-model
  prompt pack and synthesizes when the user pastes (or Safari-harvests) replies.
  Use when the user invokes /massive or wants a dual-model Grok Heavy + Gemini view.
when-to-use: "For difficult, high-stakes, or ambiguous engineering/research questions where dual-model consensus, disagreement, and unique angles add value. Trigger on '/massive <question>', 'run this through massive', 'massive synthesis on...', or any request for parallel Grok Heavy + Gemini perspectives with structured comparison."
allowed-tools: ["read_file", "grep", "list_dir", "write", "run_terminal_command", "web_search", "web_fetch", "open_page", "open_page_with_find", "memory_search", "memory_get", "todo_write", "x_keyword_search"]
argument-hint: "<the hard question or task> [optional: specific context files or constraints]"
metadata:
  short-description: "Grok Heavy + Gemini dual query via Safari + structured synthesis"
  version: "2.0.0"
  browser: "Safari only (authenticated sessions)"
  models: ["Grok Heavy", "Gemini Thinking"]
---

# Massive — Grok Heavy + Gemini (Safari)

## Contract

Query **exactly two** models with the **same prompt** and each model’s **required conversation setting**:

| Model        | URL                           | Required setting | Notes |
|--------------|-------------------------------|------------------|--------|
| Grok         | https://grok.com/             | `Heavy`          | X Premium / Grok Heavy subscription; use authenticated Safari session |
| Gemini       | https://gemini.google.com/app | `Thinking`       | Google Gemini subscription; use authenticated Safari session |

Do **not** query Meta AI, Deepseek, Microsoft Copilot, Claude, ChatGPT, or any other model.
Do **not** use Playwright, Chromium, Comet, or any non-Safari browser.

**Browser rule (non-negotiable on this Mac):** all open / interact / harvest steps use **Safari** via the `safari-browser` skill scripts under `~/.grok/skills/safari-browser/scripts/`.

**Two execution modes (priority order):**

1. **Safari automation mode (primary):** open both services in Safari, confirm settings, submit the identical prompt, wait for completion, harvest page text with Safari extract scripts, synthesize.
2. **Prompt-pack + Safari harvest / paste mode (fallback):** if UI submit cannot be completed reliably, emit the two ready-to-paste prompts, open the URLs in Safari for the user, track the run, and when replies are available (pasted by the user or harvested from the open Safari tabs), perform synthesis and write `massive-YYYY-MM-DD-HHMM.md`.

## Safari tooling (required)

Always load and follow `~/.grok/skills/safari-browser/SKILL.md`. Happy path commands:

```bash
SAFARI="$HOME/.grok/skills/safari-browser/scripts"

# Open a service (authenticated Safari session)
bash "$SAFARI/safari_open.sh" 'https://grok.com/'
bash "$SAFARI/safari_open.sh" 'https://gemini.google.com/app'

# Harvest response text from the current or specified tab
bash "$SAFARI/safari_read_page.sh" 'https://grok.com/' \
  --output /tmp/massive-grok.txt --wait 12

bash "$SAFARI/safari_read_page.sh" 'https://gemini.google.com/app' \
  --output /tmp/massive-gemini.txt --wait 12

# Already-open tab (faster re-read while waiting for generation)
python3 "$SAFARI/safari_extract_fast.py" 'https://grok.com/' \
  --no-open --output /tmp/massive-grok.txt --wait 2
```

**Forbidden for this skill:** Playwright, Chromium, `web_fetch` as the transcript source for gated chat UIs, Comet multi-model launchers.

## Required Workflow

### 1. Ingest context

- Use `read_file`, `grep`, `list_dir`, `memory_search` to gather the **minimum** local context needed (code, specs, prior results, AGENTS.md constraints, etc.).
- Never send more than necessary; keep the prompt focused.

### 2. Build canonical prompt

- One identical prompt for **both** models.
- Include the user’s objective + minimum context + explicit output shape requested by the user (or a concise task-appropriate default).
- Before finalizing, check whether the prompt transmits sensitive data. If so, list the exact data and **both destinations** (Grok Heavy, Gemini) and **ask for confirmation** before any Safari open/submit or paste instructions.

### 3. Track the run

Write a lightweight state file (e.g. `.massive-run-YYYYMMDD-HHMM.json` or `.md`) recording:

- original request
- canonical prompt
- timestamp
- models targeted: Grok (Heavy), Gemini (Thinking)
- status per model (`pending` / `submitted` / `received` / `blocked`)
- browser: Safari

### 4. Safari submit path (primary)

1. **Sensitive-data gate** already passed (or confirmed by user).
2. Open **new chats** for each model in Safari (prefer separate tabs/windows so both can run):
   - Grok: `https://grok.com/`
   - Gemini: `https://gemini.google.com/app`
3. **Verify settings before submit:**
   - Grok: conversation mode / model control shows **Heavy**
   - Gemini: mode shows **Thinking**
4. If a required setting cannot be verified or selected, **do not invent a substitute mode**. Mark that model `blocked`, state the exact UI blocker, and ask the user how to proceed (manual set, skip model, or fallback paste).
5. Submit the **identical** canonical prompt to each model that is ready (one atomic user message per model). Prefer:
   - clipboard paste of the full prompt into the chat composer, then send
   - AppleScript / System Events only as needed for paste+submit
   - never Playwright
6. Prefer starting both runs, then alternating harvest polls rather than idle-waiting on one model only.
7. **Harvest** with `safari_read_page.sh` / `safari_extract_fast.py` into run-local files (e.g. under the active project’s `experiments/` or `/tmp/massive-<run-id>-{grok,gemini}.txt`).
8. Re-poll until each response looks complete, or until a clear timeout / incomplete state is reached. Do not invent missing content.
9. Proceed to synthesis.

### 5. Fallback: prompt pack + Safari open

If automated submit fails or is unreliable:

1. Emit a ready-to-copy block for **each** of the two models:
   - Exact model + required setting
   - Full prompt text (one atomic message)
2. Open both URLs in Safari for the user.
3. Instruct: set **Heavy** (Grok) / **Thinking** (Gemini), paste, send.
4. Either:
   - user pastes both answers back labeled `Grok:` / `Gemini:`, or
   - agent harvests the open Safari tabs after the user signals completion.
5. Then synthesize.

### 6. Collect & synthesize

For each model response:

- model name
- selected setting (confirm it matched the table: Heavy / Thinking)
- prompt submitted (or reference to the canonical one)
- response text (full harvest or as pasted)
- whether the response appears complete

Write the final `massive-YYYY-MM-DD-HHMM.md` (or user-specified path) using LF line endings.

## Prompt Handling

- Build one canonical prompt from the user’s request + minimum local context.
- Keep the prompt **identical** across Grok and Gemini.
- Do not add hidden instructions to favor either model.
- Do not ask different questions to different models.

## Markdown Output Document

Create (via `write`) a file named `massive-YYYY-MM-DD-HHMM.md` (or user path) containing exactly:

1. Title and timestamp.
2. Original prompt (the canonical one sent).
3. Models run (Grok Heavy, Gemini Thinking) and browser (Safari).
4. One summary per model (~500 characters each; quote key passages).
5. Synthesis section:
   - Where the models agree (strongest dual-model consensus)
   - Where the models disagree (with model attributions)
   - Unique responses or angles split by model
6. **Orchestrator analysis** based on the combined feedback:
   - State the strongest supported conclusion early.
   - Bound it with exact assumptions, limits, and unresolved questions.
   - Surface any PGS-relevant invariants or contracts if the workspace AGENTS.md applies.

## Guardrails

- **Only** Grok (Heavy) and Gemini (Thinking). No other models.
- **Only** Safari for browser work. Never Playwright / Chromium / Comet for this skill.
- Never silently change the prompt per model.
- Never invent or complete truncated model responses.
- Sensitive-data check is mandatory before any external submission (Safari or paste).
- In prime-gap-structure workspaces: the canonical prompt must respect the PGS-first contract (PGS objects → invariants → rules) if the question touches the domain. The synthesis must not downgrade proved deterministic results to probabilistic language.
- The skill never replaces the user’s actual question with a “safer” or narrower one.
- Output the synthesis document even if only one model responded; clearly label the missing model.

## Success Criteria

- The user receives either:
  - (Safari mode) a complete dual run with both answers harvested from Safari, or
  - (fallback) a clean two-model prompt pack + Safari tabs opened + state tracking + synthesis when answers are available.
- The final synthesis document is immediately usable: strongest conclusion first, disagreements explicit, limits precise.
- No model response is distorted or completed by the skill.
- Artifact naming and structure match this document.

## Usage Notes

```text
/massive <your hard question>
```

Or invoke the skill directly with the question and optional context paths.

Expected agent behavior:

1. Ingest minimum context → build one prompt → write run tracker.
2. Open Grok + Gemini in **Safari**, enforce **Heavy** + **Thinking**, submit the same prompt.
3. Harvest both replies via Safari extract scripts.
4. Write `massive-YYYY-MM-DD-HHMM.md` with dual-model synthesis.

If submit automation cannot verify settings or complete paste/send, fall back to the two-block prompt pack while still using Safari for open + harvest.
