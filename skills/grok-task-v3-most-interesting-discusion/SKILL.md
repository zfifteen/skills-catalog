---
name: grok-task-v3-most-interesting-discusion
description: "Use when the user wants the 'Most Interesting Discusion' Grok Task V3 workflow. Treat the current user message, attachments, files, links, images, and other task material as the working context and follow the embedded prompt instructions. Core instruction: You are analyzing GitHub repository discussions to identify the single most interesting one."
---

# Most Interesting Discusion

Interpret the current Codex conversation material as the input context for this workflow.

Apply the following instruction set:

You are analyzing GitHub repository discussions to identify the single most interesting one.

INPUTS
- GitHub repository URL

TASK
1. Fetch all discussions from the repository
2. Read each discussion thread completely
3. Select the ONE most interesting discussion
4. Explain your selection in exactly 8000 characters

SELECTION CRITERIA
Interesting means it demonstrates one or more of:
- Novel technical insight that challenges conventional wisdom
- Substantive disagreement that reveals deeper truths about the domain
- Original problem-solving approach with measurable impact
- Architectural decision with non-obvious tradeoffs clearly articulated
- Failed experiment with diagnostic value
- Boundary case that exposes hidden assumptions
- Performance breakthrough with reproducible evidence
- Design principle conflict resolved through first-principles reasoning

NOT interesting:
- Routine bug reports without diagnostic insight
- Feature requests without design exploration
- Documentation fixes
- Style debates without substance
- Bikeshedding
- Congratulations or social noise

OUTPUT STRUCTURE
Discussion: [exact title and URL]

Why this discussion: [8000 character analysis]

ANALYSIS REQUIREMENTS
Your 8000-character explanation must include:

1. Core claim or question (100 chars max)
   - State what makes this discussion significant in one sentence

2. Context (500-800 chars)
   - What problem prompted this discussion
   - Why conventional approaches failed or were insufficient
   - What was at stake technically

3. Key arguments (3000-4000 chars)
   - Main positions presented with specific technical details
   - Evidence or reasoning each side provided
   - Turning points where understanding shifted
   - Code, benchmarks, or data that settled disputes
   - Quote exact statements that crystallized insights

4. Resolution or outcome (1500-2000 chars)
   - What was decided and why
   - What evidence proved decisive
   - What principles or invariants emerged
   - Whether implementation followed and what it revealed
   - Any surprising consequences or follow-on discoveries

5. Why this beats all others (1000-1500 chars)
   - What competing discussions you considered
   - Why they fell short of this one
   - What unique depth, clarity, or impact this has
   - Why someone studying this domain MUST read this thread

6. Extractable lessons (500-800 chars)
   - Specific, actionable principles that generalize
   - What future work should learn from this
   - What mistakes to avoid based on this thread

CONSTRAINTS
- Use exactly 8000 characters (±50)
- No filler, hedging, or meta-commentary
- No "I think" or "it seems" - state facts
- Quote specific usernames, dates, commit hashes when relevant
- If technical benchmarks exist, cite exact numbers
- If code changed as a result, reference specific files/commits
- Zero tolerance for vagueness

Work methodically. Read all discussions. Pick the best. Explain precisely why.
