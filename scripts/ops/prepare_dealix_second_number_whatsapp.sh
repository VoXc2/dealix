#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

RUN_USER="dealix"
REPO="Dealix-sa/dealix"
SOURCE_REF="${DEALIX_WHATSAPP_SOURCE_REF:-main}"
REPO_DIR="/opt/dealix/workspace/dealix"
CONTROL_DIR="/opt/dealix/control"
PROMPT_DIR="${CONTROL_DIR}/prompts"
STATE_DIR="/opt/dealix/company-agents/whatsapp"
PROOF_DIR="/opt/dealix/logs"
STAMP="$(date +%Y%m%d-%H%M%S)"
PROOF="${PROOF_DIR}/second-number-whatsapp-prep-${STAMP}.log"
MASTER_LOCAL="${PROMPT_DIR}/DEALIX_SECOND_NUMBER_WHATSAPP_MASTER.md"

mkdir -p "$PROOF_DIR"
touch "$PROOF"
chmod 0600 "$PROOF"
exec > >(tee -a "$PROOF") 2>&1

log() { printf '[%s] %s\n' "$(date -Is)" "$*"; }

if [[ "$(id -u)" -ne 0 ]]; then
  echo "BLOCKED: run as root"
  exit 2
fi

if ! id "$RUN_USER" >/dev/null 2>&1; then
  echo "BLOCKED: user '$RUN_USER' missing"
  exit 3
fi

if [[ ! -d "$REPO_DIR/.git" ]]; then
  echo "BLOCKED: canonical Dealix checkout missing at $REPO_DIR"
  exit 4
fi

mkdir -p "$PROMPT_DIR" "$STATE_DIR"
chown -R "$RUN_USER:$RUN_USER" "$PROMPT_DIR" "$STATE_DIR"
chmod 0750 "$PROMPT_DIR" "$STATE_DIR"

log "===== IDENTITY / REPOSITORY ====="
LOGIN="$(sudo -iu "$RUN_USER" gh api user --jq '.login' 2>/dev/null || true)"
PRIVATE="$(sudo -iu "$RUN_USER" gh api "repos/${REPO}" --jq '.private' 2>/dev/null || true)"
echo "github_login=${LOGIN:-unknown}"
echo "repository_private=${PRIVATE:-unknown}"
echo "source_ref=$SOURCE_REF"
if [[ "$PRIVATE" != "true" ]]; then
  echo "BLOCKED: repository must remain private"
  exit 5
fi

log "===== FETCH CURRENT CANONICAL WHATSAPP MASTER ====="
sudo -iu "$RUN_USER" gh api \
  -H 'Accept: application/vnd.github.raw+json' \
  "repos/${REPO}/contents/docs/ops/DEALIX_SECOND_NUMBER_WHATSAPP_MASTER.md?ref=${SOURCE_REF}" \
  > "$MASTER_LOCAL"
chown "$RUN_USER:$RUN_USER" "$MASTER_LOCAL"
chmod 0640 "$MASTER_LOCAL"
test -s "$MASTER_LOCAL"
echo "master_prompt=${MASTER_LOCAL}"

log "===== EXISTING WHATSAPP ASSET INVENTORY ====="
REQUIRED=(
  "integrations/whatsapp.py"
  "integrations/green_api.py"
  "api/routers/webhooks.py"
  "auto_client_acquisition/email/whatsapp_multi_provider.py"
  "docs/WHATSAPP_OPERATOR_FLOW.md"
  "docs/WHATSAPP_PRODUCTION_CUTOVER.md"
  "docs/integrations/WHATSAPP_BUSINESS_SETUP.md"
  "docs/ops/WHATSAPP_GREEN_TO_META_EXECUTION_20260908.md"
  "trust/WHATSAPP_OUTREACH_SAFETY_POLICY.md"
  "tests/test_whatsapp_signature.py"
  "tests/test_whatsapp_webhook_integration.py"
  "tests/unit/test_green_api_webhook.py"
  "tests/unit/test_full_os_smoke.py"
)
MISSING=0
for rel in "${REQUIRED[@]}"; do
  if [[ -f "$REPO_DIR/$rel" ]]; then
    echo "PASS asset=$rel"
  else
    echo "FAIL asset_missing=$rel"
    MISSING=1
  fi
done
if [[ "$MISSING" -ne 0 ]]; then
  echo "BLOCKED: canonical WhatsApp assets are incomplete; do not build a parallel engine"
  exit 6
fi

log "===== STATIC SAFETY ASSERTIONS ====="
python3 - "$REPO_DIR" <<'PY'
from pathlib import Path
import sys
root = Path(sys.argv[1])
checks = {
    "meta_live_send_gate": (root / "integrations/whatsapp.py", "whatsapp_allow_live_send"),
    "meta_signature_verify": (root / "integrations/whatsapp.py", "verify_signature"),
    "meta_webhook_route": (root / "api/routers/webhooks.py", '@router.post("/whatsapp")'),
    "green_webhook_route": (root / "api/routers/webhooks.py", '@router.post("/green-api")'),
    "green_webhook_auth": (root / "api/routers/webhooks.py", "GREEN_API_WEBHOOK_TOKEN"),
    "strict_meta_signature": (root / "api/routers/webhooks.py", "missing_or_invalid_signature"),
    "provider_official_first": (root / "auto_client_acquisition/email/whatsapp_multi_provider.py", '("meta_cloud", _send_via_meta_cloud)'),
    "provider_no_silent_meta_fallback": (root / "auto_client_acquisition/email/whatsapp_multi_provider.py", "Meta failure must be surfaced"),
    "no_cold_policy": (root / "docs/WHATSAPP_OPERATOR_FLOW.md", "No **cold** WhatsApp"),
    "rollback_flag": (root / "docs/WHATSAPP_PRODUCTION_CUTOVER.md", "WHATSAPP_ALLOW_LIVE_SEND=false"),
    "durable_consent_gate": (root / "scripts/ops/verify_controlled_live_readiness.py", "persistent consent evidence is proven"),
}
failed=[]
for name,(p,needle) in checks.items():
    text=p.read_text(encoding="utf-8")
    ok=needle in text
    print(f"{'PASS' if ok else 'FAIL'} {name}")
    if not ok: failed.append(name)
if failed:
    raise SystemExit("Static safety assertions failed: " + ", ".join(failed))
PY

log "===== TARGETED TESTS ====="
set +e
sudo -iu "$RUN_USER" bash -lc '
  cd /opt/dealix/workspace/dealix
  if [ -x .venv/bin/python ]; then PY=.venv/bin/python; else PY=python3; fi
  "$PY" -m pytest -q \
    tests/test_whatsapp_signature.py \
    tests/test_whatsapp_webhook_integration.py \
    tests/unit/test_green_api_webhook.py \
    tests/unit/test_full_os_smoke.py
'
TEST_RC=$?
set -e
echo "whatsapp_tests_rc=$TEST_RC"

log "===== CONTROLLED-LIVE READINESS (READ ONLY) ====="
set +e
sudo -iu "$RUN_USER" bash -lc '
  cd /opt/dealix/workspace/dealix
  if [ -x .venv/bin/python ]; then PY=.venv/bin/python; else PY=python3; fi
  "$PY" scripts/ops/verify_controlled_live_readiness.py
'
CONTROLLED_LIVE_RC=$?
set -e
echo "controlled_live_readiness_rc=$CONTROLLED_LIVE_RC"
echo "NOTE: non-zero is expected while durable consent/suppression remain unproven."

log "===== PRIVATE RUNTIME POSTURE ====="
printf 'n8n='; docker ps --filter name=dealix-n8n --format '{{.Status}} {{.Ports}}' 2>/dev/null || true
printf 'ollama='; systemctl is-active ollama 2>/dev/null || true
printf 'openclaw_gateway='; sudo -iu "$RUN_USER" /home/dealix/.openclaw/bin/openclaw gateway status --require-rpc >/dev/null 2>&1 && echo PASS || echo DEGRADED
printf 'agent_council_timer='; systemctl is-active dealix-agent-council.timer 2>/dev/null || true

log "===== WHATSAPP ACTIVATION STATE ====="
cat > "${STATE_DIR}/ACTIVATION.md" <<'EOF'
# Dealix WhatsApp Activation State

## Canonical role
Dedicated Dealix Business WhatsApp number is the long-term Meta Business Platform identity. GREEN-API is a bounded transition transport only.

## Founder command lane
Telegram / OpenClaw remains the founder command and approval channel.

## Current authority
- inbound processing: allowed internally after provider authentication
- classification/research/qualification/drafting: allowed internally
- negotiation analysis: allowed internally
- approval-card generation: allowed internally
- external WhatsApp send: BLOCKED until exact approval + durable consent + production cutover
- bulk/cold outreach: PROHIBITED

## Transition sequence
1. Authorize GREEN-API instance from the phone using Linked Devices / QR.
2. Merge/deploy accepted GREEN webhook source under exact production authority.
3. Store GREEN_API_WEBHOOK_TOKEN only in the approved secret store.
4. Keep WHATSAPP_ALLOW_LIVE_SEND=false through inbound verification.
5. Prove authenticated GREEN inbound -> canonical Dealix intake.
6. Complete Meta Business/WABA/dedicated-number setup.
7. Store Meta credentials only in the approved production secret store.
8. Prove Meta signed inbound webhook and canonical Dealix ingestion.
9. Close durable consent + suppression (#1533).
10. Cut provider preference explicitly to meta_cloud under exact authority.
11. Enable controlled-live only after the readiness verifier genuinely passes.
12. Retire GREEN linked session after Meta stability/rollback window.

## Required secret names (names only, never values)
Transition:
- GREEN_API_INSTANCE_ID
- GREEN_API_TOKEN
- GREEN_API_WEBHOOK_TOKEN

Meta canonical:
- WHATSAPP_PHONE_NUMBER_ID
- WHATSAPP_ACCESS_TOKEN
- WHATSAPP_APP_SECRET
- WHATSAPP_VERIFY_TOKEN
- WHATSAPP_BUSINESS_ACCOUNT_ID

Selection/safety:
- WHATSAPP_PROVIDER_PREFERENCE
- WHATSAPP_ALLOW_LIVE_SEND

## Acceptance
- valid authenticated inbound => accepted
- invalid provider authentication/signature => fail closed
- inbound => canonical Dealix lead/opportunity/customer context
- response => draft + approval path
- no external send before consent/approval/controlled-live authority
- opt-out => durable suppression
- no silent Meta -> unofficial fallback
EOF
chown "$RUN_USER:$RUN_USER" "${STATE_DIR}/ACTIVATION.md"
chmod 0640 "${STATE_DIR}/ACTIVATION.md"

cat > "${STATE_DIR}/WORKFLOWS.md" <<'EOF'
# Governed WhatsApp Workflow Labels

WA_01_Inbound_Triage
WA_02_Identity_Opportunity_Update
WA_03_Lead_Qualification
WA_04_Sales_Reply_Draft
WA_05_Negotiation_Approval
WA_06_Approved_Send
WA_07_Delivery_Reply_Proof
WA_08_Customer_Support
WA_09_Appointment_Proposal_Handoff
WA_10_Suppression_Consent
WA_11_Customer_Success_Expansion
WA_12_Conversation_Learning

These labels orchestrate existing Dealix contracts. They are not a new Company Brain, CRM, Approval Center, Proof Ledger or source of truth.
EOF
chown "$RUN_USER:$RUN_USER" "${STATE_DIR}/WORKFLOWS.md"
chmod 0640 "${STATE_DIR}/WORKFLOWS.md"

log "===== PRODUCTION MUTATION CHECK ====="
echo "credentials_written=false"
echo "railway_variables_changed=false"
echo "whatsapp_live_send_enabled=false"
echo "external_messages_sent=0"
echo "production_deploy_triggered=false"
echo "dns_changed=false"
echo "merge_to_main=false"

log "===== RESULT ====="
echo "master_prompt=$MASTER_LOCAL"
echo "activation_state=${STATE_DIR}/ACTIVATION.md"
echo "workflow_map=${STATE_DIR}/WORKFLOWS.md"
echo "proof=$PROOF"
if [[ "$TEST_RC" -eq 0 ]]; then
  echo "DEALIX_WHATSAPP_GREEN_TO_META_PREP=PASS"
  exit 0
fi

echo "DEALIX_WHATSAPP_GREEN_TO_META_PREP=DEGRADED_TESTS"
echo "Preparation is installed, but cutover is blocked until targeted tests pass."
exit 20
