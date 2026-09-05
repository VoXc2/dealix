#!/usr/bin/env bash
set -Eeuo pipefail
umask 027

ROOT="$(git rev-parse --show-toplevel)"
EXPECTED_SHA="${1:-}"
ACTUAL_SHA="$(git -C "$ROOT" rev-parse HEAD)"
PYTHON_BIN="${DEALIX_AUTOMATION_PYTHON:-$ROOT/.venv/bin/python}"

if [[ ! "$EXPECTED_SHA" =~ ^[0-9a-f]{40}$ || "$ACTUAL_SHA" != "$EXPECTED_SHA" ]]; then
  echo "DEALIX_E2E_ACCEPTANCE=BLOCKED_HEAD_MISMATCH_OR_MISSING"
  echo "expected=$EXPECTED_SHA"
  echo "actual=$ACTUAL_SHA"
  exit 2
fi

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "DEALIX_E2E_ACCEPTANCE=BLOCKED_PYTHON_NOT_EXECUTABLE"
  echo "python=$PYTHON_BIN"
  exit 3
fi

if [[ -n "$(git -C "$ROOT" status --porcelain --untracked-files=normal)" ]]; then
  echo "DEALIX_E2E_ACCEPTANCE=BLOCKED_DIRTY_SOURCE"
  exit 4
fi

PROOF_ROOT="${DEALIX_E2E_PROOF_ROOT:-$(mktemp -d "/tmp/dealix-e2e-company-$ACTUAL_SHA.XXXXXX")}"
if [[ -L "$PROOF_ROOT" || -e "$PROOF_ROOT/receipt.json" ]]; then
  echo "DEALIX_E2E_ACCEPTANCE=BLOCKED_UNSAFE_OR_REUSED_PROOF_ROOT"
  exit 5
fi
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
export APP_ENV=test
export PYTHONNOUSERSITE=1
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$ROOT"

cd "$ROOT"

run() {
  local name="$1"
  shift
  echo "[$name]"
  "$@" 2>&1 | tee "$PROOF_ROOT/$name.log"
}

run quarantine_logic_tests \
  "$PYTHON_BIN" -m unittest discover -s tests -p test_autonomous_quarantine_verifier.py
run autonomous_quarantine \
  "$PYTHON_BIN" scripts/ops/verify_autonomous_quarantine.py
run composite_contract \
  "$PYTHON_BIN" scripts/ops/verify_end_to_end_company_acceptance_v1.py
run company_machine \
  "$PYTHON_BIN" scripts/ops/verify_autonomous_company_machine_v2.py
run continuous_operations \
  "$PYTHON_BIN" scripts/verify_continuous_company_operations_v1.py
run governed_channels \
  "$PYTHON_BIN" scripts/verify_governed_channel_runtime_v1.py
run commercial_fabric \
  "$PYTHON_BIN" scripts/verify_commercial_execution_fabric_v2.py
run focused_tests \
  "$PYTHON_BIN" -m pytest -q \
    tests/test_end_to_end_company_acceptance_v1.py \
    tests/test_ai_workforce_canonical_delegation.py \
    tests/test_ai_workforce_revenue_factory_blueprint.py

if [[ "$(git -C "$ROOT" rev-parse HEAD)" != "$ACTUAL_SHA" || \
      -n "$(git -C "$ROOT" status --porcelain --untracked-files=normal)" ]]; then
  echo "DEALIX_E2E_ACCEPTANCE=BLOCKED_SOURCE_CHANGED_DURING_RUN"
  exit 6
fi

python_version="$($PYTHON_BIN --version 2>&1)"
created_at="$(date -u +%FT%TZ)"

cat > "$PROOF_ROOT/receipt.json" <<EOF_RECEIPT
{
  "schema": "dealix.end-to-end-company-acceptance-receipt.v1",
  "git_sha": "$ACTUAL_SHA",
  "created_at": "$created_at",
  "python": "$python_version",
  "result": "PASS",
  "authority_class": "L4_INTERNAL_VERIFICATION",
  "external_effects": "NONE_FAIL_CLOSED",
  "quarantine_scope": "TEST_ENV_IMPORTED_APPLICATION_ONLY",
  "deployed_production_verified": false,
  "tenant_isolation_verified": false,
  "agents": 5,
  "runtime_specialist_roles": 12,
  "revenue_factory_specialist_roles": 15,
  "automation_plays": 30,
  "systems": 12,
  "lifecycle_stages": 18,
  "founder_control": "TELEGRAM_OPENCLAW_E2E_RECEIPT_REQUIRED_SEPARATELY",
  "next_action": "independent_same_head_review_then_runtime_and_production_gates"
}
EOF_RECEIPT

sha256sum "$PROOF_ROOT/receipt.json" > "$PROOF_ROOT/receipt.sha256"

echo "DEALIX_E2E_ACCEPTANCE=PASS"
echo "git_sha=$ACTUAL_SHA"
echo "proof_root=$PROOF_ROOT"
cat "$PROOF_ROOT/receipt.json"
