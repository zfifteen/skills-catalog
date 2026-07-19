---
name: ui-ux
description: >
  Apply UX psychology to design, critique, or redesign product screens and flows
  (onboarding, forms, signup walls, upgrades, pricing, conversion moments). Uses six
  evidence-backed principles: smart defaults, goal-gradient progress, reciprocity,
  IKEA/endowment ownership, loss aversion, and contrast/anchoring — with ethical
  anti-dark-pattern guardrails. Use when the user says "UI/UX", "UX psychology",
  "critique this screen", "improve conversion", "onboarding UX", "signup wall",
  "pricing screen", "upgrade modal", "design this flow", "/ui-ux", or wants
  before/after product UI recommendations grounded in how people actually decide.
when-to-use: >
  Product UI/UX review or design work where decision psychology, conversion, or
  retention matters more than pure visual polish. Screens, Figma/export descriptions,
  app flows, web forms, paywalls, checkouts.
argument-hint: "<screen/flow description, screenshot path, or URL> [critique|redesign|checklist]"
metadata:
  short-description: "UX psychology for screens: defaults, progress, reciprocity, ownership, loss, contrast"
  source: "uxpeak — The UX Psychology Behind Apps People Can't Stop Using (https://youtu.be/2TlIg3VokY8)"
  principles-ref: "references/principles.md"
---

# UI/UX (Psychology-First Product Design)

## Purpose

Help the user **design, critique, or redesign** product UI so the next action feels
obvious, valuable, and worth completing. Visual polish alone is not the goal.
**Decision psychology** is the goal.

Apps fail more often from ignoring how people decide than from ugly pixels.

## Core Contract

1. Ground every recommendation in one or more of the **six principles** below.
2. Prefer concrete **before → after** screen changes over abstract advice.
3. Prefer **one primary action** per moment of friction.
4. Use psychology to **reduce confusion and build trust**, never to deceive.
5. If the user only wants visual style (colors, type, glassmorphism), say so and
   either narrow to psychology or defer — this skill owns **behavioral UX**, not
   pure aesthetic art direction.

## Six Principles (Quick Map)

| # | Principle | User-job shift | Primary surfaces |
|---|-----------|----------------|------------------|
| 1 | **Smart defaults** | Fill from scratch → scan & adjust | Forms, filters, booking, settings |
| 2 | **Goal-gradient (never start at 0%)** | Standing still → already in motion | Onboarding, checklists, profiles |
| 3 | **Reciprocity (value before wall)** | Hostage → gift then invite | Results gates, signup walls, freemium |
| 4 | **IKEA + endowment (invest first)** | Disposable form → something that's mine | Pre-auth setup, personalization |
| 5 | **Loss aversion + status quo** | Pitch to ignore → cost of inaction | Upgrades, storage limits, renewals |
| 6 | **Contrast / anchoring** | Absolute price shock → relative fit | Pricing, add-ons, protection plans |

Full before/after rules, study anchors, and anti-patterns:
`references/principles.md` (read when applying in depth or when the user wants sources).

## Modes

Infer mode from the request; default to **critique** if ambiguous.

| Mode | When | Output emphasis |
|------|------|-----------------|
| **critique** | Existing screen/flow | Friction inventory + ranked principle hits |
| **redesign** | User wants a better version | Concrete before→after changes + copy + layout notes |
| **checklist** | Audit many screens / ship readiness | Pass/fail per principle with one fix each |
| **design-from-scratch** | New flow, no UI yet | Ordered flow + key screens using the six principles |

## Workflow

### 1. Load the target

- Read attached screenshots/images with `read_file` (multimodal).
- Read local design files, HTML/React screens, or copy docs.
- If only a verbal description is given, restate the assumed screen layout before advising.
- Do **not** invent product data the user never provided; mark assumptions explicitly.

### 2. Name the decision moment

In one sentence:

> User is deciding whether to **[action]** after **[context]**, with **[stakes]**.

Examples: "continue onboarding", "create account", "upgrade now", "add protection plan".

### 3. Map friction to principles

For each blocking moment, ask:

1. Are they forced to invent answers we already know? → **defaults**
2. Does progress start at zero or feel endless? → **goal-gradient**
3. Are we asking before giving anything real? → **reciprocity**
4. Is there nothing yet that feels *theirs*? → **IKEA / endowment**
5. Is the CTA a gain pitch with a free "maybe later"? → **loss aversion**
6. Is a cost shown without a controlled first number? → **contrast**

Skip principles that do not apply. Do not force all six onto every screen.

### 4. Propose changes (smallest that move behavior)

For each high-impact issue:

- **Principle:** name it
- **Current:** what the UI does now
- **Change:** exact UI/copy/structure change
- **Why it works:** one sentence in behavioral terms
- **Risk / ethics check:** any dark-pattern edge?

Prefer **one decisive redesign** over ten micro-nits when conversion is the goal.

### 5. Ethics gate (mandatory)

Reject or rewrite any recommendation that:

- Fakes urgency, scarcity, progress, results, or social proof
- Locks already-earned value behind a surprise wall after implying it was free
- Uses loss framing for harm (fear, shame) without a truthful stake
- Pre-selects paid plans, dark-pattern checkboxes, or hard-to-find dismiss controls
- Mislabels secondary actions to guilt the user ("No, I hate saving money")

Allowed: honest defaults, real partial value, real progress, real cost of inaction,
transparent relative pricing.

If the user's request is manipulative, refuse the dark version and offer an ethical
equivalent that still uses the principle.

## Output Shape

Use this structure unless the user asks for a different format:

```markdown
# UI/UX Review: <screen or flow name>

## Decision moment
<one sentence>

## What's working
- ...

## Friction → principle map
| Moment | Principle | Severity (H/M/L) | Fix in one line |
|--------|-----------|------------------|-----------------|

## Recommended redesign (before → after)
### 1. <change title>
- **Before:** ...
- **After:** ...
- **Principle:** ...
- **Copy (if needed):** "..."

## Primary CTA & secondary
- Primary: ...
- Secondary: ... (honest, not a guilt trap)

## Ethics check
- Pass / concerns + mitigations

## Optional next probe
- One measurement or A/B that would falsify whether the change helped
```

For **checklist** mode, use a six-row table (principle / status / evidence / fix).

For **design-from-scratch**, output:

1. User job + success metric  
2. Step sequence (ordered)  
3. Key screens with principle tags  
4. Empty states / failure / dismiss behavior  
5. What *not* to add (complexity that reintroduces decision fatigue)

## Working With Visuals

When screenshots or mockups are present:

1. Describe what you actually see (layout regions, hierarchy, CTAs) before advising.
2. Point to specific UI regions ("top progress bar", "blurred results panel", "footer dismiss").
3. Prefer overlay-style notes: *where* to change, not only *that* something should change.
4. If generating a visual mock with image tools, keep labels legible and match the
   product's existing visual language unless redesigning brand.

## Related Skills

- **playwright / safari-browser** — observe live product behavior; this skill interprets UX intent.
- **hyperframes / imagegen** — produce motion or mock visuals *after* the behavioral design is set.
- **user-story / technical-task** — turn agreed UX changes into implementation work items.
- **method-simplification** — compress overbuilt flows while preserving the conversion contract.

## Success Criteria

- Recommendations cite named principles, not vibes.
- At least one concrete before→after per high-severity friction.
- Ethics gate is explicit.
- User can implement the top change without guessing copy or structure.
- Unused principles are omitted, not shoehorned.

## Invocation Examples

- `/ui-ux critique this onboarding screenshot`
- `UI/UX redesign our signup wall for the SEO analyzer`
- `/ui-ux checklist the upgrade modal in src/components/Paywall.tsx`
- `Apply UX psychology to this checkout add-on pricing row`
- `/skills ui-ux` then attach a flow description

## Source Note

Principles distilled from uxpeak's public lesson
"The UX Psychology Behind Apps People Can't Stop Using"
(https://youtu.be/2TlIg3VokY8), expanded into an agent-operable workflow.
Treat cited classic studies (jam choice, car-wash stamps, Kahneman loss aversion,
Cialdini reciprocity, IKEA effect, contrast effect) as **design heuristics with
famous anchors**, not as peer-reviewed claims re-verified in this skill file.
When the user needs academic precision, flag uncertainty and offer to verify sources.
