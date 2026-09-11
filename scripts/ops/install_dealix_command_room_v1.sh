#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

# Install the Dealix command-room executables into the EXISTING autonomous-company
# control plane. This script deliberately does not create a second scheduler.

REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
CONTROL="${DEALIX_CONTROL:-/opt/dealix/control}"
RUN_USER="${DEALIX_RUN_USER:-dealix}"
AUTONOMY="$CONTROL/autonomous-company"
BIN="$AUTONOMY/bin"
COMMAND_WRAPPER="$BIN/dealix-command-room-cycle"
REPLY_WRAPPER="$BIN/dealix-founder-whatsapp-reply"
PY="${DEALIX_PYTHON:-$REPO/.venv/bin/python}"

[[ "$(id -u)" -eq 0 ]] || { echo "INSTALL=BLOCKED_ROOT_REQUIRED"; exit 2; }
id "$RUN_USER" >/dev/null 2>&1 || { echo "INSTALL=BLOCKED_RUN_USER_MISSING"; exit 2; }
sudo -u "$RUN_USER" -H git -C "$REPO" rev-parse --is-inside-work-tree >/dev/null 2>&1 || { echo "INSTALL=BLOCKED_REPO_MISSING"; exit 2; }
[[ -x "$PY" ]] || { echo "INSTALL=BLOCKED_TRUSTED_PYTHON_MISSING"; exit 2; }
[[ -f "$REPO/scripts/commercial/run_dealix_command_room_v1.py" ]] || { echo "INSTALL=BLOCKED_COMMAND_ROOM_RUNNER_MISSING"; exit 2; }
[[ -f "$REPO/scripts/commercial/verify_dealix_command_room_v1.py" ]] || { echo "INSTALL=BLOCKED_COMMAND_ROOM_VERIFIER_MISSING"; exit 2; }
[[ -f "$REPO/scripts/commercial/prepare_founder_whatsapp_reply_v1.py" ]] || { echo "INSTALL=BLOCKED_REPLY_WORKER_MISSING"; exit 2; }

RUN_GROUP="$(id -gn "$RUN_USER")"
install -d -m 0750 -o "$RUN_USER" -g "$RUN_GROUP" "$BIN"

sudo -u "$RUN_USER" -H "$PY" "$REPO/scripts/commercial/verify_dealix_command_room_v1.py"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

cat >"$TMP_DIR/command-room" <<EOF
#!/usr/bin/env bash
set -Eeuo pipefail
umask 077
export TZ=Asia/Riyadh
export PYTHONNOUSERSITE=1
export DEALIX_EXTERNAL_SEND=0
export EMAIL_LIVE_SEND=0
export WHATSAPP_ALLOW_LIVE_SEND=0
export PUBLIC_PUBLISH=0
export PAYMENT_EXECUTION=0
export PRODUCTION_MUTATION=0
exec "$PY" "$REPO/scripts/commercial/run_dealix_command_room_v1.py" --mode draft-only "\$@"
EOF

cat >"$TMP_DIR/founder-whatsapp-reply" <<EOF
#!/usr/bin/env bash
set -Eeuo pipefail
umask 077
export TZ=Asia/Riyadh
export PYTHONNOUSERSITE=1
export LOCAL_LLM_PROVIDER=vllm
export VLLM_BASE_URL=http://127.0.0.1:11999/v1
export VLLM_MODEL=dealix-local
export DEALIX_EXTERNAL_SEND=0
export EMAIL_LIVE_SEND=0
export WHATSAPP_ALLOW_LIVE_SEND=0
export PUBLIC_PUBLISH=0
export PAYMENT_EXECUTION=0
export PRODUCTION_MUTATION=0
exec "$PY" "$REPO/scripts/commercial/prepare_founder_whatsapp_reply_v1.py" "\$@"
EOF

install -m 0750 -o "$RUN_USER" -g "$RUN_GROUP" "$TMP_DIR/command-room" "$COMMAND_WRAPPER"
install -m 0750 -o "$RUN_USER" -g "$RUN_GROUP" "$TMP_DIR/founder-whatsapp-reply" "$REPLY_WRAPPER"

# One-Company Law: do not add a timer. The already-installed canonical scheduler
# calls the command-room cycle for reconciliation. Conversation events/n8n call
# the reply wrapper directly; this installer does not create a per-channel daemon.
STATE="$AUTONOMY/state"
install -d -m 0750 -o "$RUN_USER" -g "$RUN_GROUP" "$STATE"
printf '%s\n' "$COMMAND_WRAPPER" > "$STATE/command_room_cycle_path"
printf '%s\n' "$REPLY_WRAPPER" > "$STATE/founder_whatsapp_reply_path"
chown "$RUN_USER:$RUN_GROUP" "$STATE/command_room_cycle_path" "$STATE/founder_whatsapp_reply_path"
chmod 0640 "$STATE/command_room_cycle_path" "$STATE/founder_whatsapp_reply_path"

printf 'DEALIX_COMMAND_ROOM_INSTALL=PASS\n'
printf 'COMMAND_ROOM_CYCLE=%s\n' "$COMMAND_WRAPPER"
printf 'FOUNDER_WHATSAPP_REPLY=%s\n' "$REPLY_WRAPPER"
printf 'SCHEDULER_CREATED=false\n'
printf 'PER_CHANNEL_DAEMON_CREATED=false\n'
printf 'LIVE_EXTERNAL_SEND_ENABLED=false\n'
printf 'NEXT=use_existing_canonical_scheduler_for_reconciliation_and_event_queue_for_reply_worker_after_exact_acceptance\n'
