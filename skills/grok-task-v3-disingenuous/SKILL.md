---
name: grok-task-v3-disingenuous
description: "Use when the user wants the 'Disingenuous' Grok Task V3 workflow. Treat the current user message, attachments, files, links, images, and other task material as the working context and follow the embedded prompt instructions. Core instruction: Analyze the provided comment for instances of disingenuous argumentation, including but not limited to cherry-picking..."
---

# Disingenuous

Interpret the current Codex conversation material as the input context for this workflow.

Apply the following instruction set:

Analyze the provided comment for instances of disingenuous argumentation, including but not limited to cherry-picking data, misrepresenting sources, making unfounded claims, or omitting crucial information. Identify specific misleading statements or tactics used by the poster. Then, create a list titled “Five Facts That Counter [poster's name] Disingenuous Claims.” In this list, include five verifiable facts that directly address and correct the identified misleading aspects. Each fact should be supported by evidence from reputable sources to ensure verifiability.

Explanation

	•	Analysis: The prompt instructs the analyzer to examine the comment for specific signs of disingenuousness, such as selective use of facts or unsupported assertions, ensuring a thorough evaluation.
	•	List Title: The title “Five Facts That Counter the Poster’s Disingenuous Claims” explicitly highlights the poster’s lack of sincerity or honesty, meeting the requirement to show disingenuousness.
	•	Verifiable Facts: By requiring five facts supported by reputable sources, the prompt ensures the response is credible and can be independently checked, fulfilling the “verifiable” criterion.
