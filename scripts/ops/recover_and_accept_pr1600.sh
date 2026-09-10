#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

# Dealix PR #1600 execution-plane closure.
# This command is deliberately read/test + observe only. It accepts the exact
# current PR head first, then proves the existing runner/Issue bridge health.
# It NEVER installs, refreshes, starts, stops, or restarts live control-plane
# code/services. Any repair that would mutate the live control plane is L5 and
# must be executed separately with action-bound authority after acceptance.

export TZ=Asia/Riyadh
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
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

REPOSITORY="Dealix-sa/dealix"
FOUNDER="VoXc2"
RUN_USER="dealix"
CONTROL="/opt/dealix/control"
RUNNER_DIR="/opt/dealix/actions-runner"
BRIDGE_TIMER="dealix-vps-issue-bridge.timer"
BRIDGE_SERVICE="dealix-vps-issue-bridge.service"
SCRIPT_DIR="$(CDPATH='' cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ACCEPTANCE="$SCRIPT_DIR/run_pr1600_live_full_acceptance.sh"
LOCK="/run/lock/dealix-pr1600-execution-plane.lock"
STAMP="$(date +%Y%m%dT%H%M%S)"
PROOF="$CONTROL/proof/pr1600-execution-plane-$STAMP"

hold() {
  local reason="$1"
  echo "RESULT=HOLD_$reason"
  echo "PROOF=$PROOF"
  echo "PRODUCTION_GREEN=false"
  echo "MERGE_EXECUTED=false"
  echo "DEPLOY_EXECUTED=false"
  exit 1
}

[[ "$(id -u)" -eq 0 ]] || { echo "BLOCKED: run as root"; exit 2; }
command -v flock >/dev/null 2>&1 || { echo "BLOCKED: flock missing"; exit 3; }
id "$RUN_USER" >/dev/null 2>&1 || { echo "BLOCKED: missing user $RUN_USER"; exit 4; }
[[ -x "$ACCEPTANCE" || -f "$ACCEPTANCE" ]] || { echo "BLOCKED: PR1600 acceptance runner missing"; exit 5; }

exec 9>"$LOCK"
flock -n 9 || { echo "RESULT=HOLD_ALREADY_RUNNING"; exit 75; }

mkdir -p "$CONTROL/proof"
install -d -m 0700 -o root -g root "$PROOF"
exec > >(tee -a "$PROOF/run.log") 2>&1

printf '=== DEALIX PR1600 EXECUTION-PLANE TRUST CLOSURE ===\n'
date -Is
printf 'production_green=false\nmerge_executed=false\ndeploy_executed=false\ncontrol_plane_mutation=false\n'

printf '\n=== 1. AUTHORITY ===\n'
command -v gh >/dev/null 2>&1 || hold GH_MISSING
sudo -iu "$RUN_USER" gh auth status >/dev/null 2>&1 || hold GH_AUTH_MISSING
LOGIN="$(sudo -iu "$RUN_USER" gh api user --jq '.login' 2>/dev/null || true)"
PRIVATE="$(sudo -iu "$RUN_USER" gh api "repos/$REPOSITORY" --jq '.private' 2>/dev/null || true)"
printf 'github_login=%s\nrepository_private=%s\n' "${LOGIN:-unknown}" "${PRIVATE:-unknown}"
[[ "$LOGIN" == "$FOUNDER" ]] || hold FOUNDER_AUTH_MISMATCH
[[ "$PRIVATE" == "true" ]] || hold REPOSITORY_NOT_PRIVATE

printf '\n=== 2. CURRENT EXACT-HEAD ACCEPTANCE — BEFORE CONTROL-PLANE OBSERVATION ===\n'
bash "$ACCEPTANCE" | tee "$PROOF/pr1600-acceptance.log"
grep -qx 'RESULT=PR1600_CURRENT_EXACT_FULL_PASS' "$PROOF/pr1600-acceptance.log" \
  || hold ACCEPTANCE_RESULT_MISSING
grep -qx 'EXACT_HEAD_STABILITY=PASS' "$PROOF/pr1600-acceptance.log" \
  || hold ACCEPTANCE_HEAD_STABILITY_MISSING
printf 'PR1600_EXACT_HEAD_ACCEPTANCE=PASS\n'

printf '\n=== 3. SELF-HOSTED RUNNER — OBSERVE ONLY ===\n'
if [[ ! -f "$RUNNER_DIR/.runner" || ! -x "$RUNNER_DIR/svc.sh" ]]; then
  printf 'SELF_HOSTED_RUNNER=HOLD reason=runner_not_configured control_plane_mutation=false\n'
  hold RUNNER_REPAIR_REQUIRES_ACTION_BOUND_L5
fi
set +e
"$RUNNER_DIR/svc.sh" status > "$PROOF/runner-status.log" 2>&1
RUNNER_RC=$?
set -e
cat "$PROOF/runner-status.log" || true
if (( RUNNER_RC != 0 )); then
  printf 'SELF_HOSTED_RUNNER=HOLD reason=service_unhealthy control_plane_mutation=false\n'
  hold RUNNER_REPAIR_REQUIRES_ACTION_BOUND_L5
fi
printf 'SELF_HOSTED_RUNNER=PASS observed_only=true\n'

printf '\n=== 4. PRIVATE ISSUE BRIDGE — OBSERVE ONLY ===\n'
systemctl cat "$BRIDGE_TIMER" >/dev/null 2>&1 || hold BRIDGE_TIMER_UNIT_MISSING
systemctl cat "$BRIDGE_SERVICE" >/dev/null 2>&1 || hold BRIDGE_SERVICE_UNIT_MISSING
TIMER_STATE="$(systemctl is-active "$BRIDGE_TIMER" 2>/dev/null || true)"
SERVICE_ACTIVE="$(systemctl is-active "$BRIDGE_SERVICE" 2>/dev/null || true)"
SERVICE_RESULT="$(systemctl show "$BRIDGE_SERVICE" -p Result --value 2>/dev/null || true)"
SERVICE_STATUS="$(systemctl show "$BRIDGE_SERVICE" -p ExecMainStatus --value 2>/dev/null || true)"
printf 'bridge_timer=%s\nbridge_service_active=%s\nbridge_result=%s\nbridge_exec_status=%s\n' \
  "${TIMER_STATE:-unknown}" "${SERVICE_ACTIVE:-unknown}" "${SERVICE_RESULT:-unknown}" "${SERVICE_STATUS:-unknown}"
[[ "$TIMER_STATE" == "active" ]] || hold BRIDGE_REPAIR_REQUIRES_ACTION_BOUND_L5
# A timer-driven oneshot bridge is normally inactive between successful polls.
if [[ "$SERVICE_ACTIVE" != "active" && "$SERVICE_ACTIVE" != "inactive" ]]; then
  hold BRIDGE_REPAIR_REQUIRES_ACTION_BOUND_L5
fi
if [[ -n "$SERVICE_RESULT" && "$SERVICE_RESULT" != "success" ]]; then
  hold BRIDGE_REPAIR_REQUIRES_ACTION_BOUND_L5
fi
if [[ -n "$SERVICE_STATUS" && "$SERVICE_STATUS" != "0" ]]; then
  hold BRIDGE_REPAIR_REQUIRES_ACTION_BOUND_L5
fi
printf 'ISSUE_BRIDGE=PASS observed_only=true\n'

printf '\n=== FINAL ===\n'
printf 'PR1600_EXACT_HEAD_ACCEPTANCE=PASS\n'
printf 'SELF_HOSTED_RUNNER=PASS observed_only=true\n'
printf 'ISSUE_BRIDGE=PASS observed_only=true\n'
printf 'CONTROL_PLANE_MUTATION=false\n'
printf 'MERGE_EXECUTED=false\nDEPLOY_EXECUTED=false\nRAILWAY_STAGED_APPLY=false\n'
printf 'DNS_MUTATION=false\nDB_MUTATION=false\nSECRET_MUTATION=false\n'
printf 'EXTERNAL_SEND=false\nPAYMENT_EXECUTION=false\nPUBLIC_PUBLISH=false\n'
printf 'PRODUCTION_GREEN=false\n'
printf 'RESULT=PR1600_EXECUTION_PLANE_HEALTHY_AND_EXACT_HEAD_ACCEPTED\n'
printf 'PROOF=%s\n' "$PROOF"