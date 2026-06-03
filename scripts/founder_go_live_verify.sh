#!/usr/bin/env bash
# Founder go-live verify — business NOW + golden chain + capability + truth matrix summary.
# Usage: bash scripts/founder_go_live_verify.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export APP_ENV=test

PYTHON_BIN="$(command -v python3 2>/dev/null || true)"
if [[ -z "${PYTHON_BIN}" ]] && command -v py >/dev/null 2>&1; then
  PYTHON_BIN="py -3"
fi
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "FOUNDER_GO_LIVE: FAIL — python3 not found"
  exit 1
fi
FAIL=0

echo "== Founder go-live: Business NOW =="
if bash "${ROOT}/scripts/run_business_now.sh"; then
  echo "  business_now: PASS"
else
  echo "  business_now: FAIL"
  FAIL=1
fi

echo ""
echo "== Founder go-live: golden chain =="
if pytest tests/test_revenue_os_golden_chain_smoke.py -q --no-cov; then
  echo "  golden_chain: PASS"
else
  echo "  golden_chain: FAIL"
  FAIL=1
fi

echo ""
echo "== Founder go-live: capability slice =="
if bash "${ROOT}/scripts/dealix_capability_verify.sh"; then
  echo "  capability: PASS"
else
  echo "  capability: FAIL (non-blocking for local dev)"
fi

echo ""
echo "== Founder go-live: commercial autopilot docs =="
COMM_FAIL=0
for f in \
  "docs/commercial/DEALIX_UNIFIED_REVENUE_ATLAS_AR.md" \
  "docs/commercial/DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md" \
  "docs/commercial/DEALIX_COMPANY_DAILY_AUTOPILOT_AR.md" \
  ".github/workflows/daily-revenue-machine.yml" \
  "scripts/run_founder_commercial_day.sh" \
  "scripts/generate_weekly_content_drafts.py"; do
  if [[ -f "${ROOT}/${f}" ]]; then
    echo "  ok: ${f}"
  else
    echo "  MISSING: ${f}"
    COMM_FAIL=1
  fi
done
if [[ "$COMM_FAIL" -ne 0 ]]; then
  FAIL=1
else
  echo "  commercial_docs: PASS"
fi

echo ""
echo "== Founder go-live: revenue_ops_autopilot import =="
if $PYTHON_BIN -c "from dealix.revenue_ops_autopilot.orchestrator import get_default_orchestrator; get_default_orchestrator()"; then
  echo "  orchestrator: PASS"
else
  echo "  orchestrator: FAIL"
  FAIL=1
fi

STORE="${ROOT}/var/revenue_ops_autopilot.json"
if [[ -f "$STORE" ]]; then
  echo "  war_room_store: present ($STORE)"
else
  echo "  war_room_store: absent (ok at cold start — seed via API or imports)"
fi

echo ""
echo "== Founder go-live: commercial soft launch =="
if $PYTHON_BIN "$ROOT/scripts/verify_commercial_launch_ready.py"; then
  echo "  commercial_launch: PASS"
else
  echo "  commercial_launch: FAIL"
  FAIL=1
fi

echo ""
echo "== Founder go-live: integration truth summary =="
$PYTHON_BIN -c "
from dealix.business_now.integration_truth import build_integration_truth_summary
s = build_integration_truth_summary()
c = s.get('counts') or {}
print('  overall_status:', s.get('overall_status'))
print('  counts: green=%s yellow=%s red=%s' % (c.get('green',0), c.get('yellow',0), c.get('red',0)))
print('  yaml:', s.get('source_yaml'))
print('  doc:', s.get('doc_matrix'))
" || FAIL=1

echo ""
if [[ "$FAIL" -eq 0 ]]; then
  echo "FOUNDER_GO_LIVE_VERDICT: PASS"
  echo "Next: bash scripts/run_founder_commercial_day.sh · docs/commercial/DEALIX_COMPANY_DAILY_AUTOPILOT_AR.md"
  exit 0
fi
echo "FOUNDER_GO_LIVE_VERDICT: FAIL"
exit 1
