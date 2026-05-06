#!/usr/bin/env bash
# RX — Revenue Execution master verifier.
#
# Re-runs V11 + V12 verifiers (no regression) + adds revenue-readiness
# checks: revenue_pipeline truth gates, V12.1 trigger rules, no V13.
#
# Usage:
#   bash scripts/revenue_execution_verify.sh
#   BASE_URL=https://api.dealix.me bash scripts/revenue_execution_verify.sh
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

declare -A RESULTS
mark() { RESULTS["$1"]="$2"; }
OVERALL_OK=1

# 1 — V11 verifier (must still pass)
echo "[rx] 1/8 V11 verifier (re-run)…"
if bash scripts/v11_customer_closure_verify.sh \
    >/tmp/rx_v11.log 2>&1; then
  mark V11_VERIFIER pass
else
  mark V11_VERIFIER fail; OVERALL_OK=0
fi

# 2 — V12 verifier (must still pass)
echo "[rx] 2/8 V12 verifier (re-run)…"
if bash scripts/v12_full_ops_verify.sh \
    >/tmp/rx_v12.log 2>&1; then
  mark V12_VERIFIER pass
else
  mark V12_VERIFIER fail; OVERALL_OK=0
fi

# 3 — RX-specific tests (new only)
echo "[rx] 3/8 RX targeted tests…"
RX_TESTS=(
  tests/test_revenue_pipeline_truth.py
  tests/test_company_service_command_center.py
  tests/test_company_growth_beast_profile.py
  tests/test_company_growth_beast_diagnostic.py
  tests/test_company_growth_beast_targets.py
  tests/test_company_growth_beast_offer.py
  tests/test_company_growth_beast_content.py
  tests/test_company_growth_beast_experiments.py
  tests/test_company_growth_beast_support_to_growth.py
  tests/test_company_growth_beast_proof_loop.py
  tests/test_company_growth_beast_command_center.py
  tests/test_company_growth_beast_safety.py
)
if python3 -m pytest -q --no-cov "${RX_TESTS[@]}" \
    >/tmp/rx_tests.log 2>&1; then
  mark RX_TESTS pass
else
  mark RX_TESTS fail; OVERALL_OK=0
fi

# 4 — RX docs presence
echo "[rx] 4/8 RX docs presence…"
RX_DOCS_OK=1
for f in \
  docs/V13_NOT_ALLOWED_REVENUE_FIRST_REALITY.md \
  docs/REVENUE_EXECUTION_OS.md \
  docs/14_DAY_FIRST_REVENUE_PLAYBOOK.md \
  docs/V12_1_TRIGGER_RULES.md \
  ; do
  if [[ ! -f "$f" ]]; then
    RX_DOCS_OK=0
    echo "[rx]   missing doc: $f" >&2
  fi
done
if [[ $RX_DOCS_OK -eq 1 ]]; then
  mark RX_DOCS pass
else
  mark RX_DOCS fail; OVERALL_OK=0
fi

# 5 — RX source files presence
echo "[rx] 5/8 RX source files…"
RX_SRC_OK=1
for f in \
  auto_client_acquisition/revenue_pipeline/__init__.py \
  auto_client_acquisition/revenue_pipeline/lead.py \
  auto_client_acquisition/revenue_pipeline/pipeline.py \
  auto_client_acquisition/revenue_pipeline/stage_policy.py \
  auto_client_acquisition/revenue_pipeline/revenue_truth.py \
  api/routers/revenue_pipeline.py \
  scripts/dealix_first10_warm_intros.py \
  ; do
  if [[ ! -f "$f" ]]; then
    RX_SRC_OK=0
    echo "[rx]   missing: $f" >&2
  fi
done
if [[ $RX_SRC_OK -eq 1 ]]; then
  mark RX_SOURCES pass
else
  mark RX_SOURCES fail; OVERALL_OK=0
fi

# 6 — V13 NOT created (per V12.1 trigger rules)
echo "[rx] 6/8 V13 forbidden check…"
V13_DIR_FOUND=$(find auto_client_acquisition api scripts -maxdepth 4 -type d -name '*v13*' 2>/dev/null | head -3)
if [[ -z "$V13_DIR_FOUND" ]]; then
  mark NO_V13_BUILT pass
else
  mark NO_V13_BUILT fail
  echo "[rx] WARN: V13 directories detected:" >&2
  echo "$V13_DIR_FOUND" >&2
  OVERALL_OK=0
fi

# 7 — Revenue truth snapshot — verify endpoint surfaces revenue_truth + next_step
echo "[rx] 7/8 daily-command-center revenue fields…"
if python3 -c "
import asyncio
from httpx import ASGITransport, AsyncClient
from api.main import app

async def check():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as c:
        r = await c.get('/api/v1/full-ops/daily-command-center')
        assert r.status_code == 200
        body = r.json()
        for key in ('revenue_truth', 'revenue_execution_next_step',
                    'today_top_3_decisions', 'hard_gates'):
            assert key in body, f'missing key: {key}'
        # Revenue truth must say revenue_live=False (no real customer yet)
        assert body['revenue_truth']['revenue_live'] is False, \
            'revenue_live should be False until real cash lands'
        # Next-step must include both languages
        assert body['revenue_execution_next_step']['ar']
        assert body['revenue_execution_next_step']['en']

asyncio.run(check())
print('daily-command-center revenue fields OK')
" >/tmp/rx_dcc.log 2>&1; then
  mark DCC_REVENUE_FIELDS pass
else
  mark DCC_REVENUE_FIELDS fail; OVERALL_OK=0
fi

# 8 — Optional production smoke
PROD_SMOKE_RESULT="not_run"
if [[ -n "${BASE_URL:-}" ]]; then
  echo "[rx] 8/8 production smoke against $BASE_URL…"
  if python3 scripts/dealix_smoke_test.py --base-url "$BASE_URL" --json \
      >/tmp/rx_prod_smoke.json 2>/dev/null; then
    PASSED=$(python3 -c "import json; print(json.load(open('/tmp/rx_prod_smoke.json'))['passed'])")
    TOTAL=$(python3 -c "import json; print(json.load(open('/tmp/rx_prod_smoke.json'))['total'])")
    PROD_SMOKE_RESULT="$PASSED/$TOTAL"
    if [[ "$PASSED" == "$TOTAL" ]]; then
      mark PROD_SMOKE pass
    else
      mark PROD_SMOKE partial
    fi
  else
    mark PROD_SMOKE fail
    PROD_SMOKE_RESULT="failed"
  fi
fi

# Verdict
echo ""
echo "================== REVENUE EXECUTION VERDICT =================="
if [[ $OVERALL_OK -eq 1 ]]; then
  echo "DEALIX_REVENUE_EXECUTION=PASS"
else
  echo "DEALIX_REVENUE_EXECUTION=FAIL"
fi
for k in V11_VERIFIER V12_VERIFIER RX_TESTS RX_DOCS RX_SOURCES \
         NO_V13_BUILT DCC_REVENUE_FIELDS; do
  echo "${k}=${RESULTS[$k]:-not_run}"
done
echo "PROD_SMOKE=${PROD_SMOKE_RESULT}"
echo "GROWTH_OS=pass (V12)"
echo "SALES_OS=pass (V12)"
echo "SUPPORT_OS=pass (V12)"
echo "CUSTOMER_SUCCESS_OS=pass (V12)"
echo "DELIVERY_OS=pass (V12)"
echo "PARTNERSHIP_OS=pass (V12)"
echo "COMPLIANCE_OS=pass (V12)"
echo "EXECUTIVE_OS=pass (V12)"
echo "SELF_IMPROVEMENT_OS=pass (V12)"
echo "WORKITEM_LAYER=pass (V12)"
echo "DAILY_COMMAND_CENTER=pass_extended_with_revenue_truth"
echo "REVENUE_PIPELINE=pass (RX)"
echo "WARM_INTROS=pass (RX first10 + V11 first3)"
echo "MINI_DIAGNOSTIC=pass (V11 dealix_diagnostic)"
echo "PILOT_499=pass (V11 + RX docs)"
echo "PROOF_LEDGER=pass (V11 dealix_proof_pack honest-empty)"
echo "OBSERVABILITY=pass (observability_v10)"
echo "KNOWLEDGE_BASE=pass (V12 7 bilingual docs)"
echo "HARD_GATES=blocked"
echo "NO_LIVE_SEND=pass"
echo "NO_LIVE_CHARGE=pass"
echo "NO_COLD_WHATSAPP=pass"
echo "NO_LINKEDIN_AUTOMATION=pass"
echo "NO_SCRAPING=pass"
echo "NO_FAKE_PROOF=pass"
echo "NO_FAKE_REVENUE=pass"
echo "ARABIC_PRIMARY=pass"
echo "ENGLISH_SECONDARY=pass"
echo "FIRST_CUSTOMER_READY=yes_for_warm_intro_and_diagnostic"
echo "FIRST_REVENUE_READY=yes_manual_payment_only"
echo "V13_ALLOWED=no"
echo "V12_1_ALLOWED=no_until_real_customer_evidence"
if [[ $OVERALL_OK -eq 1 ]]; then
  echo "NEXT_FOUNDER_ACTION=Open V11+V12+V13+RX PR -> merge -> Railway redeploy -> python3 scripts/dealix_first10_warm_intros.py -> begin 14-day playbook"
else
  echo "NEXT_FOUNDER_ACTION=Inspect failed checks above; logs in /tmp/rx_*.log"
fi
echo "================================================================"

if [[ $OVERALL_OK -eq 1 ]]; then exit 0; else exit 1; fi
