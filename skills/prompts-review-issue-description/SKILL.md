---
name: prompts-review-issue-description
description: "Use when the user wants the 'Review Issue Description' prompt-library workflow. Treat the current user message, attachments, files, links, images, and other task material as `{shortcut_input}` and follow the embedded prompt instructions to analyze a GitHub issue description for logic, documentation, and computational gaps."
---

# Review Issue Description

Interpret `{shortcut_input}` as the user-provided material in the current Codex conversation.

Apply the following instruction set:

Analyze this GitHub Issue for logical inconsistencies, documentation gaps, or computational hurdles in the proposed task. Research technical remedies, algorithmic strategies, or architectural patterns that align with the stated goal and context. If the issue is technically sound, complete, and actionable as written, output exactly “Approved”. Otherwise, provide a complete, revised issue description that resolves all identified flaws, followed by a detailed explanation of the changes made. Limit the entire response to 8,000 characters.

URL: {shortcut_input}
