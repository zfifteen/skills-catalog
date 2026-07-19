# Skills Catalog Project Plan

## Overview
Enhance `build_catalog.py` to ensure every skill has a description in the UI. If a `description` field is missing from a skill's YAML frontmatter, the script will automatically extract an excerpt from the body of the `SKILL.md` file (the first non-empty paragraph after the frontmatter) to serve as the description.

## Step 1: Scaffolding (Phase 1)
- `scripts/build_catalog.py`: Update the `parse_skill_metadata` method to include logic for extracting a fallback excerpt from the markdown body.

## Step 2: Review (Phase 2)
- Operator will review the updated logic plan before proceeding to implementation.

## Step 3: Incremental Implementation (Phase 3)
- Implement the fallback logic in `parse_skill_metadata`.
- Re-run `build_catalog.py` to regenerate `data.js` with the new descriptions.
- Verify visually that skills now have descriptions.

## Step 4: Verification and Report (Phase 4)
- Perform code review.
- Produce final report.
