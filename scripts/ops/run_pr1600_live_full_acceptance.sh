#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

# Live, exact-head, full acceptance wrapper for PR #1600.
# Read/test only. No merge, deploy, Railway staged apply, DNS/DB/secret mutation,
# payment, public publish, contract execution, or external send.

REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
CONTROL="${DEALIX_CONTROL:-/opt/dealix/control}"
RUN_USER="${DEALIX_RUN_USER:-dealix}"
REPOSITORY="Dealix-sa/dealix"
PR=1600
STAMP="$(date +%Y%m%dT%H%M%S)"
WT="$CONTROL/worktrees/pr1600-full-$STAMP"
PROOF="$CONTROL/proof/pr1600-full-$STAMP"
REF="refs/dealix/pr1600-full-$STAMP"
GIT_REMOTE="https://github.com/${REPOSITORY}.git"

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
export WHATSAPP_COLD_OUTBOUND=0
export PUBLIC_PUBLISH=0
export SOCIAL_AUTO_PUBLISH=0
export LINKEDIN_AUTO_DM=0
export PAID_SPEND=0
export PAYMENT_EXECUTION=0
export REFUND_EXECUTION=0
export PRODUCTION_MUTATION=0
export RAILWAY_STAGED_APPLY=0
export DNS_MUTATION=0
export DB_MUTATION=0
export SECRET_MUTATION=0
export CONTRACT_EXECUTION=0
export TENDER_EXECUTION=0
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

# Use the already-authenticated GitHub CLI as a one-command credential helper.
# This does not mutate ~/.gitconfig, does not print the token, and does not rely
# on the repository's origin URL being HTTPS rather than SSH.
git_repo() {
  as_dealix git -C "$REPO" -c 'credential.helper=!gh auth git-credential' "$@"
}

[[ "$(id -u)" -eq 0 ]] || hold ROOT_REQUIRED
id "$RUN_USER" >/dev/null 2>&1 || hold RUN_USER_MISSING
[[ -d "$REPO/.git" ]] || hold REPO_MISSING
command -v gh >/dev/null 2>&1 || hold GH_MISSING
command -v shellcheck >/dev/null 2>&1 || hold SHELLCHECK_MISSING
PY="$REPO/.venv/bin/python"
[[ -x "$PY" ]] || hold VERIFIED_PYTHON_MISSING
as_dealix gh auth status >/dev/null 2>&1 || hold GH_AUTH_MISSING
LOGIN="$(as_dealix gh api user --jq '.login' 2>/dev/null || true)"
[[ "$LOGIN" == "VoXc2" ]] || hold GH_FOUNDER_AUTH_MISMATCH
PRIVATE="$(as_dealix gh api "repos/$REPOSITORY" --jq '.private' 2>/dev/null || true)"
[[ "$PRIVATE" == "true" ]] || hold REPOSITORY_NOT_PRIVATE

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
git_repo fetch "$GIT_REMOTE" "+refs/heads/main:refs/remotes/origin/main" --force --quiet
git_repo fetch "$GIT_REMOTE" "+refs/pull/$PR/head:$REF" --force --quiet
MAIN="$(as_dealix git -C "$REPO" rev-parse origin/main)"
HEAD="$(as_dealix git -C "$REPO" rev-parse "$REF")"
API_HEAD="$(as_dealix gh api "repos/$REPOSITORY/pulls/$PR" --jq '.head.sha')"
STATE="$(as_dealix gh api "repos/$REPOSITORY/pulls/$PR" --jq '.state')"
DRAFT="$(as_dealix gh api "repos/$REPOSITORY/pulls/$PR" --jq '.draft')"
echo "MAIN=$MAIN"
echo "PR_HEAD=$HEAD"
echo "API_HEAD=$API_HEAD"
echo "PR_STATE=$STATE"
echo "PR_DRAFT=$DRAFT"
[[ "$STATE" == "open" ]] || hold PR_NOT_OPEN
[[ "$HEAD" == "$API_HEAD" ]] || hold PR_HEAD_RACE
[[ "$(as_dealix git -C "$REPO" merge-base "$MAIN" "$HEAD")" == "$MAIN" ]] || hold PR_BEHIND_MAIN

set +e
as_dealix git -C "$REPO" merge-tree --write-tree "$MAIN" "$HEAD" > "$PROOF/merge-tree.log" 2>&1
MERGE_RC=$?
set -e
if (( MERGE_RC != 0 )); then
  tail -n 200 "$PROOF/merge-tree.log" || true
  hold MERGE_SIMULATION
fi
echo "MERGE_SIMULATION=PASS"

as_dealix git -C "$REPO" worktree add --detach "$WT" "$HEAD"
[[ "$(as_dealix git -C "$WT" rev-parse HEAD)" == "$HEAD" ]] || hold EXACT_HEAD_MISMATCH
[[ -z "$(as_dealix git -C "$WT" status --porcelain)" ]] || hold FRESH_WORKTREE_DIRTY
as_dealix git -C "$WT" diff --check --ws-error-highlight=all "$MAIN"...HEAD

echo "EXACT_HEAD=PASS sha=$HEAD"
echo "GIT_DIFF_CHECK=PASS"

ACCEPT="$WT/scripts/ops/accept_release_trust_pr.sh"
[[ -f "$ACCEPT" ]] || hold ACCEPTANCE_RUNNER_MISSING

set +e
as_dealix env \
  TZ=Asia/Riyadh \
  LC_ALL=C.UTF-8 \
  LANG=C.UTF-8 \
  PYTHONPATH="$WT" \
  PYTHONNOUSERSITE=1 \
  DEALIX_ACCEPT_EXPECTED_HEAD="$HEAD" \
  DEALIX_ACCEPT_EXPECTED_BASE="$MAIN" \
  DEALIX_ACCEPT_PYTHON="$PY" \
  DEALIX_ACCEPT_NODE_IMAGE=node:22-bookworm \
  DEALIX_ACCEPT_FULL_PYTEST=1 \
  bash "$ACCEPT" > "$PROOF/full-acceptance.log" 2>&1
RC=$?
set -e

tail -n 500 "$PROOF/full-acceptance.log" || true
if (( RC != 0 )); then
  grep -E 'FAILED|FAIL|ERROR|BLOCKED_ENVIRONMENT|SKIPPED_ENVIRONMENT|AssertionError|Traceback|short test summary' \
    "$PROOF/full-acceptance.log" > "$PROOF/red-lines.txt" || true
  echo "FULL_ACCEPTANCE=FAIL rc=$RC"
  cat "$PROOF/red-lines.txt" || true
  hold FULL_ACCEPTANCE
fi

END_HEAD="$(as_dealix git -C "$WT" rev-parse HEAD)"
git_repo fetch "$GIT_REMOTE" "+refs/heads/main:refs/remotes/origin/main" --force --quiet
git_repo fetch "$GIT_REMOTE" "+refs/pull/$PR/head:$REF" --force --quiet
END_MAIN="$(as_dealix git -C "$REPO" rev-parse origin/main)"
END_PR="$(as_dealix git -C "$REPO" rev-parse "$REF")"
[[ "$END_HEAD" == "$HEAD" ]] || hold LOCAL_HEAD_MOVED
[[ "$END_MAIN" == "$MAIN" ]] || hold MAIN_MOVED
[[ "$END_PR" == "$HEAD" ]] || hold PR_MOVED

echo "FULL_ACCEPTANCE=PASS"
echo "EXACT_HEAD_STABILITY=PASS"
echo "MERGE_EXECUTED=false"
echo "DEPLOY_EXECUTED=false"
echo "RAILWAY_STAGED_APPLY=false"
echo "DNS_MUTATION=false"
echo "DB_MUTATION=false"
echo "SECRET_MUTATION=false"
echo "EXTERNAL_SEND=false"
echo "PAYMENT_EXECUTION=false"
echo "PUBLIC_PUBLISH=false"
echo "PRODUCTION_GREEN=false"
echo "RESULT=PR1600_CURRENT_EXACT_FULL_PASS"
