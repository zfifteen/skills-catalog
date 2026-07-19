---
name: google-drive
description: >
  Use the globally configured Google Drive MCP server to list, search, download,
  upload, and manage files in the user's Google Drive from any Grok project.
  OAuth and tokens live in ~/.config/google-drive-mcp/ (user-wide, not per-project).
  Trigger when the user mentions Google Drive, Drive folder sync, pulling/pushing
  files to Drive, or accessing Drive deliverables. Do not re-run OAuth setup unless
  tokens are missing or expired.
metadata:
  short-description: "Global Google Drive MCP (already configured)"
  version: "1.0.0"
---

# Google Drive MCP (Global)

Google Drive is **already configured for all Grok projects** via user-scoped MCP in `~/.grok/config.toml`.

## Do not repeat setup

Unless auth fails, **do not** ask the user to recreate OAuth clients, re-enable APIs, or add test users again.

## Global paths

| Path | Purpose |
|------|---------|
| `~/.grok/config.toml` | `[mcp_servers.google-drive]` — loads in every project |
| `~/.config/google-drive-mcp/gcp-oauth.keys.json` | OAuth client credentials |
| `~/.config/google-drive-mcp/tokens.json` | Saved tokens (auto-refresh) |

## Agent workflow

1. Confirm server is healthy: `grok mcp doctor google-drive`
2. Use MCP tools via `search_tool` / `use_tool` (namespaced `google-drive__*`)
3. For SSDI evidence work, canonical local folder:
   `~/IdeaProjects/SSDI/SSDI_Phase1_Evidence_Package_Dionisio_Lopez/`
4. Known SSDI Drive folder ID: `1HhnVzJ7IZLc6Uv_Da8VaX0leceArMLeP`

## If auth breaks

```bash
npx -y @piotr-agier/google-drive-mcp auth
```

Then `/mcps` → refresh in Grok.

## Health check (quick)

```bash
grok mcp doctor google-drive
```

Expected: healthy, 104 tools, account `dionisio.lopez@gmail.com` when Drive API responds.