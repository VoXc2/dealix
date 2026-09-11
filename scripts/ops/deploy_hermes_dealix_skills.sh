#!/usr/bin/env bash
# Deploy repo-governed Dealix Hermes skills to the local Hermes home.
# Idempotent. No secrets, no external send, no production mutation.
set -Eeuo pipefail

MODE="check"
if [[ "${1:-}" == "--apply" ]]; then MODE="apply"; fi

REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
SRC="$REPO/skills/hermes"
DEST="${HERMES_HOME:-$HOME/.hermes}/skills"

[[ -d "$SRC" ]] || { echo "HERMES_SKILLS_SRC=MISSING"; exit 2; }
mkdir -p "$DEST"

count=0
for skill_dir in "$SRC"/*/; do
  [[ -d "$skill_dir" ]] || continue
  name="$(basename "$skill_dir")"
  file="$skill_dir/SKILL.md"
  [[ -f "$file" ]] || { echo "SKIP=$name reason=no_skill_md"; continue; }
  fm_name="$(awk '/^name:/{print $2; exit}' "$file")"
  [[ "$fm_name" == "$name" ]] || { echo "SKILL_FRONTMATTER_MISMATCH=$name"; exit 3; }
  if [[ "$MODE" == "apply" ]]; then
    mkdir -p "$DEST/$name"
    cp -f "$file" "$DEST/$name/SKILL.md"
    echo "HERMES_SKILL_DEPLOYED=$name"
  else
    echo "HERMES_SKILL_PRESENT=$name"
  fi
  count=$((count + 1))
done

echo "HERMES_SKILLS_COUNT=$count"
echo "HERMES_SKILLS_MODE=$MODE"
if (( count >= 5 )); then
  echo "DEALIX_HERMES_SKILLS_VERDICT=PASS"
else
  echo "DEALIX_HERMES_SKILLS_VERDICT=FAIL"
  exit 1
fi
