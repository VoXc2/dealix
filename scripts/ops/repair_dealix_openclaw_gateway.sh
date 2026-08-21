#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

RUN_USER="dealix"
OPENCLAW_BIN="/home/${RUN_USER}/.openclaw/bin/openclaw"
OPENCLAW_HOME="/home/${RUN_USER}/.openclaw"
CONFIG="${OPENCLAW_HOME}/openclaw.json"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP="${CONFIG}.pre-gateway-repair-${STAMP}.bak"
PROOF="/opt/dealix/logs/openclaw-gateway-repair-${STAMP}.log"

mkdir -p /opt/dealix/logs
touch "$PROOF"
chmod 0600 "$PROOF"
exec > >(tee -a "$PROOF") 2>&1

redact() {
  sed -E \
    -e 's#([0-9]{6,}:[A-Za-z0-9_-]{20,})#[REDACTED_TELEGRAM_TOKEN]#g' \
    -e 's#(gateway\.auth\.token[= :]+)[^ ,}\"]+#\1[REDACTED]#Ig' \
    -e 's#(Authorization: Bearer )[A-Za-z0-9._-]+#\1[REDACTED]#Ig'
}

if [[ "$(id -u)" -ne 0 ]]; then
  echo "BLOCKED: run as root"
  exit 2
fi

if [[ ! -x "$OPENCLAW_BIN" ]]; then
  echo "BLOCKED: OpenClaw binary missing: $OPENCLAW_BIN"
  exit 3
fi

if [[ ! -f "$CONFIG" ]]; then
  echo "BLOCKED: OpenClaw config missing: $CONFIG"
  exit 4
fi

cp -a "$CONFIG" "$BACKUP"
chown "$RUN_USER:$RUN_USER" "$BACKUP"
chmod 0600 "$BACKUP"

echo "===== OPENCLAW PRE-REPAIR ====="
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" --version || true
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" status --all 2>&1 | redact || true
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" gateway probe 2>&1 | redact || true
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" gateway status 2>&1 | redact || true

echo
echo "===== DOCTOR READ-ONLY ====="
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" doctor 2>&1 | redact || true

echo
echo "===== DOCTOR FIX ====="
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" doctor --fix 2>&1 | redact || true

# Re-assert Dealix-safe gateway invariants after doctor repair.
echo
echo "===== REASSERT SAFE GATEWAY CONFIG ====="
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set gateway.mode local >/dev/null
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set gateway.bind loopback >/dev/null
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set gateway.port 18789 >/dev/null
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set tools.profile messaging >/dev/null
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set tools.deny '["group:runtime","group:fs","exec","process","write","edit","apply_patch"]' --strict-json >/dev/null
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set tools.elevated.enabled false >/dev/null || true
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set channels.telegram.enabled true >/dev/null
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set channels.telegram.dmPolicy pairing >/dev/null
# Founder control is DM-only by default. Never enable wildcard Telegram groups.
# An explicit founder-reviewed group/user allowlist can be added later if there is a real need.
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set channels.telegram.groups '{}' --strict-json >/dev/null
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set channels.telegram.groupAllowFrom '[]' --strict-json >/dev/null

# Ensure local Ollama is healthy before gateway restart.
echo
echo "===== OLLAMA ====="
if curl -fsS --max-time 10 http://127.0.0.1:11434/api/tags >/dev/null; then
  echo "ollama_api=PASS"
else
  echo "ollama_api=FAIL"
fi

# Keep user service running after SSH logout.
loginctl enable-linger "$RUN_USER" >/dev/null 2>&1 || true

# Reinstall service metadata with current OpenClaw binary, then restart.
echo
echo "===== GATEWAY SERVICE REPAIR ====="
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" gateway install --force 2>&1 | redact || true
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" gateway restart 2>&1 | redact || true
sleep 5

# If still down, capture a short redacted journal and try one foreground probe.
if ! sudo -iu "$RUN_USER" "$OPENCLAW_BIN" gateway status --require-rpc >/tmp/dealix-openclaw-gateway-status.$$ 2>&1; then
  echo "gateway_first_restart=FAIL"
  cat /tmp/dealix-openclaw-gateway-status.$$ | redact || true
  rm -f /tmp/dealix-openclaw-gateway-status.$$
  echo
  echo "===== REDACTED USER SERVICE JOURNAL ====="
  sudo -iu "$RUN_USER" bash -lc 'journalctl --user -u openclaw-gateway.service -n 120 --no-pager' 2>&1 | redact || true
  echo
  echo "===== SECOND RESTART ====="
  sudo -iu "$RUN_USER" "$OPENCLAW_BIN" gateway restart 2>&1 | redact || true
  sleep 5
else
  cat /tmp/dealix-openclaw-gateway-status.$$ | redact || true
  rm -f /tmp/dealix-openclaw-gateway-status.$$
fi

echo
echo "===== FINAL OPENCLAW PROOF ====="
set +e
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" status --all 2>&1 | redact
STATUS_RC=${PIPESTATUS[0]}
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" gateway probe 2>&1 | redact
PROBE_RC=${PIPESTATUS[0]}
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" gateway status --require-rpc 2>&1 | redact
GATEWAY_RC=${PIPESTATUS[0]}
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" channels status --probe 2>&1 | redact
CHANNEL_RC=${PIPESTATUS[0]}
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" pairing list telegram 2>&1 | redact
PAIR_RC=${PIPESTATUS[0]}
set -e

echo
echo "===== RAILWAY LOCAL LINK ====="
# Local CLI context only; no deploy/domain/variable/production mutation.
sudo -iu "$RUN_USER" bash -lc '
  export PATH="$HOME/.railway/bin:$HOME/.local/bin:$PATH"
  cd /opt/dealix/workspace/dealix
  railway link --project Dealix --environment production >/dev/null 2>&1 || true
  railway status || true
  railway service list || true
' 2>&1 | redact || true

echo
echo "===== RESULT ====="
echo "status_rc=${STATUS_RC}"
echo "probe_rc=${PROBE_RC}"
echo "gateway_rc=${GATEWAY_RC}"
echo "channel_rc=${CHANNEL_RC}"
echo "pairing_rc=${PAIR_RC}"
echo "config_backup=${BACKUP}"
echo "proof=${PROOF}"

if [[ $GATEWAY_RC -eq 0 && $PROBE_RC -eq 0 ]]; then
  echo "OPENCLAW_GATEWAY=PASS"
  exit 0
fi

echo "OPENCLAW_GATEWAY=DEGRADED"
exit 20
