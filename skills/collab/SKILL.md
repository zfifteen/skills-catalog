---
name: collab
description: Use when the user wants Collab Mode, says /collab, asks to keep Collab Mode active for the session, or asks for responses that commit and push referenced artifacts before replying and end with a bulleted list of GitHub links for every referenced artifact.
---

# Collab

Activate this skill when the user explicitly asks for `collab`, `/collab`, or a workflow where referenced artifacts must be committed and pushed before the reply is sent.

Invoking `collab` or `/collab` enters Collab Mode for the rest of the current session. Continue applying this skill on every later turn in the same session until the user explicitly asks to leave Collab Mode or the session ends.

## Behavior

When this skill is active:

- Before sending a reply, identify every workspace artifact you plan to reference.
- If a referenced artifact was created or changed in a Git repository with a GitHub remote, stage it, commit it, and push it before you send the reply.
- Do not reference a changed artifact before the push succeeds.
- Do not invent GitHub URLs. Use actual links that match the pushed remote, branch, commit, PR, or file location.
- Treat Collab Mode as session state after `collab` or `/collab` is invoked. The user does not need to repeat the trigger on later turns in the same session.

## End Of Reply Requirement

End every reply with a flat bulleted list for referenced artifacts.

- Include one bullet per referenced artifact.
- Each bullet must be a GitHub link for that artifact.
- If no artifacts were referenced, include one bullet that says no artifacts were referenced.

## Failure Rule

If an artifact you need to reference is not in a Git repository with a usable GitHub remote, or the push fails, stop and say that plainly before making artifact-based references.

Do not silently skip the commit-and-push requirement.

## Scope

Apply this rule only to artifacts referenced in the reply.

It does not require committing unrelated files that are not referenced.
