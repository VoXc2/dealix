#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

RUN_USER="dealix"
OPENCLAW_BIN="/home/${RUN_USER}/.openclaw/bin/openclaw"
SECRET_DIR="/home/${RUN_USER}/.config/dealix-secrets"
TG_TOKEN_FILE="${SECRET_DIR}/openclaw-telegram.token"

if [[ "$(id -u)" -ne 0 ]]; then
  echo "BLOCKED: run as root"
  exit 2
fi

if [[ ! -x "$OPENCLAW_BIN" ]]; then
  echo "BLOCKED: OpenClaw is not installed at $OPENCLAW_BIN"
  exit 3
fi

mkdir -p "$SECRET_DIR"
chown "$RUN_USER:$RUN_USER" "$SECRET_DIR"
chmod 0700 "$SECRET_DIR"

# The previous token must already be revoked/rotated at BotFather because it was exposed.
# Remove only the stale local token file; never print its content.
rm -f "$TG_TOKEN_FILE"

if [[ ! -r /dev/tty ]]; then
  echo "BLOCKED: interactive TTY required for hidden Telegram token input"
  exit 4
fi

printf 'Paste the NEW BotFather token (hidden; do not paste into chat): ' >/dev/tty
IFS= read -r -s TG_TOKEN </dev/tty
printf '\n' >/dev/tty

if [[ -z "$TG_TOKEN" ]]; then
  echo "BLOCKED: empty token"
  exit 5
fi

# Validate in memory BEFORE persisting it.
TG_META="$(curl -fsS --max-time 20 "https://api.telegram.org/bot${TG_TOKEN}/getMe" 2>/dev/null || true)"
if ! python3 - "$TG_META" <<'PY'
import json,sys
try:
    d=json.loads(sys.argv[1])
    r=d.get('result') or {}
    ok=bool(d.get('ok')) and bool(r.get('is_bot')) and bool(r.get('username'))
except Exception:
    ok=False
raise SystemExit(0 if ok else 1)
PY
then
  unset TG_TOKEN TG_META
  echo "BLOCKED: Telegram getMe validation failed; nothing was saved."
  exit 6
fi

BOT_USERNAME="$(python3 - "$TG_META" <<'PY'
import json,sys
r=json.loads(sys.argv[1]).get('result') or {}
print(r.get('username','unknown'))
PY
)"
unset TG_META

printf '%s\n' "$TG_TOKEN" > "$TG_TOKEN_FILE"
unset TG_TOKEN
chown "$RUN_USER:$RUN_USER" "$TG_TOKEN_FILE"
chmod 0600 "$TG_TOKEN_FILE"

sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set channels.telegram.enabled true >/dev/null
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set channels.telegram.dmPolicy pairing >/dev/null
# Founder command is intentionally DM-only. Group commands remain fail-closed.
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set channels.telegram.groups '{}' --strict-json >/dev/null
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set channels.telegram.groupAllowFrom '[]' --strict-json >/dev/null
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" config set channels.telegram.tokenFile "$TG_TOKEN_FILE" >/dev/null

loginctl enable-linger "$RUN_USER" >/dev/null 2>&1 || true
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" gateway install --force >/dev/null 2>&1 || true
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" gateway restart >/dev/null 2>&1 || sudo -iu "$RUN_USER" "$OPENCLAW_BIN" gateway start >/dev/null 2>&1 || true
sleep 3

echo "===== OPENCLAW TELEGRAM RECOVERY PROOF ====="
echo "bot_username=@${BOT_USERNAME}"
echo "token_validation=PASS"
echo "token_file_permissions=$(stat -c '%a' "$TG_TOKEN_FILE" 2>/dev/null || echo unknown)"
echo "token_printed=false"
echo "telegram_group_commands=BLOCKED_DEFAULT"

echo
echo "===== GATEWAY ====="
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" gateway status --require-rpc || true

echo
echo "===== TELEGRAM ====="
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" channels status --probe || true

echo
echo "===== PAIRING ====="
sudo -iu "$RUN_USER" "$OPENCLAW_BIN" pairing list telegram || true

echo
echo "NEXT: DM the bot, then approve only your own pairing code locally."
