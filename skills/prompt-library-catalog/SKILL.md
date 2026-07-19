---
name: prompt-library-catalog
description: >
  Emit a clean, numbered catalog of the prompt-library skills (focused analysis, review, insight, scaffolding, and synthesis workflows ported from Codex/Shortcuts). 
  Use when the user asks to "list my prompt skills", "show the prompt library", "what prompt-library skills are available", "catalog the prompts", "prompt catalog", or runs /prompt-library-catalog. 
  Also use proactively when a user seems unaware of the available specialized prompt workflows.
when-to-use: "Return ONLY a plain numbered list in the exact canonical format with no introduction, summary, headers, or commentary. Filter if the user requests a subset. Strong trigger for inventorying focused prompt tools."
metadata:
  short-description: "Numbered catalog of prompt-library skills"
---

# Prompt Library Catalog

Return **only** a numbered list. Every entry must follow this exact format:

```
1. [Prompt Name]: A concise description of the prompt
```

**Strict rules:**
- No introductory sentence, no summary paragraph, no closing remarks.
- No grouping headers, no nested bullets, no extra commentary or explanations.
- Preserve exact prompt names from the source of truth.
- Do not include internal skill IDs, file paths, or `$` handles unless the user explicitly asks for them.

## Source of Truth

Read the file `references/catalog.md` located in the same directory as this SKILL.md (resolve via the system-provided absolute path to the skill file, then sibling `references/`).

Use the descriptions and names exactly as listed there. If the catalog reference is missing or unreadable, fall back to a minimal in-memory list of the Batch 5 prompt skills (the 11 core ones) but still output only the numbered list.

## Workflow

1. **Load catalog**: Use `read_file` on the absolute path to `references/catalog.md`.
2. **Parse entries**: Extract the numbered items under the relevant section (Core Prompt Library Skills or equivalent).
3. **Filter if requested**:
   - Full catalog request (default): emit every entry.
   - Subset request (e.g., "only the review/fix ones", "the insight skills", "scaffolding prompts"): emit only matching entries while preserving the numbered-list format (renumber sequentially from 1 for the filtered result).
4. **Output**: Print the list and nothing else.

## Success Criteria

- Output contains nothing except the numbered list lines.
- Names and descriptions match the reference exactly (or faithful adaptation for Grok context).
- If filtering, the filter is applied intelligently against names and descriptions.
- User can copy-paste the list directly into notes or another prompt.

## Grok-Specific Adaptation

This skill works in any context. When invoked inside a project that contains the `skills/ported-from-codex/` tree (such as prime-gap-structure), it can optionally cross-check discovered subdirectories under `ported-from-codex/` via `list_dir` for additional ported prompt skills and merge them into the emitted list (still as plain numbered output). This keeps the catalog live as more batches are ported.
