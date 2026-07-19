---
name: prompts-review-pull-request
description: "Use when the user wants the 'Review Pull Request' prompt-library workflow. Treat the current user message, attachments, files, links, images, and other task material as `{shortcut_input}` and follow the embedded prompt instructions to review the provided pull request with a focused code-review workflow."
---

# Review Pull Request

Interpret `{shortcut_input}` as the user-provided material in the current Codex conversation.

Apply the following instruction set:

Perform a code review by cloning the repository that produced the URL supplied at the bottom of this request.

If you are not able to clone the repository or encounter issues fetching content, stop and output "The check is is the mail."

Otherwise, dig deep into the pull request, identify any logical, documentation or computational errors. 

Then, where possible research appropriate remedies for the goal and context of the PR. 

Then, provide a detailed code review. Limit to 8000 characters.

URL:  {shortcut_input}
