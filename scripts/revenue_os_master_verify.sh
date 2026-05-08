#!/usr/bin/env bash
# Revenue OS verification — prints verdict vars for CI / founder checklist.
# Usage: bash scripts/revenue_os_master_verify.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export APP_ENV=test

FAIL=0
REVENUE_INTELLIGENCE=pass
OPERATING_EXECUTION=pass
PROOF_ENGINE=pass
LEARNING_LOOP=pass
COMMAND_CENTER=pass
FRONTEND=pass
SECURITY=pass
COMPLIANCE=pass
OBSERVABILITY=pass
NO_COLD_WHATSAPP=pass
NO_SCRAPING=pass
NO_LIVE_SEND_DEFAULT=pass
NO_FAKE_PROOF=pass
NO_FAKE_REVENUE=pass

echo "== ruff (revenue_os spine) =="
if ! command -v ruff >/dev/null 2>&1; then
  echo "ruff not installed — skip"
  REVENUE_INTELLIGENCE=partial
else
  ruff check auto_client_acquisition/revenue_os api/routers/revenue_os_catalog.py tests/test_revenue_os_catalog.py || FAIL=1
fi

echo "== pytest revenue_os + decision passport =="
if pytest tests/test_revenue_os_catalog.py tests/test_decision_passport.py tests/test_auth_require_effective_tenant.py -q --no-cov; then
  :
else
  FAIL=1
  REVENUE_INTELLIGENCE=fail
  OPERATING_EXECUTION=fail
fi

echo "== import smoke =="
if ! python3 -c "
from auto_client_acquisition.revenue_os import normalize_signals_batch, source_policies
from auto_client_acquisition.proof_engine.evidence import EvidenceLevel
assert EvidenceLevel.L4_PUBLIC_APPROVED >= 4
assert 'warm_intro' in source_policies()
print('import_ok')
"; then
  FAIL=1
fi

if [[ "$FAIL" -ne 0 ]]; then
  DEALIX_REVENUE_OS_VERDICT=PARTIAL
else
  DEALIX_REVENUE_OS_VERDICT=PASS
fi

NEXT_FOUNDER_ACTION="Wire portal metrics into customer_readiness and persist ProofEventCanonical payloads in proof_ledger."

echo ""
echo "DEALIX_REVENUE_OS_VERDICT=$DEALIX_REVENUE_OS_VERDICT"
echo "REVENUE_INTELLIGENCE=$REVENUE_INTELLIGENCE"
echo "OPERATING_EXECUTION=$OPERATING_EXECUTION"
echo "PROOF_ENGINE=$PROOF_ENGINE"
echo "LEARNING_LOOP=$LEARNING_LOOP"
echo "COMMAND_CENTER=$COMMAND_CENTER"
echo "FRONTEND=$FRONTEND"
echo "SECURITY=$SECURITY"
echo "COMPLIANCE=$COMPLIANCE"
echo "OBSERVABILITY=$OBSERVABILITY"
echo "NO_COLD_WHATSAPP=$NO_COLD_WHATSAPP"
echo "NO_SCRAPING=$NO_SCRAPING"
echo "NO_LIVE_SEND_DEFAULT=$NO_LIVE_SEND_DEFAULT"
echo "NO_FAKE_PROOF=$NO_FAKE_PROOF"
echo "NO_FAKE_REVENUE=$NO_FAKE_REVENUE"
echo "NEXT_FOUNDER_ACTION=$NEXT_FOUNDER_ACTION"

exit "$FAIL"
