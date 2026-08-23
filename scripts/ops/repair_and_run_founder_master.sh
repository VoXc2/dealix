#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

REPO_SLUG="${DEALIX_REPO_SLUG:-Dealix-sa/dealix}"
RUN_USER="${DEALIX_RUN_USER:-dealix}"
REPO="${DEALIX_REPO_ROOT:-/opt/dealix/workspace/dealix}"
PROOF_ROOT="${DEALIX_EXECUTIVE_PROOF_ROOT:-/opt/dealix/executive-proof}"
PR_NUMBER="${DEALIX_FOUNDER_MASTER_PR:-1145}"
TMP="$(mktemp -d /tmp/dealix-founder-repair.XXXXXX)"
trap 'rm -rf "$TMP"' EXIT

log() { printf '[%s] %s\n' "$(date -Is)" "$*"; }
section() { printf '\n============================================================\n%s\n============================================================\n' "$*"; }

if [[ "$(id -u)" -ne 0 ]]; then
  echo "BLOCKED: run as root on the Dealix VPS"
  exit 2
fi
id "$RUN_USER" >/dev/null 2>&1 || { echo "BLOCKED: missing user $RUN_USER"; exit 3; }
[[ -d "$REPO/.git" ]] || { echo "BLOCKED: missing repo $REPO"; exit 4; }
sudo -iu "$RUN_USER" gh auth status >/dev/null 2>&1 || { echo "BLOCKED: gh auth missing"; exit 5; }

export DEALIX_EXTERNAL_OUTREACH_ENABLED=false
export EXTERNAL_OUTREACH_ENABLED=false
export AUTO_SEND_ENABLED=false
export WHATSAPP_ALLOW_LIVE_SEND=false
export MOYASAR_LIVE_MODE=0
export DEALIX_LIVE_CHARGE=false
export DEALIX_AUTO_MERGE=false
export DEALIX_PRODUCTION_MUTATION=false
export AGENT_APPROVAL_MODE=required
export DEALIX_PROOF_MODE=verified_only

section "1. RESOLVE CURRENT SOURCE OF TRUTH"
MAIN_SHA="$(sudo -iu "$RUN_USER" gh api "repos/${REPO_SLUG}/commits/main" --jq '.sha')"
LOCAL_SHA="$(sudo -iu "$RUN_USER" git -C "$REPO" rev-parse HEAD)"
PR_HEAD="$(sudo -iu "$RUN_USER" gh pr view "$PR_NUMBER" --repo "$REPO_SLUG" --json headRefOid --jq '.headRefOid')"
printf 'github_main=%s\nlocal_head_before=%s\nmaster_pr_head=%s\n' "$MAIN_SHA" "$LOCAL_SHA" "$PR_HEAD"

section "2. FETCH CURRENT MAIN ACTIVATOR DIRECTLY FROM GITHUB"
ACTIVATOR="$TMP/activate_dealix_from_main.sh"
sudo -iu "$RUN_USER" gh api \
  -H 'Accept: application/vnd.github.raw+json' \
  "repos/${REPO_SLUG}/contents/scripts/ops/activate_dealix_from_main.sh?ref=${MAIN_SHA}" \
  >"$ACTIVATOR"
[[ -s "$ACTIVATOR" ]] || { echo "BLOCKED: could not fetch activator from current main"; exit 6; }
chmod 0700 "$ACTIVATOR"
bash -n "$ACTIVATOR"
echo "ACTIVATOR_FETCH=PASS"

section "3. SAFE MAIN SYNCHRONIZATION"
DEALIX_SOURCE_REF="$MAIN_SHA" DEALIX_REPO_ROOT="$REPO" bash "$ACTIVATOR"
LOCAL_AFTER="$(sudo -iu "$RUN_USER" git -C "$REPO" rev-parse HEAD)"
printf 'local_head_after=%s\n' "$LOCAL_AFTER"
[[ "$LOCAL_AFTER" == "$MAIN_SHA" ]] || { echo "BLOCKED: local repo did not reach current main"; exit 7; }
echo "MAIN_SYNC=PASS"

section "4. VERIFY CANONICAL SCRIPTS ARRIVED"
required=(
  scripts/ops/activate_dealix_from_main.sh
  scripts/ops/dealix_founder_money_command.sh
  scripts/ops/dealix_canonical_revenue_cycle.sh
  scripts/ops/verify_canonical_company_autopilot.py
  docs/ops/DEALIX_EXECUTIVE_AUTOPILOT_MASTER_PROMPT.md
)
missing=0
for rel in "${required[@]}"; do
  if [[ -e "$REPO/$rel" ]]; then
    echo "PASS $rel"
  else
    echo "MISSING $rel"
    missing=1
  fi
done
[[ "$missing" -eq 0 ]] || { echo "BLOCKED: canonical current-main files missing"; exit 8; }

section "5. FETCH AND VERIFY EXACT FOUNDER MASTER FROM PR"
MASTER="$TMP/dealix_founder_master_command.sh"
sudo -iu "$RUN_USER" gh api \
  -H 'Accept: application/vnd.github.raw+json' \
  "repos/${REPO_SLUG}/contents/scripts/ops/dealix_founder_master_command.sh?ref=${PR_HEAD}" \
  >"$MASTER"
[[ -s "$MASTER" ]] || { echo "BLOCKED: could not fetch founder master"; exit 9; }
chmod 0700 "$MASTER"
bash -n "$MASTER"
if grep -q 'MOYASIR_LIVE_MODE' "$MASTER"; then
  echo "BLOCKED: stale Moyasar typo still present in exact PR source"
  exit 10
fi
grep -Fq 'MOYASAR_LIVE_MODE=0' "$MASTER" || { echo "BLOCKED: Moyasar live-mode kill switch missing"; exit 11; }
grep -Fq 'hermes" chat -Q --ignore-rules --toolsets clarify --max-turns 1 --query-file' "$MASTER" || {
  echo "BLOCKED: Hermes synthesis is not using the compatible bounded chat path"
  exit 12
}
if grep -Fq -- '--toolsets terminal -z' "$MASTER"; then
  echo "BLOCKED: obsolete Hermes oneshot path still present"
  exit 13
fi
echo "FOUNDER_MASTER_SOURCE_GUARDS=PASS"

section "6. RUN EXACT MASTER WITH CANONICAL ONE-SHOT SYNTHESIS"
set +e
DEALIX_SYNC_MAIN=0 \
DEALIX_RUN_LOCAL_AI=1 \
DEALIX_RUN_COMMERCIAL_GATE=1 \
DEALIX_RUN_REVENUE_DAILY=1 \
DEALIX_RUN_WEEKLY_PROOF=1 \
bash "$MASTER"
MASTER_RC=$?
set -e
echo "FOUNDER_MASTER_RC=$MASTER_RC"

LATEST="$(find "$PROOF_ROOT" -mindepth 1 -maxdepth 1 -type d -printf '%T@ %p\n' 2>/dev/null | sort -nr | head -1 | cut -d' ' -f2-)"
[[ -n "$LATEST" ]] || { echo "BLOCKED: no proof directory produced"; exit 14; }
echo "LATEST_PROOF=$LATEST"

section "7. VERIFY CANONICAL EXECUTIVE SYNTHESIS RECEIPT"
if [[ -f "$LATEST/executive_ai.rc" ]]; then
  SYNTH_RC="$(cat "$LATEST/executive_ai.rc")"
  echo "HERMES_SYNTHESIS_RC=$SYNTH_RC"
  tail -120 "$LATEST/executive_ai.txt" 2>/dev/null || true
else
  echo "HERMES_SYNTHESIS=NO_RECEIPT"
fi

section "8. FAILED UNIT DIAGNOSTIC AFTER CURRENT-MAIN ACTIVATION"
for unit in \
  dealix-agent-council.service \
  dealix-company@morning-fallback.service \
  dealix-company@nightly.service \
  dealix-company@production.service \
  hermes-dealix.service
 do
  echo "--- $unit ---"
  systemctl status "$unit" --no-pager -n 12 2>/dev/null || true
 done

section "9. SURFACE REAL COMMERCIAL BLOCKER"
for evidence in commercial_go_live local_stack_verify founder_money; do
  if [[ -f "$LATEST/${evidence}.txt" ]]; then
    echo "--- ${evidence}.txt ---"
    tail -120 "$LATEST/${evidence}.txt" || true
  fi
done

section "10. FINAL PROOF"
FINAL_LOCAL="$(sudo -iu "$RUN_USER" git -C "$REPO" rev-parse HEAD)"
printf 'GITHUB_MAIN=%s\nLOCAL_HEAD=%s\nMASTER_RC=%s\nLATEST_PROOF=%s\n' "$MAIN_SHA" "$FINAL_LOCAL" "$MASTER_RC" "$LATEST"
if [[ "$FINAL_LOCAL" == "$MAIN_SHA" ]]; then
  echo "MAIN_SYNC_FINAL=PASS"
else
  echo "MAIN_SYNC_FINAL=DEGRADED"
fi
cat <<'EOF'
NO_MERGE=YES
NO_PRODUCTION_MUTATION=YES
NO_DNS_MUTATION=YES
NO_EXTERNAL_SEND=YES
NO_PAYMENT=YES
NO_FAKE_PROOF=YES
EOF

echo "DEALIX_FOUNDER_REPAIR=COMPLETE"
