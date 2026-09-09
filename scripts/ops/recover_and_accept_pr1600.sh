#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

# Dealix PR #1600 execution-plane closure.
# Scope: recover the existing self-hosted Actions runner and existing private
# Issue bridge, then execute the existing exact-head PR #1600 acceptance.
# Explicitly NOT in scope: merge, deploy/redeploy, Railway staged apply,
# DNS/DB/secret mutation, external send, publish, payment/refund, or contracts.

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
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
RUNNER_INSTALLER="$SCRIPT_DIR/install_dealix_self_hosted_runner.sh"
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
[[ -x "$RUNNER_INSTALLER" ]] || { echo "BLOCKED: runner installer missing"; exit 5; }
[[ -x "$ACCEPTANCE" || -f "$ACCEPTANCE" ]] || { echo "BLOCKED: PR1600 acceptance runner missing"; exit 6; }

exec 9>"$LOCK"
flock -n 9 || { echo "RESULT=HOLD_ALREADY_RUNNING"; exit 75; }

install -d -m 0750 -o root -g root "$CONTROL/proof"
install -d -m 0700 -o root -g root "$PROOF"
exec > >(tee -a "$PROOF/run.log") 2>&1

printf '=== DEALIX PR1600 EXECUTION-PLANE RECOVERY ===\n'
date -Is
printf 'production_green=false\nmerge_executed=false\ndeploy_executed=false\n'

printf '\n=== 1. AUTHORITY ===\n'
command -v gh >/dev/null 2>&1 || hold GH_MISSING
sudo -iu "$RUN_USER" gh auth status >/dev/null 2>&1 || hold GH_AUTH_MISSING
LOGIN="$(sudo -iu "$RUN_USER" gh api user --jq '.login' 2>/dev/null || true)"
PRIVATE="$(sudo -iu "$RUN_USER" gh api "repos/$REPOSITORY" --jq '.private' 2>/dev/null || true)"
printf 'github_login=%s\nrepository_private=%s\n' "${LOGIN:-unknown}" "${PRIVATE:-unknown}"
[[ "$LOGIN" == "$FOUNDER" ]] || hold FOUNDER_AUTH_MISMATCH
[[ "$PRIVATE" == "true" ]] || hold REPOSITORY_NOT_PRIVATE

printf '\n=== 2. SELF-HOSTED RUNNER ===\n'
bash "$RUNNER_INSTALLER" | tee "$PROOF/runner-recovery.log"
[[ -f "$RUNNER_DIR/.runner" ]] || hold RUNNER_NOT_CONFIGURED
[[ -x "$RUNNER_DIR/svc.sh" ]] || hold RUNNER_SERVICE_HELPER_MISSING
"$RUNNER_DIR/svc.sh" status | tee "$PROOF/runner-status.log" || hold RUNNER_SERVICE_UNHEALTHY
printf 'SELF_HOSTED_RUNNER=PASS\n'

printf '\n=== 3. PRIVATE ISSUE BRIDGE ===\n'
# Never call the bridge installer here. Its explicit bootstrap intentionally
# advances past history and would discard the current pending founder commands.
systemctl cat "$BRIDGE_TIMER" >/dev/null 2>&1 || hold BRIDGE_TIMER_UNIT_MISSING
systemctl cat "$BRIDGE_SERVICE" >/dev/null 2>&1 || hold BRIDGE_SERVICE_UNIT_MISSING

systemctl reset-failed "$BRIDGE_SERVICE" >/dev/null 2>&1 || true
if ! systemctl is-active --quiet "$BRIDGE_TIMER"; then
  systemctl start "$BRIDGE_TIMER" || hold BRIDGE_TIMER_START_FAILED
fi
systemctl is-active --quiet "$BRIDGE_TIMER" || hold BRIDGE_TIMER_INACTIVE

# One synchronous poll cycle drains the durable queue in order. Existing bridge
# state decides whether a command is safe to execute/resume; missing/corrupt or
# ambiguous state fails closed inside the bridge.
if ! systemctl start "$BRIDGE_SERVICE"; then
  systemctl --no-pager --full status "$BRIDGE_SERVICE" | sed -n '1,80p' || true
  hold BRIDGE_POLL_FAILED
fi
BRIDGE_RESULT="$(systemctl show "$BRIDGE_SERVICE" -p Result --value 2>/dev/null || true)"
BRIDGE_STATUS="$(systemctl show "$BRIDGE_SERVICE" -p ExecMainStatus --value 2>/dev/null || true)"
printf 'bridge_timer=active\nbridge_result=%s\nbridge_exec_status=%s\n' "${BRIDGE_RESULT:-unknown}" "${BRIDGE_STATUS:-unknown}"
[[ "$BRIDGE_RESULT" == "success" && "${BRIDGE_STATUS:-1}" == "0" ]] || hold BRIDGE_RESULT_NOT_SUCCESS
printf 'ISSUE_BRIDGE=PASS\n'

printf '\n=== 4. CURRENT EXACT-HEAD ACCEPTANCE ===\n'
# The acceptance wrapper re-resolves main + PR head at start and end, creates a
# detached worktree, runs the full trust surface, and fails if either ref moves.
bash "$ACCEPTANCE" | tee "$PROOF/pr1600-acceptance.log"

grep -qx 'RESULT=PR1600_CURRENT_EXACT_FULL_PASS' "$PROOF/pr1600-acceptance.log" \
  || hold ACCEPTANCE_RESULT_MISSING

grep -qx 'EXACT_HEAD_STABILITY=PASS' "$PROOF/pr1600-acceptance.log" \
  || hold ACCEPTANCE_HEAD_STABILITY_MISSING

printf '\n=== FINAL ===\n'
printf 'SELF_HOSTED_RUNNER=PASS\n'
printf 'ISSUE_BRIDGE=PASS\n'
printf 'PR1600_EXACT_HEAD_ACCEPTANCE=PASS\n'
printf 'MERGE_EXECUTED=false\nDEPLOY_EXECUTED=false\nRAILWAY_STAGED_APPLY=false\n'
printf 'DNS_MUTATION=false\nDB_MUTATION=false\nSECRET_MUTATION=false\n'
printf 'EXTERNAL_SEND=false\nPAYMENT_EXECUTION=false\nPUBLIC_PUBLISH=false\n'
printf 'PRODUCTION_GREEN=false\n'
printf 'RESULT=PR1600_EXECUTION_PLANE_RECOVERED_AND_EXACT_HEAD_ACCEPTED\n'
printf 'PROOF=%s\n' "$PROOF"
