---
name: reiterate
description: >
  Verify comprehension before any action by restating the user's intended
  meaning in structured, domain-appropriate language. Use when the user invokes
  /reiterate, "$reiterate", "make sure you understand", "formalize this",
  "restate my intent", or wants a precise, auditable capture of a claim,
  requirement, research goal, or specification before planning, editing, coding,
  or researching proceeds. Prevents expensive mis-execution on the wrong
  interpretation.
when-to-use: "Explicitly before any non-trivial action, implementation, research probe, or edit when the request is complex, novel, or high-stakes. Also useful mid-conversation to re-anchor after scope has drifted."
allowed-tools: ["read_file", "grep", "list_dir", "memory_search", "memory_get"]
argument-hint: "<the request, claim, or artifact whose intent must be reiterated>"
metadata:
  short-description: "Precise restatement of user intent in domain language before action"
---

# Reiterate

## Purpose

Demonstrate to the user — before any tool use, edit, plan, or analysis — that their exact intent has been received and can be expressed back in the precise language of the relevant domain. This is a verification gate, not a planning or execution skill.

This is the Grok-native port of the Codex "reiterate" skill, with added memory awareness and explicit PGS-domain language support for workspaces that contain AGENTS.md.

## Strict Separation

- Reiterate only. Do not propose next steps, implementation plans, task lists, or begin using tools for the underlying task.
- Only after the user confirms "yes, that matches" or "proceed from that framing" do other skills (actualize, ooda, task-chain, search_replace, etc.) become appropriate.

## Method

1. **Identify the Concrete Elements**
   - Subject
   - Intended claim or distinction
   - Desired outcome or artifact
   - Target audience / domain / contract (e.g., "for a senior number theorist", "for the AGENTS.md contract", "for a code reviewer who will inherit this diff")

2. **Preserve Scope Exactly**
   - Do not widen, weaken defensively, or substitute a nearby abstraction.
   - Do not add safety disclaimers the user did not request.

3. **Translate into Structured Domain Language**
   - Use the vocabulary and distinctions native to the subject (for PGS work: ordered prime-gap state, divisor-count field, DNI, GWR, endpoint-chain, chamber reset, structural certificate, reciprocal transport, modulus-link closure, unresolved PGS state, etc.).
   - Name variables, invariants, constraints, regimes, and unresolved distinctions the request depends on.

4. **Separate Assertion from Request**
   - Clearly distinguish what the user appears to be asserting from what they appear to be asking the system to do.

5. **Minimal Auditable Structure**
   - Use the smallest set of headings that makes the understanding checkable.
   - Common headings (use only those that apply):
     - What I Understand
     - Structured Form (or Contract Language, Definitions and Claims, etc.)
     - Key Distinctions
     - Ambiguity To Confirm (only if genuine ambiguity exists that would change meaning)

6. **Close with Explicit Verification Sentence**
   - "If that matches your intent, I can act from this framing."
   - "The only point I would confirm before acting is ..."
   - "I understand the request as X, not Y."

## Success Criteria

- The user can reply with a single short correction or "correct, proceed" and the subsequent work will be on the right target.
- No action tools have been invoked during the reiterate turn.
- The restatement uses the user's actual concepts and the domain's native terminology, not generic assistant language.
- In a PGS workspace: the restatement demonstrates correct use of the PGS-first frame from AGENTS.md.

## Guardrails

- This skill must never leak into planning or execution.
- Do not correct the user on wording unless the difference changes the operational meaning.
- Do not introduce disclaimers, scope reductions, or "but we should also consider..." that the user did not ask for.
- Do not replace domain language with vague "helpful assistant" phrasing.
- Do not end with a menu of options or "would you like me to...".
- Higher contracts (AGENTS.md, explicit user constraints, safety) are surfaced only if they directly affect the captured intent.

## Grok Environment Notes

- `memory_search` and `memory_get` are used to pull prior context so the reiterate can be consistent with long-running threads.
- `read_file` / `grep` / `list_dir` let the skill ground the restatement in actual workspace artifacts when the user's request references them.
- After a successful reiterate + user confirmation, the clean framing produced here becomes excellent input for `actualize`, `ooda`, `task-chain`, or direct `search_replace` / `write`.

## Example (PGS-flavored, abbreviated)

**What I Understand**  
You want a precise restatement of the current open problem in leftmost-minimum-divisor selection for simultaneous multi-chamber resets, using only the language of the Divisor Normalization Identity and GWR, for the purpose of writing a one-page proof obligation map.

**Structured Form (PGS-native)**  
... (exact restatement using the required objects and invariants) ...

**Key Distinctions**  
- The distinction between a chamber reset and a modulus-link closure.  
- ...

**Ambiguity To Confirm**  
Whether the map must also cover the case of a divisor-count field that is not yet fully normalized.

If that matches your intent, I can act from this framing.

This skill is the single most effective defense against expensive "I thought you meant..." failures in technical work.
