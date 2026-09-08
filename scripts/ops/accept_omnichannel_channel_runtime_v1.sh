#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

export TZ="${TZ:-Asia/Riyadh}"
export LC_ALL="${LC_ALL:-C.UTF-8}"
export LANG="${LANG:-C.UTF-8}"
export GH_PROMPT_DISABLED=1
export GIT_TERMINAL_PROMPT=0
export PYTHONNOUSERSITE=1

EXPECTED_SHA="${DEALIX_EXPECTED_SHA:-${1:-}}"
if [[ -z "$EXPECTED_SHA" ]]; then
  echo "RESULT=HOLD_EXPECTED_SHA_REQUIRED"
  exit 20
fi

ROOT="$(git rev-parse --show-toplevel)"
CURRENT_SHA="$(git -c safe.directory="$ROOT" -C "$ROOT" rev-parse HEAD)"

if [[ "$CURRENT_SHA" != "$EXPECTED_SHA" ]]; then
  echo "EXPECTED_SHA=$EXPECTED_SHA"
  echo "CURRENT_SHA=$CURRENT_SHA"
  echo "RESULT=HOLD_EXACT_HEAD_MISMATCH"
  exit 21
fi

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

export EXTERNAL_SEND_ENABLED=false
export EMAIL_SEND_ENABLED=false
export EMAIL_LIVE_SEND=0
export WHATSAPP_SEND_ENABLED=false
export WHATSAPP_ALLOW_LIVE_SEND=false
export WHATSAPP_OUTBOUND=0
export SMS_SEND_ENABLED=false
export VOICE_OUTBOUND_ENABLED=false
export PUBLIC_PUBLISH=0
export PAID_SPEND=0
export PAYMENT_EXECUTION=0

PY="${DEALIX_PYTHON:-python}"

cd "$ROOT"

echo "OMNICHANNEL_ACCEPTANCE_SHA=$CURRENT_SHA"

"$PY" scripts/verify_governed_channel_runtime_v1.py
"$PY" scripts/verify_metricool_distribution_adapter_v1.py
"$PY" -m pytest -q \
  tests/test_governed_channel_runtime_v1.py \
  tests/test_metricool_distribution_adapter_v1.py

git -c safe.directory="$ROOT" -C "$ROOT" diff --check

if [[ -x "$ROOT/bin/dealix" ]]; then
  "$ROOT/bin/dealix" verify trust --worktree
else
  echo "RESULT=HOLD_BIN_DEALIX_MISSING"
  exit 22
fi

END_SHA="$(git -c safe.directory="$ROOT" -C "$ROOT" rev-parse HEAD)"
if [[ "$END_SHA" != "$EXPECTED_SHA" ]]; then
  echo "END_SHA=$END_SHA"
  echo "RESULT=HOLD_HEAD_MOVED_DURING_ACCEPTANCE"
  exit 23
fi

if [[ -n "$(git -c safe.directory="$ROOT" -C "$ROOT" status --porcelain)" ]]; then
  echo "RESULT=HOLD_WORKTREE_DIRTY_AFTER_ACCEPTANCE"
  exit 24
fi

echo "METRICOOL_PUBLIC_PUBLISH_AUTHORITY=NONE"
echo "EXTERNAL_SEND_AUTHORITY=NONE"
echo "PRODUCTION_MUTATION_AUTHORITY=NONE"
echo "RESULT=PASS_OMNICHANNEL_CHANNEL_RUNTIME_V1_SOURCE_ACCEPTANCE"
