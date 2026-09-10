#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

ROOT="${DEALIX_REPO_ROOT:-/opt/dealix/workspace/dealix}"
CONTROL="${DEALIX_CONTROL_ROOT:-/opt/dealix/control}"
RUN_USER="${DEALIX_RUN_USER:-dealix}"
PY="${DEALIX_PYTHON:-$ROOT/.venv/bin/python}"
AUTONOMY="$CONTROL/autonomous-company"
PROMPT_SOURCE="$ROOT/prompts/company/DEALIX_OMEGA_FOUNDER_COMMAND_ROOM_MASTER_PROMPT.md"
PROMPT_DIR="$AUTONOMY/prompts"
PROMPT_TARGET="$PROMPT_DIR/DEALIX_OMEGA_FOUNDER_COMMAND_ROOM_MASTER_PROMPT.md"
BIN_DIR="$AUTONOMY/bin"
LAUNCHER="$BIN_DIR/dealix-master-company-cycle"
STATE_DIR="$AUTONOMY/state"
VERIFY="$ROOT/scripts/commercial/verify_dealix_master_prompt_binding_v1.py"
RUNNER="$ROOT/scripts/commercial/run_dealix_master_company_cycle_v1.py"

[[ "$(id -u)" -eq 0 ]] || { echo "MASTER_COMPANY_INSTALL=BLOCKED_ROOT_REQUIRED"; exit 2; }
id "$RUN_USER" >/dev/null 2>&1 || { echo "MASTER_COMPANY_INSTALL=BLOCKED_RUN_USER_MISSING"; exit 2; }
[[ -d "$ROOT/.git" ]] || { echo "MASTER_COMPANY_INSTALL=BLOCKED_REPO_MISSING"; exit 2; }
[[ -x "$PY" ]] || { echo "MASTER_COMPANY_INSTALL=BLOCKED_TRUSTED_PYTHON_MISSING"; exit 2; }
[[ -f "$PROMPT_SOURCE" ]] || { echo "MASTER_COMPANY_INSTALL=BLOCKED_PROMPT_MISSING"; exit 2; }
[[ -f "$VERIFY" ]] || { echo "MASTER_COMPANY_INSTALL=BLOCKED_VERIFIER_MISSING"; exit 2; }
[[ -f "$RUNNER" ]] || { echo "MASTER_COMPANY_INSTALL=BLOCKED_RUNNER_MISSING"; exit 2; }

RUN_GROUP="$(id -gn "$RUN_USER")"
sudo -u "$RUN_USER" -H "$PY" "$VERIFY"
install -d -m 0750 -o "$RUN_USER" -g "$RUN_GROUP" "$PROMPT_DIR" "$BIN_DIR" "$STATE_DIR"
install -m 0640 -o "$RUN_USER" -g "$RUN_GROUP" "$PROMPT_SOURCE" "$PROMPT_TARGET"
PROMPT_SHA="$(sha256sum "$PROMPT_TARGET" | awk '{print $1}')"

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT
cat >"$TMP" <<EOF
#!/usr/bin/env bash
set -Eeuo pipefail
umask 077
export TZ=Asia/Riyadh
export PYTHONNOUSERSITE=1
export DEALIX_COMPANY_MASTER_PROMPT="$PROMPT_TARGET"
export DEALIX_COMPANY_MASTER_PROMPT_SHA256="$PROMPT_SHA"
export DEALIX_MASTER_PROMPT_BOUND=1
export DEALIX_EXTERNAL_SEND=0
export EMAIL_LIVE_SEND=0
export WHATSAPP_ALLOW_LIVE_SEND=0
export PUBLIC_PUBLISH=0
export PAYMENT_EXECUTION=0
export PRODUCTION_MUTATION=0
exec "$PY" "$RUNNER" "\$@"
EOF
install -m 0750 -o "$RUN_USER" -g "$RUN_GROUP" "$TMP" "$LAUNCHER"
printf '%s\n' "$LAUNCHER" >"$STATE/master_company_cycle_path"
printf '%s\n' "$PROMPT_TARGET" >"$STATE/master_prompt_path"
printf '%s\n' "$PROMPT_SHA" >"$STATE/master_prompt_sha256"
chown "$RUN_USER:$RUN_GROUP" "$STATE/master_company_cycle_path" "$STATE/master_prompt_path" "$STATE/master_prompt_sha256"
chmod 0640 "$STATE/master_company_cycle_path" "$STATE/master_prompt_path" "$STATE/master_prompt_sha256"

printf 'DEALIX_MASTER_COMPANY_INSTALL=PASS\n'
printf 'MASTER_COMPANY_CYCLE=%s\n' "$LAUNCHER"
printf 'MASTER_PROMPT_PATH=%s\n' "$PROMPT_TARGET"
printf 'MASTER_PROMPT_SHA256=%s\n' "$PROMPT_SHA"
printf 'SCHEDULER_CREATED=false\n'
printf 'CANONICAL_SCHEDULER_REUSED=true\n'
printf 'LIVE_EXTERNAL_SEND_ENABLED=false\n'
printf 'NEXT=bind_existing_canonical_scheduler_to_MASTER_COMPANY_CYCLE_after_exact_acceptance\n'
