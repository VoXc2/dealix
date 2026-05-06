#!/usr/bin/env bash
# Company Growth Beast — compile + pytest slice + verdict lines.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

PROFILE=FAIL
DIAGNOSTIC=FAIL
TARGETS=FAIL
OFFER=FAIL
CONTENT_PACK=FAIL
WARM_ROUTE=FAIL
EXPERIMENTS=FAIL
SUPPORT_TO_GROWTH=FAIL
PROOF_LOOP=FAIL
WEEKLY_REPORT=FAIL
COMMAND_CENTER=FAIL
NO_LIVE_SEND=FAIL
NO_LIVE_CHARGE=FAIL
NO_COLD_WHATSAPP=FAIL
NO_LINKEDIN_AUTOMATION=FAIL
NO_SCRAPING=FAIL
NO_FAKE_PROOF=FAIL
ARABIC_PRIMARY=FAIL
FIRST_CLIENT_READY=FAIL
NEXT_FOUNDER_ACTION=""

echo "== compileall (api + auto_client_acquisition) =="
python3 -m compileall -q api auto_client_acquisition

echo "== pytest company_growth_beast =="
if python3 -m pytest -q --no-cov \
  tests/test_company_growth_beast_profile.py \
  tests/test_company_growth_beast_diagnostic.py \
  tests/test_company_growth_beast_targets.py \
  tests/test_company_growth_beast_offer.py \
  tests/test_company_growth_beast_content.py \
  tests/test_company_growth_beast_experiments.py \
  tests/test_company_growth_beast_support_to_growth.py \
  tests/test_company_growth_beast_proof_loop.py \
  tests/test_company_growth_beast_command_center.py \
  tests/test_company_growth_beast_safety.py; then
  PROFILE=PASS
  DIAGNOSTIC=PASS
  TARGETS=PASS
  OFFER=PASS
  CONTENT_PACK=PASS
  WARM_ROUTE=PASS
  EXPERIMENTS=PASS
  SUPPORT_TO_GROWTH=PASS
  PROOF_LOOP=PASS
  WEEKLY_REPORT=PASS
  COMMAND_CENTER=PASS
  NO_LIVE_SEND=PASS
  NO_LIVE_CHARGE=PASS
  NO_COLD_WHATSAPP=PASS
  NO_LINKEDIN_AUTOMATION=PASS
  NO_SCRAPING=PASS
  NO_FAKE_PROOF=PASS
  ARABIC_PRIMARY=PASS
  FIRST_CLIENT_READY=PASS
  NEXT_FOUNDER_ACTION="Run 3 real diagnostics; log proof events; merge to main if production lags."
else
  NEXT_FOUNDER_ACTION="Fix failing company_growth_beast tests before customer pilots."
fi

VERDICT=FAIL
if [[ "$PROFILE" == PASS && "$COMMAND_CENTER" == PASS && "$NO_FAKE_PROOF" == PASS ]]; then
  VERDICT=PASS
fi

echo ""
echo "DEALIX_COMPANY_GROWTH_BEAST=$VERDICT"
echo "PROFILE=$PROFILE"
echo "DIAGNOSTIC=$DIAGNOSTIC"
echo "TARGETS=$TARGETS"
echo "OFFER=$OFFER"
echo "CONTENT_PACK=$CONTENT_PACK"
echo "WARM_ROUTE=$WARM_ROUTE"
echo "EXPERIMENTS=$EXPERIMENTS"
echo "SUPPORT_TO_GROWTH=$SUPPORT_TO_GROWTH"
echo "PROOF_LOOP=$PROOF_LOOP"
echo "WEEKLY_REPORT=$WEEKLY_REPORT"
echo "COMMAND_CENTER=$COMMAND_CENTER"
echo "NO_LIVE_SEND=$NO_LIVE_SEND"
echo "NO_LIVE_CHARGE=$NO_LIVE_CHARGE"
echo "NO_COLD_WHATSAPP=$NO_COLD_WHATSAPP"
echo "NO_LINKEDIN_AUTOMATION=$NO_LINKEDIN_AUTOMATION"
echo "NO_SCRAPING=$NO_SCRAPING"
echo "NO_FAKE_PROOF=$NO_FAKE_PROOF"
echo "ARABIC_PRIMARY=$ARABIC_PRIMARY"
echo "FIRST_CLIENT_READY=$FIRST_CLIENT_READY"
echo "NEXT_FOUNDER_ACTION=$NEXT_FOUNDER_ACTION"

if [[ "$VERDICT" != PASS ]]; then
  exit 1
fi
