#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

# Resolve the candidate repository from this script, not from the caller's CWD.
# This keeps exact-head acceptance isolated and avoids depending on root/global
# Git safe.directory state when invoked from a detached worktree.
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd -P)"
EXPECTED_SHA="${1:-}"
PY="${DEALIX_AUTOMATION_PYTHON:-}"
if [[ -z "$PY" || ! -x "$PY" ]]; then
  if [[ -x "$ROOT/.venv/bin/python" ]]; then
    PY="$ROOT/.venv/bin/python"
  else
    PY="$(command -v python3 2>/dev/null || true)"
  fi
fi

if [[ -z "$EXPECTED_SHA" ]]; then
  echo "DEALIX_TELEGRAM_PROOF_ACCEPTANCE=BLOCKED_EXPECTED_SHA_REQUIRED"
  exit 2
fi

HEAD_SHA="$(git -c safe.directory="$ROOT" -C "$ROOT" rev-parse HEAD)"
if [[ "$HEAD_SHA" != "$EXPECTED_SHA" ]]; then
  echo "DEALIX_TELEGRAM_PROOF_ACCEPTANCE=BLOCKED_HEAD_MISMATCH"
  echo "expected=$EXPECTED_SHA"
  echo "actual=$HEAD_SHA"
  exit 2
fi

if [[ -z "$PY" || ! -x "$PY" ]]; then
  echo "DEALIX_TELEGRAM_PROOF_ACCEPTANCE=BLOCKED_PYTHON_MISSING"
  exit 3
fi

PROOF_ROOT="${DEALIX_TELEGRAM_PROOF_ACCEPTANCE_ROOT:-/opt/dealix/control/proof/telegram-proof-acceptance/$HEAD_SHA}"
mkdir -p "$PROOF_ROOT"
chmod 0700 "$PROOF_ROOT"

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

cd "$ROOT"
export PYTHONPATH="$ROOT${PYTHONPATH:+:$PYTHONPATH}"

"$PY" scripts/ops/verify_telegram_proof_plane_v1.py \
  | tee "$PROOF_ROOT/source-verifier.log"

"$PY" -m pytest -q tests/test_telegram_proof_plane_v1.py \
  | tee "$PROOF_ROOT/pytest.log"

BUILDER_ROOT="$PROOF_ROOT/generated"
"$PY" scripts/ops/build_telegram_founder_proof.py \
  --source-sha "$HEAD_SHA" \
  --truth-class HOLD \
  --status HOLD \
  --subject "Telegram Proof Plane exact-head acceptance" \
  --decision "Source contract and renderer executed on exact candidate SHA" \
  --risk "Live Telegram delivery and runtime hardening remain separately unproven" \
  --next-action "Run current Telegram/OpenClaw Founder Control runtime acceptance" \
  --evidence "$PROOF_ROOT/source-verifier.log" \
  --evidence "$PROOF_ROOT/pytest.log" \
  --output-root "$BUILDER_ROOT" \
  | tee "$PROOF_ROOT/builder.log"

if ! grep -Fq "TELEGRAM_SENT=false" "$PROOF_ROOT/builder.log"; then
  echo "DEALIX_TELEGRAM_PROOF_ACCEPTANCE=FAIL_SEND_GUARD"
  exit 4
fi
if ! grep -Fq "L5_EXECUTED=false" "$PROOF_ROOT/builder.log"; then
  echo "DEALIX_TELEGRAM_PROOF_ACCEPTANCE=FAIL_L5_GUARD"
  exit 4
fi

sha256sum \
  "$PROOF_ROOT/source-verifier.log" \
  "$PROOF_ROOT/pytest.log" \
  "$PROOF_ROOT/builder.log" \
  > "$PROOF_ROOT/sha256sums.txt"
find "$PROOF_ROOT" -type d -exec chmod 0700 {} +
find "$PROOF_ROOT" -type f -exec chmod 0600 {} +

cat > "$PROOF_ROOT/receipt.env" <<EOF
DEALIX_TELEGRAM_PROOF_ACCEPTANCE=PASS
SOURCE_SHA=$HEAD_SHA
SOURCE_VERIFIER=PASS
TARGETED_TESTS=PASS
SYNTHETIC_PROOF=PASS
TELEGRAM_SENT=false
L5_EXECUTED=false
LIVE_TELEGRAM_DELIVERY=UNKNOWN_NOT_EVIDENCE_BACKED
OPENCLAW_RUNTIME_HARDENING=UNKNOWN_NOT_EVIDENCE_BACKED
EOF
chmod 0600 "$PROOF_ROOT/receipt.env"

echo "DEALIX_TELEGRAM_PROOF_ACCEPTANCE=PASS"
echo "SOURCE_SHA=$HEAD_SHA"
echo "PROOF_ROOT=$PROOF_ROOT"
echo "TELEGRAM_SENT=false"
echo "L5_EXECUTED=false"
