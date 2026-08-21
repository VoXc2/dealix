#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

REPO="Dealix-sa/dealix"
FOUNDER="VoXc2"
BRANCH="ops/dealix-vps-self-hosted-control-20260820"
RUN_USER="dealix"
AUTOPILOT_ROOT="/opt/dealix/company-autopilot"
CONTROL_ROOT="/opt/dealix/control"
BIN_DIR="${CONTROL_ROOT}/bin"
AUTOPILOT_BIN="${BIN_DIR}/dealix_company_autopilot.sh"
ISSUE_BRIDGE_INSTALLER_PATH="scripts/ops/install_dealix_vps_issue_bridge.sh"
OLLAMA_DROPIN_DIR="/etc/systemd/system/ollama.service.d"
OLLAMA_SAFE_DROPIN="${OLLAMA_DROPIN_DIR}/90-dealix-safe-ai.conf"
SAFE_LOCAL_MODEL="qwen3:4b-instruct-2507-q4_K_M"

if [[ "$(id -u)" -ne 0 ]]; then
  echo "BLOCKED: run as root"
  exit 2
fi
if ! id "$RUN_USER" >/dev/null 2>&1; then
  echo "BLOCKED: missing OS user $RUN_USER"
  exit 3
fi
if ! sudo -iu "$RUN_USER" gh auth status >/dev/null 2>&1; then
  echo "BLOCKED: GitHub CLI is not authenticated for $RUN_USER"
  exit 4
fi
LOGIN="$(sudo -iu "$RUN_USER" gh api user --jq '.login' 2>/dev/null || true)"
PRIVATE="$(sudo -iu "$RUN_USER" gh api "repos/${REPO}" --jq '.private' 2>/dev/null || true)"
if [[ "$LOGIN" != "$FOUNDER" ]]; then
  echo "BLOCKED: authenticated GitHub login is not $FOUNDER"
  exit 5
fi
if [[ "$PRIVATE" != "true" ]]; then
  echo "BLOCKED: $REPO must remain private"
  exit 6
fi

# Install only tiny runtime dependencies if they are actually missing.
missing_pkgs=()
command -v curl >/dev/null 2>&1 || missing_pkgs+=(curl)
command -v jq >/dev/null 2>&1 || missing_pkgs+=(jq)
command -v flock >/dev/null 2>&1 || missing_pkgs+=(util-linux)
if (( ${#missing_pkgs[@]} > 0 )); then
  echo "Installing missing runtime packages: ${missing_pkgs[*]}"
  export DEBIAN_FRONTEND=noninteractive
  apt-get update -y
  apt-get install -y --no-install-recommends "${missing_pkgs[@]}"
fi

for cmd in curl jq flock python3 systemctl systemd-analyze git docker ollama gh; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "BLOCKED: required command missing after dependency check: $cmd"
    exit 7
  fi
done

install -d -m 0750 -o "$RUN_USER" -g "$RUN_USER" \
  "$AUTOPILOT_ROOT" "$AUTOPILOT_ROOT/logs" "$AUTOPILOT_ROOT/state" "$AUTOPILOT_ROOT/reports" \
  "$CONTROL_ROOT" "$BIN_DIR"

TMP_AUTOPILOT="$(mktemp)"
TMP_BRIDGE_INSTALLER="$(mktemp)"
cleanup() { rm -f "$TMP_AUTOPILOT" "$TMP_BRIDGE_INSTALLER"; }
trap cleanup EXIT

sudo -iu "$RUN_USER" gh api \
  -H 'Accept: application/vnd.github.raw+json' \
  "repos/${REPO}/contents/scripts/ops/dealix_company_autopilot.sh?ref=${BRANCH}" \
  >"$TMP_AUTOPILOT"

# Reinstall safety: the original bootstrap carried a 64K benchmark alias as a
# fallback. This VPS is CPU-only/16GB and live proof showed that alias can consume
# roughly 12GB. Never reinstall that fallback into the runtime control plane.
python3 - "$TMP_AUTOPILOT" <<'PY'
from pathlib import Path
import sys
p = Path(sys.argv[1])
s = p.read_text(encoding="utf-8")
s = s.replace(
    'LOCAL_MODEL_FALLBACK="dealix-qwen3-4b-64k"',
    'LOCAL_MODEL_FALLBACK="${DEALIX_LOCAL_MODEL:-qwen3:4b-instruct-2507-q4_K_M}"',
)
if 'LOCAL_MODEL_FALLBACK="dealix-qwen3-4b-64k"' in s:
    raise SystemExit("BLOCKED: unsafe 64K fallback remains")
p.write_text(s, encoding="utf-8")
PY

bash -n "$TMP_AUTOPILOT"
install -m 0750 -o "$RUN_USER" -g "$RUN_USER" "$TMP_AUTOPILOT" "$AUTOPILOT_BIN"

# Canonical safe Ollama posture for this VPS. This drop-in sorts after the legacy
# dealix.conf and therefore makes a reinstall deterministic without deleting
# historical config/backups. Ollama stays loopback-only and one-model/one-request.
install -d -m 0755 "$OLLAMA_DROPIN_DIR"
cat >"$OLLAMA_SAFE_DROPIN" <<'EOF'
[Service]
Environment="OLLAMA_HOST=127.0.0.1:11434"
Environment="OLLAMA_KEEP_ALIVE=2m"
Environment="OLLAMA_MAX_LOADED_MODELS=1"
Environment="OLLAMA_NUM_PARALLEL=1"
Environment="OLLAMA_CONTEXT_LENGTH=8192"
CPUQuota=300%
MemoryMax=8G
EOF
chmod 0644 "$OLLAMA_SAFE_DROPIN"

cat >/etc/systemd/system/dealix-company@.service <<EOF
[Unit]
Description=Dealix Company Autopilot (%i)
After=network-online.target docker.service ollama.service
Wants=network-online.target

[Service]
Type=oneshot
User=dealix
Group=dealix
WorkingDirectory=/opt/dealix/workspace/dealix
Environment="HOME=/home/dealix"
Environment="TZ=Asia/Riyadh"
Environment="PATH=/home/dealix/.local/bin:/home/dealix/.railway/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
Environment="DEALIX_EXTERNAL_OUTREACH_ENABLED=false"
Environment="EXTERNAL_OUTREACH_ENABLED=false"
Environment="AUTO_SEND_ENABLED=false"
Environment="AGENT_APPROVAL_MODE=required"
Environment="WHATSAPP_ALLOW_LIVE_SEND=false"
Environment="MOYASAR_LIVE_MODE=0"
Environment="DEALIX_LOCAL_MODEL=${SAFE_LOCAL_MODEL}"
# Local-only OpenAI-compatible fallback for existing Dealix code paths that
# already understand the OpenAI provider. This never changes Railway production.
Environment="OPENAI_API_KEY=ollama-local"
Environment="OPENAI_BASE_URL=http://127.0.0.1:11434/v1"
Environment="OPENAI_MODEL=${SAFE_LOCAL_MODEL}"
ExecStart=/opt/dealix/control/bin/dealix_company_autopilot.sh %i
TimeoutStartSec=55min
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=full
ProtectHome=read-only
ProtectKernelTunables=true
ProtectKernelModules=true
ProtectControlGroups=true
RestrictSUIDSGID=true
LockPersonality=true
ReadWritePaths=/opt/dealix/company-autopilot /opt/dealix/control/state /opt/dealix/workspace/dealix
Nice=10
IOSchedulingClass=best-effort
IOSchedulingPriority=6

[Install]
WantedBy=multi-user.target
EOF

write_interval_timer() {
  local name="$1" boot="$2" interval="$3" random="$4"
  cat >"/etc/systemd/system/dealix-company-${name}.timer" <<EOF
[Unit]
Description=Dealix Company Autopilot timer (${name})

[Timer]
OnBootSec=${boot}
OnUnitActiveSec=${interval}
RandomizedDelaySec=${random}
Persistent=true
Unit=dealix-company@${name}.service

[Install]
WantedBy=timers.target
EOF
}

write_calendar_timer() {
  local name="$1" calendar="$2" random="$3"
  systemd-analyze calendar "$calendar" >/dev/null
  cat >"/etc/systemd/system/dealix-company-${name}.timer" <<EOF
[Unit]
Description=Dealix Company Autopilot timer (${name})

[Timer]
OnCalendar=${calendar}
RandomizedDelaySec=${random}
Persistent=true
Unit=dealix-company@${name}.service

[Install]
WantedBy=timers.target
EOF
}

# Continuous low-cost control plane.
write_interval_timer heartbeat 2min 5min 15s
write_interval_timer production 3min 15min 30s
write_calendar_timer repo-watch '*-*-* *:17:00 Asia/Riyadh' 2min

# Saudi business-day operating cadence. GitHub already owns 07:00 revenue and
# 08:00 governed-full-ops; the VPS preflights and only runs a local fallback if
# those scheduled workflows did not finish successfully.
write_calendar_timer preflight 'Sun..Thu *-*-* 06:30:00 Asia/Riyadh' 2min
write_calendar_timer morning-fallback 'Sun..Thu *-*-* 08:45:00 Asia/Riyadh' 2min
write_calendar_timer midday 'Sun..Thu *-*-* 12:30:00 Asia/Riyadh' 3min
write_calendar_timer evening 'Sun..Thu *-*-* 19:00:00 Asia/Riyadh' 3min
write_calendar_timer local-ai 'Sun..Thu *-*-* 21:15:00 Asia/Riyadh' 4min
write_calendar_timer nightly '*-*-* 23:30:00 Asia/Riyadh' 5min
write_calendar_timer weekly 'Sat *-*-* 21:00:00 Asia/Riyadh' 5min

# Recover RAM from the earlier long-lived 64K Hermes benchmark. Scheduled local
# AI uses the normal 4B model at 8K context and unloads it after each synthesis.
ollama stop dealix-qwen3-4b-64k >/dev/null 2>&1 || true
ollama stop "$SAFE_LOCAL_MODEL" >/dev/null 2>&1 || true

systemctl daemon-reload
systemctl restart ollama.service
sleep 4
curl -fsS --max-time 10 http://127.0.0.1:11434/api/tags >/dev/null

# Verify the effective global context guard before enabling any local-AI timer.
OLLAMA_ENV="$(systemctl show ollama.service -p Environment --value 2>/dev/null || true)"
if [[ "$OLLAMA_ENV" != *"OLLAMA_CONTEXT_LENGTH=8192"* ]]; then
  echo "BLOCKED: effective Ollama context is not pinned to 8192"
  exit 8
fi
if [[ "$OLLAMA_ENV" != *"OLLAMA_HOST=127.0.0.1:11434"* ]]; then
  echo "BLOCKED: Ollama is not pinned to loopback"
  exit 9
fi

systemctl enable --now \
  dealix-company-heartbeat.timer \
  dealix-company-production.timer \
  dealix-company-repo-watch.timer \
  dealix-company-preflight.timer \
  dealix-company-morning-fallback.timer \
  dealix-company-midday.timer \
  dealix-company-evening.timer \
  dealix-company-local-ai.timer \
  dealix-company-nightly.timer \
  dealix-company-weekly.timer

# Refresh the private Issue bridge/dispatcher from this branch so the new
# autopilot commands become remotely callable. The installer is idempotent and
# bootstraps past historical comments to prevent replay.
sudo -iu "$RUN_USER" gh api \
  -H 'Accept: application/vnd.github.raw+json' \
  "repos/${REPO}/contents/${ISSUE_BRIDGE_INSTALLER_PATH}?ref=${BRANCH}" \
  >"$TMP_BRIDGE_INSTALLER"
chmod 0700 "$TMP_BRIDGE_INSTALLER"
bash -n "$TMP_BRIDGE_INSTALLER"
bash "$TMP_BRIDGE_INSTALLER"

# Execute only cheap proof cycles immediately. Heavy business cycles stay on
# schedule or explicit private commands.
systemctl start dealix-company@heartbeat.service || true
systemctl start dealix-company@production.service || true
systemctl start dealix-company@status.service || true

cat <<EOF

===== DEALIX COMPANY AUTOPILOT INSTALLED =====
repository_private=true
github_login=${LOGIN}
autopilot=${AUTOPILOT_BIN}
local_model=${SAFE_LOCAL_MODEL}
ollama_context=8192
ollama_loopback=true
external_send=false
production_mutation=false
payment_execution=false
merge_to_main=false

EOF
systemctl list-timers 'dealix-company-*' --no-pager

echo
echo "===== CURRENT PROOF ====="
systemctl --no-pager --full status dealix-company@heartbeat.service | sed -n '1,18p' || true
systemctl --no-pager --full status dealix-company@production.service | sed -n '1,18p' || true

echo
echo "===== RESOURCE BASELINE ====="
free -h
ollama ps || true

echo "===== END ====="