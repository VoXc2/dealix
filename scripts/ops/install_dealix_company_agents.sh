#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

REPO="Dealix-sa/dealix"
BRANCH="ops/dealix-vps-self-hosted-control-20260820"
RUN_USER="dealix"
REPO_ROOT="/opt/dealix/workspace/dealix"
CONTROL_DIR="/opt/dealix/control/bin"
COUNCIL_ROOT="/opt/dealix/company-agents"
OPENCLAW_HOME="/home/${RUN_USER}/.openclaw"
OPENCLAW_WORKSPACE="${OPENCLAW_HOME}/workspace"
OPENCLAW_BIN="${OPENCLAW_HOME}/bin/openclaw"
STAMP="$(date +%Y%m%d-%H%M%S)"
TMP="$(mktemp -d)"

cleanup() { rm -rf "$TMP"; }
trap cleanup EXIT

if [[ "$(id -u)" -ne 0 ]]; then
  echo "BLOCKED: run as root"
  exit 2
fi
if ! id "$RUN_USER" >/dev/null 2>&1; then
  echo "BLOCKED: missing OS user $RUN_USER"
  exit 3
fi
if [[ ! -d "$REPO_ROOT/.git" ]]; then
  echo "BLOCKED: canonical repository missing at $REPO_ROOT"
  exit 4
fi
if ! sudo -iu "$RUN_USER" gh auth status >/dev/null 2>&1; then
  echo "BLOCKED: GitHub CLI is not authenticated for $RUN_USER"
  exit 5
fi

PRIVATE="$(sudo -iu "$RUN_USER" gh api "repos/${REPO}" --jq '.private' 2>/dev/null || true)"
LOGIN="$(sudo -iu "$RUN_USER" gh api user --jq '.login' 2>/dev/null || true)"
if [[ "$PRIVATE" != "true" || "$LOGIN" != "VoXc2" ]]; then
  echo "BLOCKED: expected private Dealix repository and founder GitHub identity"
  exit 6
fi

fetch_raw() {
  local path="$1" target="$2"
  sudo -iu "$RUN_USER" gh api \
    -H 'Accept: application/vnd.github.raw+json' \
    "repos/${REPO}/contents/${path}?ref=${BRANCH}" >"$target"
  test -s "$target"
}

mkdir -p "$CONTROL_DIR" "$COUNCIL_ROOT/reports" "$COUNCIL_ROOT/logs" "$COUNCIL_ROOT/state"
chown -R "$RUN_USER:$RUN_USER" "$COUNCIL_ROOT"
chmod 0750 "$COUNCIL_ROOT" "$COUNCIL_ROOT/reports" "$COUNCIL_ROOT/logs" "$COUNCIL_ROOT/state"

fetch_raw scripts/ops/dealix_agent_council.sh "$TMP/dealix_agent_council.sh"
fetch_raw scripts/verify_company_agent_operating_registry.py "$TMP/verify_company_agent_operating_registry.py"
fetch_raw dealix/registers/company_agent_operating_registry.json "$TMP/company_agent_operating_registry.json"

# The Council is analysis-only, but its recommendations can still corrupt the
# Proof Ledger if a model treats a hypothetical event as real. Make the proof
# policy part of every reinstall before the script is installed.
python3 - "$TMP/dealix_agent_council.sh" <<'PY'
from pathlib import Path
import sys

p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8")
marker = "DEALIX PROOF INTEGRITY — NON-NEGOTIABLE"

if marker not in s:
    anchor = "run_role() {"
    if anchor not in s:
        raise SystemExit("BLOCKED: council structure changed; proof policy not injected")
    policy = r'''
PROOF_INTEGRITY_POLICY=$(cat <<'POLICY_EOF'
DEALIX PROOF INTEGRITY — NON-NEGOTIABLE

You may analyze evidence but you may never manufacture it.

The following MUST NOT be described as FACT, EXECUTED, REAL, VERIFIED,
DELIVERED, SENT, PAID, RECEIVED, ACKNOWLEDGED, COMPLETED, or PRODUCTION-LIVE
unless the CURRENT PACKET contains an explicit verifiable source proving it:
- customer identity or customer interaction
- customer acknowledgement or meeting completion
- diagnostic/proposal/proof-pack delivery
- invoice sent or payment received
- signed agreement or partnership
- revenue
- production deployment or route health

Synthetic, demo, test, placeholder, hypothetical, model-generated, or fixture
information never satisfies a real customer/revenue/payment/delivery proof gate.
Missing evidence MUST remain a Proof Gap. A recommendation is not execution.
Never recommend writing a fabricated "real" customer event into
`docs/commercial/operations/evidence_events_tracker.csv` or any Proof Ledger.
Never recommend synthetic evidence as a substitute for a Truth Matrix proof.

Keep trust dimensions separate: a healthy API does not prove the frontend is
healthy; a frontend 404 does not prove the API is down.

Approval Items contain only actions that actually require an L5 founder gate:
external send/publish, merge to main, production/DNS/secret mutation,
payment/refund/financial commitment, deletion, or legal commitment. Reading or
filling an internal KPI file with already verified internal source data is not
an L5 approval by itself.
POLICY_EOF
)
'''
    s = s.replace(anchor, policy + "\n" + anchor, 1)

prompt_anchor = (
    "You are not allowed to execute or authorize external effects. You are analyzing "
    "a sanitized current-state packet. Use web research only when it materially verifies "
    "a time-sensitive public fact. Do not invent customers, revenue, payments, proof, "
    "partnerships, or production state."
)
if "${PROOF_INTEGRITY_POLICY}" not in s:
    if prompt_anchor not in s:
        raise SystemExit("BLOCKED: council prompt changed; proof policy not attached")
    s = s.replace(
        prompt_anchor,
        prompt_anchor + "\n\n${PROOF_INTEGRITY_POLICY}",
        1,
    )

if marker not in s or "${PROOF_INTEGRITY_POLICY}" not in s:
    raise SystemExit("BLOCKED: proof-integrity policy verification failed")

p.write_text(s, encoding="utf-8")
print("COUNCIL_PROOF_INTEGRITY=ENFORCED")
PY

bash -n "$TMP/dealix_agent_council.sh"
python3 -m py_compile "$TMP/verify_company_agent_operating_registry.py"
python3 - "$TMP/company_agent_operating_registry.json" <<'PY'
import json, sys
p=sys.argv[1]
d=json.load(open(p, encoding='utf-8'))
assert d['authority']['external_send_enabled'] is False
assert d['authority']['production_mutation_enabled'] is False
assert d['authority']['merge_to_main_enabled'] is False
assert d['authority']['payment_execution_enabled'] is False
assert d['agent_council']['external_actions_executed'] == 0
print('REGISTRY_SAFETY=PASS')
PY

install -m 0750 -o "$RUN_USER" -g "$RUN_USER" "$TMP/dealix_agent_council.sh" "$CONTROL_DIR/dealix_agent_council.sh"

# Install compact founder-facing OpenClaw workspace files. Back up only existing
# bootstrap files; no tokens/config/secrets are copied or printed.
mkdir -p "$OPENCLAW_WORKSPACE"
chown "$RUN_USER:$RUN_USER" "$OPENCLAW_WORKSPACE"
BACKUP_DIR="${OPENCLAW_WORKSPACE}/backups/${STAMP}"
mkdir -p "$BACKUP_DIR"
chown -R "$RUN_USER:$RUN_USER" "${OPENCLAW_WORKSPACE}/backups"
chmod 0700 "${OPENCLAW_WORKSPACE}/backups" "$BACKUP_DIR"

for name in AGENTS.md SOUL.md IDENTITY.md USER.md TOOLS.md HEARTBEAT.md; do
  if [[ -f "${OPENCLAW_WORKSPACE}/${name}" ]]; then
    cp -a "${OPENCLAW_WORKSPACE}/${name}" "${BACKUP_DIR}/${name}"
  fi
  fetch_raw "docs/ops/openclaw_workspace/${name}" "$TMP/${name}"
  install -m 0640 -o "$RUN_USER" -g "$RUN_USER" "$TMP/${name}" "${OPENCLAW_WORKSPACE}/${name}"
done

# A brand-new BOOTSTRAP ritual is intentionally not installed: identity is
# already explicit and the gateway has already been configured.

cat >/etc/systemd/system/dealix-agent-council.service <<'EOF'
[Unit]
Description=Dealix Governed Company Agent Council
After=network-online.target ollama.service
Wants=network-online.target ollama.service
ConditionPathExists=/opt/dealix/control/bin/dealix_agent_council.sh

[Service]
Type=oneshot
User=dealix
Group=dealix
WorkingDirectory=/opt/dealix/workspace/dealix
Environment=HOME=/home/dealix
Environment=PATH=/home/dealix/.local/bin:/home/dealix/.hermes/bin:/home/dealix/.openclaw/bin:/usr/local/bin:/usr/bin:/bin
Environment=TZ=Asia/Riyadh
Environment=DEALIX_EXTERNAL_OUTREACH_ENABLED=false
Environment=EXTERNAL_OUTREACH_ENABLED=false
Environment=AUTO_SEND_ENABLED=false
Environment=AGENT_APPROVAL_MODE=required
Environment=WHATSAPP_ALLOW_LIVE_SEND=false
Environment=MOYASAR_LIVE_MODE=0
Environment=DEALIX_LOCAL_MODEL=qwen3:4b-instruct-2507-q4_K_M
ExecStart=/opt/dealix/control/bin/dealix_agent_council.sh
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=read-only
ReadOnlyPaths=/opt/dealix/workspace/dealix /home/dealix/.openclaw
ReadWritePaths=/opt/dealix/company-agents /home/dealix/.hermes /home/dealix/.cache
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectKernelLogs=true
ProtectControlGroups=true
ProtectClock=true
RestrictSUIDSGID=true
LockPersonality=true
RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6
CapabilityBoundingSet=
# Hermes is orchestration; the model memory belongs to the separately bounded
# Ollama service. Do not allow the Council process to consume the whole 16GB VPS.
MemoryMax=6G
CPUQuota=300%
TimeoutStartSec=7200
StandardOutput=journal
StandardError=journal
EOF

cat >/etc/systemd/system/dealix-agent-council.timer <<'EOF'
[Unit]
Description=Run Dealix Agent Council on Saudi workdays

[Timer]
OnCalendar=Sun,Mon,Tue,Wed,Thu *-*-* 10:15:00 Asia/Riyadh
Persistent=true
RandomizedDelaySec=60
Unit=dealix-agent-council.service

[Install]
WantedBy=timers.target
EOF

systemd-analyze calendar 'Sun,Mon,Tue,Wed,Thu *-*-* 10:15:00 Asia/Riyadh' --iterations=1 >/dev/null
systemd-analyze verify /etc/systemd/system/dealix-agent-council.service /etc/systemd/system/dealix-agent-council.timer >/dev/null
systemctl daemon-reload

# Install the Council fail-closed. A successful install is not proof that Hermes
# can run safely at the VPS 8K memory budget. The total-company launcher performs
# the one-shot Hermes acceptance and is the only component allowed to enable this
# timer automatically after that proof.
systemctl disable --now dealix-agent-council.timer 2>/dev/null || true

# Harden the existing founder-facing OpenClaw configuration without changing
# Telegram credentials, gateway auth token, model credentials, or owner identity.
if [[ -x "$OPENCLAW_BIN" ]]; then
  sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set agents.defaults.contextInjection continuation-skip >/dev/null || true
  sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set agents.defaults.subagents.maxConcurrent 2 >/dev/null || true
  sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set agents.defaults.subagents.runTimeoutSeconds 900 >/dev/null || true
  sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set agents.defaults.subagents.delegationMode prefer >/dev/null || true
  sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set tools.subagents.tools.deny '["gateway","cron","exec","process","write","edit","apply_patch"]' --strict-json >/dev/null || true
  sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set channels.telegram.dmPolicy pairing >/dev/null || true
  sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set channels.telegram.groups '{"*":{"requireMention":true}}' --strict-json >/dev/null || true
  sudo -iu "$RUN_USER" "$OPENCLAW_BIN" gateway restart >/dev/null 2>&1 || true
fi

# The council is a missing AI synthesis layer, not a duplicate of the existing
# 06:30 / 08:45 / 12:30 / 19:00 / 21:15 / 23:30 Company Autopilot jobs.
echo "===== DEALIX COMPANY AGENTS INSTALLED ====="
echo "repository_private=true"
echo "github_login=${LOGIN}"
echo "council_proof_integrity=enforced"
echo "agent_council_timer=$(systemctl is-active dealix-agent-council.timer 2>/dev/null || true)"
echo "agent_council_enabled=$(systemctl is-enabled dealix-agent-council.timer 2>/dev/null || true)"
echo "agent_council_activation=requires_hermes_8k_acceptance"
echo "agent_council_schedule_if_enabled:"
systemctl list-timers dealix-agent-council.timer --all --no-pager || true

echo
echo "===== OPENCLAW ====="
if [[ -x "$OPENCLAW_BIN" ]]; then
  sudo -iu "$RUN_USER" "$OPENCLAW_BIN" gateway status --require-rpc || true
  sudo -iu "$RUN_USER" "$OPENCLAW_BIN" channels status --probe || true
else
  echo "OpenClaw not installed; Agent Council can still run through Hermes after acceptance."
fi

echo
echo "===== HERMES ====="
if [[ -x /home/dealix/.local/bin/hermes ]]; then
  sudo -iu "$RUN_USER" /home/dealix/.local/bin/hermes --version || true
else
  echo "Hermes missing"
fi

echo
echo "external_send=false"
echo "merge_to_main=false"
echo "production_mutation=false"
echo "payment_execution=false"
echo "workspace_backup=${BACKUP_DIR}"
echo "secret_values_printed=false"
echo "===== END ====="
