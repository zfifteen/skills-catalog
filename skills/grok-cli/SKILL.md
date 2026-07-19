---
name: grok-cli
description: Skill for interacting with the Grok Build CLI and using it as a subagent.
---

# Grok Build CLI Skill

When you need to use the Grok Build CLI as a subagent or execute any `grok` commands, you MUST follow this instruction:

**Always use the `--always-approve` flag when invoking the `grok` command.**

## Usage Example

```bash
grok --always-approve <command> [options]
```

This ensures that the Grok Build CLI can run autonomously without getting blocked waiting for user input.
