---
name: mail-draft
description: >
  Draft an email in the local macOS Mail app by opening a pre-filled compose window using a mailto: URL + AppleScript. 
  Use when the user says "draft an email", "open Mail and prepare a message", "prefill recipient, subject, and body in Mail", or provides email fields to populate.
  Prefer this local helper over generic Mail automation, browser mail, or MCP mail tools.
when-to-use: "Any request to draft or pre-fill an email in the native macOS Mail application. Triggers on phrases like 'draft email to...', 'mail this to X with subject Y', 'open a draft in Mail'. macOS-specific; falls back gracefully with the generated mailto: URL if osascript fails."
allowed-tools: ["run_terminal_cmd", "read_file", "ask_user_question"]
argument-hint: "--to 'recipient@example.com' --subject 'Subject line' --body 'Message body...' [--cc ...] [--body-file /path]"
metadata:
  short-description: "Open prefilled draft in macOS Mail.app via mailto: + osascript"
  source: "Codex 'mail-draft' skill + ~/.codex/tools/mailto_draft.py (ported 2026-05-24)"
---

# Mail Draft (Grok Port)

## Core Job

Open a pre-filled draft window in the user's default macOS Mail application. This skill does **not** send mail — it only stages the draft for the user to review and send.

This is the low-friction, native macOS path. It is deliberately preferred over:
- Direct `open` of the Mail binary
- Generic MCP "Mail" tools (if any)
- AppleScript `tell application "Mail"` flows written by the agent
- Browser-based mailto or webmail automation

## The Bundled Helper Script

The heart of the skill is the self-contained Python script:

**`<SKILL_DIR>/scripts/mailto_draft.py`**

It builds a properly encoded `mailto:` URL from the supplied fields and uses `osascript` to execute `open location "mailto:..."` so the system default handler (Mail.app) opens a new draft with the fields populated.

**Invocation examples (via `run_terminal_cmd`):**

```bash
python3 "<SKILL_DIR>/scripts/mailto_draft.py" \
  --to "alice@example.com" \
  --subject "Project update" \
  --body "Hi Alice,

Here is the latest status..."

# With body from file (recommended for multi-line or long bodies)
python3 "<SKILL_DIR>/scripts/mailto_draft.py" \
  --to "team@company.com" \
  --subject "Weekly report" \
  --body-file /tmp/draft-body.txt

# Dry run (just see the URL)
python3 "<SKILL_DIR>/scripts/mailto_draft.py" --to "x@y.z" --subject "Test" --body "Hi" --dry-run
```

The script accepts:
- `--to`, `--cc`, `--bcc`
- `--subject`
- `--body` (string) or `--body-file` (UTF-8 path) or stdin when non-tty
- `--dry-run`

It always prints the resulting mailto: URL to stdout (useful for logging or copy-paste).

## Workflow

1. **Gather fields from the user request**
   - Extract `to`, `subject`, `body` (and optional cc/bcc) from the current prompt or conversation.
   - If any required field is missing or ambiguous, use `ask_user_question` (or direct clarification) to obtain it. Do not guess recipients.

2. **Prepare body (multiline safe)**
   - For anything longer than a single line, write to a temp file first:
     ```bash
     body_file="$(mktemp /tmp/grok-mail-body.XXXXXX.txt)"
     cat >"$body_file" <<'EOF'
     Line one
     Line two
     ...
     EOF
     python3 "<SKILL_DIR>/scripts/mailto_draft.py" --to "..." --subject "..." --body-file "$body_file"
     ```

3. **Invoke the helper**
   - Run via `run_terminal_cmd` with the arguments above.
   - Capture the printed mailto: URL.

4. **Confirm & surface**
   - After the command succeeds, tell the user: "Draft opened in Mail.app with the following fields populated:" and list To / Subject / (body excerpt if short).
   - If `--dry-run` or the open failed, provide the mailto: URL so the user can click it or paste into a browser / mail client.

5. **Error handling**
   - If osascript or the open fails (non-macOS, no default mail handler, permissions), print the exact mailto: URL and a clear one-line explanation.
   - Never fall back to writing `.eml` files, launching web Gmail, or inventing other clients unless the user explicitly asks for behavior beyond "draft in local Mail".

## Guardrails (preserved)

- This skill **only drafts**. It never sends.
- If the user omits recipient, leave To: blank (user can fill in Mail).
- Preserve the user's exact wording for subject and body unless they ask you to rewrite.
- After opening, give a brief, factual confirmation of what was populated.
- On macOS only. On other OSes the script will fail at the osascript step; surface the mailto: URL as the portable fallback.

## Grok-Specific Notes

- The `ask_user_question` tool is the natural way to collect missing email fields mid-workflow with structured choices when appropriate.
- Combine with other skills: after drafting, the user may ask you to iterate on the body (use search_replace on the temp file then re-invoke the script) or attach files (user does this manually in Mail).
- If the environment has a different connected "mail" MCP, still prefer this native macOS path for the stated use case unless the user overrides.

## Success Criteria

- A Mail compose window opens with the requested To/Subject/Body (and cc/bcc) pre-filled.
- The user sees a clear confirmation of exactly which fields were set.
- The exact mailto: URL is available in the transcript for audit or fallback.
- No mail is sent; the draft remains fully under user control.

This port keeps the original's "prefer the local helper" philosophy while making the implementation a first-class, documented, runnable artifact inside the Grok skill.
