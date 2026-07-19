---
name: 30-30-30-technical-note
description: >
  Turn a PGS research finding into a three-layer technical note bundle: (1) Grade-10
  plain prose, (2) embedded SVG infographic with concise figures, (3) PhD-level
  rigorous technical treatment; plus a PNG export of the SVG. Output lives under
  research/<chapter>/30-30-30-technical-note/. Use when the user asks for a
  "30/30/30 technical note", "30-30-30 tech note", "/30-30-30-technical-note",
  or wants the standard finding bundle format for a research chapter.
when-to-use: Use when the user requests a 30/30/30 technical note on a finding or matter, or invokes /30-30-30-technical-note to produce the three-part prose + SVG + PNG bundle under the target research chapter.
argument-hint: "[finding name or research chapter path, e.g. derived half-coefficient / research/18-derived-half-coefficient]"
metadata:
  short-description: "30/30/30 finding bundle: plain prose, SVG, PhD note"
  version: "1.0.0"
---

# 30/30/30 Technical Note

Produce a **finding bundle** with three reading layers and two image artifacts.

## Output location

```text
research/<chapter>/30-30-30-technical-note/
├── TECHNICAL_NOTE.md      # all three parts in one file
├── infographic.svg        # concise visual summary
└── infographic.png        # raster export of the SVG
```

- `<chapter>` is the existing research folder (e.g. `18-derived-half-coefficient`).
- If the chapter folder does not exist, create it first with a minimal `README.md`
  before writing the bundle.
- Do **not** place the bundle at repo root or under `docs/` unless the user
  explicitly overrides.

## Mandatory workflow

### Step 1 — Gather source material

Read before writing:

1. The finding statement or theorem authority (`PROOF.md`, chapter `docs/`,
   `FINDING_STATEMENT.md`, prior digests).
2. Any measured/audit artifacts cited by the finding.
3. An existing technical note in the repo for tone reference:
   `research/twin-prime-resonance-technical-note-2026-07/TECHNICAL_NOTE.md`.

Use tools. Do not invent proof status or numbers.

### Step 2 — Write `TECHNICAL_NOTE.md`

Use this exact skeleton:

```markdown
# <Finding Title> Technical Note

**Date:** YYYY-MM-DD
**Finding / Theorem:** <ID or name>
**Status:** <proved | measured | hypothesis | corollary>
**Authority:** <paths>

---

## Part I — Plain-Language Summary

<Grade-10 prose — see rules below>

---

## Part II — Visual Summary

![<alt>](infographic.svg)

*PNG export:* [infographic.png](infographic.png)

<3–6 bullet caption of what the diagram shows>

---

## Part III — Technical Treatment

<Rigorous PhD-level exposition — see rules below>
```

### Step 3 — Part I rules (Grade 10)

Follow the **grade-ten** skill discipline:

- Short sentences. Everyday words. Define any unavoidable term immediately.
- **No metaphors, no analogies** ("like a…", "think of it as…").
- State what is proved, what is measured, and what is hypothesis.
- Include one concrete numeric example when the finding allows it.
- Target length: **~250–400 words** unless the user asks for longer.

### Step 4 — Part II rules (SVG infographic)

Create `infographic.svg` in the bundle folder.

**Design contract** (match repo house style from twin-prime note):

- Canvas ~1600px wide; height as needed (typically 1200–1700px).
- Palette: warm off-white background (`#f7f5ef`), dark ink (`#1f2528`),
  muted captions (`#586069`), colored step boxes with distinct stroke colors.
- Font stack: `Inter, ui-sans-serif, system-ui, sans-serif`.
- Structure: **numbered steps** (usually 4–6) with arrows between stages.
- Include: theorem/finding title, one key formula, status badge, boundary line
  ("does not prove RH" when relevant).
- Text in the SVG must stay **concise** — labels and short clauses, not paragraphs.

Embed in markdown as:

```markdown
![<descriptive alt>](infographic.svg)
```

### Step 5 — Part III rules (PhD level)

- Full notation block, formal theorem statement(s), lemma chain or proof architecture.
- Display math with LaTeX (`$...$`, `$$...$$`).
- Cross-reference authority files with paths and section names.
- Explicit **boundary** paragraph: what the finding does **not** establish.
- Cite finite certificates, audit tables, or external validation when present.
- Target length: as long as needed for completeness; do not compress proofs into hand-waving.

### Step 6 — Export PNG

Run the bundled script:

```bash
bash "$HOME/.grok/skills/30-30-30-technical-note/scripts/export_infographic_png.sh" \
  "<path-to-infographic.svg>"
```

Requires `rsvg-convert` (Homebrew `librsvg`). Fallback: `magick convert` at 2× density.

Verify `infographic.png` exists and is non-empty.

### Step 7 — Link from chapter README

Add a row or bullet in `research/<chapter>/README.md` pointing to:

```text
30-30-30-technical-note/TECHNICAL_NOTE.md
```

## Status vocabulary (do not mix tiers)

| Label | Use when |
|-------|----------|
| `proved` | Universal theorem in `PROOF.md` or equivalent proof artifact |
| `measured` | Finite computational audit with pinned regime |
| `hypothesis` | Interpretive bridge; not proved |
| `corollary` | Derived from a named parent theorem |

## Quality checklist before delivery

- [ ] Part I readable at Grade 10 (no jargon without definition, no metaphors)
- [ ] SVG renders; PNG export present
- [ ] Part III theorem statement matches authority file
- [ ] Boundaries explicit (especially RH / Cramér / PNT if nearby)
- [ ] Chapter README updated with bundle link
- [ ] All three parts in **one** `TECHNICAL_NOTE.md` file

## Trigger phrases

- "30/30/30 technical note"
- "30-30-30 tech note"
- "/30-30-30-technical-note"
- "create the standard finding bundle"

## Reference bundle

Canonical example:

```text
research/18-derived-half-coefficient/30-30-30-technical-note/
```