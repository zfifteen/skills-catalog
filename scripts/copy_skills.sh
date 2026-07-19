#!/bin/bash
set -e

PROJECT_DIR="/Users/velocityworks/IdeaProjects/skills-catalog"
SKILLS_DIR="$PROJECT_DIR/skills"

mkdir -p "$SKILLS_DIR"

# List of skill source directories (taking dirname of SKILL.md paths)
SKILL_DIRS=(
  "/Users/velocityworks/.gemini/antigravity-cli/builtin/skills/antigravity_guide"
  "/Users/velocityworks/.gemini/skills/grok-task-v3-disturbing-implications"
  "/Users/velocityworks/.gemini/skills/flaws"
  "/Users/velocityworks/.gemini/skills/grok-task-v3-gaslight-check"
  "/Users/velocityworks/.gemini/skills/grok-cli"
  "/Users/velocityworks/.gemini/skills/grok-share"
  "/Users/velocityworks/.gemini/skills/grok-task-v3-trap-questions"
  "/Users/velocityworks/.gemini/skills/implementation-plan"
  "/Users/velocityworks/.gemini/skills/grok-task-v3-implications"
  "/Users/velocityworks/.gemini/skills/insight-ooda-loop"
  "/Users/velocityworks/.gemini/skills/ooda"
  "/Users/velocityworks/.gemini/skills/pdf"
  "/Users/velocityworks/.gemini/skills/playwright"
  "/Users/velocityworks/.gemini/skills/prompts-1-fix-in-pr"
  "/Users/velocityworks/.gemini/skills/prompts-review-pull-request"
  "/Users/velocityworks/.gemini/skills/grok-task-v3-repo-deep-dive"
  "/Users/velocityworks/.gemini/skills/safari-browser"
  "/Users/velocityworks/.gemini/skills/scientific-code-review"
  "/Users/velocityworks/.gemini/skills/scientific-fraud-investigator"
  "/Users/velocityworks/.gemini/skills/technical-design-document"
  "/Users/velocityworks/.gemini/skills/x-api"
  "/Users/velocityworks/.gemini/skills/x-post-creator"
  "/Users/velocityworks/.gemini/skills/youtube"
)

for DIR in "${SKILL_DIRS[@]}"; do
  if [ -d "$DIR" ]; then
    cp -r "$DIR" "$SKILLS_DIR/"
    echo "Copied: $(basename "$DIR")"
  else
    echo "Warning: Directory not found: $DIR"
  fi
done

echo "Done copying skills."
