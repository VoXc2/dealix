#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

# Dealix Slack Founder Room V1 — read-only VPS acceptance.
#
# This script does not create credentials, start services, send Slack messages,
# mutate production, merge code, or raise authority. It only verifies evidence
# after the Socket Mode bridge has been configured and a real command receipt
# exists.

REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
CONTROL="${DEALIX_CONTROL:-/opt/dealix/control}"
ENVFILE="$CONTROL/etc/slack-founder.env"
RECEIPT_DIR="$CONTROL/runs/slack-founder-receipts"
SERVICE="dealix-slack-founder.service"
PY="${DEALIX_PYTHON:-$REPO/.venv/bin/python}"

EXPECTED_SHA="${1:-}"

pass() { printf '[PASS] %s\n' "$*"; }
warn() { printf '[WARN] %s\n' "$*"; }
block() { printf '[BLOCKED] %s\n' "$*"; exit 3; }
fail() { printf '[FAIL] %s\n' "$*" >&2; exit 1; }

[[ -d "$REPO/.git" ]] || fail "canonical repository missing: $REPO"
[[ -x "$PY" ]] || fail "Dealix Python missing: $PY"

cd "$REPO"
HEAD="$(git rev-parse HEAD)"

if [[ -n "$EXPECTED_SHA" && "$HEAD" != "$EXPECTED_SHA" ]]; then
  fail "source SHA mismatch: HEAD=$HEAD expected=$EXPECTED_SHA"
fi
pass "source_sha=$HEAD"

"$PY" scripts/ops/verify_slack_founder_room_v1.py
pass "Founder Room contract verifier"

"$PY" scripts/ops/verify_autonomous_company_machine_v2.py
pass "Company Machine V2 verifier"

[[ -f "$ENVFILE" ]] || block "Slack secret file not configured: $ENVFILE"

# Verify presence only. Never print token values.
"$PY" - "$ENVFILE" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
values = {}
for raw in path.read_text(encoding="utf-8").splitlines():
    line = raw.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    key, value = line.split("=", 1)
    values[key.strip()] = value.strip().strip('"').strip("'")

required = ["SLACK_BOT_TOKEN", "SLACK_APP_TOKEN", "DEALIX_SLACK_COMMAND_CHANNEL_ID"]
missing = [key for key in required if not values.get(key)]
if missing:
    raise SystemExit("BLOCKED missing required Slack env keys: " + ", ".join(missing))

if values["DEALIX_SLACK_COMMAND_CHANNEL_ID"] != "C0BTMAWR3NY":
    raise SystemExit("FAIL command channel id does not match canonical Founder Room")

print("PASS Slack secret contract present (values redacted)")
PY
pass "Slack credentials/channel presence verified without disclosure"

if ! systemctl is-active --quiet "$SERVICE"; then
  block "$SERVICE is not active"
fi
pass "$SERVICE active"

# No standalone Slack timer is allowed; bridge is an event-driven service.
if systemctl list-unit-files --type=timer --no-legend 2>/dev/null \
  | awk '{print $1}' \
  | grep -Eq '^dealix-slack-(founder|bridge).*\.timer$'; then
  fail "parallel Slack scheduler/timer detected"
fi
pass "no Slack bridge timer/scheduler detected"

UNIT_TEXT="$(systemctl cat "$SERVICE" 2>/dev/null || true)"
[[ "$UNIT_TEXT" == *"DEALIX_EXTERNAL_SEND=0"* ]] || fail "external-send fail-closed env missing"
[[ "$UNIT_TEXT" == *"DEALIX_WHATSAPP_OUTBOUND=0"* ]] || fail "WhatsApp fail-closed env missing"
[[ "$UNIT_TEXT" == *"DEALIX_PUBLIC_PUBLISH=0"* ]] || fail "public-publish fail-closed env missing"
[[ "$UNIT_TEXT" == *"DEALIX_PAYMENT_EXECUTION=0"* ]] || fail "payment fail-closed env missing"
[[ "$UNIT_TEXT" == *"DEALIX_PRODUCTION_MUTATION=0"* ]] || fail "production-mutation fail-closed env missing"
pass "L5 external effects remain fail-closed"

[[ -d "$RECEIPT_DIR" ]] || block "receipt directory missing: $RECEIPT_DIR"

LATEST_RECEIPT="$({
  find "$RECEIPT_DIR" -maxdepth 1 -type f -name 'slack-*.json' -printf '%T@ %p\n' 2>/dev/null || true
} | sort -nr | head -1 | cut -d' ' -f2-)"

[[ -n "$LATEST_RECEIPT" && -f "$LATEST_RECEIPT" ]] \
  || block "no real Slack Founder Room receipt exists yet"

"$PY" scripts/ops/verify_slack_founder_bridge_receipt.py \
  "$LATEST_RECEIPT" \
  --expected-source-sha "$HEAD"
pass "latest Slack bridge receipt matches canonical source SHA"

FAILED_COUNT="$(systemctl --failed --no-legend 2>/dev/null | sed '/^[[:space:]]*$/d' | wc -l | tr -d ' ')"
if [[ "$FAILED_COUNT" != "0" ]]; then
  warn "systemd has $FAILED_COUNT failed unit(s); inspect separately"
else
  pass "systemd failed units = 0"
fi

printf '\nDEALIX_SLACK_FOUNDER_BRIDGE_V1=PASS\n'
printf 'source_sha=%s\n' "$HEAD"
printf 'service=%s\n' "$SERVICE"
printf 'receipt=%s\n' "$LATEST_RECEIPT"
printf 'scheduler_created=false\n'
printf 'parallel_agent_fleet_created=false\n'
printf 'external_effects=FAIL_CLOSED\n'
