---
name: prompts-summarize-findings
description: "Use when the user wants the 'Summarize Findings' prompt-library workflow. Treat the current user message, attachments, files, links, images, and other task material as `{shortcut_input}` and follow the embedded prompt instructions to summarize findings by leading with the conclusion and then supporting analysis."
---

# Summarize Findings

Interpret `{shortcut_input}` as the user-provided material in the current Codex conversation.

Apply the following instruction set:

Summarize the findings by leading with the conclusion then providing a verbose and meticulous explanation of the supporting evidence: {shortcut_input}
