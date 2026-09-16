#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

ROOT="${DEALIX_REPO_ROOT:-/opt/dealix/workspace/dealix}"
CONTROL="${DEALIX_CONTROL_ROOT:-/opt/dealix/control}"
RUN_USER="${DEALIX_RUN_USER:-dealix}"
PY="${DEALIX_PYTHON:-$ROOT/.venv/bin/python}"
AUTONOMY="$CONTROL/autonomous-company"
PROMPT_SOURCE="$ROOT/prompts/company/DEALIX_AUTONOMOUS_COMPANY_MASTER_EXECUTION_PROMPT_2026_09_16.md"
META_SOURCE="$ROOT/config/company/dealix_meta_operating_system_v2.json"
BINDING_SOURCE="$ROOT/config/company/dealix_master_prompt_binding_v1.json"
PROMPT_DIR="$AUTONOMY/prompts"
CONFIG_DIR="$AUTONOMY/config"
PROMPT_TARGET="$PROMPT_DIR/DEALIX_AUTONOMOUS_COMPANY_MASTER_EXECUTION_PROMPT_2026_09_16.md"
META_TARGET="$CONFIG_DIR/dealix_meta_operating_system_v2.json"
BINDING_TARGET="$CONFIG_DIR/dealix_master_prompt_binding_v1.json"
BIN_DIR="$AUTONOMY/bin"
LAUNCHER="$BIN_DIR/dealix-master-company-cycle"
STATE_DIR="$AUTONOMY/state"
VERIFY="$ROOT/scripts/commercial/verify_dealix_master_prompt_binding_v1.py"
RUNNER="$ROOT/scripts/commercial/run_dealix_master_company_cycle_v1.py"

[[ "$(id -u)" -eq 0 ]] || { echo "MASTER_COMPANY_INSTALL=BLOCKED_ROOT_REQUIRED"; exit 2; }
id "$RUN_USER" >/dev/null 2>&1 || { echo "MASTER_COMPANY_INSTALL=BLOCKED_RUN_USER_MISSING"; exit 2; }
[[ -d "$ROOT/.git" || -f "$ROOT/.git" ]] || { echo "MASTER_COMPANY_INSTALL=BLOCKED_REPO_MISSING"; exit 2; }
[[ -x "$PY" ]] || { echo "MASTER_COMPANY_INSTALL=BLOCKED_TRUSTED_PYTHON_MISSING"; exit 2; }
for f in "$PROMPT_SOURCE" "$META_SOURCE" "$BINDING_SOURCE" "$VERIFY" "$RUNNER"; do
  [[ -f "$f" ]] || { echo "MASTER_COMPANY_INSTALL=BLOCKED_REQUIRED_FILE_MISSING file=$f"; exit 2; }
done

RUN_GROUP="$(id -gn "$RUN_USER")"
sudo -u "$RUN_USER" -H env PYTHONPATH="$ROOT" "$PY" "$VERIFY"
install -d -m 0750 -o "$RUN_USER" -g "$RUN_GROUP" "$PROMPT_DIR" "$CONFIG_DIR" "$BIN_DIR" "$STATE_DIR"

atomic_install() {
  local source="$1" target="$2" mode="$3" tmp
  tmp="${target}.new.$$"
  install -m "$mode" -o "$RUN_USER" -g "$RUN_GROUP" "$source" "$tmp"
  [[ "$(sha256sum "$source" | awk '{print $1}')" == "$(sha256sum "$tmp" | awk '{print $1}')" ]] || {
    rm -f "$tmp"; echo "MASTER_COMPANY_INSTALL=BLOCKED_COPY_HASH_MISMATCH target=$target"; exit 2;
  }
  mv -f "$tmp" "$target"
}

atomic_install "$PROMPT_SOURCE" "$PROMPT_TARGET" 0640
atomic_install "$META_SOURCE" "$META_TARGET" 0640
atomic_install "$BINDING_SOURCE" "$BINDING_TARGET" 0640
PROMPT_SHA="$(sha256sum "$PROMPT_TARGET" | awk '{print $1}')"
META_SHA="$(sha256sum "$META_TARGET" | awk '{print $1}')"
BINDING_SHA="$(sha256sum "$BINDING_TARGET" | awk '{print $1}')"
SOURCE_HEAD="$(git -c safe.directory="$ROOT" -C "$ROOT" rev-parse --verify HEAD 2>/dev/null)" || {
  echo "MASTER_COMPANY_INSTALL=BLOCKED_SOURCE_HEAD_UNRESOLVED"
  exit 2
}
[[ "$SOURCE_HEAD" =~ ^[0-9a-f]{40}$ ]] || {
  echo "MASTER_COMPANY_INSTALL=BLOCKED_SOURCE_HEAD_INVALID"
  exit 2
}

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT
cat >"$TMP" <<EOF
#!/usr/bin/env bash
set -Eeuo pipefail
umask 077
export TZ=Asia/Riyadh
export PYTHONNOUSERSITE=1
export DEALIX_MASTER_BINDING_PATH="$BINDING_TARGET"
export DEALIX_MASTER_BINDING_SHA256="$BINDING_SHA"
export DEALIX_COMPANY_MASTER_PROMPT="$PROMPT_TARGET"
export DEALIX_COMPANY_MASTER_PROMPT_SHA256="$PROMPT_SHA"
export DEALIX_META_CONTROL_PATH="$META_TARGET"
export DEALIX_META_CONTROL_SHA256="$META_SHA"
export DEALIX_MASTER_PROMPT_BOUND=1
export DEALIX_META_CONTROL_BOUND=1
export DEALIX_UNIVERSAL_L5=0
export DEALIX_EXTERNAL_SEND=0
export EMAIL_LIVE_SEND=0
export WHATSAPP_ALLOW_LIVE_SEND=0
export WHATSAPP_OUTBOUND=0
export PUBLIC_PUBLISH=0
export PAID_SPEND=0
export PAYMENT_EXECUTION=0
export PRODUCTION_MUTATION=0
export DNS_MUTATION=0
export DB_MUTATION=0
export SECRET_MUTATION=0
exec "$PY" "$RUNNER" "\$@"
EOF
install -m 0750 -o "$RUN_USER" -g "$RUN_GROUP" "$TMP" "$LAUNCHER"

printf '%s\n' "$LAUNCHER" >"$STATE_DIR/master_company_cycle_path"
printf '%s\n' "$BINDING_TARGET" >"$STATE_DIR/master_binding_path"
printf '%s\n' "$BINDING_SHA" >"$STATE_DIR/master_binding_sha256"
printf '%s\n' "$PROMPT_TARGET" >"$STATE_DIR/master_prompt_path"
printf '%s\n' "$PROMPT_SHA" >"$STATE_DIR/master_prompt_sha256"
printf '%s\n' "$META_TARGET" >"$STATE_DIR/meta_control_path"
printf '%s\n' "$META_SHA" >"$STATE_DIR/meta_control_sha256"
printf '%s\n' "$SOURCE_HEAD" >"$STATE_DIR/source_head"
chown "$RUN_USER:$RUN_GROUP" "$STATE_DIR"/*
chmod 0640 "$STATE_DIR"/*

printf 'DEALIX_MASTER_COMPANY_INSTALL=PASS\n'
printf 'SOURCE_HEAD=%s\n' "$SOURCE_HEAD"
printf 'MASTER_COMPANY_CYCLE=%s\n' "$LAUNCHER"
printf 'MASTER_BINDING_SHA256=%s\n' "$BINDING_SHA"
printf 'MASTER_PROMPT_SHA256=%s\n' "$PROMPT_SHA"
printf 'META_CONTROL_SHA256=%s\n' "$META_SHA"
printf 'RUNTIME_BINDING=INSTALLED_ARTIFACTS_SHA256_FAIL_CLOSED\n'
printf 'PERMANENT_AGENTS=5 (logical business roles / compatibility aliases)\n'
printf 'ARMS_TOTAL=44\n'
printf 'SCHEDULER_CREATED=false\n'
printf 'CANONICAL_SCHEDULER_REUSED=true\n'
printf 'LIVE_EXTERNAL_SEND_ENABLED=false\n'
printf 'MATERIAL_EXTERNAL_EFFECTS_ENABLED=false\n'
printf 'NEXT=promote_existing_canonical_scheduler_only_after_accepted_source_promotion\n'