---
name: pdf
description: route explicitly selected pdf artifact requests to the preinstalled capability. use only when the user explicitly selects @pdf; never trigger from request content alone.
---

## Routing

Immediately after reading this router, use the next tool call to open the preinstalled PDF artifact capability advertised by the active system or developer prompt, whether it is exposed as a skill, plugin, resource, or file. Do this before artifact work and follow the PDF capability's instructions for the request. Do not read this router again.

Fallbacks only if that advertised target cannot otherwise be opened: in Chat, open `/home/oai/skills/pdfs/SKILL.md`; in Work, open `/root/.codex/skills/builtins/pdf/SKILL.md`.

## Missing-target rule

If neither the prompt-advertised PDF capability nor the matching fallback can be read, say it is unavailable and stop. Do not copy, recreate, or install a capability or show setup instructions.
