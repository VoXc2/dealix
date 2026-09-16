#!/usr/bin/env bash
set -Eeuo pipefail

REPO="Dealix-sa/dealix"
FOUNDER="VoXc2"
SOURCE_REF="${DEALIX_SOURCE_REF:-main}"
ISSUE="1119"
RUNNER_USER="dealix"
CONTROL_ROOT="/opt/dealix/control"
BIN_DIR="${CONTROL_ROOT}/bin"
STATE_DIR="${CONTROL_ROOT}/state"
CACHE_DIR="${CONTROL_ROOT}/cache"
STATE_FILE="${STATE_DIR}/issue_bridge.json"
BRIDGE="${BIN_DIR}/dealix_vps_issue_bridge.py"
DISPATCHER="${BIN_DIR}/dealix_vps_control.sh"
SERVICE="dealix-vps-issue-bridge.service"
TIMER="dealix-vps-issue-bridge.timer"
SAFE_LOCAL_MODEL="${DEALIX_LOCAL_MODEL:-qwen3:4b-instruct-2507-q4_K_M}"

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

resolve_source_sha() {
  local resolved
  if [[ "$SOURCE_REF" == "main" ]]; then
    resolved="$(sudo -iu "$RUNNER_USER" gh api "repos/${REPO}/commits/main" --jq '.sha' 2>/dev/null || true)"
  elif [[ "$SOURCE_REF" =~ ^[0-9a-f]{40}$ ]]; then
    resolved="$(sudo -iu "$RUNNER_USER" gh api "repos/${REPO}/commits/${SOURCE_REF}" --jq '.sha' 2>/dev/null || true)"
  else
    echo "BLOCKED: DEALIX_SOURCE_REF must be 'main' or an exact 40-character commit SHA." >&2
    return 1
  fi
  [[ "$resolved" =~ ^[0-9a-f]{40}$ ]] || {
    echo "BLOCKED: unable to resolve canonical Dealix source SHA." >&2
    return 1
  }
  printf '%s\n' "$resolved"
}

SOURCE_SHA="$(resolve_source_sha)" || exit 7

install -d -m 0750 -o "$RUNNER_USER" -g "$RUNNER_USER" \
  "$CONTROL_ROOT" "$BIN_DIR" "$STATE_DIR" "$CACHE_DIR"

TMP_BRIDGE="$(mktemp)"
TMP_DISPATCHER="$(mktemp)"
cleanup() {
  rm -f "$TMP_BRIDGE" "$TMP_DISPATCHER"
}
trap cleanup EXIT

# The root caller owns TMP_BRIDGE intentionally; only the authenticated `gh`
# process is demoted to the bounded Dealix runner user.
# shellcheck disable=SC2024
sudo -iu "$RUNNER_USER" gh api \
  -H 'Accept: application/vnd.github.raw+json' \
  "repos/${REPO}/contents/scripts/ops/dealix_vps_issue_bridge.py?ref=${SOURCE_SHA}" \
  >"$TMP_BRIDGE"

# The root caller owns TMP_DISPATCHER intentionally for the same reason.
# shellcheck disable=SC2024
sudo -iu "$RUNNER_USER" gh api \
  -H 'Accept: application/vnd.github.raw+json' \
  "repos/${REPO}/contents/scripts/ops/dealix_vps_control.sh?ref=${SOURCE_SHA}" \
  >"$TMP_DISPATCHER"

python3 -m py_compile "$TMP_BRIDGE"
bash -n "$TMP_DISPATCHER"

# Quiesce only this bridge while replacing its two allowlisted runtime files.
# State is never deleted or rewound.
systemctl stop "$TIMER" 2>/dev/null || true
systemctl stop "$SERVICE" 2>/dev/null || true

install -m 0750 -o "$RUNNER_USER" -g "$RUNNER_USER" "$TMP_BRIDGE" "$BRIDGE"
install -m 0750 -o "$RUNNER_USER" -g "$RUNNER_USER" "$TMP_DISPATCHER" "$DISPATCHER"

cat >"/etc/systemd/system/${SERVICE}" <<EOF
[Unit]
Description=Dealix private GitHub Issue to VPS command bridge
After=network-online.target ollama.service
Wants=network-online.target

[Service]
Type=oneshot
User=${RUNNER_USER}
Group=${RUNNER_USER}
WorkingDirectory=${CONTROL_ROOT}
Environment="HOME=/home/${RUNNER_USER}"
Environment="XDG_CACHE_HOME=${CACHE_DIR}"
Environment="PATH=/home/${RUNNER_USER}/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
Environment="DEALIX_LOCAL_MODEL=${SAFE_LOCAL_MODEL}"
# Local-only OpenAI-compatible fallback for safe internal model work such as
# Sales Arena. The credential is a non-secret loopback placeholder and never
# authorizes a remote provider.
Environment="OPENAI_API_KEY=ollama-local"
Environment="OPENAI_BASE_URL=http://127.0.0.1:11434/v1"
Environment="OPENAI_MODEL=${SAFE_LOCAL_MODEL}"
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

# First install bootstraps beyond historical comments. Reinstall preserves the
# durable cursor and pending receipt state exactly; it never replays history.
if [[ -e "$STATE_FILE" || -L "$STATE_FILE" ]]; then
  [[ -f "$STATE_FILE" && ! -L "$STATE_FILE" ]] || {
    echo "BLOCKED: existing bridge state must be a regular non-symlink file."
    exit 8
  }
  python3 -m json.tool "$STATE_FILE" >/dev/null || {
    echo "BLOCKED: existing bridge state is not valid JSON."
    exit 9
  }
  STATE_ACTION="preserved"
else
  sudo -iu "$RUNNER_USER" env \
    XDG_CACHE_HOME="$CACHE_DIR" \
    PATH="/home/${RUNNER_USER}/.local/bin:/usr/local/bin:/usr/bin:/bin" \
    python3 "$BRIDGE" --bootstrap
  STATE_ACTION="bootstrapped"
fi

systemctl enable --now "$TIMER"
systemctl start "$SERVICE"

TIMER_ENABLED="$(systemctl is-enabled "$TIMER" 2>/dev/null || true)"
TIMER_ACTIVE="$(systemctl is-active "$TIMER" 2>/dev/null || true)"
SERVICE_RESULT="$(systemctl show "$SERVICE" -p Result --value 2>/dev/null || true)"

if [[ "$TIMER_ENABLED" != "enabled" || "$TIMER_ACTIVE" != "active" || "$SERVICE_RESULT" != "success" ]]; then
  echo "BLOCKED: bridge activation proof is incomplete."
  exit 10
fi

BRIDGE_SHA256="$(sha256sum "$BRIDGE" | awk '{print $1}')"
DISPATCHER_SHA256="$(sha256sum "$DISPATCHER" | awk '{print $1}')"

# Self-report installation to the private GitHub control issue. No secret
# values or environment contents are printed.
INSTALL_PROOF="$(printf '%s\n' \
  'DEALIX_VPS_BRIDGE_INSTALLED' \
  '' \
  '- host: srv1916256' \
  '- repository_private: true' \
  "- github_login: ${LOGIN}" \
  "- source_ref: ${SOURCE_REF}" \
  "- source_sha: ${SOURCE_SHA}" \
  "- state_action: ${STATE_ACTION}" \
  "- bridge_sha256: ${BRIDGE_SHA256}" \
  "- dispatcher_sha256: ${DISPATCHER_SHA256}" \
  "- timer_enabled: ${TIMER_ENABLED}" \
  "- timer_active: ${TIMER_ACTIVE}" \
  "- service_result: ${SERVICE_RESULT}" \
  '- local_llm_fallback: loopback_ollama' \
  '- historical_comments_ignored=true' \
  '- historical_comments_ignored_or_state_preserved=true' \
  '- secret_values_printed: false')"

sudo -iu "$RUNNER_USER" env XDG_CACHE_HOME="$CACHE_DIR" \
  gh api --method POST "repos/${REPO}/issues/${ISSUE}/comments" \
  -f "body=${INSTALL_PROOF}" >/dev/null

echo
echo "===== DEALIX PRIVATE COMMAND BRIDGE PROOF ====="
echo "repository_private=true"
echo "github_login=${LOGIN}"
echo "source_ref=${SOURCE_REF}"
echo "source_sha=${SOURCE_SHA}"
echo "state_action=${STATE_ACTION}"
echo "bridge=${BRIDGE}"
echo "dispatcher=${DISPATCHER}"
echo "bridge_sha256=${BRIDGE_SHA256}"
echo "dispatcher_sha256=${DISPATCHER_SHA256}"
echo "timer_enabled=${TIMER_ENABLED}"
echo "timer_active=${TIMER_ACTIVE}"
echo "service_result=${SERVICE_RESULT}"
echo "local_llm_fallback=loopback_ollama"
echo "secret_values_printed=false"
echo "historical_comments_ignored=true"
echo "historical_comments_ignored_or_state_preserved=true"
echo "private_issue_proof_posted=true"
echo "===== END ====="