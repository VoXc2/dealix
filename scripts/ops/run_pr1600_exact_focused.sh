#!/usr/bin/env bash
# Exact-head, read/test-only orchestrator for PR #1600 focused acceptance.
#
# This wrapper exists to replace pasted ad-hoc heredoc runners. It deliberately
# contains no heredoc and cannot turn a non-zero canonical acceptance exit into
# PASS. It never merges, deploys, publishes, sends, charges, mutates production,
# applies Railway staged changes, or changes DNS/DB/secrets.
set -Eeuo pipefail
umask 077

export TZ="${TZ:-Asia/Riyadh}"
export LC_ALL="${LC_ALL:-C.UTF-8}"
export LANG="${LANG:-C.UTF-8}"
export PYTHONNOUSERSITE=1
export GH_PROMPT_DISABLED=1
export GIT_TERMINAL_PROMPT=0

REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
CONTROL="${DEALIX_CONTROL:-/opt/dealix/control}"
RUN_USER="${DEALIX_RUN_USER:-dealix}"
REPOSITORY="Dealix-sa/dealix"
PR="${DEALIX_PR:-1600}"
STAMP="$(date +%Y%m%dT%H%M%S)"
WT="$CONTROL/worktrees/pr${PR}-focused-$STAMP"
PROOF="$CONTROL/proof/pr${PR}-focused-$STAMP"
REF="refs/dealix/pr${PR}-focused-$STAMP"

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

log() {
  printf '\n======================================================================\n'
  printf '[%s] %s\n' "$(date -Is)" "$*"
  printf '======================================================================\n'
}

hold() {
  local reason="$1"
  local rc="${2:-1}"
  printf '\nRESULT=HOLD_%s\n' "$reason"
  printf 'PROOF=%s\n' "$PROOF"
  printf 'PRODUCTION_GREEN=false\n'
  exit "$rc"
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
command -v git >/dev/null 2>&1 || hold GIT_MISSING
command -v gh >/dev/null 2>&1 || hold GH_MISSING

RUN_GROUP="$(id -gn "$RUN_USER")"
install -d -m 0750 -o "$RUN_USER" -g "$RUN_GROUP" \
  "$CONTROL/worktrees" "$CONTROL/proof" "$PROOF"

PY="$REPO/.venv/bin/python"
[[ -x "$PY" ]] || hold VERIFIED_PYTHON_MISSING

exec > >(tee -a "$PROOF/run.log") 2>&1

cleanup() {
  local rc=$?
  trap - EXIT
  if [[ -d "$WT" ]]; then
    set +e
    as_dealix git -C "$REPO" worktree remove --force "$WT" >/dev/null 2>&1
    set -e
  fi
  printf 'FINAL_PROOF=%s\n' "$PROOF"
  exit "$rc"
}
trap cleanup EXIT

log "LIVE MAIN + PR HEAD"
as_dealix git -C "$REPO" fetch origin main --quiet
as_dealix git -C "$REPO" fetch origin "+refs/pull/$PR/head:$REF" --force --quiet
MAIN="$(as_dealix git -C "$REPO" rev-parse origin/main)"
HEAD="$(as_dealix git -C "$REPO" rev-parse "$REF")"
API_HEAD="$(as_dealix gh api "repos/$REPOSITORY/pulls/$PR" --jq '.head.sha')"
PR_STATE="$(as_dealix gh api "repos/$REPOSITORY/pulls/$PR" --jq '.state')"
PR_DRAFT="$(as_dealix gh api "repos/$REPOSITORY/pulls/$PR" --jq '.draft')"
printf 'MAIN=%s\nPR_HEAD=%s\nAPI_HEAD=%s\nPR_STATE=%s\nPR_DRAFT=%s\n' \
  "$MAIN" "$HEAD" "$API_HEAD" "$PR_STATE" "$PR_DRAFT"
[[ "$PR_STATE" == "open" ]] || hold PR_NOT_OPEN
[[ "$HEAD" == "$API_HEAD" ]] || hold PR_HEAD_RACE

MERGE_BASE="$(as_dealix git -C "$REPO" merge-base "$MAIN" "$HEAD")"
printf 'MERGE_BASE=%s\n' "$MERGE_BASE"
[[ "$MERGE_BASE" == "$MAIN" ]] || hold PR_BEHIND_MAIN

log "MERGE SIMULATION"
set +e
as_dealix git -C "$REPO" merge-tree --write-tree "$MAIN" "$HEAD" \
  >"$PROOF/merge-tree.log" 2>&1
MERGE_RC=$?
set -e
if (( MERGE_RC != 0 )); then
  tail -n 200 "$PROOF/merge-tree.log"
  hold MERGE_SIMULATION "$MERGE_RC"
fi
printf 'MERGE_SIMULATION=PASS\n'

log "FRESH EXACT-HEAD WORKTREE"
as_dealix git -C "$REPO" worktree add --detach "$WT" "$HEAD"
ACTUAL="$(as_dealix git -C "$WT" rev-parse HEAD)"
[[ "$ACTUAL" == "$HEAD" ]] || hold EXACT_HEAD_MISMATCH
[[ -z "$(as_dealix git -C "$WT" status --porcelain)" ]] || hold FRESH_WORKTREE_DIRTY
printf 'EXACT_HEAD=PASS sha=%s\n' "$HEAD"

ACCEPT="$WT/scripts/ops/accept_release_trust_pr.sh"
[[ -f "$ACCEPT" ]] || hold ACCEPTANCE_RUNNER_MISSING

log "CANONICAL FOCUSED ACCEPTANCE"
set +e
as_dealix env \
  TZ="$TZ" \
  LC_ALL="$LC_ALL" \
  LANG="$LANG" \
  PYTHONNOUSERSITE=1 \
  PYTHONPATH="$WT" \
  DEALIX_ACCEPT_EXPECTED_HEAD="$HEAD" \
  DEALIX_ACCEPT_EXPECTED_BASE="$MAIN" \
  DEALIX_ACCEPT_PYTHON="$PY" \
  DEALIX_ACCEPT_NODE_IMAGE="${DEALIX_ACCEPT_NODE_IMAGE:-node:22-bookworm}" \
  DEALIX_ACCEPT_FULL_PYTEST=0 \
  bash "$ACCEPT" >"$PROOF/focused.log" 2>&1
FOCUSED_RC=$?
set -e

tail -n 350 "$PROOF/focused.log"
printf 'FOCUSED_RC=%s\n' "$FOCUSED_RC"

if (( FOCUSED_RC != 0 )); then
  set +e
  grep -E 'FAILED|FAIL|ERROR|BLOCKED_ENVIRONMENT|SKIPPED_ENVIRONMENT|Traceback|AssertionError' \
    "$PROOF/focused.log" >"$PROOF/red-lines.txt"
  set -e
  printf '\n================ CURRENT EXACT-HEAD RED LINES =================\n'
  if [[ -s "$PROOF/red-lines.txt" ]]; then
    cat "$PROOF/red-lines.txt"
  else
    printf 'No grep summary; inspect focused.log directly.\n'
  fi
  printf '===============================================================\n'
  {
    printf 'DEALIX_PR1600_EXACT_FOCUSED\n'
    printf 'TIMESTAMP=%s\n' "$(date -Is)"
    printf 'MAIN=%s\n' "$MAIN"
    printf 'PR_HEAD=%s\n' "$HEAD"
    printf 'FOCUSED_ACCEPTANCE=FAIL\n'
    printf 'FOCUSED_RC=%s\n' "$FOCUSED_RC"
    printf 'FULL_PYTEST_EXECUTED=false\n'
    printf 'MERGE_EXECUTED=false\n'
    printf 'DEPLOY_EXECUTED=false\n'
    printf 'RAILWAY_STAGED_APPLY=false\n'
    printf 'PRODUCTION_GREEN=false\n'
  } >"$PROOF/RECEIPT.txt"
  hold CURRENT_EXACT_FOCUSED "$FOCUSED_RC"
fi

log "HEAD STABILITY"
END_LOCAL="$(as_dealix git -C "$WT" rev-parse HEAD)"
as_dealix git -C "$REPO" fetch origin main --quiet
as_dealix git -C "$REPO" fetch origin "+refs/pull/$PR/head:$REF" --force --quiet
END_MAIN="$(as_dealix git -C "$REPO" rev-parse origin/main)"
END_HEAD="$(as_dealix git -C "$REPO" rev-parse "$REF")"
printf 'START_MAIN=%s\nEND_MAIN=%s\nSTART_PR_HEAD=%s\nEND_PR_HEAD=%s\nLOCAL_HEAD=%s\n' \
  "$MAIN" "$END_MAIN" "$HEAD" "$END_HEAD" "$END_LOCAL"
[[ "$MAIN" == "$END_MAIN" ]] || hold MAIN_MOVED_DURING_ACCEPTANCE
[[ "$HEAD" == "$END_HEAD" ]] || hold PR_HEAD_MOVED_DURING_ACCEPTANCE
[[ "$HEAD" == "$END_LOCAL" ]] || hold LOCAL_HEAD_MOVED
[[ -z "$(as_dealix git -C "$WT" status --porcelain)" ]] || hold ACCEPTANCE_MUTATED_SOURCE
printf 'HEAD_STABILITY=PASS\n'

{
  printf 'DEALIX_PR1600_EXACT_FOCUSED\n'
  printf 'TIMESTAMP=%s\n' "$(date -Is)"
  printf 'MAIN=%s\n' "$MAIN"
  printf 'PR_HEAD=%s\n' "$HEAD"
  printf 'MERGE_SIMULATION=PASS\n'
  printf 'FOCUSED_ACCEPTANCE=PASS\n'
  printf 'HEAD_STABILITY=PASS\n'
  printf 'FULL_PYTEST_EXECUTED=false\n'
  printf 'MERGE_EXECUTED=false\n'
  printf 'DEPLOY_EXECUTED=false\n'
  printf 'RAILWAY_STAGED_APPLY=false\n'
  printf 'PRODUCTION_GREEN=false\n'
} >"$PROOF/RECEIPT.txt"
cat "$PROOF/RECEIPT.txt"
printf '\nRESULT=PR1600_CURRENT_EXACT_FOCUSED_PASS\n'
printf 'PROOF=%s\n' "$PROOF"
printf 'NEXT=FULL_PYTHON_ON_THIS_EXACT_HEAD_ONLY\n'
