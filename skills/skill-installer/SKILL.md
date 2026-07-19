---
name: skill-installer
description: >
  Discover, fetch, validate, and install Grok skills from local directories, GitHub
  repository URLs (or tree paths), or known curated collections. Creates the proper
  directory structure under the chosen scope (~/.grok/skills/, <repo>/.grok/skills/,
  or ./ .grok/skills/), validates the SKILL.md frontmatter, optionally runs a post-
  install check, and reports exactly what was installed. Use when the user says
  "install the X skill", "$skill-installer ...", "add this skill from github",
  "skill-installer", or wants to bring in a ported-from-codex or community skill.
when-to-use: Use when the user wants to install a new or updated skill (local path, GitHub URL, or named curated skill) into one of the Grok skill search locations.
argument-hint: "<skill-name-or-path-or-github-url> [to <scope: user|project|local>]"
metadata:
  short-description: "Install skills from local, GitHub, or curated sources into Grok"
  source: "ported-from-codex/skill-installer (inferred from Codex $skill-installer behavior + vendor_imports)"
  original_codex: "skill-installer (built-in Codex command / $skill-installer)"
---

# Skill Installer

Install or update Grok skills safely and repeatably.

## Scopes (in priority order for the running Grok)
- Local (CWD): `./.grok/skills/<name>/`
- Project (repo root): `<repo-root>/.grok/skills/<name>/`
- User: `~/.grok/skills/<name>/`

The skill will ask or infer the best scope (default Project if inside a git repo, else User).

## Step 1: Parse the Request
Accept inputs like:
- `my-skill` (name only — will search known locations or prompt for source)
- `./path/to/local/skill-dir`
- `https://github.com/org/repo/tree/main/skills/my-skill`
- `install the create-plan skill from .experimental`
- Named curated skills (the skill can maintain a small built-in catalog or fetch a manifest)

Resolve the source to a concrete location (local dir or clonable GitHub URL).

## Step 2: Fetch / Copy the Skill
- **Local path**: Validate it exists and contains SKILL.md. Copy (or symlink in dev mode) the entire directory.
- **GitHub URL**: Use `grok_com_github` MCP tools (get_file_contents on SKILL.md + supporting files, or fall back to `run_terminal_cmd git clone --depth 1 --filter=blob:none` + sparse checkout of the skill subtree). Or use `open_page` / `web_fetch` + manual reconstruction for simple cases.
- Create the target directory under the chosen scope using `run_terminal_cmd mkdir -p` or by writing files via the `write` / `search_replace` tools.

## Step 3: Validate the Skill (Use the Helper Script)
Always run the bundled validator:

```bash
python3 "<skill-dir>/scripts/install_skill.py" validate "<path-to-candidate-skill-dir>"
```

The script checks:
- Presence and parseability of SKILL.md
- Valid YAML frontmatter with required `name` and `description`
- `name` matches the directory name (or warns)
- No obvious dangerous content (e.g. exec in frontmatter)
- Presence of referenced scripts/ (they must exist if declared)
- Basic size / structure sanity

Only proceed on clean validation (or explicit user override after showing warnings).

## Step 4: Install / Write the Files
- For each file in the source skill (SKILL.md, scripts/*, references/*, templates/*, etc.):
  - Read source content (via `read_file` for local, MCP get_file_contents or web for remote).
  - Write to the target location using the agent's `write` tool (or `search_replace` with empty old_string for new files).
- Preserve executable bits on scripts where possible (the helper can emit `chmod +x` commands for the agent to run).
- Record an install receipt: `installed-from.json` inside the target skill dir with source, commit-ish (if git), timestamp, and validation result.

## Step 5: Post-Install
- Tell the user the exact final path.
- Instruct: "Run `grok inspect --json` or `/skills` to verify. The skill should appear within seconds (auto-reload on disk change)."
- Offer to immediately test it: "Would you like me to inject `/<name>` now and run a quick smoke test?"
- If the skill declares a `post_install` hook or test command in metadata, surface it.

## Step 6: Update / Re-install
If the target already exists:
- Show a diff summary (or full `git diff` style if the target is tracked).
- Ask for confirmation before overwriting.
- Support `--force` / "update in place".

## The Helper Script
`scripts/install_skill.py` (real Python, invoked via `run_terminal_cmd`):
- Subcommands: `validate`, `install`, `diff`, `receipt`
- Understands both local filesystem paths and can be extended for GitHub tree URLs.
- Is the single source of truth for "is this a valid Grok skill?"
- Designed to be run from the workspace root; resolves the target skill dir relative to SKILL.md location of *this* installer skill when needed.

See the script source for exact CLI and behavior.

## Success Criteria
- The installed skill is immediately discoverable by Grok (appears in `/skills` and `grok inspect`).
- All files from the source are present and bit-for-bit identical (modulo line endings on Windows).
- Validation passed or user explicitly accepted the warnings.
- The user knows exactly where it landed and how to invoke it.
- No silent overwrites of user-modified skills.

## Safety & Ethics
- Never install skills from untrusted sources without explicit user confirmation.
- Show the full source URL / path and a summary of what will be written before writing anything.
- If the skill contains references/ or large assets, warn about disk usage.
- Support "dry-run" mode that only prints the plan.

## For This Repo (Prime Gap Structure)
When installing skills here, prefer the project scope (`<repo>/.grok/skills/`) so the whole team benefits. After install, review the new skill against AGENTS.md before using it on PGS work.

## Related Skills
- `create-skill` (the bundled interactive creator) — use this installer to bring in ports or community skills; use create-skill for brand-new ones authored in-session.
