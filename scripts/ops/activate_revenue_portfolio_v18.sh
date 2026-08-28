#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

# Dealix V18 Revenue Portfolio Control Plane — bounded server activation.
#
# This adapter is intentionally authority-aware but execution-neutral:
# - it reads the ACTIVE checkout's commercial authority;
# - it accepts both known authority modes (fail-closed or channel-governed);
# - it NEVER performs an external send itself;
# - it NEVER starts a foreground LLM/Hermes one-shot;
# - it creates no timer/cron/agent and performs no merge/deploy/payment/tender.
#
# The goal is durable truth + handoff, not another execution owner.

[[ "$(id -u)" -eq 0 ]] || { echo "ERROR=RUN_AS_ROOT"; exit 20; }

RUN_USER="${DEALIX_RUN_USER:-dealix}"
RUN_GROUP="${DEALIX_RUN_GROUP:-dealix}"
RUN_HOME="${DEALIX_RUN_HOME:-/home/dealix}"
REPO="${DEALIX_REPO_ROOT:-/opt/dealix/workspace/dealix}"
REPO_SLUG="${DEALIX_REPO_SLUG:-Dealix-sa/dealix}"

OS_ROOT="${DEALIX_OS_ROOT:-/opt/dealix/company-os}"
CURRENT="$OS_ROOT/current"
FOUNDER="$OS_ROOT/founder-os"
PROMPTS="/opt/dealix/executive-prompts"
PROOF_ROOT="/opt/dealix/executive-proof/revenue-portfolio-v18"
LOCK="/run/lock/dealix-revenue-portfolio-v18.lock"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
RUN="$PROOF_ROOT/$STAMP"
POLICY="$FOUNDER/config/REVENUE_PORTFOLIO_CONTROL_PLANE_V18.json"
STATUS="$CURRENT/REVENUE_PORTFOLIO_V18_STATUS.json"
PROMPT="$PROMPTS/DEALIX_V18_REVENUE_PORTFOLIO_CONTROL_PLANE.md"

install -d -o "$RUN_USER" -g "$RUN_GROUP" -m 0750 \
  "$CURRENT" "$FOUNDER/config" "$PROMPTS" "$PROOF_ROOT" "$RUN"

exec 9>"$LOCK"
flock -n 9 || { echo "V18=SKIPPED_LOCKED"; exit 0; }

section(){ printf '\n================================================================\n %s\n================================================================\n' "$*"; }
as_dealix(){ runuser -u "$RUN_USER" -- env HOME="$RUN_HOME" USER="$RUN_USER" LOGNAME="$RUN_USER" XDG_RUNTIME_DIR="/run/user/$(id -u "$RUN_USER")" PATH="$RUN_HOME/.local/bin:$RUN_HOME/.openclaw/bin:/usr/local/bin:/usr/bin:/bin" "$@"; }

section "1. HOST / REPO TRUTH"
[[ -d "$REPO/.git" ]] || { echo "ERROR=REPO_NOT_FOUND"; exit 21; }
hostname | tee "$RUN/hostname.txt"
date -Is | tee "$RUN/date.txt"
as_dealix git -C "$REPO" status -sb >"$RUN/git-status.txt" 2>&1 || true
as_dealix git -C "$REPO" rev-parse HEAD >"$RUN/head.txt" 2>&1 || true
as_dealix git -C "$REPO" rev-parse origin/main >"$RUN/origin-main.txt" 2>&1 || true
printf 'HEAD=%s\n' "$(cat "$RUN/head.txt" 2>/dev/null || echo UNKNOWN)"
printf 'ORIGIN_MAIN=%s\n' "$(cat "$RUN/origin-main.txt" 2>/dev/null || echo UNKNOWN)"

section "2. CORE RUNTIME — READ ONLY"
for svc in docker ollama tailscaled hermes-dealix dealix-llm-router; do
  if systemctl list-unit-files "$svc.service" >/dev/null 2>&1; then
    printf '%s=' "$svc"
    systemctl is-active "$svc.service" || true
  fi
done
if command -v docker >/dev/null 2>&1; then
  docker ps --format '{{.Names}} {{.Status}}' >"$RUN/docker-ps.txt" 2>&1 || true
fi
if curl -fsS --max-time 5 http://127.0.0.1:11434/api/tags >/dev/null 2>&1; then
  echo "OLLAMA_LOOPBACK=PASS"
else
  echo "OLLAMA_LOOPBACK=UNKNOWN_OR_FAIL"
fi
if command -v ss >/dev/null 2>&1 && ss -lnt 2>/dev/null | grep -Eq ':11434[[:space:]]'; then
  if ss -lnt 2>/dev/null | grep ':11434' | grep -vqE '127\.0\.0\.1:11434|\[::1\]:11434'; then
    echo "OLLAMA_PUBLIC_BIND=FAIL"
    exit 22
  fi
fi

section "3. ACTIVE COMMERCIAL AUTHORITY"
GATE="$REPO/dealix/config/first_launch_offer_gate.yaml"
BUSINESS="$REPO/docs/DEALIX_BUSINESS_MODEL.md"
IDENTITY="$REPO/COMMERCIAL_IDENTITY.md"
for f in "$GATE" "$BUSINESS" "$IDENTITY"; do
  [[ -f "$f" ]] || { echo "ERROR=MISSING_AUTHORITY_FILE:$f"; exit 23; }
done

AUTHORITY_MODE="UNKNOWN"
if grep -Eq 'external_send_allowed:[[:space:]]*false' "$GATE" && grep -Eq 'warm_consented_only' "$GATE"; then
  AUTHORITY_MODE="FAIL_CLOSED"
elif grep -Eq 'external_send_allowed:[[:space:]]*true' "$GATE" && grep -Eq 'channel_eligible_evidence_backed' "$GATE"; then
  AUTHORITY_MODE="CHANNEL_GOVERNED_OPEN"
else
  echo "ERROR=UNKNOWN_COMMERCIAL_AUTHORITY_MODE"
  exit 24
fi

echo "ACTIVE_COMMERCIAL_AUTHORITY_MODE=$AUTHORITY_MODE"
echo "SERVER_CONTROL_EXTERNAL_SEND=BLOCKED"
echo "SERVER_CONTROL_CUSTOMER_FACING_EXECUTION=NONE"

if grep -RInE '(499[[:space:]]*SAR|999[[:space:]]*SAR|1500[[:space:]]*SAR|money[- ]back|guaranteed revenue)' \
  "$REPO/data/commercial" "$REPO/docs/commercial" 2>/dev/null >"$RUN/legacy-commercial-hits.txt"; then
  echo "LEGACY_COMMERCIAL_HITS=FOUND_REVIEW_REQUIRED"
else
  echo "LEGACY_COMMERCIAL_HITS=NONE_IN_CANONICAL_PATHS"
fi

authority_hash(){ sha256sum "$1" | awk '{print $1}'; }

section "4. GITHUB EXECUTION GRAPH — READ ONLY"
if command -v gh >/dev/null 2>&1; then
  for n in 1277 1273 1274; do
    as_dealix gh issue view "$n" --repo "$REPO_SLUG" --json number,title,state,url >"$RUN/issue-$n.json" 2>&1 || true
  done
  for n in 1275 1276 1281 1283; do
    as_dealix gh pr view "$n" --repo "$REPO_SLUG" --json number,title,state,isDraft,mergeable,headRefName,headRefOid,baseRefName,url >"$RUN/pr-$n.json" 2>&1 || true
  done
fi

section "5. ECONOMIC TRUTH — READ ONLY"
REV=""
for p in /usr/local/bin/dealix-revenue "$REPO/bin/dealix-revenue"; do
  [[ -x "$p" ]] && { REV="$p"; break; }
done

REAL_CONTACTS="UNKNOWN"
VERIFIED_PAID_PILOTS="UNKNOWN"
VERIFIED_REVENUE_SAR="UNKNOWN"
INTERACTION_ROWS="UNKNOWN"
CANDIDATE_ROWS="UNKNOWN"
TRUTH_FIREWALL_ATTENTION="UNKNOWN"

if [[ -n "$REV" ]]; then
  for sub in today interactions candidates money; do
    set +e
    timeout 60 runuser -u "$RUN_USER" -- env HOME="$RUN_HOME" USER="$RUN_USER" LOGNAME="$RUN_USER" XDG_RUNTIME_DIR="/run/user/$(id -u "$RUN_USER")" PATH="$RUN_HOME/.local/bin:$RUN_HOME/.openclaw/bin:/usr/local/bin:/usr/bin:/bin" "$REV" "$sub" >"$RUN/revenue-$sub.txt" 2>&1
    rc=$?
    set -e
    echo "DEALIX_REVENUE_${sub^^}_RC=$rc"
  done

  if [[ -s "$RUN/revenue-money.txt" ]]; then
    REAL_CONTACTS="$(awk -F= '/^REAL_CONTACTS=/{v=$2} END{if(v!="")print v}' "$RUN/revenue-money.txt")"
    VERIFIED_PAID_PILOTS="$(awk -F= '/^VERIFIED_PAID_PILOTS=/{v=$2} END{if(v!="")print v}' "$RUN/revenue-money.txt")"
    VERIFIED_REVENUE_SAR="$(awk -F= '/^VERIFIED_REVENUE_SAR=/{v=$2} END{if(v!="")print v}' "$RUN/revenue-money.txt")"
  fi
  REAL_CONTACTS="${REAL_CONTACTS:-UNKNOWN}"
  VERIFIED_PAID_PILOTS="${VERIFIED_PAID_PILOTS:-UNKNOWN}"
  VERIFIED_REVENUE_SAR="${VERIFIED_REVENUE_SAR:-UNKNOWN}"

  INTERACTION_ROWS="$(awk -F'\t' 'NF>=3{c++} END{print c+0}' "$RUN/revenue-interactions.txt" 2>/dev/null || echo 0)"
  CANDIDATE_ROWS="$(awk -F'\t' 'NF>=3{c++} END{print c+0}' "$RUN/revenue-candidates.txt" 2>/dev/null || echo 0)"
  TRUTH_FIREWALL_ATTENTION="NO"
  if [[ "$REAL_CONTACTS" == "0" ]] && { [[ "$INTERACTION_ROWS" -gt 0 ]] || [[ "$CANDIDATE_ROWS" -gt 0 ]]; }; then
    TRUTH_FIREWALL_ATTENTION="YES_UNVERIFIED_OR_SELF_TEST_MARKERS_VISIBLE"
  fi
else
  echo "DEALIX_REVENUE_CLI=NOT_FOUND"
fi

echo "REAL_CONTACTS=$REAL_CONTACTS"
echo "VERIFIED_PAID_PILOTS=$VERIFIED_PAID_PILOTS"
echo "VERIFIED_REVENUE_SAR=$VERIFIED_REVENUE_SAR"
echo "INTERACTION_ROWS=$INTERACTION_ROWS"
echo "CANDIDATE_ROWS=$CANDIDATE_ROWS"
echo "TRUTH_FIREWALL_ATTENTION=$TRUTH_FIREWALL_ATTENTION"

section "6. WRITE POLICY + EXECUTIVE HANDOFF"
python3 - "$POLICY" "$AUTHORITY_MODE" <<'PY'
import json, sys
from datetime import datetime, timezone
p, authority_mode = sys.argv[1:]
data={
  "schema":"dealix.revenue-portfolio-control-plane.v18.1",
  "generated_at":datetime.now(timezone.utc).isoformat(),
  "north_star":"FIRST_VERIFIED_PAID_PILOT",
  "active_commercial_authority_mode":authority_mode,
  "server_control_external_send":False,
  "hierarchy":{"1277":"PORTFOLIO_WHERE","1273":"ACCOUNT_WHAT","1274":"CAMPAIGN_HOW","1275":"REVENUE_MESH_IMPLEMENTATION","1276":"UNIFIED_COMMERCIAL_IMPLEMENTATION","1281":"SERVER_CONTROL_ADAPTER","1283":"BRAND_DISTRIBUTION_AUTOPILOT"},
  "infrastructure_freeze":True,
  "truth_rules":["research_is_not_relationship","target_is_not_lead","draft_is_not_send","provider_acceptance_is_not_delivery","invoice_is_not_revenue","payment_requires_evidence","synthetic_is_not_customer_proof","self_test_never_qualifies"],
  "authority":{"l0_l4_internal":True,"server_control_external_send":False,"merge_main":False,"production_mutation":False,"dns_mutation":False,"payment":False,"tender_submission":False},
  "resource_rule":"maximize_risk_adjusted_expected_verified_movement_per_scarce_resource",
  "notification_rule":"notify_only_on_material_state_change_or_real_external_signal",
  "scheduler_rule":"reuse_existing_owner_no_duplicate_scheduler",
  "llm_rule":"no_foreground_llm_in_server_activation"
}
with open(p,'w',encoding='utf-8') as f:
    json.dump(data,f,ensure_ascii=False,indent=2)
PY
chown "$RUN_USER:$RUN_GROUP" "$POLICY"; chmod 0640 "$POLICY"

cat >"$PROMPT" <<'PROMPT'
# DEALIX V18.1 — REVENUE PORTFOLIO CONTROL PLANE HANDOFF
North star: FIRST VERIFIED PAID PILOT → CUSTOMER PROOF → REPEATABLE OFFER → RECURRING REVENUE → PRODUCTIZED COMPANY OS.

This file is a durable handoff for existing owners. The server-control activation does not run a foreground LLM.

Hierarchy:
#1277 decides WHERE scarce Dealix resources go.
#1273 decides WHAT to do for each real account/opportunity.
#1274 owns HOW evidence/target/campaign/draft/review orchestration runs.
PR #1275 is the deterministic Revenue Mesh implementation surface.
PR #1276 is the Unified Commercial/Event/Proposal/Channel-Governance surface.
PR #1281 is server-control/readiness only.
PR #1283 is Brand + Distribution Autopilot stacked on #1276.

Truth firewall:
RESEARCH != RELATIONSHIP
TARGET != LEAD
PUBLIC CONTACT != CONSENT
DRAFT != SEND
PROVIDER_ACCEPTED != DELIVERY
QUOTE != PAYMENT
INVOICE != REVENUE
SYNTHETIC != CUSTOMER PROOF
SELF TEST != PIPELINE

Always resolve the ACTIVE checkout's authority before any customer-facing action. A Draft PR is not active authority. If authority is channel-governed, recipient-level consent/relationship/suppression/cadence/channel gates still decide eligibility. Named quote/price, contract, tender, payment and sensitive commitments retain their specific gates.

Event-to-cash priority through 3 September 2026:
REAL INTERACTION → VERIFIED RELATIONSHIP → QUALIFIED PROBLEM → MINI DIAGNOSTIC → DISCOVERY → CUSTOMER-SPECIFIC PROPOSAL → PAID PILOT → PAYMENT PROOF → DELIVERY PROOF.

Big 5: 30 Aug–2 Sep 2026, 4 PM–10 PM, ROSHN Front.
LEAP x DeepFest: 31 Aug–3 Sep 2026, RECC Malham; general admission 1 PM–9 PM.

Do not create a parallel CRM, Opportunity Graph, Company Brain, Approval Center, Proof Ledger, Revenue Engine, Proposal Engine, Agent Fleet, scheduler or CI engine.
PROMPT
chown "$RUN_USER:$RUN_GROUP" "$PROMPT"; chmod 0640 "$PROMPT"

section "7. EXISTING AUTOMATION OWNERSHIP — OBSERVE ONLY"
systemctl list-timers --all --no-pager >"$RUN/systemd-timers.txt" 2>&1 || true
HERMES=""
for p in "$RUN_HOME/.local/bin/hermes" "$RUN_HOME/.hermes/bin/hermes" /usr/local/bin/hermes /usr/bin/hermes; do
  [[ -x "$p" ]] && { HERMES="$p"; break; }
done
HERMES_LIST_RC="NA"
if [[ -n "$HERMES" ]]; then
  set +e
  timeout 60 runuser -u "$RUN_USER" -- env HOME="$RUN_HOME" USER="$RUN_USER" LOGNAME="$RUN_USER" XDG_RUNTIME_DIR="/run/user/$(id -u "$RUN_USER")" "$HERMES" cron list --all >"$RUN/hermes-crons.txt" 2>&1
  HERMES_LIST_RC=$?
  set -e
fi
echo "HERMES_LIST_RC=$HERMES_LIST_RC"
echo "HERMES_FOREGROUND_EXECUTION=DISABLED"
echo "DAILY_OPS_FOREGROUND_EXECUTION=DISABLED"
echo "NEW_TIMER_CREATED=NO"
echo "NEW_CRON_CREATED=NO"
echo "NEW_AGENT_CREATED=NO"

section "8. WRITE DURABLE RECEIPT"
HEAD="$(cat "$RUN/head.txt" 2>/dev/null || echo UNKNOWN)"
ORIGIN_MAIN="$(cat "$RUN/origin-main.txt" 2>/dev/null || echo UNKNOWN)"
python3 - "$STATUS" "$STAMP" "$HEAD" "$ORIGIN_MAIN" "$AUTHORITY_MODE" "$REAL_CONTACTS" "$VERIFIED_PAID_PILOTS" "$VERIFIED_REVENUE_SAR" "$INTERACTION_ROWS" "$CANDIDATE_ROWS" "$TRUTH_FIREWALL_ATTENTION" "$(authority_hash "$GATE")" "$(authority_hash "$BUSINESS")" "$(authority_hash "$IDENTITY")" <<'PY'
import json, sys
from datetime import datetime, timezone
(p,stamp,head,origin,authority_mode,real_contacts,paid_pilots,revenue,interaction_rows,candidate_rows,truth_attention,gate,biz,ident)=sys.argv[1:]
data={
 "schema":"dealix.revenue-portfolio-control-plane.status.v18.1",
 "generated_at":datetime.now(timezone.utc).isoformat(),
 "run_id":stamp,
 "north_star":"FIRST_VERIFIED_PAID_PILOT",
 "repo":{"head":head,"origin_main":origin},
 "active_commercial_authority_mode":authority_mode,
 "authority_hashes":{"first_launch_gate":gate,"business_model":biz,"commercial_identity":ident},
 "economic_truth":{"real_contacts":real_contacts,"verified_paid_pilots":paid_pilots,"verified_revenue_sar":revenue,"interaction_rows":interaction_rows,"candidate_rows":candidate_rows,"truth_firewall_attention":truth_attention},
 "execution":{"foreground_hermes":False,"foreground_daily_ops":False,"new_timer_created":False,"new_cron_created":False,"new_agent_created":False},
 "safety":{"server_control_external_send":False,"merge_main":False,"production_mutation":False,"payment":False,"tender_submission":False},
 "next":"EVENT_TO_CASH_REAL_INTERACTION_CAPTURE_AND_TRUTH_FIREWALL_ROOT_CAUSE"
}
with open(p,'w',encoding='utf-8') as f:
    json.dump(data,f,ensure_ascii=False,indent=2)
PY
chown "$RUN_USER:$RUN_GROUP" "$STATUS"; chmod 0640 "$STATUS"
cp "$STATUS" "$RUN/FINAL_RECEIPT.json"

section "9. FINAL"
echo "DEALIX_V18_1_SERVER_CONTROL=PASS"
echo "ACTIVE_COMMERCIAL_AUTHORITY_MODE=$AUTHORITY_MODE"
echo "SERVER_CONTROL_EXTERNAL_SEND=BLOCKED"
echo "HERMES_FOREGROUND_EXECUTION=DISABLED"
echo "DAILY_OPS_FOREGROUND_EXECUTION=DISABLED"
echo "REAL_CONTACTS=$REAL_CONTACTS"
echo "VERIFIED_PAID_PILOTS=$VERIFIED_PAID_PILOTS"
echo "VERIFIED_REVENUE_SAR=$VERIFIED_REVENUE_SAR"
echo "TRUTH_FIREWALL_ATTENTION=$TRUTH_FIREWALL_ATTENTION"
echo "NEW_TIMER=NO"
echo "NEW_CRON=NO"
echo "NEW_AGENT=NO"
echo "MERGE_MAIN=BLOCKED"
echo "PRODUCTION_MUTATION=BLOCKED"
echo "POLICY=$POLICY"
echo "PROMPT=$PROMPT"
echo "STATUS=$STATUS"
echo "PROOF=$RUN"
