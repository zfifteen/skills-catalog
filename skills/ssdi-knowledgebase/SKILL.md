---
id: kb-grok-skill
name: ssdi-knowledgebase
title: SSDI Knowledge Base — Global Grok Skill
type: skill
tier: meta
tags: [skill, agent-retrieval, ssdi, grok]
confidence: high
last_verified: 2026-06-29
citations:
  - title: SSA Disability Benefits
    url: https://www.ssa.gov/benefits/disability/
    source_tier: A
  - title: SSA — Apply for Disability Benefits
    url: https://www.ssa.gov/applyfordisability/
    source_tier: A
description: >
  Load and apply the verified SSDI filing best-practices knowledge base at
  /Users/velocityworks/IdeaProjects/SSDI/knowledgebase/ for evidence-based,
  citable guidance on Social Security Disability Insurance claims. Covers
  eligibility, onset/SGA, Listings (12.15 PTSD), RFC, medical evidence hierarchy,
  VA/SSDI bridge, substance/material-factor framing, checklists, and post-submission
  follow-up. Optimized for 100% P&T VA veteran cases with PTSD-dominant and pain
  co-morbidities; maps answers to local artifacts at /Users/velocityworks/IdeaProjects/SSDI/.
  Use when the user asks about SSDI filing strategy, what evidence to submit,
  application order, common mistakes, VA corroboration, or runs /ssdi-knowledgebase
  or /ssdi-kb. Never substitute forum advice for KB citations. Informational only —
  not legal advice.
canonical_source: /Users/velocityworks/IdeaProjects/SSDI/knowledgebase/grok-skill/SKILL.md
install_script: /Users/velocityworks/IdeaProjects/SSDI/scripts/install-ssdi-kb-skill.sh
installed_copy: /Users/velocityworks/.grok/skills/ssdi-knowledgebase/SKILL.md
local_artifacts:
  - ../../source-records/
  - ../../SSDI_Phase1_Evidence_Package_Dionisio_Lopez/
  - ../../SSDI_Phase1_Evidence_Package_Dionisio_Lopez/Project_Context_SSDI_Evidence_Package.md
disclaimer: Informational only — not legal advice.
---

# SSDI Knowledge Base

Use this skill to answer SSDI filing questions from the verified knowledge base — not from memory or forums. **All paths below are absolute** so the skill works from any Grok project cwd.

**Canonical copy:** edit this file in the repo, then run `scripts/install-ssdi-kb-skill.sh` to install to `~/.grok/skills/ssdi-knowledgebase/SKILL.md`.

## Root paths

| Resource | Absolute path |
|----------|---------------|
| KB index | `/Users/velocityworks/IdeaProjects/SSDI/knowledgebase/INDEX.md` |
| Glossary | `/Users/velocityworks/IdeaProjects/SSDI/knowledgebase/glossary/GLOSSARY.md` |
| Locked framing | `/Users/velocityworks/IdeaProjects/SSDI/SSDI_Phase1_Evidence_Package_Dionisio_Lopez/Project_Context_SSDI_Evidence_Package.md` |
| Evidence package | `/Users/velocityworks/IdeaProjects/SSDI/SSDI_Phase1_Evidence_Package_Dionisio_Lopez/Final_SSDI_Evidence_Package_Optimized.pdf` |
| Blue Button | `/Users/velocityworks/IdeaProjects/SSDI/source-records/VA-Blue-Button-report-Dionisio-Lopez-6-27-2026_1052pm.pdf` |
| Summary export | `/Users/velocityworks/IdeaProjects/SSDI/source-records/Health Records - Dionisio Lopez - 2026-06-27 at 22.19.50.pdf` |
| Project context | `/Users/velocityworks/IdeaProjects/SSDI/PROJECT_CONTEXT.md` |
| Manifest | `/Users/velocityworks/IdeaProjects/SSDI/MANIFEST.md` |

## Retrieval workflow

1. Read `/Users/velocityworks/IdeaProjects/SSDI/knowledgebase/INDEX.md` for navigation and locked framing.
2. Read `/Users/velocityworks/IdeaProjects/SSDI/SSDI_Phase1_Evidence_Package_Dionisio_Lopez/Project_Context_SSDI_Evidence_Package.md` before case-specific advice.
3. Open the matching playbook or article (absolute paths in tables below).
4. Map answers to local evidence using the root paths table — reference files, do not duplicate PDFs.
5. Cite SSA.gov URLs from each file's YAML `citations`, `confidence`, and `last_verified` frontmatter.

## Priority playbooks

| Topic | Absolute path |
|-------|---------------|
| VA / SSDI bridge | `/Users/velocityworks/IdeaProjects/SSDI/knowledgebase/playbooks/va-ssdi-bridge.md` |
| Onset & SGA | `/Users/velocityworks/IdeaProjects/SSDI/knowledgebase/playbooks/onset-and-sga.md` |
| Listing 12.15 (PTSD) | `/Users/velocityworks/IdeaProjects/SSDI/knowledgebase/playbooks/listing-12-15-ptsd.md` |
| RFC & functional impact | `/Users/velocityworks/IdeaProjects/SSDI/knowledgebase/playbooks/rfc-functional-impact.md` |
| Medical evidence hierarchy | `/Users/velocityworks/IdeaProjects/SSDI/knowledgebase/playbooks/medical-evidence-hierarchy.md` |
| Substance / material-factor framing | `/Users/velocityworks/IdeaProjects/SSDI/knowledgebase/playbooks/substance-material-factor-framing.md` |
| Initial application checklist | `/Users/velocityworks/IdeaProjects/SSDI/knowledgebase/playbooks/initial-application-checklist.md` |
| Post-submission follow-up | `/Users/velocityworks/IdeaProjects/SSDI/knowledgebase/playbooks/post-submission-follow-up.md` |

## Atomic articles

| Topic | Absolute path |
|-------|---------------|
| SSA-16 application | `/Users/velocityworks/IdeaProjects/SSDI/knowledgebase/articles/ssa-16-application.md` |
| SSA-3368 disability report | `/Users/velocityworks/IdeaProjects/SSDI/knowledgebase/articles/ssa-3368-disability-report.md` |
| SSA-3373 function report | `/Users/velocityworks/IdeaProjects/SSDI/knowledgebase/articles/ssa-3373-function-report.md` |
| SSA-827 medical release | `/Users/velocityworks/IdeaProjects/SSDI/knowledgebase/articles/ssa-827-medical-release.md` |
| Sequential evaluation | `/Users/velocityworks/IdeaProjects/SSDI/knowledgebase/articles/sequential-evaluation.md` |

## Locked framing (always preserve)

- **Primary impairments:** chronic PTSD + recurrent pain.
- **Substance history:** minimal, episodic, secondary; recent negative labs support current control where records support it.
- **VA 100% P&T:** corroborating evidence only — **not determinative** for SSA.

## Answer requirements

When answering "what to file, with what evidence, in what order, and what mistakes to avoid":

1. State the **application phase** (initial, reconsideration, hearing) if relevant.
2. Give an **ordered action list** tied to specific forms and evidence types.
3. **Reference absolute local artifact paths** where the user's package already contains the evidence.
4. Include **at least one citation** from the playbook frontmatter (SSA.gov Tier A preferred).
5. Flag **common pitfalls** from the relevant playbook.
6. Do **not** guarantee approval, predict outcomes, or give legal advice.
7. Do **not** use Reddit, forums, or anecdotal "approval hacks."

## Source policy

| Tier | Use |
|------|-----|
| A | SSA.gov, official SSA forms/instructions |
| B | NOSSCR/NADE summaries tracking SSA policy (secondary) |
| C | Local project artifacts under `/Users/velocityworks/IdeaProjects/SSDI/` |
| Excluded | Forums, Reddit, unverified anecdotes |

## Out of scope

- Legal advice or guaranteed-approval claims
- SSI state supplements
- Re-building evidence PDFs (KB guides; deliverables stay in Phase1 package)

## Slash command

`/ssdi-knowledgebase` or `/ssdi-kb`