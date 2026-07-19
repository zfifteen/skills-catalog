---
name: gh-project
description: >
  Create new GitHub repositories with low-friction, default-first interactive menus. Infer a complete plan (owner, location under ~/IdeaProjects, visibility public, MIT license, README+MIT, safe slug names, generated description and topics) then walk the user through every configurable setting using structured choice menus before final confirmation. Never create until the user explicitly selects "Create GitHub project".
  Use when the user invokes /gh-project or $gh-project, asks to create a new GitHub project/repo/repository, or wants a local folder plus GitHub repository created from inferred defaults.
when-to-use: "User wants to bootstrap a new GitHub repository + local clone with sensible defaults (public, MIT, README, good topics). 'create a new repo', 'start a new project on GitHub', 'gh project for my new idea X', 'set up a GitHub repo for this'."
allowed-tools: ["run_terminal_cmd", "read_file", "list_dir", "ask_user_question", "grok_com_github", "web_search"]
argument-hint: "<project name or short description> [private|org-name]"
metadata:
  short-description: "Low-friction GitHub repo + local clone wizard with smart defaults and full menu coverage"
  source: "Codex 'gh-project' skill (ported 2026-05-24)"
---

# GitHub Project (Grok Port)

## Overview

Create a new GitHub repository and matching local clone from a default-first plan. In this skill, "GitHub project" means a GitHub repository unless the user explicitly asks for a GitHub Projects board.

**Do not create anything until the user explicitly confirms `Create GitHub project`.**

The interaction is deliberately low-friction: every configurable setting gets a native structured menu (via the `ask_user_question` tool), defaults are always the first option and clearly marked `(Recommended)`, and the user can accept the entire inferred plan by repeatedly choosing the recommended option.

## Defaults (inferred before any menus)

- **Artifact**: GitHub repository (not Projects board).
- **Owner**: active authenticated account (from `gh auth status` or MCP `get_me`).
- **Parent location**: `~/IdeaProjects` (expanded).
- **Visibility**: public.
- **License**: MIT.
- **Initial contents**: README plus MIT license.
- **Repo features**: GitHub defaults (do not toggle issues/wiki/projects/discussions unless requested).
- **Folder name**: GitHub-safe slug inferred from the project name/purpose.
- **Repo name**: same as folder name (unless user requests otherwise).
- **Friendly name**: human-readable title inferred from the request.
- **Description**: generated from the project purpose, capped at 350 characters, plain and searchable.
- **Topics**: 6–10 GitHub repository topics optimized for discoverability (search terms users would actually use).

Topics are **repository topics**, not issue labels and not hashtag text.

## Prerequisites Check

Before any menus:
1. Verify `gh --version` (or MCP github connectivity).
2. Verify authentication (`gh auth status` or MCP `get_me`).
3. If `gh` / MCP github is missing or unauthenticated, stop and report the exact blocker with install/auth instructions.

Resolve the active owner name.

## High-Level Wizard Flow (use ask_user_question for each)

Present one setting at a time. The first option in every menu is the inferred default with `(Recommended)`.

Required menus, in order:

1. **Parent location**
   - `~/IdeaProjects (Recommended)`
   - `Specify` (then free-form input for another base dir)
   - `Do something else`

2. **Repo, folder, and friendly name**
   - The inferred names as one recommended option: `Use <slug> / <Friendly Name> (Recommended)`
   - `Change names`
   - `Do something else`

3. **Description**
   - `Use generated description (Recommended)` (show the proposed text)
   - `Specify`
   - `Do something else`

4. **Topics**
   - `Use generated topics (Recommended)` (list the 6–10)
   - `Specify`
   - `Do something else`

5. **Visibility**
   - `Public (Recommended)`
   - `Private`
   - `Do something else`

6. **License**
   - `MIT (Recommended)`
   - `Apache-2.0`
   - `GPL-3.0`
   - (Other licenses via the free-form "Other" path of ask_user_question when needed)

7. **Initial contents**
   - `README plus MIT license (Recommended)`
   - `README only`
   - `Do something else`

8. **.gitignore**
   - If the stack is clear from the request: the matching GitHub template as recommended.
   - Otherwise: `None (Recommended)`
   - Always include `Specify` and `Do something else` options as appropriate.

After names + location are confirmed, perform collision checks (see below) before the final menu.

## Collision Checks (mandatory before final confirmation)

- Expand `~/IdeaProjects` (or chosen parent) to absolute path.
- If the target local folder already exists → stop and ask for a new name.
- Check whether the target GitHub repository already exists (via `gh repo view OWNER/REPO` or MCP equivalent). If it does → stop and ask for a new name.
- Re-run the affected checks after any name/location change.

## Final Confirmation Menu

After all settings and collision checks:

- `Create GitHub project`  ← the only action that proceeds to creation
- `Change settings`
- `Do something else`

If "Change settings", offer a category menu:
- `Location or names`
- `Description or topics`
- `Visibility, license, contents, or gitignore`

After any change, re-run collision checks and return to the final confirmation menu.

## Creation (only after explicit "Create GitHub project")

Run from the chosen parent directory.

**Preferred (Grok MCP):** Use the `grok_com_github` `create_repository` tool (after schema discovery) with the resolved parameters. Then use follow-up tools for topics (`add topic` equivalents) and local clone if the MCP surface supports it.

**Fallback (gh CLI via run_terminal_cmd):**
```bash
gh repo create REPO --public --clone --add-readme --license mit --description "DESCRIPTION"
```
Adjust flags for the chosen visibility/license. Include `--gitignore TEMPLATE` only when selected.

After creation:
```bash
gh repo edit OWNER/REPO --add-topic topic-a,topic-b,topic-c,...
```

Report the local path, GitHub URL, visibility, license, description, and topics.

If any command fails, report the exact failed command and stop. Do not retry alternate paths unless asked.

## Menu Behavior (ask_user_question translation)

Every menu is rendered via the `ask_user_question` tool, with the recommended choice first, clear labels, and "Do something else" / free-form paths available.

Example for parent location (single-select):

Question: "Parent location for the new project"
Options:
- "~/IdeaProjects (Recommended)"  → use ~/IdeaProjects
- "Specify" → follow-up free-form path question
- "Do something else"

Similar structure for all other settings. The first choice is always the strong default.

For names/description/topics that are long, show the proposed value in the label or description of the recommended option.

## Stop Conditions

Stop and ask (without creating) when:
- User asks for a GitHub Projects board instead of a repository.
- `gh` / GitHub MCP is unavailable or unauthenticated.
- Active owner cannot be resolved.
- Local folder collision.
- GitHub repository name collision.
- User has not explicitly selected `Create GitHub project`.
- A required menu decision is needed but the `ask_user_question` surface is unavailable in the current mode.

## Grok-Specific Adaptations & Notes

- The original "native menus / request_user_input" surface is mapped directly onto Grok's `ask_user_question` tool (with excellent support for structured choices and free-form "Other" paths).
- MCP `grok_com_github` is the preferred integration for creation and editing operations. The skill documents both paths.
- The heavy emphasis on "every setting gets a menu even when the default is good" is preserved — this is a deliberate UX choice for low cognitive load and auditability.
- Topics are generated for discoverability (user search terms), not as marketing copy.
- The skill is intentionally chatty about the plan before creation; the user should feel they have full control without ever being surprised.

## Success Criteria

- A complete, human-reviewed plan is shown before any repository is created.
- The created repository matches the final confirmed settings exactly.
- Local clone (when requested) succeeds and is in the expected location.
- User receives a concise, actionable summary with paths and URLs.
- No creation occurs without the explicit final "Create GitHub project" selection.

This port faithfully reproduces the original Codex wizard's deliberate, default-first, fully-auditable experience using Grok's native interactive and GitHub MCP tooling.
