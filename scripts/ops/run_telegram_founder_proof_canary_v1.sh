#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd -P)"
EXPECTED_SHA="${1:-}"
CANARY_AUTH="${DEALIX_FOUNDER_TELEGRAM_CANARY:-0}"
RUN_USER="dealix"
OPENCLAW_HOME="/home/$RUN_USER/.openclaw"
OPENCLAW_BIN="$OPENCLAW_HOME/bin/openclaw"
CONFIG="$OPENCLAW_HOME/openclaw.json"
PROOF_ACCEPT_ROOT="/opt/dealix/control/proof/telegram-proof-acceptance/$EXPECTED_SHA"
CANARY_ROOT="/opt/dealix/control/proof/telegram-founder-canary/$EXPECTED_SHA"

fail() {
  echo "DEALIX_TELEGRAM_PROOF_CANARY=BLOCKED_$1"
  exit "${2:-2}"
}

[[ -n "$EXPECTED_SHA" ]] || fail "EXPECTED_SHA_REQUIRED"
[[ "$CANARY_AUTH" == "1" ]] || fail "EXPLICIT_CANARY_FLAG_REQUIRED"
[[ "$(sudo -u "$RUN_USER" git -C "$ROOT" rev-parse HEAD)" == "$EXPECTED_SHA" ]] || fail "HEAD_MISMATCH"
[[ "$(id -u)" -eq 0 ]] || fail "ROOT_REQUIRED_FOR_RUNTIME_ACCEPTANCE"
[[ -x "$OPENCLAW_BIN" ]] || fail "OPENCLAW_BINARY_MISSING"
[[ -f "$CONFIG" && ! -L "$CONFIG" ]] || fail "OPENCLAW_CONFIG_UNSAFE"

# The exact detached worktree is owned by dealix while this canary must run as
# root for read-only runtime evidence. Keep Git trust process-local and exact;
# never persist a wildcard/global safe.directory mutation.
export GIT_CONFIG_COUNT=1
export GIT_CONFIG_KEY_0=safe.directory
export GIT_CONFIG_VALUE_0="$ROOT"

export DEALIX_EXTERNAL_SEND=0
export DEALIX_EMAIL_LIVE_SEND=0
export DEALIX_WHATSAPP_OUTBOUND=0
export DEALIX_PUBLIC_PUBLISH=0
export DEALIX_PAID_SPEND=0
export DEALIX_PAYMENT_EXECUTION=0
export DEALIX_PRODUCTION_MUTATION=0
export DEALIX_DNS_MUTATION=0
export DEALIX_DB_MUTATION=0
export DEALIX_SECRET_MUTATION=0
export DEALIX_IDENTITY_MUTATION=0
export DEALIX_AGENT_SELF_AUTHORITY=0
export DEALIX_AUTONOMY_LEVEL=4
export DEALIX_MODE=draft-only

mkdir -p "$CANARY_ROOT"
chmod 0700 "$CANARY_ROOT"

# Gate 1: exact-head proof-plane source/test/synthetic receipt acceptance.
bash "$ROOT/scripts/ops/accept_telegram_proof_plane_v1.sh" "$EXPECTED_SHA" \
  >"$CANARY_ROOT/proof-plane-acceptance.log" 2>&1 || {
    chmod 0600 "$CANARY_ROOT/proof-plane-acceptance.log"
    fail "PROOF_PLANE_ACCEPTANCE_NOT_PASS" 3
  }
chmod 0600 "$CANARY_ROOT/proof-plane-acceptance.log"

grep -Fqx "DEALIX_TELEGRAM_PROOF_ACCEPTANCE=PASS" "$PROOF_ACCEPT_ROOT/receipt.env" \
  || fail "PROOF_PLANE_RECEIPT_NOT_PASS" 3

# Gate 2: existing canonical Telegram/OpenClaw runtime acceptance. This is
# intentionally reused rather than creating a second Founder Control verifier.
bash "$ROOT/scripts/ops/accept_founder_command_authority_v1.sh" "$EXPECTED_SHA" \
  >"$CANARY_ROOT/founder-control-acceptance.log" 2>&1 || {
    chmod 0600 "$CANARY_ROOT/founder-control-acceptance.log"
    fail "FOUNDER_CONTROL_ACCEPTANCE_NOT_PASS" 4
  }
chmod 0600 "$CANARY_ROOT/founder-control-acceptance.log"

grep -Fq "DEALIX_FOUNDER_COMMAND_ACCEPTANCE=PASS" "$CANARY_ROOT/founder-control-acceptance.log" \
  || fail "FOUNDER_CONTROL_RECEIPT_NOT_PASS" 4

# Resolve exactly one numeric founder identity in memory. Do not print or
# persist the raw Telegram ID in the canary receipt.
OWNER_ID="$(/usr/bin/python3 - "$CONFIG" <<'PY'
import json, re, sys
from pathlib import Path
payload = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
values = payload.get('commands', {}).get('ownerAllowFrom', [])
if not isinstance(values, list):
    raise SystemExit(2)
ids = []
for value in values:
    match = re.fullmatch(r'telegram:([0-9]{4,20})', str(value).strip(), flags=re.I)
    if match:
        ids.append(match.group(1))
if len(set(ids)) != 1 or len(ids) != 1:
    raise SystemExit(3)
print(ids[0])
PY
)" || fail "EXACT_FOUNDER_TARGET_UNRESOLVED" 5

OWNER_FP="$(printf 'telegram:%s' "$OWNER_ID" | sha256sum | awk '{print substr($1,1,20)}')"

LATEST_NAME="$(cat "$PROOF_ACCEPT_ROOT/generated/LATEST")"
[[ "$LATEST_NAME" =~ ^proof_[0-9a-f]{16}\.json$ ]] || fail "LATEST_PROOF_POINTER_INVALID" 6
PROOF_JSON="$PROOF_ACCEPT_ROOT/generated/$LATEST_NAME"
PROOF_MESSAGE="${PROOF_JSON%.json}.telegram.txt"
[[ -f "$PROOF_JSON" && ! -L "$PROOF_JSON" ]] || fail "PROOF_JSON_UNSAFE" 6
[[ -f "$PROOF_MESSAGE" && ! -L "$PROOF_MESSAGE" ]] || fail "PROOF_MESSAGE_UNSAFE" 6

PROOF_DIGEST="$(/usr/bin/python3 - "$PROOF_JSON" <<'PY'
import json, re, sys
from pathlib import Path
payload = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
digest = str(payload.get('envelope_sha256') or '')
if not re.fullmatch(r'[0-9a-f]{64}', digest):
    raise SystemExit(2)
print(digest)
PY
)" || fail "PROOF_DIGEST_INVALID" 6

# Resolve the bundled Node runtime exactly as the canonical runtime acceptance
# does, without installing or mutating PATH on disk.
NODE_BIN="$(find "$OPENCLAW_HOME/tools" -type f -path '*/bin/node' -perm -0100 2>/dev/null | sort | tail -n 1 || true)"
[[ -n "$NODE_BIN" ]] || fail "BUNDLED_NODE_MISSING" 7
OPENCLAW_PATH="$(dirname "$NODE_BIN"):$OPENCLAW_HOME/bin:/home/$RUN_USER/.local/bin:/usr/local/bin:/usr/bin:/bin"

# This is a single founder-internal synthetic INFO/HOLD canary. It carries no
# approval button and grants no authority. Suppress CLI output because raw
# target identifiers must not enter proof logs.
set +e
sudo -iu "$RUN_USER" env \
  HOME="/home/$RUN_USER" \
  PATH="$OPENCLAW_PATH" \
  "$OPENCLAW_BIN" message send \
    --channel telegram \
    --target "$OWNER_ID" \
    --message "$(cat "$PROOF_MESSAGE")" \
    --silent \
    >/dev/null 2>&1
SEND_RC=$?
set -e

if [[ "$SEND_RC" -ne 0 ]]; then
  cat >"$CANARY_ROOT/receipt.env" <<EOF
DEALIX_TELEGRAM_PROOF_CANARY=FAIL_PROVIDER_SEND
SOURCE_SHA=$EXPECTED_SHA
FOUNDER_TARGET_FINGERPRINT=sha256:$OWNER_FP
PROOF_SHA256=$PROOF_DIGEST
PROOF_PLANE_ACCEPTANCE=PASS
FOUNDER_CONTROL_ACCEPTANCE=PASS
TELEGRAM_PROVIDER_ACCEPTED=false
L5_EXECUTED=false
CUSTOMER_SEND=false
EOF
  chmod 0600 "$CANARY_ROOT/receipt.env"
  echo "DEALIX_TELEGRAM_PROOF_CANARY=FAIL_PROVIDER_SEND"
  echo "receipt=$CANARY_ROOT/receipt.env"
  exit 8
fi

cat >"$CANARY_ROOT/receipt.env" <<EOF
DEALIX_TELEGRAM_PROOF_CANARY=PASS
SOURCE_SHA=$EXPECTED_SHA
FOUNDER_TARGET_FINGERPRINT=sha256:$OWNER_FP
PROOF_SHA256=$PROOF_DIGEST
PROOF_PLANE_ACCEPTANCE=PASS
FOUNDER_CONTROL_ACCEPTANCE=PASS
TELEGRAM_PROVIDER_ACCEPTED=true
TELEGRAM_MESSAGE_IS_EXECUTION_PROOF=false
APPROVAL_BUTTON_PRESENT=false
L5_EXECUTED=false
CUSTOMER_SEND=false
PUBLIC_PUBLISH=false
PAYMENT_EXECUTION=false
PRODUCTION_MUTATION=false
DNS_DB_SECRET_MUTATION=false
EOF
chmod 0600 "$CANARY_ROOT/receipt.env"
sha256sum "$CANARY_ROOT/receipt.env" >"$CANARY_ROOT/receipt.env.sha256"
chmod 0600 "$CANARY_ROOT/receipt.env.sha256"

echo "DEALIX_TELEGRAM_PROOF_CANARY=PASS"
echo "source_sha=$EXPECTED_SHA"
echo "founder_target_fingerprint=sha256:$OWNER_FP"
echo "proof_sha256=$PROOF_DIGEST"
echo "telegram_provider_accepted=true"
echo "telegram_message_is_execution_proof=false"
echo "approval_button_present=false"
echo "L5_EXECUTED=false"
echo "receipt=$CANARY_ROOT/receipt.env"
