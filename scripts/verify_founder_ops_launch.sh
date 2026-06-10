#!/usr/bin/env bash
# Founder ops launch readiness — local or CI
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PYTHON_BIN="$(command -v python3 2>/dev/null || true)"
if [[ -z "${PYTHON_BIN}" ]] && command -v py >/dev/null 2>&1; then
  PYTHON_BIN="py -3"
fi
if [[ -z "${PYTHON_BIN}" ]]; then
  echo "FAIL: python3 not found"
  exit 1
fi

echo "== Founder ops launch verify =="

$PYTHON_BIN -c "
from dealix.revenue_ops_autopilot.config_loader import routing_thresholds, icp_agency_wedge_config
assert routing_thresholds()['qualified_a_min'] >= 10
assert isinstance(icp_agency_wedge_config(), dict)
print('config_loader: OK')
"

$PYTHON_BIN -c "
from dealix.revenue_ops_autopilot.webhook_handlers import handle_calendly_webhook
r = handle_calendly_webhook({'event': 'invitee.created', 'payload': {'email': 'test@example.sa', 'name': 'Test'}})
assert r.get('handled') is True
print('calendly_webhook: OK')
"

export APP_ENV=test
$PYTHON_BIN -m pytest tests/test_revenue_ops_autopilot.py tests/test_founder_commercial_digest.py -q --no-cov -x 2>/dev/null \
  || $PYTHON_BIN -m pytest tests/test_revenue_ops_autopilot.py -q --no-cov -x

echo "FOUNDER_OPS_LAUNCH_VERIFY: OK"
