#!/usr/bin/env bash
# Compliance + GTM gates before sector expansion or paid launch motion.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="$(command -v python3)"

cd "$ROOT"

echo "== Compliance/GTM: PDPL checklist artifact =="
PDPL="${ROOT}/docs/SECURITY_PDPL_CHECKLIST.md"
if [[ ! -f "$PDPL" ]]; then
  echo "Missing ${PDPL}" >&2
  exit 1
fi
echo "OK: ${PDPL}"

echo ""
echo "== Compliance/GTM: category expansion gates =="
bash "${ROOT}/scripts/run_pre_scale_gate_bundle.sh"

echo ""
echo "== Compliance/GTM: revenue_os gate (when pipeline/catalog changed) =="
bash "${ROOT}/scripts/verify_ceo_signal_readiness.sh" revenue_os

echo ""
echo "== Compliance/GTM: Phase 3 billing docs present =="
for doc in \
  "${ROOT}/docs/BILLING_MOYASAR_RUNBOOK.md" \
  "${ROOT}/docs/MOYASAR_LIVE_CUTOVER.md" \
  "${ROOT}/docs/DPA_PILOT_TEMPLATE.md"
do
  if [[ ! -f "$doc" ]]; then
    echo "Missing ${doc}" >&2
    exit 1
  fi
  echo "OK: $(basename "$doc")"
done

echo ""
echo "COMPLIANCE_GTM_GATE_BUNDLE: PASS"
echo "Reminder: Moyasar live keys only after MOYASAR_LIVE_CUTOVER checklist; no auto external sends."
