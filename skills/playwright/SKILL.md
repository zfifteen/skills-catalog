---
name: playwright
description: >
  Automate a real browser from the terminal for navigation, form filling, element interaction, snapshots, screenshots, PDF capture, tracing, and UI flow debugging. 
  Use the bundled `playwright_cli.sh` wrapper (npx-based, no global install required) or a global @playwright/cli. 
  Use when the user needs deterministic browser automation, live element reference workflow (snapshot → interact by stable ref like e12), debugging of web UIs, scraping with interaction, or capturing artifacts (screenshots, traces, PDFs) that web_search/open_page tools cannot provide because they lack full JS execution, sessions, or headed visual inspection.
  Trigger phrases: "use playwright", "browser automation", "fill the form with playwright", "take a playwright snapshot", "debug this UI flow", "screenshot the app with playwright", "run playwright open".
when-to-use: "Real browser automation and element-ref driven interaction where snapshot-based stable references (eNN) are required. Complements Grok web tools (open_page, web_fetch) for cases needing clicks, typing, multi-step flows, auth sessions, or visual DOM inspection. Always prefer the wrapper script for portability."
allowed-tools: ["run_terminal_cmd", "read_file", "write", "search_replace", "list_dir", "grep", "web_search", "open_page"]
argument-hint: "<browser task e.g. 'open https://example.com/login, snapshot, fill credentials, submit, screenshot the dashboard'>"
---

# Playwright CLI Skill (Grok Port)

Drive a real browser (Chromium, Firefox, or WebKit) from the terminal using the Playwright CLI. This is a **CLI-first automation skill**. The primary interface is the bundled wrapper script that ensures the CLI works via `npx --yes` even without a global `@playwright/cli` installation.

**Grok Adaptation:** Grok's built-in tools (`open_page`, `web_fetch`, `web_search`) are excellent for one-shot content retrieval and research. Use **this skill** when you need:
- Interactive multi-step flows (login → navigate → act)
- Stable element references that survive DOM changes (the `eNN` snapshot system)
- Headed visual debugging
- Full tracing, HAR, video, or PDF capture of real browser sessions
- JavaScript-heavy sites where static fetch is insufficient

Do not pivot to writing `@playwright/test` specs unless the user explicitly requests test code.

## Prerequisite Check (Always First)

Before any commands, verify `npx` availability via `run_terminal_cmd`:

```bash
command -v npx >/dev/null 2>&1 && echo "npx OK" || echo "npx MISSING"
node --version || true
npm --version || true
```

If `npx` is missing:
- Instruct the user to install Node.js (LTS recommended) for their OS.
- Provide the exact global install once Node is present:
  ```bash
  npm install -g @playwright/cli@latest
  playwright-cli --help
  ```
- Then proceed.

Once `npx` exists, the wrapper (preferred) works immediately.

## The Wrapper Script

Location (resolve relative to this SKILL.md using the absolute path provided by the Grok skills system):

`<dirname of this SKILL.md>/scripts/playwright_cli.sh`

Export convenience in your thinking or commands:
```bash
export PWCLI="<absolute path to scripts/playwright_cli.sh>"
```

The wrapper:
- Runs `npx --yes --package @playwright/cli playwright-cli ...`
- Honors `PLAYWRIGHT_CLI_SESSION` env var for persistent browser contexts (unless `--session` is passed explicitly).
- Is fully portable across user and project skill installations.

Always prefer the wrapper unless the environment already has a well-maintained global `playwright-cli`.

## Core Workflow (Snapshot → Act Loop)

1. **Open** the target (use `--headed` for visual debugging when helpful):
   ```bash
   "$PWCLI" open https://example.com --headed
   ```

2. **Snapshot** to obtain stable element references (`e1`, `e2`, ...). This is **mandatory** before referencing any element by id:
   ```bash
   "$PWCLI" snapshot
   ```

3. **Interact** using the refs from the latest snapshot:
   - `click e3`
   - `dblclick e7`
   - `fill e5 "user@example.com"`
   - `type "search terms"`
   - `press Enter`
   - `drag e2 e8`
   - `select e4 "Option Value"`
   - etc.

4. **Re-snapshot** after any navigation, major DOM mutation, modal open/close, tab switch, or when a ref command fails because the element is stale.

5. **Capture artifacts** as needed:
   - `screenshot` (or `screenshot --full-page`)
   - `pdf`
   - `tracing-start` / `tracing-stop` (for traces)
   - `har` etc.

Minimal reliable loop example:
```bash
"$PWCLI" open https://example.com/login --headed
"$PWCLI" snapshot
"$PWCLI" fill e1 "user@example.com"
"$PWCLI" fill e2 "secret123"
"$PWCLI" click e3
"$PWCLI" snapshot
# ... continue with new refs
```

## Recommended Patterns

**Form fill + submit:**
```bash
"$PWCLI" open https://example.com/form
"$PWCLI" snapshot
"$PWCLI" fill e1 "user@example.com"
"$PWCLI" fill e2 "password123"
"$PWCLI" click e3
"$PWCLI" snapshot
```

**Debug UI flow with tracing:**
```bash
"$PWCLI" open https://example.com/complex-flow --headed
"$PWCLI" tracing-start
# interactions...
"$PWCLI" tracing-stop
# Open the produced trace with playwright trace viewer or upload
```

**Multi-tab / context work:**
```bash
"$PWCLI" tab-new https://example.com
"$PWCLI" tab-list
"$PWCLI" tab-select 0
"$PWCLI" snapshot
```

**Session persistence (advanced):**
Set `PLAYWRIGHT_CLI_SESSION` to a stable name before starting a long flow; the wrapper will attach to it automatically.

## References (Original Codex)

- `references/cli.md` (core commands) — the most common verbs are shown above.
- `references/workflows.md` — practical end-to-end flows and troubleshooting (read on demand for complex scenarios).

In this Grok port, the commands and loop discipline are preserved inline. For full original reference text, the source Codex skill files remain available at `~/.codex/skills/playwright/`.

## Guardrails (Non-Negotiable)

- **Always snapshot before using `eNN` refs.** Never guess or hardcode element ids.
- Re-snapshot on any navigation or significant change. Stale refs are the #1 source of failures.
- Prefer explicit CLI commands over raw `eval` or code execution unless you have a very good reason.
- When no fresh snapshot exists, use placeholder refs (`eX`) and explicitly state why you are doing so.
- Use `--headed` (or the equivalent) when a human or visual inspection will help debug.
- Capture artifacts into `output/playwright/` (create the dir via terminal) when working inside a project. Avoid scattering files at repo root.
- This skill is for **automation and debugging**, not for writing Playwright test suites (unless user explicitly asks for `.spec.ts` files).
- Combine with Grok web tools: use `open_page` or `web_fetch` for initial reconnaissance, then hand off to Playwright only for the interactive or snapshot-driven portion.

## Grok-Specific Notes

- The `run_terminal_cmd` tool is how you invoke the wrapper and all browser actions. Capture its output (especially snapshot results) carefully.
- For purely read-only content extraction where no interaction or JS state is required, prefer Grok's native `open_page`, `open_page_with_find`, `web_fetch` first — they are faster and do not consume browser sessions.
- When the task involves authentication that must persist across turns, use a named session via the `PLAYWRIGHT_CLI_SESSION` mechanism and document the session name for the user.
- Screenshots and other artifacts produced by the CLI can be read later with `read_file` (Grok vision will describe them) or moved into the conversation.

## Success Criteria

- The browser task completes with stable, reproducible element-ref commands.
- Every interaction step is preceded by a fresh `snapshot` (or explicit justification why not).
- Artifacts (screenshots, traces, PDFs) are produced at documented paths and inspected where relevant.
- User receives clear, copy-pasteable command sequences plus the final state or artifact locations.
- If the site is heavily protected or the CLI fails, the failure is reported with exact error output and suggested next steps (different browser, headed mode, updated selectors via snapshot, etc.).

The user should feel: "I can drive the browser exactly like a human would, using stable references, and I have the screenshots/traces to prove every step."

## Installation Reminder (for Users)

After the first use of the wrapper, Playwright browsers may need installation:
```bash
npx --yes playwright install chromium  # or firefox, webkit
```
The wrapper will surface the exact message if needed.
