#!/usr/bin/env bash
set -Eeuo pipefail

REPO="Dealix-sa/dealix"
FOUNDER="VoXc2"
BRANCH="ops/dealix-vps-self-hosted-control-20260820"
ISSUE="1119"
RUNNER_USER="dealix"
CONTROL_ROOT="/opt/dealix/control"
BIN_DIR="${CONTROL_ROOT}/bin"
STATE_DIR="${CONTROL_ROOT}/state"
CACHE_DIR="${CONTROL_ROOT}/cache"
BRIDGE="${BIN_DIR}/dealix_vps_issue_bridge.py"
DISPATCHER="${BIN_DIR}/dealix_vps_control.sh"
SERVICE="dealix-vps-issue-bridge.service"
TIMER="dealix-vps-issue-bridge.timer"

if [[ "$(id -u)" -ne 0 ]]; then
  echo "BLOCKED: run as root."
  exit 2
fi

if ! id "$RUNNER_USER" >/dev/null 2>&1; then
  echo "BLOCKED: missing OS user '$RUNNER_USER'."
  exit 3
fi

if ! sudo -iu "$RUNNER_USER" gh auth status >/dev/null 2>&1; then
  echo "BLOCKED: GitHub CLI is not authenticated for '$RUNNER_USER'."
  exit 4
fi

LOGIN="$(sudo -iu "$RUNNER_USER" gh api user --jq '.login' 2>/dev/null || true)"
if [[ "$LOGIN" != "$FOUNDER" ]]; then
  echo "BLOCKED: expected GitHub login '$FOUNDER'; got '${LOGIN:-unknown}'."
  exit 5
fi

PRIVATE="$(sudo -iu "$RUNNER_USER" gh api "repos/${REPO}" --jq '.private' 2>/dev/null || true)"
if [[ "$PRIVATE" != "true" ]]; then
  echo "BLOCKED: ${REPO} must be private."
  exit 6
fi

install -d -m 0750 -o "$RUNNER_USER" -g "$RUNNER_USER" \
  "$CONTROL_ROOT" "$BIN_DIR" "$STATE_DIR" "$CACHE_DIR"

TMP_BRIDGE="$(mktemp)"
TMP_DISPATCHER="$(mktemp)"
cleanup() {
  rm -f "$TMP_BRIDGE" "$TMP_DISPATCHER"
}
trap cleanup EXIT

sudo -iu "$RUNNER_USER" gh api \
  -H 'Accept: application/vnd.github.raw+json' \
  "repos/${REPO}/contents/scripts/ops/dealix_vps_issue_bridge.py?ref=${BRANCH}" \
  >"$TMP_BRIDGE"

sudo -iu "$RUNNER_USER" gh api \
  -H 'Accept: application/vnd.github.raw+json' \
  "repos/${REPO}/contents/scripts/ops/dealix_vps_control.sh?ref=${BRANCH}" \
  >"$TMP_DISPATCHER"

python3 -m py_compile "$TMP_BRIDGE"
bash -n "$TMP_DISPATCHER"

install -m 0750 -o "$RUNNER_USER" -g "$RUNNER_USER" "$TMP_BRIDGE" "$BRIDGE"
install -m 0750 -o "$RUNNER_USER" -g "$RUNNER_USER" "$TMP_DISPATCHER" "$DISPATCHER"

cat >"/etc/systemd/system/${SERVICE}" <<EOF
[Unit]
Description=Dealix private GitHub Issue to VPS command bridge
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
User=${RUNNER_USER}
Group=${RUNNER_USER}
WorkingDirectory=${CONTROL_ROOT}
Environment="HOME=/home/${RUNNER_USER}"
Environment="XDG_CACHE_HOME=${CACHE_DIR}"
Environment="PATH=/home/${RUNNER_USER}/.local/bin:/home/${RUNNER_USER}/.railway/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=/usr/bin/python3 ${BRIDGE}
TimeoutStartSec=35min
NoNewPrivileges=true
PrivateTmp=true
PrivateDevices=true
ProtectSystem=full
ProtectHome=read-only
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true
RestrictSUIDSGID=true
LockPersonality=true
ReadWritePaths=${CONTROL_ROOT} /opt/dealix/workspace/dealix

[Install]
WantedBy=multi-user.target
EOF

cat >"/etc/systemd/system/${TIMER}" <<EOF
[Unit]
Description=Poll private Dealix GitHub command queue every minute

[Timer]
OnBootSec=2min
OnUnitActiveSec=60s
RandomizedDelaySec=5s
Persistent=true
Unit=${SERVICE}

[Install]
WantedBy=timers.target
EOF

systemctl daemon-reload

# Ignore every historical comment. Only commands posted after installation may run.
sudo -iu "$RUNNER_USER" env \
  XDG_CACHE_HOME="$CACHE_DIR" \
  PATH="/home/${RUNNER_USER}/.local/bin:/home/${RUNNER_USER}/.railway/bin:/usr/local/bin:/usr/bin:/bin" \
  python3 "$BRIDGE" --bootstrap

systemctl enable --now "$TIMER"
systemctl start "$SERVICE"

TIMER_ENABLED="$(systemctl is-enabled "$TIMER" 2>/dev/null || true)"
TIMER_ACTIVE="$(systemctl is-active "$TIMER" 2>/dev/null || true)"
SERVICE_RESULT="$(systemctl show "$SERVICE" -p Result --value 2>/dev/null || true)"

# Self-report the installation to the private GitHub control issue so the
# operator can verify activation without asking the founder to paste logs.
INSTALL_PROOF="$(printf '%s\n' \
  'DEALIX_VPS_BRIDGE_INSTALLED' \
  '' \
  "- host: srv1916256" \
  "- repository_private: true" \
  "- github_login: ${LOGIN}" \
  "- timer_enabled: ${TIMER_ENABLED}" \
  "- timer_active: ${TIMER_ACTIVE}" \
  "- service_result: ${SERVICE_RESULT}" \
  '- historical_comments_ignored: true' \
  '- secret_values_printed: false')"

sudo -iu "$RUNNER_USER" env XDG_CACHE_HOME="$CACHE_DIR" \
  gh api --method POST "repos/${REPO}/issues/${ISSUE}/comments" \
  -f "body=${INSTALL_PROOF}" >/dev/null

echo
echo "===== DEALIX PRIVATE COMMAND BRIDGE PROOF ====="
echo "repository_private=true"
echo "github_login=${LOGIN}"
echo "bridge=${BRIDGE}"
echo "dispatcher=${DISPATCHER}"
echo "timer_enabled=${TIMER_ENABLED}"
echo "timer_active=${TIMER_ACTIVE}"
echo "service_result=${SERVICE_RESULT}"
systemctl --no-pager --full status "$SERVICE" | sed -n '1,18p' || true
systemctl list-timers "$TIMER" --no-pager || true
echo "secret_values_printed=false"
echo "historical_comments_ignored=true"
echo "private_issue_proof_posted=true"
echo "===== END ====="
