#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

ACTION_ID="dealix-no-deepseek-runtime-cutover-v1"
MODE="${1:-plan}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ROUTER_SOURCE="$ROOT/scripts/ops/dealix_local_ai_router.py"
MIGRATOR="$ROOT/scripts/ops/migrate_openclaw_no_deepseek.py"
ROUTER_RUNTIME="/opt/dealix/ai-router/router.py"
OPENCLAW_CONFIG="/home/dealix/.openclaw/openclaw.json"
DROPIN_DIR="/etc/systemd/system/dealix-llm-router.service.d"
DROPIN="$DROPIN_DIR/99-dealix-no-deepseek.conf"
STAMP="$(date +%Y%m%dT%H%M%S)"
BACKUP_DIR="/opt/dealix/control/backups/no-deepseek-cutover/$STAMP"
CANDIDATE="/tmp/dealix-openclaw-no-deepseek-$STAMP.json"

plan() {
  printf '%s\n' \
    "ACTION=$ACTION_ID" \
    "MODE=PLAN_ONLY" \
    "POLICY=NO_DEEPSEEK" \
    "NO_SECOND_ROUTER=1" \
    "ROUTER_RUNTIME=$ROUTER_RUNTIME" \
    "OPENCLAW_CONFIG=$OPENCLAW_CONFIG"
  printf '%s\n' \
    "EFFECTS_IF_APPROVED=replace_existing_router,remove_router_credential_binding,migrate_openclaw_fallbacks,restart_existing_router_and_gateway" \
    "ROLLBACK=runtime_router,systemd_dropin,openclaw_config" \
    "APPROVAL_REQUIRED=DEALIX_L5_APPROVAL_ACTION=$ACTION_ID"
}

if [[ "$MODE" == "plan" ]]; then
  plan
  exit 0
fi
if [[ "$MODE" != "apply" ]]; then
  echo "BLOCKED: use plan or apply" >&2
  exit 2
fi
if [[ "${DEALIX_L5_APPROVAL_ACTION:-}" != "$ACTION_ID" ]]; then
  echo "BLOCKED_L5: exact approval action required: $ACTION_ID" >&2
  exit 3
fi
if [[ "$(id -u)" -ne 0 ]]; then
  echo "BLOCKED: apply requires root" >&2
  exit 4
fi

python3 -m py_compile "$ROUTER_SOURCE" "$MIGRATOR"
[[ -f "$ROUTER_RUNTIME" && -f "$OPENCLAW_CONFIG" ]] || {
  echo "BLOCKED: live runtime files missing" >&2
  exit 5
}
python3 "$MIGRATOR" prepare --input "$OPENCLAW_CONFIG" --output "$CANDIDATE" \
  >/tmp/dealix-openclaw-migrate-receipt.json
python3 "$MIGRATOR" verify --input "$CANDIDATE" \
  >/tmp/dealix-openclaw-verify-receipt.json

mkdir -p "$BACKUP_DIR" "$DROPIN_DIR"
chmod 0700 "$BACKUP_DIR"
cp -a "$ROUTER_RUNTIME" "$BACKUP_DIR/router.py.before"
cp -a "$OPENCLAW_CONFIG" "$BACKUP_DIR/openclaw.json.before"
if [[ -f "$DROPIN" ]]; then
  cp -a "$DROPIN" "$BACKUP_DIR/99-dealix-no-deepseek.conf.before"
fi

rollback() {
  set +e
  install -o dealix -g dealix -m 0750 "$BACKUP_DIR/router.py.before" "$ROUTER_RUNTIME"
  install -o dealix -g dealix -m 0600 "$BACKUP_DIR/openclaw.json.before" "$OPENCLAW_CONFIG"
  if [[ -f "$BACKUP_DIR/99-dealix-no-deepseek.conf.before" ]]; then
    install -o root -g root -m 0644 \
      "$BACKUP_DIR/99-dealix-no-deepseek.conf.before" "$DROPIN"
  else
    rm -f "$DROPIN"
  fi
  systemctl daemon-reload
  systemctl restart dealix-llm-router.service
  sudo -u dealix env XDG_RUNTIME_DIR=/run/user/1000 \
    systemctl --user restart openclaw-gateway.service
  echo "ROLLBACK=ATTEMPTED backup=$BACKUP_DIR" >&2
}
trap rollback ERR

install -o dealix -g dealix -m 0750 "$ROUTER_SOURCE" "$ROUTER_RUNTIME"
install -o dealix -g dealix -m 0600 "$CANDIDATE" "$OPENCLAW_CONFIG"
cat >"$DROPIN" <<'EOF'
[Service]
LoadCredential=
Environment=DEALIX_NO_DEEPSEEK=1
EOF
chmod 0644 "$DROPIN"

systemctl daemon-reload
systemctl restart dealix-llm-router.service
sudo -u dealix env XDG_RUNTIME_DIR=/run/user/1000 \
  systemctl --user restart openclaw-gateway.service

for _ in $(seq 1 30); do
  if curl -fsS --max-time 2 http://127.0.0.1:11999/healthz \
    >/tmp/dealix-router-health.json 2>/dev/null; then
    break
  fi
  sleep 1
done
python3 - <<'PY'
import json
p = json.load(open("/tmp/dealix-router-health.json"))
assert p.get("no_deepseek") is True, p
assert p.get("cloud_auto_allowed") is False, p
assert p.get("router_alive") is True, p
PY
python3 "$MIGRATOR" verify --input "$OPENCLAW_CONFIG" \
  >/tmp/dealix-openclaw-live-verify.json

curl -fsS --max-time 120 http://127.0.0.1:11999/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"dealix-auto","messages":[{"role":"user","content":"Reply only ROUTER_LOCAL_OK"}],"max_tokens":16,"stream":false}' \
  >/tmp/dealix-router-local-canary.json
python3 - <<'PY'
import json
p = json.load(open("/tmp/dealix-router-local-canary.json"))
assert p.get("dealix_route") == "local", p
assert p.get("dealix_estimated_usd") == 0.0, p
assert p.get("no_deepseek") is True, p
PY

trap - ERR
rm -f "$CANDIDATE"
echo "CUTOVER=PASS action=$ACTION_ID backup=$BACKUP_DIR"
