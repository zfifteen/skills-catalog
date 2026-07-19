---
name: grok-share
description: >
  Read full public Grok online chat sessions from grok.com/share or x.com/i/grok/share
  URLs using Safari (authenticated session on this Mac). Use when the user shares a
  Grok conversation link, asks to read/import/sync/retrieve an online Grok chat
  transcript, says "get the full Grok share", "read this grok.com/share", runs
  /grok-share or /read-grok-share, or needs online session content for research.
  Happy path: ~/.grok/skills/safari-browser/scripts/safari_read_page.sh — NOT Playwright.
  Do NOT use web_fetch, curl, or x-api alone for transcripts. Complements local
  ~/.grok/sessions for CLI sessions.
metadata:
  short-description: "Extract full grok.com/share conversation transcripts"
  version: "1.0.0"
  canonical-phoenix-skill: "/Users/velocityworks/IdeaProjects/phoenix/.grok/skills/grok-share/SKILL.md"
---

# Grok Share Reader (global)

Extract **full conversation turns** from public Grok share links.

## Non-negotiable access path (this Mac)

| Method | Result |
|--------|--------|
| `web_fetch` / `curl` | SPA shell — title only, no turns |
| x-api MCP | Post metadata / preview — **not** full transcript |
| Playwright `read_share.sh` | Works but **deprecated here** — use Safari instead |
| **`safari_read_page.sh`** (safari-browser skill) | **Happy path — clean innerText in ~13s** |

```bash
bash "$HOME/.grok/skills/safari-browser/scripts/safari_read_page.sh" \
  '<grok-share-url>' --output experiments/<topic>/safari_transcript.txt --wait 12
```

Always use the Safari happy path on this machine. Never guess DOM selectors ad hoc.

## Supported URL forms

- `https://grok.com/share/bGVnYWN5_<uuid>`
- `https://x.com/i/grok/share/<id>` (X-hosted share page; same conversation)

## Quick usage

```bash
GROK_SHARE="$HOME/.grok/skills/grok-share/scripts/read_share.sh"

# Markdown to stdout (default)
bash "$GROK_SHARE" 'https://grok.com/share/bGVnYWN5_...'

# Save artifact in the active project
bash "$GROK_SHARE" 'https://grok.com/share/...' \
  --output experiments/my-topic/grok_share_transcript.md

# Structured JSON
bash "$GROK_SHARE" 'https://grok.com/share/...' --json
```

Slow networks / heavy pages:

```bash
GROK_SHARE_WAIT_SECONDS=12 GROK_SHARE_POLL_ATTEMPTS=20 \
  bash "$GROK_SHARE" '<url>'
```

Optional: set `PWCLI` to `~/.grok/skills/playwright/scripts/playwright_cli.sh` when available.

## Agent workflow

When the user provides a Grok share URL or asks for online chat content:

1. **Do not** start with `web_fetch` or x-api for the transcript body.
2. Run `read_share.sh` with the URL. Add `--output` when the project should keep a durable artifact (prefer `experiments/<topic>/` or `docs/` under the active repo).
3. Read the Markdown or JSON output as ground truth for the conversation.
4. If extraction fails, retry once with higher `GROK_SHARE_WAIT_SECONDS` / `GROK_SHARE_POLL_ATTEMPTS`.
5. Only then summarize, advance research, or align repo work to the extracted turns.

### x-api complementary role

Use x-api **after** or **beside** share extraction when you need:

- who posted or linked a share on X
- tweet context, thread replies, or outreach targets
- title/description preview from `x.com/i/grok/share/` links embedded in posts

x-api does **not** replace `read_share.sh` for full transcripts.

## Output shape

Markdown (default):

- Title, source URL, extraction timestamp, turn count
- `## Turn N — User|Grok` sections with full text

JSON (`--json`):

- `title`, `url`, `extracted_at`, `turn_count`, `turns[]` with `role` + `text`

## Script files

| File | Role |
|------|------|
| `scripts/read_share.sh` | Entry point |
| `scripts/extract.js` | DOM extraction (update if grok.com layout changes) |
| `scripts/parse_playwright_result.py` | Parse playwright-cli eval output |
| `scripts/to_markdown.py` | JSON → Markdown formatter |

## Requirements

- `npx` (installs `@playwright/cli` on demand via `npx --yes`)
- `python3`

## Limits

- **Public share links only.** Private chats need a share link or manual export.
- **Read-only.** Cannot continue the online thread from this tool.
- **Layout coupling.** Targets current grok.com share DOM. If xAI changes the page, update `extract.js`.

## Local CLI sessions (alternate path)

For sessions run in **Grok CLI** on this machine, read disk state directly:

```bash
grok sessions list
grok sessions search "keyword"
# Full log: ~/.grok/sessions/<encoded-cwd>/<session-id>/updates.jsonl
```

Use **grok-share** for online shared sessions; use **`~/.grok/sessions/`** for local CLI sessions.