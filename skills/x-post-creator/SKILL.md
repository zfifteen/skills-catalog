---
name: x-post-creator
description: Create X-ready post threads and co-located story packages from the active conversation or referenced project material. Use when the user says turn this into an X-post, /x-post, make this into an X thread, or wants plain-language social posts with supporting images saved to docs/x-posts/[story-name]/.
---

# X-Post Creator

Use this skill when the user wants a conversation, document, theorem, result,
critique, or visual idea turned into an X thread.

The default deliverables are:
- a story package at `docs/x-posts/[story-name]/`
- a ready-to-post plain-text X thread in chat

## Output contract

Create:
- `docs/x-posts/[story-name]/README.md`
- all supporting images in that same `docs/x-posts/[story-name]/` folder

Do not put visuals in a subdirectory.

The markdown file is a thread-ready storyboard. It is not general repo
documentation.

## Trigger phrases

Treat any of the following as a direct instruction to use this skill:
- `turn this into an X-post`
- `/x-post`
- `make this into an X thread`
- close variants that clearly ask for an X thread or X post package

## Writing rules

Write in plain language.
Use plain text only in the prose.
Unicode is allowed.

Do not use:
- LaTeX
- formal math notation
- scientific notation

Each post-sized section should aim for about 500 characters, but that is a
soft target. Clear, coherent communication takes priority over length.

Each prose block may be:
- one free-flowing statement
- or multiple short paragraphs

## X posting contract

Current X ranking evidence favors original posts that create real user intent:
replies, reposts, photo expands, clicks, profile clicks, shares, direct-message
shares, copied links, dwell, quotes, and follows. It penalizes signals such as
not interested, block, mute, report, and no dwell.

Write every section to satisfy this contract:
- Lead with the strongest concrete claim in the first sentence.
- Make the claim specific enough that a thoughtful reader can reply to it.
- Give readers one reason to keep reading, save, share, or click through.
- Prefer original framing over copied phrasing, trend bait, outrage bait, or
  generic AI-sounding filler.
- Keep the tone precise, non-sensational, and advertiser-safe unless the user
  explicitly requests a higher-risk style.
- Avoid spam cadence. Do not create many weak posts when one stronger post or
  thread section carries the idea better.
- Do not imply certainty about X internals beyond the evidence available in the
  active task.

Before drafting, reduce the source material to:
- the strongest supported claim
- the concrete evidence or mechanism behind it
- the reader action the post should invite: reply, save, share, click, or
  follow

## Story format

Use this exact repeating structure:

1. prose block
2. at least one image immediately after that prose block
3. horizontal rule
4. repeat

Every prose block must have at least one attached image.
No text-only sections.

Image links in the markdown must be document-relative and point to files in
the same folder as the markdown document.

## Visual rules

Prioritize effective communication over asset reuse.

If an existing image already communicates the exact intended point completely,
reuse it.

If an existing image only partially supports the point, create a new visual
that fully supports the prose. Do not weaken the prose or the story structure
to reuse a partial image.

Prefer the narrowest deterministic path available in the current project:
- existing project plot scripts, if they already fit the needed visual
- simple new plots or schematics, if the concept is better served by a new
  visual

Each image should earn a likely photo expand or dwell signal. Do not attach a
decorative image just to satisfy the format. The image must clarify the claim,
show evidence, reveal structure, or make the post easier to understand at a
glance.

## Workflow

1. Identify the source material from the active conversation or referenced
   files.
2. Extract the strongest supported claim, its evidence, and the intended reader
   action.
3. Derive a short kebab-case `story-name`.
4. Build the story as post-sized prose blocks.
5. Create or select at least one visual for every prose block.
6. Review each block against the X posting contract. Rewrite weak, generic,
   bait-like, low-evidence, or low-reply sections before writing the file.
7. Write `docs/x-posts/[story-name]/README.md`.
8. Save every supporting image in that same folder.
9. Return a ready-to-post plain-text thread in chat using the same section
   order as the storyboard.

## Scope boundaries

Do not widen the task into a blog post, general repo note, policy note, or
publication draft unless the user explicitly asks for that.

If the user asks only for an X-post, still produce both:
- the repo-local story package
- the chat-ready thread draft

## Final checks

Before considering the work complete, verify:
- the folder lives at `docs/x-posts/[story-name]/`
- `README.md` exists there
- every prose block is followed by at least one image
- every image file lives in the same folder as `README.md`
- every image link is document-relative
- the prose contains no LaTeX, no inline equations, and no scientific notation
- the first sentence states a concrete claim
- every section has a reason for reply, save, share, click, dwell, or follow
- no section relies on copied phrasing, generic filler, outrage bait, or
  unsupported claims about X internals
- every image clarifies the claim, evidence, structure, or reader
  understanding
- the chat draft matches the storyboard section order cleanly
