---
name: spreadsheet
description: route explicitly selected spreadsheet artifact requests to the preinstalled capability. use only when the user explicitly selects @spreadsheet; never trigger from request content alone.
---

## Routing

Identify the preinstalled spreadsheet capability advertised by the active system or developer prompt. Before doing artifact work, use the available resource or filesystem tool to open that advertised resource, plugin, skill, or file target, then follow its instructions for the request. Do not read this router again.

## Missing-target rule

If no prompt-advertised or installed spreadsheet capability can be identified and read, say it is unavailable and stop. Do not copy, recreate, or install a capability or show setup instructions.
