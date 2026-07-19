# Six UX Psychology Principles (Reference)

Source lesson: uxpeak — *The UX Psychology Behind Apps People Can't Stop Using*
https://youtu.be/2TlIg3VokY8

Use this file when the agent needs full before/after rules, classic anchors, or
anti-pattern boundaries. The SKILL.md quick map is enough for most reviews.

**Ethics (applies to all six):** Do not fake urgency, scarcity, progress, results,
or reviews. Do not use dark patterns. Psychology should make the product clearer
and easier to use — not manipulative.

---

## 1. Smart defaults (decision fatigue)

### Problem
Blank forms force a decision per field before anything useful happens. Stacked
choices increase the chance the user makes **no** choice and leaves.

### Classic anchor (heuristic)
Choice overload / "jam study" framing (Columbia): more options → lower purchase
rate; fewer options → higher purchase rate. Use as a design story, not a
guaranteed lift number.

### Before
- Five empty fields on a booking/search screen
- CTA: generic "Search" / "Continue" with no outcome preview
- User job: invent every answer from scratch

### After
- Pre-fill the **most common** choices for each field
- CTA shows value waiting (e.g. "12 results ready")
- User job: scan and adjust only what does not fit

### Rule
Pre-select the most common choice for every field when you already know a
sensible answer. Do not make users think for known defaults.

### Stats used in lesson
~70–90% of users never change defaults in many products — treat as industry
heuristic; measure in your product.

### Anti-patterns
- Defaults that quietly opt users into paid plans or marketing without consent
- Wrong defaults that force correction (trust break)
- Hiding that values are editable

### Surfaces
Search/booking forms, filters, locale/currency, plan length, notification
settings, "who is this for" pickers.

---

## 2. Goal-gradient effect (never start at 0%)

### Problem
Onboarding that shows **0%** or empty stamps says "you haven't started and a lot
is ahead." That feeling kills momentum even when the work is small.

### Classic anchor (heuristic)
Car-wash loyalty cards: 8 empty stamps vs 10 stamps with 2 already filled
(same remaining work). Pre-progress group completed at a much higher rate
("goal-gradient").

### Before
- Progress: 0% complete, five empty steps
- Account creation treated as outside the journey

### After
- Progress already shows e.g. 20%; first step checked
- Account creation counts as step one
- User sees distance to finish, not a blank runway

### Rule
**Never start a user at zero.** Find something they already did (or that the
system legitimately completed for them) and count it. An honest head start
creates real motivation.

### Product example (lesson)
LinkedIn profile strength meter never starts at zero after signup.

### Anti-patterns
- Fake progress bars that stall or jump without user action (erodes trust)
- Claiming 80% complete when only email was entered
- Endless steps after a "almost done" claim

### Surfaces
Onboarding, profile completeness, multi-step checkout, KYC, setup wizards.

---

## 3. Reciprocity (value before the wall)

### Problem
"Sign up to see results" / blurred locked report after the user did work =
holding value **hostage**. Feels like paying before seeing the menu.

### Classic anchor (heuristic)
Reciprocity (Cialdini): give first → pull to return the favor. Free samples /
trials / freemium product access as strategic gifts, not pure charity.

### Before
- User pastes URL / answers quiz → analyze → results blurred
- CTA: "Create account to see your report"
- Zero delivered value

### After
- User gets a **real partial** result: score, top issues, what passed
- Enough to be useful and think about fixes
- Soft invite: "Want the full breakdown with steps? Save your report."

### Rule
Give something genuinely useful **before** asking for email, account, or pay.
Signup should feel like saving progress, not unlocking a hostage.

### Product patterns (lesson)
Costco samples, Spotify trial, Notion usable product before pay.

### Anti-patterns
- Teaser that looks like results but is pure fiction
- Full result then retroactive paywall on already-shown content
- Endless "one more step" after partial value was promised as complete

### Surfaces
Auditors, quizzes, calculators, "scan my site", free tools, lead magnets.

---

## 4. IKEA effect + endowment (invest before signup)

### Problem
Email + password + "Sign up" owns nothing. Closing the tab costs nothing.

### Classic anchors (heuristic)
- **IKEA effect:** people value what they helped build more than identical
  pre-built items.
- **Endowment effect:** mere sense of ownership raises valuation.

### Before
- Pure credential form
- Nothing chosen, customized, or created
- Dismiss is effortless

### After
- Pre-auth building: name, role/title, palette, style, language, goal
- CTA: **Continue** (not "Sign up") once investment exists
- Leaving feels like abandoning something they made

### Rule
Let users **build or own something first**. Capture credentials after labor
creates attachment.

### Product example (lesson)
Duolingo: language + goal + first lesson before account (~minutes invested).

### Anti-patterns
- Busywork with no connection to the product value (fake investment)
- Losing all pre-auth work if they decline signup (punishes exploration)
- Forced long customization when a smart default would suffice (conflicts #1)

### Surfaces
Makers (cards, profiles, sites), learning apps, config-heavy SaaS, games.

---

## 5. Loss aversion + status quo bias

### Problem
Feature-list upgrade + "Maybe later" = zero stakes. Gain framing is the weaker
motivator when something real is at risk.

### Classic anchors (heuristic)
- Kahneman: losses weigh roughly ~2× gains (lesson framing).
- Status quo bias: protect what is already owned.

### Before
- Premium pitch, icons, feature bullets
- CTA: "Upgrade now"
- Escape: "Maybe later" with no consequence

### After
- Show **what they lose** if they do nothing (named files, access, seats)
- Time-bound truth only if true (real expiry / real limit)
- Dismiss acknowledges risk: e.g. "I'll risk it" (honest, not cartoon guilt)

### Rule
When asking users to act, flip framing: don't only sell what they gain — show
what they **lose by inaction** when that loss is real.

### Anti-patterns
- Invented countdowns / fake file deletion threats
- Shame copy ("I don't care about my data")
- Loss framing on optional vanity upgrades with no real downside

### Surfaces
Storage limits, free trial end, seat limits, expiring shares, compliance holds.

---

## 6. Contrast effect (price anchoring)

### Problem
Same price feels expensive or cheap depending on the **previous** number. Shown
alone, users annualize and reject; shown after a large reference, it shrinks.

### Classic anchors (heuristic)
- Relative evaluation / contrast: brain measures against the last salient number
- Menu decoys (expensive steak makes mid option feel reasonable)
- Real estate: overpriced first listing makes target feel like a deal

### Before
- Protection plan alone: $50/mo → user thinks $600/year → "No thanks"

### After
- Same $50 under a $1,900 laptop
- Label relative size: "just 2.6%"
- Offer appears in cart context, not isolated sticker shock

### Rule
Don't show cost in isolation. **Control what the user sees first** — that number
becomes the ruler for everything after.

### Anti-patterns
- Misleading % of an inflated fake "list price"
- Anchoring with a price the user never actually faced
- Hiding total cost of ownership after the relative trick

### Surfaces
Add-ons, warranties, annual vs monthly, seat upgrades, "complete the set".

---

## Shared insight (all six)

Users are not purely logical:

| Mechanism | Felt as |
|-----------|---------|
| Defaults | Recommendations / social proof |
| First number | Anchor / ruler |
| Gift first | Unconscious debt (reciprocity) |
| Building | Ownership |
| Progress (honest) | Momentum |
| Loss of status quo | Stronger than feature gain |

Designers who design for these mechanisms make the next action feel natural.
Designers who only polish pixels often ship products people forget.

---

## Severity guide (for reviews)

| Severity | Meaning |
|----------|---------|
| **H** | Blocks conversion/completion for a large share of users |
| **M** | Adds friction or weakens motivation; fix after H |
| **L** | Polish / consistency; do after H/M |

Only escalate ethics issues as **blockers** regardless of conversion upside.
