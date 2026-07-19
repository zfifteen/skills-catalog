---
name: youtube
description: >
  Obtain accurate, timestamped YouTube video transcripts (preferring manual captions over auto-generated) as the primary deliverable, then derive summaries, key claims, or notes from that transcript. 
  Use when the user provides a YouTube URL (or video ID) and wants the transcript, a faithful summary, key claims with attribution, timestamped notes, or "what does this video actually say". 
  The skill is transcript-first: never substitute metadata, title, description, or search snippets for the spoken content. 
  Triggers: "youtube transcript", "get the transcript of this video", "summarize this youtube video", "what did they say in https://youtube.com/...", "key claims from this talk".
when-to-use: "Any request involving a YouTube video where the actual spoken words matter. Always retrieve the transcript before summarizing or analyzing. Complements Grok web_search / x tools; this skill owns the specialized caption extraction path via yt-dlp + youtube-transcript-api."
allowed-tools: ["run_terminal_cmd", "read_file", "write", "web_search", "open_page", "open_page_with_find"]
argument-hint: "<YouTube URL or video ID> [transcript|summary|claims] [--languages en,fr]"
---

# YouTube Transcript Skill (Grok Port)

**Core Contract (preserved from Codex):** The transcript is the primary objective and source of truth. All higher-level outputs (summaries, claims, takeaways) are strictly downstream of the extracted transcript text. Do not begin reasoning or summarizing from metadata.

## When This Skill Activates

Any time a user supplies a YouTube link (watch, youtu.be, shorts, live, embed) and asks for transcript, details, summary, claims, notes, or "what the video says". Even if they only say "summarize this video", the work centers on transcript retrieval first.

## Deterministic Workflow

1. **Resolve the video**
   - Parse URL or ID to a canonical 11-char video ID.
   - Fetch rich metadata via yt-dlp (title, uploader, channel, upload_date, duration, description, view_count, webpage_url).
   - This step confirms the target and supports transcript lookup.

2. **Obtain the transcript (the real work)**
   - Preferred: manually created captions (highest fidelity).
   - Fallback: auto-generated captions only when manual are unavailable.
   - Languages: default "en"; user may pass `--languages en,es,fr`.
   - Fail explicitly and cleanly if transcripts are disabled, video unavailable, or no transcript found for the requested languages.
   - Never fabricate dialogue or infer speech from thumbnails/comments.

3. **Normalize**
   - Clean only as needed: strip whitespace, decode entities if present, preserve start/duration timestamps.
   - Do not rewrite wording, paraphrase, or "improve" the transcript at this stage.

4. **Output transcript-first**
   - Always surface transcript status + type (manual vs auto-generated).
   - Provide the full (or meaningfully excerpted) timestamped transcript.
   - Only then, if requested, produce a summary or claims list that explicitly cites the transcript as its source.

## Local Tool (The Script)

The bundled script lives at:
`<dirname of this SKILL.md>/scripts/youtube_transcript.py`

Invoke examples (via `run_terminal_cmd`):
```bash
python3 "<SKILL_DIR>/scripts/youtube_transcript.py" metadata "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
python3 "<SKILL_DIR>/scripts/youtube_transcript.py" transcript "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --json
python3 "<SKILL_DIR>/scripts/youtube_transcript.py" transcript "dQw4w9WgXcQ" --languages en,es
```

The script:
- Accepts URL or bare video ID.
- Resolves metadata.
- Prefers manual captions.
- Emits plain timestamped text by default; `--json` for structured data.
- Exits with clear error messages on dependency or extraction failures.

**Dependency handling (exact messages preserved/adapted):**
If yt-dlp or youtube-transcript-api are missing, the script prints the exact one-line pip install targeting /tmp/grok-youtube-deps and exits with code 2. Instruct the user (or run via terminal) to install, then re-invoke with `PYTHONPATH=/tmp/grok-youtube-deps python3 ...`.

## Response Modes (Grok Context)

**Full transcript request:**
- Video metadata (title, uploader, id, etc.)
- transcript_type (manual | auto-generated)
- Timestamped transcript lines (`MM:SS\ttext` or `HH:MM:SS\ttext`)
- If very long, return first N lines + "remainder available on request" + offer to continue or summarize specific sections.

**Transcript-backed summary / claims:**
- Explicit statement: "Summary derived from the extracted transcript (type: manual/auto-generated)."
- Bulleted main points or claims, each traceable to timestamp ranges where possible.
- No invention. Attribute claims to the speaker/video.

**Failure report:**
- "Transcript could not be obtained."
- Exact failure reason from the script.
- Any successfully retrieved metadata.
- No invented summary or "the video probably says...".

## Guardrails

- Transcript retrieval is always the priority step.
- Label auto-generated captions clearly.
- Preserve uncertainty; do not smooth over unclear sections.
- Keep legal/medical/financial claims attributed to the speaker unless independently verified via other tools.
- For very long videos, it is acceptable (and often preferable) to work with a high-quality excerpt + offer deeper dives into specific timestamp ranges.
- Combine with Grok tools: use `web_search` or `x_keyword_search` for external context or reactions, but never substitute them for the transcript itself.

## Grok-Specific Adaptations

- The native Grok web tools (`open_page`, etc.) are great for the video page metadata or comments, but **this skill owns caption extraction** because many videos have captions that are not visible in the rendered page HTML.
- When the transcript is obtained, you may feed excerpts into other analysis skills or use Grok's reasoning directly.
- For videos without any captions, state the limitation plainly and offer alternatives (e.g., "No transcript available; would you like me to analyze the description + comments via web tools?").
- JSON mode is excellent for piping into downstream Grok tasks or memory.

## Success Criteria

- The transcript (or clear failure) is obtained and presented before any summary work.
- User can see exactly which captions were used (manual vs auto).
- Timestamps are present and accurate.
- Any derived analysis is explicitly anchored: "Based on the transcript at 03:45–04:12...".
- Dependencies are handled with copy-pasteable install commands.
- No hallucinated quotes or claims.

The user should feel: "I have the actual words from the video, timestamped, and anything else I asked for is directly supported by that transcript."

This port keeps the transcript-first discipline of the original Codex skill while making the helper script and invocation patterns natural for a Grok agent using `run_terminal_cmd` and the surrounding tool surface.
