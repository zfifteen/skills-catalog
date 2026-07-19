# grok.com in Safari — Computer-Use Playbook (Learned)

**Status:** Operational knowledge from successful three-mode PGS run (2026-07-12).  
**Stack:** Safari (authenticated) + open-computer-use CLI + System Events geometry + Quartz real cursor when needed.  
**Do not re-learn from scratch** — follow this before inventing a new navigation strategy.

Related artifacts (evidence):  
`~/.grok/skills/massive/runs/20260712-eyes-run/` (PASS: Fast/Expert/Heavy)  
`~/.grok/skills/massive/runs/20260712-ui-cues/` (Copy / lifecycle screenshots)

---

## 0. Operating mindset (non-negotiable)

### OODA Loop — **mandatory** (every step, no exceptions)

Interactive Safari / grok.com work **must** use the **OODA loop**.

| Phase | Required work | Forbidden |
|-------|----------------|-----------|
| **Observe** | **Screenshot first.** Read the image. Then tree/URL if needed. | Trusting logs, key names, or “I pressed PageDown” without looking at the new shot |
| **Orient** | From the **screenshot**: what is on screen? Did the last Act change anything visible? Phase of model/UI? | Assuming success because the tool returned exit 0 |
| **Decide** | One next action **only if** the last screenshot supports it | Labeling a shot `scroll-end` / `mode-ok` / `harvested` without visual proof |
| **Act** | Exactly **one** action | Anything resembling a batch |

**After every Act → immediately Observe again (new screenshot) and Orient from the image.** That closes the loop.

---

### NEVER BATCH — strictly prohibited

**BATCH IS STRICTLY PROHIBITED.**

| Batch (forbidden) | OODA (required) |
|-------------------|-----------------|
| One script: home → mode → paste → send → wait → scroll → copy | One Act, then screenshot, then analyze, then next Act |
| “Run the whole mode pipeline” | Stop after each step and look |
| Fire 5 PageDowns then one screenshot | After **each** scroll Act: screenshot → analyze → decide |
| Long unattended loops without looking | Continuous Observe |

If you catch yourself writing multi-step sequences that only snapshot at the end: **stop**. That is batch. Delete that plan.

---

### ALWAYS screenshot, then analyze

1. **Screenshot** (primary Observe)  
2. **Analyze** the image (Orient)  
3. **Decide** the single next action  
4. **Act** once  
5. **Screenshot again**  

Never Act on “what I think the UI is.” Only on **what the last screenshot shows.**

### Cadence: screenshot every 3–5 seconds

While operating the browser (especially while the model is thinking/writing, or while scrolling):

- Take a **new screenshot every 3–5 seconds**  
- On each shot: **determine state** (wrong site / home / menu / thinking / writing / finished / scrolled how far / action bar visible?)  
- **Make the next decision from that shot**  
- Do not wait for a long silent poll without images  

During waits: the loop is **screenshot → analyze state → wait 3–5s → screenshot**, not “sleep 60s and hope.”

### Absolute rule: decisions from screenshots

- **Screenshots are the primary evidence.** AX/tree and logs are secondary.
- **Never** conclude “scrolled”, “menu opened”, “mode changed”, “finished”, or “copied” unless the **latest screenshot shows it**.
- Pressing a key is **not** an outcome. The outcome is only what appears in the next image.
- If the new shot looks the same as the previous one, Orient = **Act failed** → try a different Act (e.g. click body, then scroll) — do **not** proceed as if it worked.
- Naming a file `*-scroll-end.png` does **not** make it scrolled. If the image still shows the top of the answer, you did not scroll.

OODA is the **control algorithm**, not flavor text.

### Eyes first (feeds Observe)
- Take **as many screenshots as needed** until screen state and model state are unambiguous.  
- One viewport is not the whole page. **Scroll** to read the full response before claiming you “saw” it.  
- Prefer extra screenshots over assumptions after every click, paste, mode change, send, or scroll.  
- If screenshot and AX disagree → more screenshots / scroll / wait — do not force Act.

### Scroll is only real if screenshots prove it
- **Do not** claim you scrolled because you pressed `PageDown` / `Meta+Down`. That is batch-script thinking.  
- **Gate after each scroll Act:** open/read the new screenshot. Did the visible content move? If **no** → Orient “scroll failed”; Decide a different Act.  
- **Gate before Copy:** the **last screenshot must show the bottom action bar in the viewport** (Copy + Regenerate icons visible to eyes), not only the top of the answer under the user prompt.  
- If keys don’t move the chat (shot unchanged): **click the answer body / HTML content first**, then scroll; retry until a shot **visually** advances.  
- Off-screen SE coordinates (e.g. Copy at `y=3173`) mean the control is **not** in view — keep scrolling until the **screenshot** shows the bar, then click.

### Hard rules
| Rule | Detail |
|------|--------|
| **OODA every step** | Observe → Orient → Decide → Act → Observe; no blind multi-step runs |
| Safari only | Never Playwright/Chromium unless user overrides |
| No address thrash | If already on `https://grok.com*`, **do not** retype the URL |
| In-page navigation | New chat / home via **Home page** (or in-page New chat), not the address bar |
| Stop on failure | Empty menu, wrong URL, paste not verified → **halt**, re-observe |
| No probe hosts | Never navigate to example.com or other sites “to test” |

---

## 1. Address bar (only when not already on Grok)

**Critical tool fact:** OCU `type_text` **appends even when the field text is selected**. Selection + type ≠ replace.

### Correct sequence
1. `Meta+l` — focus smart search field  
2. `Meta+a` — select all  
3. **`Backspace`** — field must be empty (verify in AX: no `Value:` or empty)  
4. `type_text` **only** `https://grok.com`  
5. **Gate:** address field value is exactly `https://grok.com` (or with trailing `/`)  
6. `Return`  
7. **Gate:** tab URL starts with `https://grok.com`; page has composer / not “Failed to open page”

### Never
- Meta+l → type without clear (produces `https://grok.comhttps//grok.com…`)  
- `force=True` reload every mode when already on Grok  
- set_value on address alone as “navigation done” without Return + URL gate  

---

## 2. Mode select (Fast / Expert / Heavy)

### Visual
- Control is the **mode pill on the right of the composer** (shows Fast / Expert / Heavy), not the avatar.  
- AX name: **`Model select`** (always; visible label is visual/width only).  
- **`pop up button F`** (bottom-left) = **avatar / account**, **not** Fast mode.

### Open + pick (proven)
1. System Events recursive UI walk → find name **`Model select`** → position + size → center.  
   Typical center ~`(1180, 538)` when window fills a 1728-wide screen (re-measure every time).  
2. **Real cursor click** (Quartz `CGEvent` move + left down/up) at screen points — AX-only click often fails on this Radix menu.  
3. **Gate:** menu lists Auto, **Fast**, **Expert**, **Heavy**.  
4. Real cursor click target mode center (re-measure from SE after open).  
   Rough offsets when menu open: Fast ~y 656, Expert ~y 716, Heavy ~y 775 at x ~1104 (re-measure).  
5. **Gate:** menu closed; optional width proxy (Fast ~111px, Expert ~129px, Heavy ~128px); screenshot shows correct label.

### SE reliability
- `entire contents of window` sometimes returns count 0. Prefer recursive `UI elements` walk.  
- Re-query geometry after layout changes; do not hardcode forever.

---

## 3. Composer: type / send

1. Focus **`text entry area` … Ask Grok anything** (OCU element click from fresh snapshot).  
2. Clear: Meta+a → Backspace.  
3. **Paste** prompt: `pbcopy` + Meta+v (preferred for long text).  
4. **Gate:** prompt sample appears in AX/tree or screenshot.  
5. Send: `Return`.  
6. Expect navigation into `/c/<conversation-id>?rid=…` after send.

Do **not** use address-bar habits on the composer. Clear-before-type still applies if reusing a field with leftover text.

---

## 4. Model / response lifecycle cues

| Phase | Human sees | AX / tree signals | Action |
|-------|------------|-------------------|--------|
| Thinking | “Thinking about your request • Ns” | `button Thinking about your request • …` | Wait; more screenshots |
| Writing | Text growing; cancel available | **`button Stop model response`** | Wait; body length may increase |
| Finished | Full answer + toolbar under reply | **No Stop**; `button Thought for 32s` (or `3s`, `1m 7s`); bottom action bar | Scroll full answer, then harvest |

### Critical disambiguation
- **`Thought for Xs`** = thinking **finished** (duration badge).  
- **`Thinking about your request • …`** = still thinking.  
- **`Stop model response` present** = still generating.

---

## 5. Bottom action bar (finished assistant message)

Left → right (icons → AX names):

| Control | AX |
|---------|-----|
| Copy | **`button Copy`** |
| Share | **`button Create share link`** |
| Like | **`pop up button Like`** |
| Dislike | **`pop up button Dislike`** |
| Regenerate | **`button Regenerate`** |
| More | **`pop up button More actions`** |
| Sources | e.g. **`button 241 sources`** |

Tree order after answer body:  
`Copy` → `Create share link` → `Like` → `Dislike` → `Regenerate` → `More actions` → sources / follow-ups.

User message may also have **Edit** / **Copy** — do **not** use that Copy for harvest. Prefer the **Copy next to Regenerate / Like**.

---

## 6. Harvest — **Copy button after every round** (required)

**After each mode/round (Fast, Expert, Heavy, or any single send): harvest with the Copy control at the end of that assistant response.** Do not skip Copy in favor of full-page scrape as the default.

### Required path (every round)
1. **OODA wait until finished** — screenshots every 3–5s; no Stop; **Thought for…** / full text stable.  
2. **Scroll with proof** — each scroll Act + new screenshot; stop only when the **bottom action bar is visible in the image** (Copy next to Regenerate / Like).  
3. **Click the assistant `Copy`** at the **end of the response** (action bar under that answer — not the user-message Copy).  
4. **Screenshot after click** (optional but good); then `pbpaste` → `*-response.txt` (or that round’s artifact).  
5. **Verify** clipboard is the answer (not the prompt; length sensible).

### Per-round discipline
| After | Harvest |
|-------|---------|
| Fast send + finished | Copy at end of Fast reply → save |
| Expert send + finished | Copy at end of Expert reply → save |
| Heavy send + finished | Copy at end of Heavy reply → save |

Never run all three modes and only scrape once at the end. **Harvest after each round** via that round’s end-of-response **Copy**.

**Fallback only if Copy is unavailable:** Safari `document.body.innerText` — noisier; log that Copy failed.

---

## 7. Multi-mode / multi-prompt runs

Between modes:
1. Click **Home page** link (AX: `link [Home page](https://grok.com/)`) — **not** address bar.  
2. Gate: URL `https://grok.com/` (or home), composer + Model select visible.  
3. Select mode → paste → send → wait → scroll → Copy harvest.  
4. One mode at a time; fail → stop and re-observe.

Proven PASS (2026-07-12): Fast ~203 words, Expert ~834, Heavy ~1271 under  
`~/.grok/skills/massive/runs/20260712-eyes-run/result.json`.

---

## 8. Coordinate spaces (do not mix)

| Space | Example | Use |
|-------|---------|-----|
| OCU screenshot pixels | 1280×802 | **Visual inspection only** — not raw click targets unless mapped |
| Screen points (Quartz/SE) | Safari window ~1728×1083 at (0, 34) on Retina laptop | Real cursor clicks |
| Mapping | `screen = window_origin + img * (win_size / shot_size)` | Only if clicking from image analysis |

**Default:** SE/AX **screen** frames for clicks on Model select, menu items, Copy.

---

## 9. Mic / sheets

If `Allow "grok.com" to use your microphone?` sheet appears, dismiss (**Don’t Allow**) before interacting with composer/mode. Sheet blocks the page.

---

## 10. Failure catalog (do not repeat)

| Failure | Cause |
|---------|--------|
| URL garbage / error page | type_text append without Backspace clear |
| Mode select never works | Screenshot coords; clicked avatar F; AX click without real cursor |
| menu=[] after open | Re-nav thrash / wrong focus / menu already closed |
| False 100% confidence | Tested nav/type without mode select |
| Contaminated session | Navigated to example.com as “probe” |
| Dirty harvest | Full page innerText without scroll/Copy |
| know-right / do-wrong | Wrote rules then ran `force=True` batch script |

---

## 11. Minimal happy path (already on grok.com) — each line is an OODA cycle

```
O: screenshot + URL + tree
O: classify (home / chat / menu / thinking / done / error)
D/A: if not on grok.com → address clear→type→verify→Return (section 1) → O again
D/A: if in /c/... and need fresh chat → click Home page → O again
D/A: select mode (section 2) → O: verify label / menu closed
D/A: paste prompt → O: verify sample in field
D/A: Return → O: sent? thinking? stop?
loop O: screenshot; Orient thinking|writing|finished
  if Thinking or Stop → wait → O again
  if Copy+Regenerate and no Stop → finished
O: scroll full answer (multiple shots) until action bar + full text seen
D/A: click assistant Copy → pbpaste → save file
O: confirm harvest file non-empty / looks like the answer
```

---

## 12. Tooling checklist

```bash
export PATH="$HOME/.npm-global/bin:$PATH"
open-computer-use doctor   # accessibility + screen recording
open-computer-use call get_app_state --args '{"app":"Safari","text_limit":"max","max_tree_nodes":5000,"max_tree_depth":100}'
```

Quartz real cursor (Python): `CGEventCreateMouseEvent` + `CGEventPost` for move/down/up.  
System Events: recursive walk for `Model select`, menu items, `Copy` positions.

---

*Last updated: 2026-07-12. Keep this file in sync when grok.com UI labels change.*
