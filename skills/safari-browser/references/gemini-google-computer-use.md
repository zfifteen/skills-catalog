# gemini.google.com in Safari — Full UI Computer-Use Playbook

**URL:** `https://gemini.google.com/app`  
**Explored:** 2026-07-12 (US authenticated session)  
**Method:** Safari + Open Computer Use (OCU), OODA, screenshot → analyze → one Act  
**Evidence (UI inventory):** `implementer/shots/` under SCRATCH `grok-goal-89c8b3daee89`  
**Evidence (PGS multimodal use):** SCRATCH `grok-goal-40cdc5ff5c5a/implementer/`  
**Prior explore:** `~/.grok/skills/massive/runs/20260712-gemini-ui-explore/shots/`  
**Account:** Google account in Safari (do **not** sign out / delete activity)

---

## Hard rules (automation)

1. **NEVER BATCH.** One Act → screenshot/AX → decide.
2. **Screenshot every 3–5s** while waiting for generation; decisions from image + AX, not assumptions.
3. Stay on `gemini.google.com` — do not thrash the address bar if already there.
4. Prefer Temporary chat for throwaway probes.
5. **No destructive account actions:** no Sign out, no Delete activity, no Delete all links, no subscription purchase.
6. Distinguish **`Copy`** (assistant answer) vs **`Copy prompt`** (user message).
7. **No special keyboard shortcuts** (`press_key` Escape/Cmd/Option, etc.). They open **macOS system menus** (Apple menu → **About This Mac** → System Information).
8. **Never click the menu bar, Apple menu, or window chrome** via OCU. Prefer **Safari JS** for page actions (composer, tools, Send).
9. **Do not thrash native file Open/Upload sheets.** Cancel with the sheet **Cancel** button only. If attach fails, document **blocked** and move on.
10. **Do not click “Download full size image”** (system save dialog hang risk).

---

## Architecture overview

| Region | Role |
|--------|------|
| Left rail | New chat, Search, Daily brief, Images, Videos, Library, Gems; Account + Settings at bottom |
| Top chrome | Temporary chat; “Temporary Chat” label when active; Open sidebar |
| Center | Conversation / destination content |
| Composer (bottom) | `+` Upload & tools, prompt field, mode pill, Microphone, **Send message** (after text) |
| Response row | Redo, Copy, Show more options; user: Copy prompt, Edit |
| During generate | **Stop response** replaces send |

---

## A. Shell / chrome

| Control | AX | Behavior | Exercise |
|---------|-----|----------|----------|
| Open sidebar | `button Open sidebar` | Expands rail | EXERCISED |
| Temporary chat | `button Temporary chat` | Enters temp mode | EXERCISED |
| Temporary label | `text Temporary Chat` | Present in temp mode | EXERCISED |
| Welcome banner | “Welcome, stranger…” | Temp chats not in history; **72h** safety store; not used to improve Google AI | EXERCISED |
| Exit temp | Leave via New chat / navigation (X when present) | | EXERCISED |
| Google Account | `link Google Account: {name}` | Opens **Account and settings** panel | EXERCISED (open only) |
| Account panel | Close, Change profile picture, Manage Google Account, Add account, **Sign out**, Privacy, Terms | **Do not Sign out** | OPENED |
| Settings | `pop up button Settings` | Settings menu | EXERCISED |
| Disclaimer | `text Gemini is AI and can make mistakes.` | Footer | noted |

### Account panel (non-destructive)

- `button Close`
- `button Change profile picture`
- Manage Google Account → myaccount.google.com
- Add account / Sign out → **BLOCKED for automation** (destructive/session)

---

## B. Side navigation destinations

| Link | URL | Page controls (sampled) | Status |
|------|-----|---------------------------|--------|
| New chat | `/app` | Empty or last chat home | EXERCISED |
| Search chats | `/search` | Recent list; search field | EXERCISED |
| Daily brief | `/daily-brief` | Personalized brief; View/More options cards; turn-off personalization link | EXERCISED |
| Images | `/images` | Create images (Nano Banana 2); templates; Deselect Images; Try it | EXERCISED |
| Videos | `/app` video tool surface | Create with Omni; templates; Deselect Videos; aspect Landscape/Portrait | EXERCISED |
| Library | `/library` | View all; Preview/open items; **Delete** (do not use casually) | EXERCISED open |
| Gems | `/gems/view` | Gem manager; premade Gems; My Gems; New Gem; Edit/Share/More options per Gem | EXERCISED |

**Sidebar expanders (DOM / JS aria, not always in shallow AX):**  
`Toggle Notebooks`, `Toggle Recents` — present when rail expanded.

---

## C. Composer

| Control | AX / aria | Notes |
|---------|-----------|-------|
| Prompt | `text entry area Enter a prompt for Gemini` | Placeholder “Ask Gemini”; contenteditable `role=textbox` |
| Upload & tools | `pop up button Upload & tools` | `+` menu |
| Mode picker | `pop up button Open mode picker, currently {Mode}` | Pill label |
| Microphone | `button Microphone` | May trigger Safari mic permission |
| **Send message** | aria `Send message` | Appears when prompt non-empty; **often missing from shallow AX** — use Safari JS `button[aria-label="Send message"]` or Return after real focus |

### Filling the composer (Safari realities)

| Method | Result |
|--------|--------|
| OCU `type_text` | Often fails: “requires a focused editable text element” even after AX click |
| OCU `set_value` | Unreliable on Gemini contenteditable |
| Clipboard + System Events paste | Unreliable without solid focus |
| **Safari JS** `document.execCommand('insertText', …)` after focus | **Works** when mode menu closed |
| Safari JS click `Send message` | **Works** |
| Return after insert | Works if editor accepted input |

Recommended send path:

```js
// 1) insertText into [contenteditable][role=textbox]
// 2) document.querySelector('button[aria-label="Send message"]').click()
```

---

## D. Mode picker (critical)

Open: click mode pill. Close: Escape or re-select.

### Model modes (mutually exclusive among the three)

| Menu item (AX) | Pill short name |
|----------------|-----------------|
| **3.1 Flash-Lite** — Fastest answers | Flash-Lite |
| **3.5 Flash** — All-around help | Flash |
| **3.1 Pro** — Advanced math and code | Pro |

### Extended thinking is a **separate toggle**

| Menu item | Behavior |
|-----------|----------|
| **Extended thinking** — Complex problem solving | Can be **Selected** alongside a model. Pill becomes e.g. **`Flash-Lite Extended`**, **`Pro Extended`**. Click again to deselect. |

Always re-read AX: `Open mode picker, currently …`.

---

## E. Upload & tools (`+`)

### Main menu (this account / 2026-07-12)

| Item | AX pattern | Behavior |
|------|------------|----------|
| Upload files | `menu item Upload files. Documents, data, code files` | Opens **macOS file picker** (Cancel / Upload) |
| Add from Drive | Sheets, Docs, Slides | Drive picker |
| **More uploads** | `pop up button More uploads` | Submenu |
| Create image | toggle (float value 0/1) | Chip **Deselect Images**; placeholder “Describe your image” |
| Create video | toggle | May show **“Start a new chat?”** dialog; landing “Create videos / Gemini Omni”; templates; **Deselect Videos**; aspect **Landscape (16:9)** / **Portrait (9:16)** |
| Create music (New) | toggle | Lyria 3; templates; **Deselect Music**; “Describe your track” |
| Canvas | toggle | **Deselect Canvas** |
| Guided learning | toggle | **Deselect Learn** |

### More uploads submenu

- Google Photos  
- Avatar  
- Import code  
- Notebooks  

### Tool start dialog

When a tool requires a clean thread:

- Heading: **Start a new chat?**
- Copy: “Selecting this tool will start a new chat.”
- `switch Don't ask me again`
- `button New chat` / `button Close dialog`

### Not observed in this session’s menu

Earlier partial map listed **Deep research** and **More tools**. On this account/UI version they did **not** appear. Document as **not present** (UI drift / entitlement / experiment), not as exercised.

---

## F. Response lifecycle

### Generating

| Control | AX | Notes |
|---------|-----|-------|
| Stop response | `button Stop response` | EXERCISED mid-stream; leaves partial answer + full action bar |
| Copy prompt | may still show on user bubble | |

### Finished action bar (assistant)

| Control | AX | Role |
|---------|-----|------|
| Copy | `button Copy` | **Harvest answer** → `pbpaste` |
| Redo | `button Redo` | Regenerate (EXERCISED) |
| Show more options | `button Show more options` | Overflow menu |

### User bubble

| Control | AX | Role |
|---------|-----|------|
| Copy prompt | `button Copy prompt` | User text only |
| Edit | `button Edit` | Opens **Edit prompt** + `button Cancel` (and update/send path) |

### Overflow (`Show more options`) — items observed

| Item | Behavior |
|------|----------|
| Listen | TTS; short replies finish quickly |
| Export to Docs | Creates Google Doc (side effect) — open carefully |
| Draft in Gmail | Opens Gmail draft flow |
| Report legal issue | Navigates to `support.google.com/legal/...` troubleshooter (**do not submit**) |
| Show thinking steps | Side panel **Thinking steps** + close; model used (e.g. “Used 3.1 Pro”) |
| See response details | Alternate overflow label on some modes (Flash-Lite) |

### Thinking steps panel

- Title: Thinking steps  
- Steps / Done / model used  
- Close via panel **X** / `button Close sidebar` (context-dependent)

---

## G. Settings menu (`pop up button Settings`)

| Item | Destination / behavior | Exercise policy |
|------|------------------------|-----------------|
| Activity | `myactivity.google.com/product/gemini` | OPEN only; **no Delete** |
| Personal Intelligence | `/personalization-settings` | Daily Brief switch, Memory, Connected Apps, Instructions |
| Import memory to Gemini (New) | Memory import | OPEN only |
| Avatar | `/likeness` — “Add your avatar” / Try now | OPEN only |
| Usage limits | `/usage` | EXERCISED |
| Scheduled actions | `/scheduled` — templates, New action | OPEN |
| Gems | Gem manager (same family as rail) | OPEN |
| Your public links | `/sharing` — list + Delete all links | OPEN; **no delete all** |
| Theme | Submenu: **System / Light / Dark** | EXERCISED (System selected) |
| Manage subscription | Billing | OPEN only |
| Upgrade to Google AI Ultra | Upsell | OPEN only |
| NotebookLM | External product link | OPEN only |
| Send feedback | Feedback UI | OPEN only |
| Help → Help Center | Help expansion | OPEN |
| Location line | e.g. “Charlotte, NC, USA From your IP address” | noted |
| Update location | Location update | OPEN only |

### Personal Intelligence switches (non-destructive read)

- Daily Brief enable  
- Personal Gemini context / Memory  

---

## H. Gems manager (detail)

- Premade: Brainstormer, Storybook, Coding partner, Chess champ, Career guide, Learning coach, Productivity planner, Writing editor, …  
- My Gems: custom gems with Edit / Share / More options  
- `button New Gem`  
- Labs promo: “Build AI apps…” with close  

---

## I. Harvest recipe (automation)

1. Wait until **no** `Stop response`.  
2. Confirm **Copy** visible in screenshot.  
3. Click assistant **`Copy`** (not Copy prompt).  
4. `pbpaste` → save artifact.  
5. Prefer Temporary chat so probes do not pollute history.

---

## J. Contrast with grok.com

| | Gemini | Grok |
|--|--------|------|
| Mode control | `Open mode picker, currently …` | `Model select` |
| Modes | Flash-Lite / Flash / Pro + **Extended thinking toggle** | Fast / Expert / Heavy (+ Auto) |
| Stop | `Stop response` | `Stop model response` |
| Harvest | `Copy` vs `Copy prompt` | `Copy` vs user Copy |
| Redo | `Redo` | `Regenerate` |
| Tools | Upload & tools menu + chips | Different tool surface |

Grok playbook: `references/grok-com-computer-use.md`.

---

## K. OCU / Safari tips specific to Gemini

1. **Element indexes are only valid for the last `get_app_state`.** Re-fetch after every menu open.  
2. Mode menu: Extended thinking is multi-select with model — deselect explicitly.  
3. Tools can force **new chat** dialog — handle New chat / Close.  
4. Video aspect: Landscape vs Portrait menu items.  
5. Mic: Safari may show **Allow / Don’t Allow / Never for This Website** — document; prefer Don’t Allow for non-voice work.  
6. Overflow **Report legal** leaves Gemini for Legal Help — switch back to Gemini tab.  
7. File upload: Cancel system dialog with Escape / Cancel button.  
8. Prefer Temporary chat for probes.

---

## L. Evidence index (goal SCRATCH shots)

| Shot | What |
|------|------|
| 001–011 prior explore | Home, modes, tools, temp, first send |
| 003–009 | Copy, Copy prompt, overflow, Listen, Thinking steps |
| 010–018 | All modes incl. Extended + Pro |
| 019–024 | Tools menu, More uploads, Create image on |
| 025–036 | Video dialog/templates/aspect, Music, Canvas, Guided |
| 037–040 | Settings, Theme, Usage, Activity |
| 041–046 | Search, Daily brief, Images, Videos, Library, Gems |
| 047–055 | Send, **Stop response**, after-stop |
| 056–057 | Redo, Edit prompt + Cancel |
| 058 | Report legal (external) |
| 059–065 | Settings destinations, Avatar |
| 066 | Microphone + Safari permission |
| 067–068 | Upload files picker, Account panel |

Inventory + matrix: `implementer/evidence/gemini-ui-inventory.md`, `gemini-ui-exercise-matrix.md`.

---

## M. PGS multimodal operate-how (2026-07-12 productive run)

**SCRATCH:** `grok-goal-40cdc5ff5c5a/implementer`  
**Log / matrix:** `evidence/pgs-gemini-usage-log.md`, `evidence/pgs-gemini-exercise-matrix.md`

### Send path (reliable)

```js
// 1) focus contenteditable[role=textbox]
// 2) execCommand selectAll + delete + insertText(prompt)
// 3) wait briefly for button[aria-label="Send message"]
// 4) click Send message
```

OCU `type_text` / `set_value` often fail on Gemini contenteditable.

### Tool enable path

1. Click `button[aria-label="Upload & tools"]` (JS).
2. Enable tool via `toolbox-drawer-item` whose **exact** trimmed text is one of:  
   `Create image` | `Create video` | `Create music` | `Canvas` | `Guided learning`.
3. Confirm chip: `Deselect Images` / `Deselect Videos` / `Deselect Music` / `Deselect Canvas` / `Deselect Learn`.
4. Send a **non-trivial PGS** prompt (not a one-word probe).

### PGS prompts used this run (examples)

| Tool/mode | Prompt theme |
|-----------|----------------|
| Flash-Lite | Even gaps after 2; residue sieves; falsifiable clustering |
| Flash | Research note outline: structure not randomness |
| Pro | Primorial modulus M=210, CRT/sieve, null hypothesis |
| Create image | 4-panel PGS infographic (number line, sieve, admissibility) |
| Canvas | Draft “Prime Gap Structure — modular constraints” |
| Guided learning | Teach g_n, even gaps, mod-3 exercise + one question |

### Harvest

- Prefer `document.querySelectorAll('model-response')[last].innerText` via Safari JS.
- Assistant **Copy** (not Copy prompt) can fill clipboard when OCU index is fresh.
- Image: capture in-page / meta (`naturalWidth`/`blob`); **do not** Download full size.

### File upload

- Opens macOS **Choose Files to Upload** sheet (Cancel / Upload).
- No stable `input[type=file]` in DOM until native sheet.
- **blocked** this run after thrash — see `evidence/upload-blocked.md`. Do not loop on Open sheet.

### Response tools (productive use)

- **Stop response** mid-stream; **Edit** + **Update** to recover empty Pro turn.
- Overflow: Listen, Export to Docs, Draft in Gmail, Report legal, Show thinking steps.

---

*Last updated: 2026-07-12 — UI inventory + PGS multimodal use*
