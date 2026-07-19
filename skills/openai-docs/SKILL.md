---
name: openai-docs
description: >
  Deep, tool-grounded work with OpenAI platform documentation, API references, model specs, and integration patterns in codebases. Retrieve current docs, compare against implementation, surface deprecations, best-practice deltas, and produce actionable guidance or patches.
  Use when the user asks to "check the OpenAI docs for this", "audit our OpenAI integration against current docs", "what does the latest Assistants API support", "update our code to the current OpenAI SDK / API", or similar external documentation + codebase alignment tasks.
when-to-use: "User needs authoritative, up-to-date information from OpenAI's official documentation or platform API reference, or wants an audit/comparison of local code against the current OpenAI contracts. 'openai docs for the responses API', 'does our code match the current function calling spec', 'migrate this to the latest openai python sdk'."
allowed-tools: ["web_fetch", "web_search", "open_page", "open_page_with_find", "read_file", "grep", "list_dir", "search_replace", "write", "run_terminal_cmd", "todo_write"]
argument-hint: "<topic or API surface> [in codebase at <path>] [compare|update|explain]"
metadata:
  short-description: "Authoritative OpenAI platform & API documentation explorer + codebase alignment auditor"
  source: "Batch 7 external integrations (openai-docs) — synthesized high-fidelity port (original not located at ~/.codex/skills/openai-docs)"
---

# OpenAI Docs (Grok Port)

## Purpose

Provide precise, current, citation-backed answers and code actions drawn directly from OpenAI's official documentation and platform surfaces, then align or update local code against those contracts.

This skill owns the "go to the source docs first" discipline for anything OpenAI-related.

## Core Principles

- **Primary sources only**: platform.openai.com/docs, the OpenAI API reference, official SDK repos, and the exact current model cards/specs. Never rely on secondary blogs, old training data, or unverified examples.
- **Grounded in the actual codebase**: when a local path or project is in context, use `read_file`, `grep`, `list_dir` to compare implementation against the docs.
- **Actionable deltas**: when drift is found, produce exact `search_replace` or `write` recipes (or terminal commands for SDK bumps).
- **Deprecation & migration clarity**: explicitly call out removed/renamed parameters, new required fields, recommended migration paths, and timeline notes from the docs.
- **Version pinning**: always note the exact doc version / "last updated" date of the page you consulted.

## Typical Workflows

1. **Pure documentation query**
   - User asks about a specific API surface (Responses API, Assistants, fine-tuning, embeddings, vision, function calling, structured outputs, etc.).
   - Fetch the canonical page(s) with `web_fetch` or `open_page` + targeted `open_page_with_find`.
   - Return the authoritative excerpt + direct link + any "as of <date>" note.
   - Offer to compare against the user's codebase.

2. **Codebase alignment / audit**
   - User points to a directory or file that uses the OpenAI SDK or REST calls.
   - Ingest the relevant source (`read_file` / `grep` for `from openai`, `client.chat.completions`, `client.beta.threads`, etc.).
   - Fetch the matching current docs.
   - Produce a gap report: deprecated usage, missing required parameters, better patterns now available, security/timeout/pagination improvements.
   - When authorized, emit precise edit recipes.

3. **Migration or update task**
   - "Migrate this script to the latest openai>=1.0 style" or "move from Assistants v1 to the current interface".
   - Fetch the migration guide sections.
   - Walk the user through (or apply) the minimal correct changes.
   - Verify with `run_terminal_cmd` (e.g. `uv pip install "openai>=1.XX"` and smoke tests) when appropriate.

4. **New integration design**
   - User describes a desired capability.
   - Retrieve the current recommended pattern from docs (including any "best practice" or "cookbook" pages).
   - Propose the smallest viable implementation (or a tiny reference script under `experiments/` or the project-appropriate location).
   - Include exact curl / Python / TypeScript snippets from the docs + citations.

## Tool Usage Patterns (Grok native)

- `web_fetch` / `open_page` / `open_page_with_find` for the live docs (always prefer these over training data).
- `web_search` with site:platform.openai.com or site:github.com/openai for official examples.
- `read_file` + `grep` (with glob filters like "*.py", "*.ts", "requirements*.txt", "pyproject.toml") for the local integration.
- `todo_write` for multi-step audits or migrations.
- `search_replace` / `write` for producing patches.
- `run_terminal_cmd` for SDK version checks (`python -c "import openai; print(openai.__version__)"`), installs, and lightweight smoke tests.

## Output Contract

- Every factual claim about OpenAI behavior is backed by a direct link to the current docs page (and ideally a short verbatim quote or `render_inline_citation`).
- Code suggestions are the *current* recommended form, not historical.
- When drift exists between code and docs, the report explicitly lists:
  - What the code currently does (with file:line)
  - What the current docs require / recommend (with link)
  - The minimal diff to align
- Version and "as of" dates are always stated.

## Guardrails

- Do not cite or recommend patterns that the current docs mark as deprecated or "legacy".
- Do not invent API parameters or behaviors.
- When the official docs say "contact us" or "enterprise only" for a capability, report that fact exactly.
- For rate limits, pricing, or regional availability, note that these can change and point to the live dashboard/docs.

## Success Criteria

- The user receives information that is verifiably correct against the live OpenAI documentation at the moment of the query.
- Any proposed code change is the smallest delta that brings the integration into compliance with the current spec.
- The user can click the provided links and see the exact same guidance the skill used.
- SDK version bumps or pattern changes are accompanied by the minimal working example from the official sources.

## Notes on Original Source

The original Codex skill at the conventional `~/.codex/skills/openai-docs/` location was not present in the scanned installation (neither in user skills nor in the large openai-curated / openai-primary-runtime / openai-bundled plugin trees). This port is a high-fidelity, idiomatic Grok recreation of the *intended* capability for the "External Integrations & Project Skills" batch, consistent with the style and rigor of the other ports in this batch and the existing ported-from-codex collection.

It is ready for refinement once an authoritative original source text is supplied.

This skill pairs excellently with `github`, `issue`, `repos`, and any implementation or research skills when OpenAI integration work is involved.
