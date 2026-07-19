---
name: grok-task-v3-most-important-development
description: "Use when the user wants the 'Most Important Development' Grok Task V3 workflow. Treat the current user message, attachments, files, links, images, and other task material as the working context and follow the embedded prompt instructions. Core instruction: Deeply examine the Git repository in the current working directory."
---

# Most Important Development

Interpret the current Codex conversation material as the input context for this workflow.

Apply the following instruction set:

Deeply examine the Git repository in the current working directory.
Your goal is to identify the single most important development activity the project owner should focus on next, based solely on an in-depth analysis of all merged pull requests (PRs).

Follow these steps precisely:

1. **Access and List Merged PRs:**
   * Use Git commands (e.g., `git log --merges --pretty=format:"%h %an %ad %s"`) to list all merged commits in the repository's history. Filter for those that appear to be pull request merges (look for commit messages containing phrases like "Merge pull request #X from branch" or similar GitHub merge patterns).
   * For each identified merged PR, fetch detailed information including:
     * PR number (if available in commit messages).
     * Title and full description.
     * All comments (including review comments, issue links, and discussion threads). If direct Git access doesn't provide comments, simulate or note that you'd need GitHub API access (e.g., via `gh pr view --json` if the `gh` CLI is installed, or suggest installing it).
   * Collect data from at least the last 50 merged PRs or the entire history if smaller. Handle any private or limited-access repos by assuming public data or prompting for authentication.

2. **Deep Analysis of Descriptions and Comments:**
   * Extract key themes, pain points, and patterns from PR titles, descriptions, and comments. Categorize them into areas like:
     * Bug fixes (e.g., error handling or stability issues).
     * Feature additions (e.g., new functionalities or modules).
     * Refactorings (e.g., code structure improvements).
     * Performance optimizations (e.g., efficiency enhancements).
     * Documentation updates (e.g., README or usage guides).
     * Dependencies or integrations (e.g., library updates).
     * Testing enhancements (e.g., unit tests or CI improvements).
   * Identify recurring motifs: Look for frequently mentioned issues (e.g., a specific keyword appearing in >20% of PRs), unresolved debates in comments, or escalations (e.g., PRs with many revisions).
     * Quantify where possible: Count occurrences of keywords using tools like grep or simple scripting.
     * Analyze sentiment: Note positive/negative tones in comments (e.g., frustration with certain features vs. praise for others).
     * Cross-reference with project goals: Align with the repo's overall purpose (infer from README, code structure, or commit history).

3. **Identify the Single Most Important Development Activity:**
   * Synthesize the analysis to pinpoint ONE primary activity to focus on next. Prioritize based on:
     * Frequency and impact: Activities addressing the most common or severe issues (e.g., if 40% of PRs fix a certain type of bug, prioritize related refinements).
     * Strategic alignment: How it advances the project's core objectives.
     * Unresolved gaps: Areas with open questions in comments.
     * Empirical rigor: Favor activities that enable measurable improvements (e.g., based on patterns in PR data).
   * Ensure it's actionable and specific (e.g., "Refine error handling in core modules" rather than vague like "improve code").

4. **Provide Detailed Justification:**
   * Explain your choice with evidence from the PR data:
     * Cite specific PR examples (e.g., "In PR #5, comments highlighted instability in computations, echoed in PR #12 and #18").
     * Include metrics (e.g., "This theme appeared in 35% of merged PRs, with a median comment thread length of 8, indicating high discussion volume").
     * Link to project implications (e.g., "Focusing here could resolve root causes in 60% of bug-related PRs").
     * Discuss why it's the *single most important* (e.g., "It addresses root causes in 60% of bug-related PRs, outweighing other areas like documentation, which only appear in 15%").

Output your response in this structured format:
   * **Merged PR Summary:** Brief overview (e.g., total merged PRs analyzed, date range).
   * **Key Themes Extracted:** Bullet list of top 3-5 themes with evidence.
   * **Most Important Development Activity:** Clear statement of the one focus area.
   * **Detailed Justification:** 3-5 paragraphs with citations and reasoning.

Be thorough, objective, and evidence-based. If data is insufficient (e.g., no merged PRs), state that and suggest alternatives like checking GitHub directly.
