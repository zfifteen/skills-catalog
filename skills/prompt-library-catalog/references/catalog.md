# Prompt Library Catalog (Grok Port)

This catalog lists the specialized prompt-library workflows ported from Codex (originally Apple Shortcuts prompt menus). These are focused, high-signal skills for analysis, review, insight generation, scaffolding, and synthesis.

Use the `prompt-library-catalog` skill to emit this list in the canonical numbered format.

## Core Prompt Library Skills (Batch 5)

1. [1 Fix in PR]: Dig deep into a pull request, identify the highest-severity logical, documentation, or computational error, and provide a tightly scoped review on only that single issue. Reply "Approved" if none found. Limited verbosity.
2. [1 Fix in Repo]: Analyze a repository for the single highest-severity issue (logical, documentation, or computational), create a branch, deliver a focused review on only that issue. Add explanatory comments for any false positives. "Looks good." if clean.
3. [C Program]: Scaffold a disciplined C-program workspace under src/c/ (or equivalent) with Makefile (including parent for GMP/MFPR large-number deps, no new deps), shell demo script, and full build that produces the executable. Keep all artifacts inside the new folder.
4. [Check for Signal]: Design and execute a decisive test that definitively proves or falsifies a target hypothesis/claim (never artificially). Create artifacts folder under experiments/, meticulously document in FINDINGS.md leading with conclusion then evidence.
5. [Hidden Insights]: Surface non-obvious insights via constraint-violation analysis, cross-domain pattern matching, predictive synthesis (testable predictions table), and source-grounded reasoning with confidence flags. No fabricated citations.
6. [Issue Deep Dive]: Perform expert-level technical investigation of a GitHub issue: comprehend context (incl. comments/links), analyze sub-issues/dependencies, deep reasoning for assumptions/insights/patterns, synthesize structured findings + concrete next actions.
7. [Most Remarkable]: Analyze experiment results, data, or repo contents to identify the single most remarkable, data-backed, or highly significant finding. Provide thorough explanation of why it is remarkable or breakthrough-level.
8. [Next Step]: As expert research engineer, analyze repo + goal + constraints, build mental model of codebase/progress, then propose exactly ONE concrete, actionable, high-leverage next step with full structured output (research goal, current state, rationale, execution plan, acceptance criteria).
9. [Presentation]: Transform the provided material (notes, findings, code, research) into a clean, presentation-ready structure suitable for slides or talks.
10. [transcribe]: Produce a complete, timestamp-free transcription of the provided video, audio, or media content.
11. [Prompt Library Catalog]: Emit a clean numbered catalog of the available prompt-library skills (no extra prose, no groupings).

## Additional Notes for Grok Users

- These skills are designed for strong focus and minimal distraction. Many intentionally limit scope to "the one thing".
- Invoke via slash commands (e.g. /prompts-1-fix-in-pr) or natural language matching the description.
- When material includes GitHub URLs, local paths, or attachments, the skills use Grok tools (read_file, grep, gh CLI, web_fetch, open_page, etc.) to ground analysis in real artifacts.
- For full original Codex catalog (including many additional research-task prompts), see the source migration or expand this reference as more batches are ported.
