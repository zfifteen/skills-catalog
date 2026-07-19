---
name: safari-browser
description: >
  Use Safari (never Playwright/Chromium) for all browser automation on this Mac.
  The user is authenticated in Safari for X, Grok, Google Drive, GitHub, and other
  web services required by research workflows. Trigger on any browser task: open a
  URL, scrape a page, read a Grok share, log into a site, fill a form, take a
  screenshot, debug a web UI, or when Playwright would otherwise be chosen.
  Happy path: safari_read_page.sh or safari_extract_fast.py (AppleScript innerText).
  Interactive grok.com chat (modes, send, harvest): see references/grok-com-computer-use.md.
  Interactive gemini.google.com chat: see references/gemini-google-computer-use.md.
  Do NOT use Playwright unless the user explicitly overrides this preference.
metadata:
  short-description: "Always use Safari for browser automation (authenticated session)"
  version: "1.2.0"
---

# Safari Browser (Global Preference)

**Hard rule:** When a task needs a real browser on this Mac, use **Safari only**.
Do not open Playwright, Chromium, or headless Chrome unless the user explicitly asks.

**Why:** Safari carries the user's live sessions for X, Grok, Google, GitHub, and other services.

## Interactive grok.com (computer use)

For **live chat** on `https://grok.com` (model mode Fast/Expert/Heavy, paste prompts, wait for generation, harvest answers), do **not** invent a new approach. Follow the learned playbook:

**[references/grok-com-computer-use.md](references/grok-com-computer-use.md)**

Summary of hard-won rules:
- **NEVER BATCH.** Batch is **strictly prohibited.** One Act only, then screenshot + analyze.
- **ALWAYS screenshot, then analyze.** Decisions come from the image, not key logs.
- **Screenshot every 3–5 seconds** while operating; determine state each time; then decide.
- **OODA Loop mandatory:** Observe → Orient → Decide → Act → Observe again.
- Scroll the full reply only if shots prove content moved; action bar must be **visible in the image** before Copy.
- **Never retype the URL** if already on grok.com; new chat via **Home page** link.
- Address bar only when needed: Meta+l → Meta+a → **Backspace** → type URL → **verify field** → Return (OCU `type_text` **appends** even when selected).
- Mode: **Model select** + real cursor (not avatar **F**).
- **Harvest after each round:** action bar visible in shot → **Copy at end of that response** → clipboard (`pbpaste`). Not full-page scrape as default.

## Happy path (use this first)

Validated on `x.com/i/grok/share/...` Grok conversations (2026-07-08):

```bash
bash "$HOME/.grok/skills/safari-browser/scripts/safari_read_page.sh" \
  'https://x.com/i/grok/share/<id>' \
  --output experiments/<topic>/safari_transcript.txt \
  --wait 12
```

**What it does:** `safari_open.sh` → wait 12s → AppleScript `document.body.innerText` in 5k chunks → clean text (~21k chars in <2s after load).

**Do not use:** Playwright, `web_fetch`, raw `source` AppleScript (pre-JS shell), Cmd+A copy (gets URL only), or WebDriver `body.text` (pulls HTML junk). WebDriver `innerText` works but is slower (~22s); reserve for `--method webdriver`.

### One-shot Python (same happy path)

```bash
python3 "$HOME/.grok/skills/safari-browser/scripts/safari_extract_fast.py" \
  '<url>' --output transcript.txt --wait 12
```

### Read current tab (already open in Safari)

```bash
python3 "$HOME/.grok/skills/safari-browser/scripts/safari_extract_fast.py" \
  '<url>' --no-open --output transcript.txt --wait 2
```

## Prerequisites (enabled on this machine)

Safari → Settings → Developer:

| Setting | Required for happy path |
|---------|-------------------------|
| **Allow JavaScript from Apple Events** | Yes — `safari_extract_fast.py` |
| **Allow remote automation** | Optional — WebDriver fallback only |

## Decision order

1. **`safari_read_page.sh` / `safari_extract_fast.py`** — default for all page reads
2. **`safari_open.sh`** — navigation only
3. **`safari_extract.py --method webdriver`** — scroll-heavy pages if fast path insufficient
4. **UI scripting** — last resort only
5. **Playwright** — forbidden unless user explicitly overrides

## Agent workflow

1. **Do not** reach for Playwright or `read_share.sh` (Playwright) for X-hosted Grok shares.
2. Run `safari_read_page.sh` with `--output` under `experiments/<topic>/`.
3. If fast path fails, check Developer toggles; do not silently fall back to Playwright.
4. Save artifact; summarize conversation from the clean transcript file.

## Grok share links

For `x.com/i/grok/share/<id>` or `grok.com/share/...`:

```bash
bash "$HOME/.grok/skills/safari-browser/scripts/safari_read_page.sh" \
  'https://x.com/i/grok/share/<id>' \
  -o experiments/grok-share-<id>/safari_transcript.txt
```

## Script files

| File | Role |
|------|------|
| `scripts/safari_read_page.sh` | **Happy path entry point** |
| `scripts/safari_extract_fast.py` | AppleScript innerText extraction |
| `scripts/safari_open.sh` | Navigate Safari to URL |
| `scripts/safari_extract.py` | Wrapper; `--method fast` (default) or `webdriver` |
| `references/grok-com-computer-use.md` | **Interactive grok.com** OCU/Safari playbook (modes, Copy harvest, OODA) |
| `references/gemini-google-computer-use.md` | **Interactive Gemini** UI map (modes, tools, Stop/Copy/Redo, Temporary chat) |

## Limits

- macOS only
- Requires authenticated Safari session for gated X/Grok content
- Cannot run inside Linux CI