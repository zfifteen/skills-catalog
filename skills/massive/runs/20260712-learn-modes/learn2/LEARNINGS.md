# Learn2 — Mode select for the three-mode Grok test case

## Honesty about prior failure
Claimed “100% confidence” after a matrix that **never exercised mode select**. The three-mode run failed with `select_mode: false` for Fast/Expert/Heavy. That was the only real blocker for the test case.

## What a human does on this page
1. Look at the composer pill on grok.com.
2. Click the mode control on the right of the input (shows current mode: Fast / Expert / Heavy) — **not** the “F” avatar bottom-left.
3. In the dropdown, click Auto / Fast / Expert / Heavy.
4. Confirm the pill label changed.
5. Then type the prompt and send.

## What actually works (proved 2026-07-11/12)

### Geometry (screen points, not screenshot pixels)
| Control | How to find | Typical center |
|---------|-------------|----------------|
| Model select | System Events recursive UI walk, `name is "Model select"` | ~`(1180, 538)` |
| Menu Fast | After open: AXMenuItem first paragraph `Fast` | ~`(1104, 656)` |
| Menu Expert | same | ~`(1104, 716)` |
| Menu Heavy | same | ~`(1104, 775)` |

**Do not** use OCU screenshot coords (1280×802) as click coords. Safari window is ~1728×1083 at (0,34). Mismatched space was why earlier coord clicks did nothing.

### Click mechanism
Real hardware cursor via Quartz `CGEvent` mouse move + left down/up at **screen** points. AX/OCU element click alone did not open this Radix-style menu reliably.

### Gates (must pass before typing a mode’s prompt)
1. After click Model select: menu lists Fast, Expert, Heavy (and Auto).
2. After click mode: menu gone.
3. Width proxy: Fast ~111px, Expert ~129px, Heavy ~128px (label length).
4. Visual: screenshot shows Fast / Expert / Heavy on the pill.

### Proven cycle (07-results.json)
- Expert: ok, width 111→129, shot `07-after-Expert.png`
- Heavy: ok, width 129→128, shot `07-after-Heavy.png`
- Fast: ok, width 128→111, shot `07-after-Fast.png`
- Result: **ALL_THREE_OK** for **mode select only**

### SE reliability
`entire contents of window` sometimes returns count=0. Prefer recursive `UI elements` walk (or OCU tree for presence + SE only for frames when needed).

### Traps
- **F** popup = avatar, not Fast mode
- Mic permission sheet blocks interaction — dismiss Don’t Allow first
- Multi Meta+t thrash — one tab, Meta+l for nav if needed
- AX name stays `"Model select"` always; visible mode is image/width only

## Still not re-proven in this learn pass
Full three-mode PGS: select mode → paste mode-specific prompt → send → wait not Generating → harvest response. Nav/type/send was known earlier; **mode select was the hole**. Next run of the full test case should use this mode path only.

## Minimal human-like algorithm
```
activate Safari on grok.com
dismiss mic sheet if present
for mode in Fast, Expert, Heavy:
  SE: find Model select → real cursor click center
  gate: menu has Fast/Expert/Heavy
  SE: find mode menu item → real cursor click center
  gate: menu closed + width/visual label
  focus Ask Grok → type prompt → send
  wait + harvest
```
