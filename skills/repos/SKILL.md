---
name: repos
description: >
  List the active GitHub account's public repositories as Markdown bullets with repository links and summaries capped at 500 characters. 
  Use when the user invokes /repos or $repos, asks for a bulleted list of public GitHub repositories with summaries, or wants a one-shot summarized public repo inventory from the currently authenticated gh account or via connected GitHub MCP.
when-to-use: "User asks to list my public repos, show my GitHub repositories, inventory of public projects, or 'what repos do I have on GitHub'. Returns clean Markdown bullets with auto-generated summaries from description or README. Complements grok_com_github MCP list/search tools when richer summaries are needed."
allowed-tools: ["run_terminal_cmd", "read_file", "web_search", "grok_com_github"]
argument-hint: "[--limit N] (defaults to all public repos via gh)"
metadata:
  short-description: "One-shot public GitHub repo inventory with README-derived summaries"
  source: "Codex skill 'repos' (ported 2026-05-24)"
---

# Repos (Grok Port)

## Purpose

Emit a clean, immediately usable Markdown list of the authenticated user's public GitHub repositories, each with a concise summary (≤500 chars) derived from the repository description or a cleaned extract of its README. This is the exact deliverable the original Codex skill produced.

**Primary path (recommended for fidelity):** Run the bundled helper script via `run_terminal_cmd`. It uses the `gh` CLI (must be installed and authenticated) and produces exactly the original output contract.

**Alternative (when grok_com_github MCP is connected and preferred):** Use the MCP tools (`get_me`, `search_repositories` or list equivalents) for basic inventory, but note that the script's README-derived summaries add unique value not always present in raw MCP responses.

## Workflow

1. **Resolve authentication & scope**
   - If `grok_com_github` MCP tools are connected and the user prefers native MCP: call the MCP schema discovery first (if names uncertain), then use `get_me` + repository listing/search tools. Document the source.
   - Otherwise (or for the signature summary behavior): invoke the helper script.

2. **Invoke the helper (primary)**
   ```bash
   python3 "<SKILL_DIR>/scripts/list_public_repos.py"
   ```
   Where `<SKILL_DIR>` is the absolute path to this skill's directory after installation (e.g. `~/.grok/skills/repos` or `<repo>/.grok/skills/repos`).

3. **Return the output verbatim**
   - The script prints one Markdown bullet per public repo.
   - Return it directly to the user with no extra commentary unless the user asked for additional processing.
   - If the script fails (e.g. `gh` not found, not authenticated, network), report the exact error from stderr and stop. Do not fall back to web scraping, search, or invented repo lists.

## The Bundled Script

Location: `<SKILL_DIR>/scripts/list_public_repos.py`

- Pure Python + `gh` CLI (no pip dependencies).
- Fetches public repos for the `gh auth` owner.
- For each: uses repo description if present; otherwise fetches README via `gh api`, strips Markdown to first ~sentence window (≤500 chars).
- Marks public forks with ` _(fork)_`.
- Repos with no usable summary text get exactly: `No public description or README summary available.`

**Example invocation (Grok agent):**
```bash
run_terminal_cmd with command is python3 "/Users/you/.grok/skills/repos/scripts/list_public_repos.py"
```

**Example output contract (preserved exactly):**
```markdown
- [prime-gap-structure](https://github.com/velocityworks/prime-gap-structure): Deep deterministic structure in prime gaps via the Divisor Normalization Identity and Leftmost Minimum-Divisor Rule.
- [flaming-horse](https://github.com/velocityworks/flaming-horse): Deterministic Manim + Qwen + ffmpeg video generation pipeline _(fork)_
- [handrail](https://github.com/velocityworks/handrail): ... (or the fallback sentence)
```

## Grok-Specific Adaptations & Integration

- **MCP preference**: If the connected `grok_com_github` server exposes convenient listing tools and the user is in a pure-MCP workflow, you may use those for the basic list and then optionally enrich summaries by cloning or fetching READMEs via `open_page` / `web_fetch` + the same cleaning logic. However, for the canonical "one-shot summarized inventory" the script remains the gold path because it encapsulates the exact summary extraction.
- **Authentication**: The script relies on `gh` being logged in (`gh auth status`). In environments where only the MCP is authenticated, fall back to MCP tools + note the limitation.
- **Rate limits / scale**: The script requests up to 1000 public repos. For very large accounts, the user can pipe or post-process.
- **Composability**: The Markdown output is designed to be pasted into issues, PRs, research notes, or fed into other skills (e.g. `prompts-issue-deep-dive`, research skills).

## Success Criteria

- The response is exactly (or clearly derived from) the script's Markdown bullet list.
- Every listed repo has a link, a summary ≤500 chars, and fork marker when applicable.
- No invented repositories or summaries.
- Failures surface the real `gh` error.
- User can immediately copy the list into GitHub, Notion, or another tool.

## Stop Conditions

- `gh` CLI missing or unauthenticated and no usable MCP github connection.
- User explicitly asks for private repos, specific orgs, or filtered subsets (then use `gh repo list` variants or MCP search directly and report).

This port preserves the original's "return the script output directly" contract while making the helper self-documenting and natural to invoke from a Grok agent equipped with `run_terminal_cmd`.
