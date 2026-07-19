# Grok chat page — UI cues & controls (Safari / AX)

Observed 2026-07-12 on authenticated grok.com chat (Heavy reply finished + Fast mid-flight tree from eyes-run).

## Lifecycle of a reply

| Phase | What a human sees | AX / tree signals | Automation gate |
|-------|-------------------|-------------------|-----------------|
| **1. Thinking** | Status like “Thinking about your request • Ns”; no full answer yet | `button Thinking about your request • …` | Do **not** harvest; do **not** expect bottom action bar |
| **2. Generating / writing** | Answer text growing; can cancel | `button Stop model response` (or similar **Stop**) | Still in flight; body length often increases between polls |
| **3. Finished** | Full answer; toolbar under reply; follow-ups; composer ready | **No** Stop; `button Thought for …` (e.g. `Thought for 32s`, `Thought for 1m 7s`); **`button Copy`** under the answer; `Create share link`, `Like`, `Dislike`, `Regenerate`; often `N sources` | Safe to harvest or click Copy |

Notes:
- “Thought for Xs” is a **finished** thinking summary control, not “still thinking.”
- While thinking, the label is **“Thinking about your request • …”** (present continuous).
- `Stop` present ⇒ still generating. `Stop` absent + bottom action bar present ⇒ done.

## Bottom-of-response action bar (finished)

Left → right (visual icons; AX names):

| Visual | AX name | Role |
|--------|---------|------|
| Copy (two-squares icon) | **`button Copy`** | Copy assistant reply to clipboard |
| Link / chain | **`button Create share link`** | Share |
| Thumbs up | **`pop up button Like`** | Feedback |
| Thumbs down / comment | **`pop up button Dislike`** | Feedback |
| Refresh / regenerate | **`button Regenerate`** | New answer |
| ⋯ | **`pop up button More actions`** | Overflow |
| Sources pill | **`button N sources`** (e.g. `241 sources`) | Citations |

Also common:
- **`button Thought for …`** near the top of the assistant turn (after thinking completes).
- User message row may have its own **Edit** / **Copy** (separate from assistant Copy at bottom).
- Follow-up suggestion chips (links) under the action bar.
- Composer: **Ask Grok** / “Ask anything”, **Model select**, Dictation, Voice.

## Copy button (focus of this note)

- Appears **after** the response is finished, under the last content of that assistant message.
- AX: plain name **`Copy`** (not “Copy response”).
- There can be **two** Copy buttons on a long page (e.g. user message vs assistant). Prefer the one **after** the assistant body and **next to** Create share link / Like / Regenerate.
- Tree order (finished assistant block):  
  `… answer text …` → **`button Copy`** → `Create share link` → `Like` → `Dislike` → `Regenerate` → `More actions` → optional sources / follow-ups.
- Harvest alternative: click Copy then read clipboard (`pbpaste`) instead of full-page `innerText` (cleaner, less chrome).

## Composer / page chrome (always relevant)

- Mode pill: **Model select** (Fast / Expert / Heavy).
- Send path: focus Ask Grok → paste → Return.
- Top-right chat: share / more on the conversation (separate from per-message Create share link).
- Sidebar: Home, search, history, etc.

## Wrong cues to avoid

| Cue | Misread | Correct |
|-----|---------|---------|
| Avatar **F** | “Fast mode” | Profile / account, not mode |
| Address bar | Must retype every turn | Only if not on grok.com |
| `Thought for Xs` | Still thinking | Thinking **done**; duration badge |
| Any `Copy` | Always the answer | May be user-message Copy; use sibling Regenerate/Like to disambiguate |
| Growing `innerText` alone | Done | Need no Stop + stable length + action bar |

## Practical wait loop (for agents)

```
after send:
  loop:
    if AX has "Stop model response" or "Thinking about your request":
      still running
    elif AX has bottom "Copy" near "Regenerate" and no Stop:
      finished → harvest or click Copy
    elif body length stable for 2+ polls and markers present and no Stop:
      finished (fallback)
```

## Artifacts

- `00-observe.png` / `00-observe-tree.txt` — finished Heavy reply + action bar
- `01-scrolled-bottom.png` — scrolled to toolbar
- `01-se-buttons.txt` — System Events button inventory
- Cross-ref mid-flight: `.../20260712-eyes-run/03-sent-tree.txt` (`Thinking…`, `Stop model response`)
