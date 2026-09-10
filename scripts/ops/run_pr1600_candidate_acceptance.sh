#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

# Immutable-candidate acceptance wrapper for PR #1600.
# This freezes one candidate SHA in a dedicated branch, runs focused then full
# acceptance on that exact commit, and only promotes the result to CURRENT PR
# evidence when the live PR head is still identical at the end.
# Read/test only: no merge, deploy, Railway staged apply, DNS/DB/secret mutation,
# payment, external send, public publish, contract execution, or scheduler mutation.

REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
CONTROL="${DEALIX_CONTROL:-/opt/dealix/control}"
RUN_USER="${DEALIX_RUN_USER:-dealix}"
REPOSITORY="Dealix-sa/dealix"
PR=1600
CANDIDATE_BRANCH="${DEALIX_ACCEPT_CANDIDATE_BRANCH:-pr1600-acceptance-candidate-current}"
STAMP="$(date +%Y%m%dT%H%M%S)"
WT="$CONTROL/worktrees/pr1600-candidate-$STAMP"
PROOF="$CONTROL/proof/pr1600-candidate-$STAMP"

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
  exit "${2:-1}"
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
command -v shellcheck >/dev/null 2>&1 || hold SHELLCHECK_MISSING
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

# Deliberately do not stop, restart, or otherwise mutate production timers here.
# If normal company automation moves main or the PR during this run, the final
# exact-head stability checks fail closed and the candidate must be re-accepted.
echo "SCHEDULER_MUTATION=false"

echo "=== CANDIDATE FREEZE ==="
as_dealix git -C "$REPO" fetch origin main --quiet
as_dealix git -C "$REPO" fetch origin \
  "+refs/heads/$CANDIDATE_BRANCH:refs/remotes/origin/$CANDIDATE_BRANCH" \
  --force --quiet
MAIN="$(as_dealix git -C "$REPO" rev-parse origin/main)"
CANDIDATE="$(as_dealix git -C "$REPO" rev-parse "origin/$CANDIDATE_BRANCH")"
LIVE_START="$(as_dealix gh api "repos/$REPOSITORY/pulls/$PR" --jq '.head.sha')"
STATE="$(as_dealix gh api "repos/$REPOSITORY/pulls/$PR" --jq '.state')"
echo "MAIN=$MAIN"
echo "CANDIDATE_BRANCH=$CANDIDATE_BRANCH"
echo "CANDIDATE_SHA=$CANDIDATE"
echo "LIVE_PR_HEAD_START=$LIVE_START"
echo "PR_STATE=$STATE"
[[ "$STATE" == "open" ]] || hold PR_NOT_OPEN
[[ "$CANDIDATE" == "$LIVE_START" ]] || hold CANDIDATE_NOT_CURRENT_AT_START
[[ "$(as_dealix git -C "$REPO" merge-base "$MAIN" "$CANDIDATE")" == "$MAIN" ]] || hold CANDIDATE_BEHIND_MAIN

set +e
as_dealix git -C "$REPO" merge-tree --write-tree "$MAIN" "$CANDIDATE" > "$PROOF/merge-tree.log" 2>&1
MERGE_RC=$?
set -e
(( MERGE_RC == 0 )) || { tail -n 200 "$PROOF/merge-tree.log" || true; hold MERGE_SIMULATION "$MERGE_RC"; }
echo "MERGE_SIMULATION=PASS"

as_dealix git -C "$REPO" worktree add --detach "$WT" "$CANDIDATE"
[[ "$(as_dealix git -C "$WT" rev-parse HEAD)" == "$CANDIDATE" ]] || hold EXACT_HEAD_MISMATCH
[[ -z "$(as_dealix git -C "$WT" status --porcelain)" ]] || hold FRESH_WORKTREE_DIRTY
as_dealix git -C "$WT" diff --check --ws-error-highlight=all "$MAIN"...HEAD
echo "EXACT_HEAD=PASS sha=$CANDIDATE"
echo "GIT_DIFF_CHECK=PASS"

ACCEPT="$WT/scripts/ops/accept_release_trust_pr.sh"
[[ -f "$ACCEPT" ]] || hold ACCEPTANCE_RUNNER_MISSING

run_acceptance() {
  local full="$1"
  local log_file="$2"
  set +e
  as_dealix env \
    TZ=Asia/Riyadh \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PYTHONPATH="$WT" \
    PYTHONNOUSERSITE=1 \
    DEALIX_ACCEPT_EXPECTED_HEAD="$CANDIDATE" \
    DEALIX_ACCEPT_EXPECTED_BASE="$MAIN" \
    DEALIX_ACCEPT_PYTHON="$PY" \
    DEALIX_ACCEPT_NODE_IMAGE=node:22-bookworm \
    DEALIX_ACCEPT_FULL_PYTEST="$full" \
    bash "$ACCEPT" > "$log_file" 2>&1
  local rc=$?
  set -e
  tail -n 500 "$log_file" || true
  return "$rc"
}

echo "=== FOCUSED ACCEPTANCE ==="
if ! run_acceptance 0 "$PROOF/focused.log"; then
  grep -E 'FAILED|FAIL|ERROR|BLOCKED_ENVIRONMENT|SKIPPED_ENVIRONMENT|AssertionError|Traceback|short test summary' \
    "$PROOF/focused.log" > "$PROOF/focused-red-lines.txt" || true
  cat "$PROOF/focused-red-lines.txt" || true
  hold FOCUSED_ACCEPTANCE
fi
echo "FOCUSED_ACCEPTANCE=PASS"

LIVE_AFTER_FOCUSED="$(as_dealix gh api "repos/$REPOSITORY/pulls/$PR" --jq '.head.sha')"
echo "LIVE_PR_HEAD_AFTER_FOCUSED=$LIVE_AFTER_FOCUSED"
[[ "$LIVE_AFTER_FOCUSED" == "$CANDIDATE" ]] || hold PR_MOVED_AFTER_FOCUSED

echo "=== FULL ACCEPTANCE ==="
if ! run_acceptance 1 "$PROOF/full.log"; then
  grep -E 'FAILED|FAIL|ERROR|BLOCKED_ENVIRONMENT|SKIPPED_ENVIRONMENT|AssertionError|Traceback|short test summary' \
    "$PROOF/full.log" > "$PROOF/full-red-lines.txt" || true
  cat "$PROOF/full-red-lines.txt" || true
  hold FULL_ACCEPTANCE
fi
echo "FULL_ACCEPTANCE=PASS"

as_dealix git -C "$REPO" fetch origin main --quiet
END_MAIN="$(as_dealix git -C "$REPO" rev-parse origin/main)"
LIVE_END="$(as_dealix gh api "repos/$REPOSITORY/pulls/$PR" --jq '.head.sha')"
LOCAL_END="$(as_dealix git -C "$WT" rev-parse HEAD)"
echo "END_MAIN=$END_MAIN"
echo "LIVE_PR_HEAD_END=$LIVE_END"
echo "LOCAL_HEAD_END=$LOCAL_END"
[[ "$END_MAIN" == "$MAIN" ]] || hold MAIN_MOVED_DURING_ACCEPTANCE
[[ "$LIVE_END" == "$CANDIDATE" ]] || hold PR_MOVED_DURING_FULL
[[ "$LOCAL_END" == "$CANDIDATE" ]] || hold LOCAL_HEAD_MOVED

echo "EXACT_HEAD_STABILITY=PASS"
echo "SCHEDULER_MUTATION=false"
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
echo "RESULT=PR1600_IMMUTABLE_CANDIDATE_FULL_PASS"