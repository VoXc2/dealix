#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

# Repo-native, fail-closed repair for the generated verify-script catalog on the
# live PR #1600 head. This is intentionally stored in the repository so it can
# be executed from SSH without pasting a large heredoc.
#
# L4 only: may commit/push the regenerated catalog to the existing PR branch.
# Never merges, deploys, applies Railway staged changes, or mutates production.

REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
CONTROL="${DEALIX_CONTROL:-/opt/dealix/control}"
RUN_USER="${DEALIX_RUN_USER:-dealix}"
REPOSITORY="Dealix-sa/dealix"
PR=1600
BRANCH="fix/release-trust-fail-closed-20260909-chatgpt"
STAMP="$(date +%Y%m%dT%H%M%S)"
WT="$CONTROL/worktrees/pr1600-catalog-repair-$STAMP"
PROOF="$CONTROL/proof/pr1600-catalog-repair-$STAMP"
REF="refs/dealix/pr1600-catalog-repair-$STAMP"

export TZ=Asia/Riyadh
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export PYTHONNOUSERSITE=1
export GH_PROMPT_DISABLED=1
export GIT_TERMINAL_PROMPT=0
export PRODUCTION_GREEN=false
export DEALIX_EXTERNAL_SEND=0
export EMAIL_LIVE_SEND=0
export WHATSAPP_OUTBOUND=0
export PUBLIC_PUBLISH=0
export PAID_SPEND=0
export PAYMENT_EXECUTION=0
export PRODUCTION_MUTATION=0
export RAILWAY_STAGED_APPLY=0
export DNS_MUTATION=0
export DB_MUTATION=0
export SECRET_MUTATION=0
export MODE=draft-only

hold() {
  echo "RESULT=HOLD_$1"
  echo "PROOF=$PROOF"
  echo "PRODUCTION_GREEN=false"
  exit 1
}

as_dealix() {
  if [[ "$(id -un)" == "$RUN_USER" ]]; then
    "$@"
  else
    sudo -u "$RUN_USER" -H "$@"
  fi
}

[[ "$(id -u)" -eq 0 ]] || hold ROOT_REQUIRED
id "$RUN_USER" >/dev/null 2>&1 || hold RUN_USER_MISSING
[[ -d "$REPO/.git" ]] || hold REPO_MISSING
command -v gh >/dev/null 2>&1 || hold GH_MISSING
PY="$REPO/.venv/bin/python"
[[ -x "$PY" ]] || hold VERIFIED_PYTHON_MISSING

RUN_GROUP="$(id -gn "$RUN_USER")"
install -d -m 0750 -o "$RUN_USER" -g "$RUN_GROUP" \
  "$CONTROL/worktrees" "$CONTROL/proof" "$PROOF"
exec > >(tee -a "$PROOF/run.log") 2>&1

cleanup() {
  local rc=$?
  trap - EXIT
  if [[ -d "$WT" ]]; then
    as_dealix git -C "$REPO" worktree remove --force "$WT" >/dev/null 2>&1 || true
  fi
  echo "FINAL_PROOF=$PROOF"
  exit "$rc"
}
trap cleanup EXIT

echo "=== LIVE EXACT TRUTH ==="
as_dealix git -C "$REPO" fetch origin main --quiet
as_dealix git -C "$REPO" fetch origin "+refs/pull/$PR/head:$REF" --force --quiet
MAIN="$(as_dealix git -C "$REPO" rev-parse origin/main)"
HEAD="$(as_dealix git -C "$REPO" rev-parse "$REF")"
API_HEAD="$(as_dealix gh api "repos/$REPOSITORY/pulls/$PR" --jq '.head.sha')"
STATE="$(as_dealix gh api "repos/$REPOSITORY/pulls/$PR" --jq '.state')"
echo "MAIN=$MAIN"
echo "PR_HEAD=$HEAD"
echo "API_HEAD=$API_HEAD"
echo "PR_STATE=$STATE"
[[ "$STATE" == "open" ]] || hold PR_NOT_OPEN
[[ "$HEAD" == "$API_HEAD" ]] || hold PR_HEAD_RACE
[[ "$(as_dealix git -C "$REPO" merge-base "$MAIN" "$HEAD")" == "$MAIN" ]] || hold PR_BEHIND_MAIN

as_dealix git -C "$REPO" worktree add --detach "$WT" "$HEAD"
[[ -z "$(as_dealix git -C "$WT" status --porcelain)" ]] || hold FRESH_WORKTREE_DIRTY

TARGET="$WT/docs/ops/VERIFY_SCRIPTS_CATALOG.md"
TMP="$(as_dealix mktemp "$PROOF/catalog.XXXXXX")"

as_dealix "$PY" "$WT/scripts/ops/build_verify_catalog.py" > "$TMP"
NEW_COUNT="$(grep '^Total scripts:' "$TMP" | awk '{print $3}')"
OLD_COUNT="$(grep '^Total scripts:' "$TARGET" 2>/dev/null | awk '{print $3}' || true)"
echo "OLD_VERIFY_SCRIPT_COUNT=${OLD_COUNT:-missing}"
echo "NEW_VERIFY_SCRIPT_COUNT=${NEW_COUNT:-missing}"

if cmp -s "$TMP" "$TARGET"; then
  as_dealix rm -f "$TMP"
  as_dealix env PYTHONPATH="$WT" "$PY" "$WT/scripts/ops/build_verify_catalog.py" --check
  as_dealix env PYTHONPATH="$WT" "$PY" -m pytest -q "$WT/tests/test_verify_catalog.py"
  echo "VERIFY_CATALOG_ALREADY_CURRENT=true"
  echo "RESULT=VERIFY_CATALOG_PASS_NO_CHANGE"
  exit 0
fi

as_dealix install -m 0644 "$TMP" "$TARGET"
as_dealix rm -f "$TMP"

as_dealix env PYTHONPATH="$WT" "$PY" "$WT/scripts/ops/build_verify_catalog.py" --check
as_dealix env PYTHONPATH="$WT" "$PY" -m pytest -q "$WT/tests/test_verify_catalog.py"
as_dealix git -C "$WT" diff --check

CHANGED="$(as_dealix git -C "$WT" status --porcelain)"
printf 'CHANGED_FILES_BEGIN\n%s\nCHANGED_FILES_END\n' "$CHANGED"
[[ "$CHANGED" == " M docs/ops/VERIFY_SCRIPTS_CATALOG.md" ]] || hold UNEXPECTED_WORKTREE_CHANGE

as_dealix git -C "$WT" diff -- docs/ops/VERIFY_SCRIPTS_CATALOG.md > "$PROOF/catalog.diff"

as_dealix git -C "$WT" add docs/ops/VERIFY_SCRIPTS_CATALOG.md
as_dealix git -C "$WT" \
  -c user.name='Dealix Release Trust' \
  -c user.email='release-trust@dealix.local' \
  commit -m 'fix(trust): regenerate verify script catalog'
NEW_HEAD="$(as_dealix git -C "$WT" rev-parse HEAD)"

LIVE_BEFORE_PUSH="$(as_dealix gh api "repos/$REPOSITORY/pulls/$PR" --jq '.head.sha')"
echo "LIVE_BEFORE_PUSH=$LIVE_BEFORE_PUSH"
echo "REPAIR_PARENT=$HEAD"
echo "REPAIR_HEAD=$NEW_HEAD"
[[ "$LIVE_BEFORE_PUSH" == "$HEAD" ]] || hold PR_MOVED_BEFORE_PUSH

as_dealix git -C "$WT" push origin "HEAD:$BRANCH"
LIVE_AFTER_PUSH="$(as_dealix gh api "repos/$REPOSITORY/pulls/$PR" --jq '.head.sha')"
[[ "$LIVE_AFTER_PUSH" == "$NEW_HEAD" ]] || hold PUSH_HEAD_MISMATCH

echo "VERIFY_CATALOG_REPAIR=PASS"
echo "PUSHED_HEAD=$NEW_HEAD"
echo "MERGE_EXECUTED=false"
echo "DEPLOY_EXECUTED=false"
echo "PRODUCTION_GREEN=false"
echo "RESULT=VERIFY_CATALOG_REPAIRED_AND_PUSHED"
