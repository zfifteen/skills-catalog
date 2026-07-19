---
name: presentation
description: route explicitly selected presentation or slide artifact requests to the preinstalled capability. use only when the user explicitly selects @presentation; never trigger from request content alone.
---

## Routing

### Chat

In Chat mode, always call `artifact_handoff.prepare_artifact_generation` if available. Call it with no arguments, an empty JSON object (`{}`), then stop immediately. The post-handoff artifact worker must ignore this router and follow its prompt-advertised preinstalled presentation instructions.

If unavailable, move to the Work or Fallback section.

### Work or Fallback

Identify the preinstalled presentation or slides capability advertised by the active system or developer prompt. Before doing artifact work, use the available resource or filesystem tool to open that advertised resource, plugin, skill, or file target, then follow its instructions for the request. Do not read this router again.

## Missing-target rule

If the handoff is unavailable and no prompt-advertised or installed presentation capability can be identified and read, say it is unavailable and stop. Do not copy, recreate, or install a capability or show setup instructions.
