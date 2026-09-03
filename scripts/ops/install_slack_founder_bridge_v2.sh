#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

# Install the bounded Slack Founder Room Socket Mode adapter without creating
# another scheduler, Company OS, agent fleet, or truth store.
#
# Default behavior is INSTALL-ONLY. Pass --activate only after the runtime
# secret file already exists and end-to-end acceptance is intended.

REPO_ROOT="${DEALIX_REPO_ROOT:-/opt/dealix/workspace/dealix}"
CONTROL_ROOT="${DEALIX_CONTROL_ROOT:-/opt/dealix/control}"
RUN_USER="${DEALIX_RUN_USER:-dealix}"
RUN_GROUP="${DEALIX_RUN_GROUP:-dealix}"
VENV="${CONTROL_ROOT}/venvs/slack-founder"
RECEIPTS="${CONTROL_ROOT}/runs/slack-founder-receipts"
ENV_FILE="${CONTROL_ROOT}/etc/slack-founder.env"
SERVICE="dealix-slack-founder.service"
SERVICE_PATH="/etc/systemd/system/${SERVICE}"
BRIDGE="${REPO_ROOT}/scripts/ops/dealix_slack_founder_bridge.py"
REQ="${REPO_ROOT}/scripts/ops/requirements-slack-founder.txt"
AUTOPILOT="${CONTROL_ROOT}/bin/dealix_company_autopilot.sh"
ACTIVATE=0

if [[ "${1:-}" == "--activate" ]]; then
  ACTIVATE=1
elif [[ $# -gt 0 ]]; then
  printf 'usage: %s [--activate]\n' "$0" >&2
  exit 64
fi

block() {
  printf 'BLOCKED: %s\n' "$*" >&2
  exit 1
}

[[ "$(id -u)" -eq 0 ]] || block "run as root"
id "$RUN_USER" >/dev/null 2>&1 || block "missing OS user: $RUN_USER"
[[ -f "$BRIDGE" ]] || block "missing bridge source: $BRIDGE"
[[ -f "$REQ" ]] || block "missing dedicated requirements: $REQ"
[[ -x "$AUTOPILOT" ]] || block "missing canonical Company Autopilot: $AUTOPILOT"
command -v python3 >/dev/null 2>&1 || block "python3 is required"
command -v systemctl >/dev/null 2>&1 || block "systemd is required"

python3 -m py_compile "$BRIDGE"
bash -n "$0"

install -d -o "$RUN_USER" -g "$RUN_GROUP" -m 0750 \
  "${CONTROL_ROOT}/venvs" \
  "$RECEIPTS"
install -d -o root -g "$RUN_GROUP" -m 0750 "${CONTROL_ROOT}/etc"

if [[ ! -x "${VENV}/bin/python" ]]; then
  python3 -m venv "$VENV"
  chown -R "$RUN_USER:$RUN_GROUP" "$VENV"
fi

sudo -u "$RUN_USER" -H "${VENV}/bin/python" -m pip install \
  --disable-pip-version-check \
  --requirement "$REQ"

cat >"$SERVICE_PATH" <<EOF
[Unit]
Description=Dealix Slack Founder Room Socket Mode Bridge
After=network-online.target
Wants=network-online.target
ConditionPathExists=${ENV_FILE}
ConditionPathExists=${BRIDGE}
ConditionPathExists=${AUTOPILOT}

[Service]
Type=simple
User=${RUN_USER}
Group=${RUN_GROUP}
UMask=0027
WorkingDirectory=${REPO_ROOT}
Environment="HOME=/home/${RUN_USER}"
Environment="PYTHONUNBUFFERED=1"
Environment="DEALIX_REPO_ROOT=${REPO_ROOT}"
Environment="DEALIX_CANONICAL_AUTOPILOT=${AUTOPILOT}"
Environment="DEALIX_SLACK_RECEIPT_DIR=${RECEIPTS}"
Environment="DEALIX_EXTERNAL_SEND=0"
Environment="DEALIX_EXTERNAL_OUTREACH_ENABLED=false"
Environment="EXTERNAL_OUTREACH_ENABLED=false"
Environment="AUTO_SEND_ENABLED=false"
Environment="DEALIX_EMAIL_LIVE_SEND=0"
Environment="DEALIX_WHATSAPP_OUTBOUND=0"
Environment="WHATSAPP_ALLOW_LIVE_SEND=false"
Environment="DEALIX_PUBLIC_PUBLISH=0"
Environment="DEALIX_PAID_SPEND=0"
Environment="DEALIX_PAYMENT_EXECUTION=0"
Environment="DEALIX_PRODUCTION_MUTATION=0"
Environment="DEALIX_DNS_MUTATION=0"
Environment="DEALIX_DB_MUTATION=0"
Environment="DEALIX_SECRET_MUTATION=0"
Environment="DEALIX_AGENT_SELF_AUTHORITY=0"
Environment="AGENT_APPROVAL_MODE=required"
Environment="MOYASAR_LIVE_MODE=0"
EnvironmentFile=${ENV_FILE}
ExecStart=${VENV}/bin/python ${BRIDGE}
Restart=on-failure
RestartSec=5s
TimeoutStopSec=20s
NoNewPrivileges=true
PrivateTmp=true
PrivateDevices=true
ProtectSystem=strict
ProtectHome=read-only
ProtectClock=true
ProtectHostname=true
ProtectKernelLogs=true
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true
RestrictSUIDSGID=true
LockPersonality=true
RestrictAddressFamilies=AF_UNIX AF_INET AF_INET6
SystemCallArchitectures=native
ReadWritePaths=${RECEIPTS} /opt/dealix/company-autopilot ${CONTROL_ROOT}/state ${REPO_ROOT}

[Install]
WantedBy=multi-user.target
EOF

chmod 0644 "$SERVICE_PATH"
systemd-analyze verify "$SERVICE_PATH" >/dev/null
systemctl daemon-reload

printf 'SLACK_FOUNDER_BRIDGE_INSTALL=PASS\n'
printf 'service=%s\n' "$SERVICE"
printf 'venv=%s\n' "$VENV"
printf 'env_file=%s\n' "$ENV_FILE"
printf 'receipt_dir=%s\n' "$RECEIPTS"
printf 'activation_requested=%s\n' "$ACTIVATE"

if [[ "$ACTIVATE" -eq 0 ]]; then
  printf 'state=INSTALLED_NOT_ACTIVATED\n'
  printf 'next=Create/verify %s outside Git with mode 0600, then rerun with --activate.\n' "$ENV_FILE"
  exit 0
fi

[[ -f "$ENV_FILE" ]] || block "activation requested but secret environment file is missing"
[[ ! -L "$ENV_FILE" ]] || block "secret environment file must not be a symlink"
[[ "$(stat -c '%a' "$ENV_FILE")" == "600" ]] || block "secret environment file must have mode 0600"
ENV_OWNER="$(stat -c '%U' "$ENV_FILE")"
[[ "$ENV_OWNER" == "root" || "$ENV_OWNER" == "$RUN_USER" ]] || block "secret environment file owner must be root or $RUN_USER"

# Parse expected assignments as data. Never source or execute this file, and
# reject every key outside the four required Slack identity values.
python3 - "$ENV_FILE" <<'PY'
from __future__ import annotations

import re
import shlex
import sys
from pathlib import Path

path = Path(sys.argv[1])
values: dict[str, str] = {}
for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
    line = raw.strip()
    if not line or line.startswith("#"):
        continue
    if "=" not in line:
        raise SystemExit(f"BLOCKED: invalid environment assignment at line {line_no}")
    key, value = line.split("=", 1)
    key = key.strip()
    if key in values:
        raise SystemExit(f"BLOCKED: duplicate environment key at line {line_no}: {key}")
    try:
        parsed = shlex.split(value.strip(), posix=True)
    except ValueError as exc:
        raise SystemExit(f"BLOCKED: invalid quoting at line {line_no}: {exc}") from exc
    if len(parsed) != 1:
        raise SystemExit(f"BLOCKED: environment value at line {line_no} must be a single literal")
    values[key] = parsed[0]

required = {
    "SLACK_BOT_TOKEN",
    "SLACK_APP_TOKEN",
    "DEALIX_SLACK_COMMAND_CHANNEL_ID",
    "DEALIX_SLACK_FOUNDER_USER_ID",
}
unknown = sorted(set(values) - required)
missing = sorted(required - set(values))
if unknown:
    raise SystemExit(f"BLOCKED: unexpected keys in Slack bridge environment file: {unknown}")
if missing:
    raise SystemExit(f"BLOCKED: missing required keys: {missing}")

if not re.fullmatch(r"xoxb-[A-Za-z0-9-]{20,}", values["SLACK_BOT_TOKEN"]):
    raise SystemExit("BLOCKED: invalid SLACK_BOT_TOKEN")
if not re.fullmatch(r"xapp-[A-Za-z0-9-]{20,}", values["SLACK_APP_TOKEN"]):
    raise SystemExit("BLOCKED: invalid SLACK_APP_TOKEN")
if not re.fullmatch(r"[CG][A-Z0-9]+", values["DEALIX_SLACK_COMMAND_CHANNEL_ID"]):
    raise SystemExit("BLOCKED: invalid command channel ID")
if not re.fullmatch(r"[UW][A-Z0-9]+", values["DEALIX_SLACK_FOUNDER_USER_ID"]):
    raise SystemExit("BLOCKED: invalid founder user ID")
PY

systemctl enable --now "$SERVICE"
sleep 2
systemctl is-active --quiet "$SERVICE" || block "service did not become active"
printf 'state=ACTIVE_PENDING_END_TO_END_RECEIPT\n'
printf 'next=Mention the bot with STATUS in the founder command channel, then verify the resulting receipt with scripts/ops/verify_slack_founder_bridge_receipt.py.\n'
