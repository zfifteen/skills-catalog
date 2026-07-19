---
name: x-api
description: >
  Search, read, and write X posts through the local X API MCP server (the same
  backend used by the Codex x-api skill). Use for searching X/x.com, reading
  threads and replies, creating lists, staging/publishing posts for @alltheputs,
  finding high-visibility reply targets for research outreach, ingesting public
  context, or any request that mentions /x-api or "search X".
metadata:
  short-description: "Read/write X.com via official API (MCP)"
  version: "0.2.0"
  canonical-codex-skill: "/Users/velocityworks/.codex/skills/x-api/SKILL.md"
---

# X API (Grok side)

Local MCP harness at `/Users/velocityworks/IdeaProjects/x-api-mcp-server` with **read + write** tools for the official X API.

Auth:

- App-only bearer (`X_API_BEARER_TOKEN`) for public read/search
- OAuth2 user-context (`~/.config/x-api/user-context.env`) for me/bookmarks/lists/posting/likes/follows

Handle: **@alltheputs**.

## MCP Server & Tool Names

Registered in `~/.grok/config.toml` as `x-api`. Tools are namespaced `x-api__*`.

### Read
- `x-api__x_get_post`
- `x-api__x_search_recent_posts`
- `x-api__x_search_all_posts`
- `x-api__x_get_thread`
- `x-api__x_get_user_by_username`
- `x-api__x_get_user_posts`
- `x-api__x_get_followers`
- `x-api__x_get_following`
- `x-api__x_get_me`
- `x-api__x_get_bookmarks`

### Write (user-context required)
- Posts: `x_create_post`, `x_delete_post`, `x_hide_reply`
- Social: `x_like_post`, `x_unlike_post`, `x_repost_post`, `x_unrepost_post`, `x_bookmark_post`, `x_delete_bookmark`, `x_follow_user`, `x_unfollow_user`, `x_mute_user`, `x_unmute_user`
- Lists: `x_create_list`, `x_update_list`, `x_delete_list`, `x_get_list`, `x_get_list_members`, `x_get_list_posts`, `x_get_owned_lists`, `x_add_list_member`, `x_add_list_members`, `x_remove_list_member`

### Local drafts (not X product Drafts)
X has no public Drafts API. Use:
- `x_stage_draft` → `x_list_drafts` / `x_get_draft` / `x_update_draft` → `x_publish_draft`
- Files under `data/drafts/` in the harness repo

**Never publish (`x_create_post` / `x_publish_draft`) without explicit user approval** unless the user authorized autonomous posting for this session.

## Mandatory Discovery Pattern (Grok)

**Never** call an `x-api__*` tool without first discovering its current schema.

1. `search_tool` (e.g. "x create post", "x list", "x draft")
2. Inspect fully-qualified `tool_name` + `input_schema`
3. `use_tool` with exact schema

## Environment Check

```sh
source ~/.zshrc >/dev/null 2>&1
[[ -n "${X_API_BEARER_TOKEN:-}" ]] && print "bearer=set" || print "bearer=unset"
[[ -n "${X_API_OAUTH2_ACCESS_TOKEN:-}" ]] && print "oauth2=set" || print "oauth2=unset"
```

If user-context tools 401:

```sh
python3 /Users/velocityworks/IdeaProjects/x-api-mcp-server/scripts/refresh_x_oauth2.py
```

The MCP reloads `~/.config/x-api/user-context.env` on every tool call.

## Core Usage Patterns

- **Single post**: `x_get_post`
- **Recent search**: `x_search_recent_posts`
- **Thread**: `x_get_thread`
- **Followers export**: `x_get_followers` with pagination
- **Draft then publish**: `x_stage_draft` → review → `x_publish_draft`
- **List curation**: `x_create_list` (private default) → `x_add_list_members`
- **Reply targets**: topical recent search, `-from:alltheputs`, rank by public metrics

## Query Syntax Highlights

- `from:alltheputs`, `-from:alltheputs`
- `conversation_id:123...`
- `"exact phrase"`, `(term1 OR term2)`
- `lang:en`, `has:links`, `has:media`, `is:reply`, `-is:retweet`

## Limitations

- No product X Drafts folder — local staging only
- No DMs in this harness (yet)
- Media upload tools not wrapped yet (pass existing `mediaIds` into create/draft)
- `x_search_all_posts` needs appropriate access tier
- Rate limits apply (especially list member adds → 429)
- Scope-denied 403 means re-authorize with the missing OAuth2 scopes

## When to Use

- `/x-api`, search X, read threads, create lists, stage/publish posts, reply targets, follower analysis
