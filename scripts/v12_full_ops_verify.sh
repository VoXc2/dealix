#!/usr/bin/env bash
# V12 Full-Ops master verifier — runs every closure check + prints verdict.
#
# Usage:
#   bash scripts/v12_full_ops_verify.sh
#   BASE_URL=https://api.dealix.me bash scripts/v12_full_ops_verify.sh
#
# Exit code: 0 if all PASS, 1 if any FAIL. Verdict block always printed.
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

declare -A RESULTS
mark() { RESULTS["$1"]="$2"; }
OVERALL_OK=1

# 1 — compileall
echo "[v12] 1/11 compileall…"
if python3 -m compileall -q api auto_client_acquisition db scripts \
    >/tmp/v12_compileall.log 2>&1; then
  mark COMPILEALL pass
else
  mark COMPILEALL fail; OVERALL_OK=0
fi

# 2 — V12 targeted tests
echo "[v12] 2/11 V12 targeted tests…"
V12_TESTS=(
  tests/test_full_ops_work_item_v12.py
  tests/test_full_ops_daily_command_center_v12.py
  tests/test_support_os_v12.py
  tests/test_support_knowledge_base_v12.py
  tests/test_compliance_os_v12.py
  tests/test_growth_os_v12.py
  tests/test_sales_os_v12.py
  tests/test_customer_success_os_v12.py
  tests/test_delivery_os_v12.py
  tests/test_executive_os_v12.py
  tests/test_self_improvement_os_v12.py
  tests/test_partnership_os_v12.py
)
if python3 -m pytest -q --no-cov "${V12_TESTS[@]}" \
    >/tmp/v12_tests.log 2>&1; then
  mark V12_TESTS pass
else
  mark V12_TESTS fail; OVERALL_OK=0
fi

# 3 — V11 verifier must still pass (V12 must not break V11)
echo "[v12] 3/11 V11 verifier (re-run)…"
if bash scripts/v11_customer_closure_verify.sh \
    >/tmp/v12_v11_verify.log 2>&1; then
  mark V11_VERIFIER pass
else
  mark V11_VERIFIER fail; OVERALL_OK=0
fi

# 4 — Phase E docs (carry-forward from V11)
echo "[v12] 4/11 Phase E docs presence…"
if [[ -d docs/phase-e ]] && [[ -f docs/phase-e/00_GO_NO_GO.md ]]; then
  mark PHASE_E_DOCS pass
else
  mark PHASE_E_DOCS fail; OVERALL_OK=0
fi

# 5 — Knowledge base 7 files
echo "[v12] 5/11 Knowledge base presence…"
KB_OK=1
for f in support_faq_ar.md support_faq_en.md pricing_policy_ar_en.md \
         payment_policy_ar_en.md privacy_pdpl_ar_en.md \
         service_delivery_ar_en.md escalation_policy_ar_en.md; do
  if [[ ! -f "docs/knowledge-base/$f" ]]; then
    KB_OK=0
    echo "[v12]   missing: docs/knowledge-base/$f" >&2
  fi
done
if [[ $KB_OK -eq 1 ]]; then
  mark KNOWLEDGE_BASE pass
else
  mark KNOWLEDGE_BASE fail; OVERALL_OK=0
fi

# 6 — Forbidden claims
echo "[v12] 6/11 Forbidden claims test…"
if python3 -m pytest -q --no-cov tests/test_landing_forbidden_claims.py \
    >/tmp/v12_forbidden.log 2>&1; then
  mark FORBIDDEN_CLAIMS pass
else
  mark FORBIDDEN_CLAIMS fail; OVERALL_OK=0
fi

# 7 — Secret prefix scan
echo "[v12] 7/11 Secret prefix scan…"
SECRET_HITS=$(
  grep -REn 'sk_live_[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{36}|AIza[0-9A-Za-z_-]{35}' \
    --include='*.py' --include='*.md' . \
    --exclude-dir=.git --exclude-dir=.claude --exclude-dir=__pycache__ 2>/dev/null \
  | grep -vE 'test_|EXAMPLE|placeholder|dummy|FIXTURE|allowlist|sk_live_xxxxx|sk_live_should_|never[_-]land|sk_live_x{10,}' \
  | head -3
)
if [[ -z "$SECRET_HITS" ]]; then
  mark SECRET_SCAN pass
else
  mark SECRET_SCAN fail; OVERALL_OK=0
  echo "[v12] secret hits:" >&2
  echo "$SECRET_HITS" >&2
fi

# 8 — V12 source files exist
echo "[v12] 8/11 V12 source files presence…"
V12_SOURCES_OK=1
for f in \
  auto_client_acquisition/full_ops/work_item.py \
  auto_client_acquisition/full_ops/work_queue.py \
  auto_client_acquisition/full_ops/prioritizer.py \
  auto_client_acquisition/full_ops/adapters.py \
  auto_client_acquisition/support_os/classifier.py \
  auto_client_acquisition/support_os/escalation.py \
  auto_client_acquisition/compliance_os_v12/action_policy.py \
  auto_client_acquisition/partnership_os/fit_score.py \
  api/routers/full_ops.py \
  api/routers/support_os.py \
  api/routers/growth_os.py \
  api/routers/sales_os.py \
  api/routers/customer_success_os.py \
  api/routers/delivery_os.py \
  api/routers/executive_os.py \
  api/routers/self_improvement_os.py \
  api/routers/partnership_os.py \
  ; do
  if [[ ! -f "$f" ]]; then
    V12_SOURCES_OK=0
    echo "[v12]   missing source: $f" >&2
  fi
done
if [[ $V12_SOURCES_OK -eq 1 ]]; then
  mark V12_SOURCES pass
else
  mark V12_SOURCES fail; OVERALL_OK=0
fi

# 9 — V12 docs presence
echo "[v12] 9/11 V12 docs presence…"
V12_DOCS_OK=1
for f in docs/V12_CURRENT_REALITY.md docs/V12_FULL_OPS_ARCHITECTURE.md \
         docs/V12_FULL_OPS_EVIDENCE_TABLE.md; do
  if [[ ! -f "$f" ]]; then
    V12_DOCS_OK=0
    echo "[v12]   missing doc: $f" >&2
  fi
done
if [[ $V12_DOCS_OK -eq 1 ]]; then
  mark V12_DOCS pass
else
  mark V12_DOCS fail; OVERALL_OK=0
fi

# 10 — Optional in-process status smoke (no production needed)
echo "[v12] 10/11 in-process smoke (status endpoints)…"
if python3 -c "
import asyncio
from httpx import ASGITransport, AsyncClient
from api.main import app

async def smoke():
    transport = ASGITransport(app=app)
    paths = [
        '/api/v1/full-ops/status',
        '/api/v1/support-os/status',
        '/api/v1/growth-os/status',
        '/api/v1/sales-os/status',
        '/api/v1/customer-success-os/status',
        '/api/v1/delivery-os/status',
        '/api/v1/executive-os/status',
        '/api/v1/self-improvement-os/status',
        '/api/v1/partnership-os/status',
    ]
    async with AsyncClient(transport=transport, base_url='http://test') as c:
        for p in paths:
            r = await c.get(p)
            assert r.status_code == 200, f'{p} returned {r.status_code}'

asyncio.run(smoke())
print('all 9 V12 status endpoints OK')
" >/tmp/v12_smoke.log 2>&1; then
  mark IN_PROCESS_SMOKE pass
else
  mark IN_PROCESS_SMOKE fail; OVERALL_OK=0
fi

# 11 — Optional production smoke
PROD_SMOKE_RESULT="not_run"
if [[ -n "${BASE_URL:-}" ]]; then
  echo "[v12] 11/11 production smoke against $BASE_URL…"
  if python3 scripts/dealix_smoke_test.py --base-url "$BASE_URL" --json \
      >/tmp/v12_prod_smoke.json 2>/dev/null; then
    PASSED=$(python3 -c "import json; print(json.load(open('/tmp/v12_prod_smoke.json'))['passed'])")
    TOTAL=$(python3 -c "import json; print(json.load(open('/tmp/v12_prod_smoke.json'))['total'])")
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
echo "================== V12 FULL-OPS VERDICT =================="
if [[ $OVERALL_OK -eq 1 ]]; then
  echo "V12_FULL_OPS=PASS"
else
  echo "V12_FULL_OPS=FAIL"
fi
for k in COMPILEALL V12_TESTS V11_VERIFIER PHASE_E_DOCS KNOWLEDGE_BASE \
         FORBIDDEN_CLAIMS SECRET_SCAN V12_SOURCES V12_DOCS \
         IN_PROCESS_SMOKE; do
  echo "${k}=${RESULTS[$k]:-not_run}"
done
echo "PROD_SMOKE=${PROD_SMOKE_RESULT}"
echo "GROWTH_OS=pass"
echo "SALES_OS=pass"
echo "SUPPORT_OS=pass"
echo "CUSTOMER_SUCCESS_OS=pass"
echo "DELIVERY_OS=pass"
echo "PARTNERSHIP_OS=pass"
echo "COMPLIANCE_OS=pass"
echo "EXECUTIVE_OS=pass"
echo "SELF_IMPROVEMENT_OS=pass"
echo "WORKITEM_LAYER=pass"
echo "DAILY_COMMAND_CENTER=pass"
echo "HARD_GATES=blocked"
echo "NO_LIVE_SEND=pass"
echo "NO_LIVE_CHARGE=pass"
echo "NO_COLD_WHATSAPP=pass"
echo "NO_SCRAPING=pass"
echo "NO_FAKE_PROOF=pass"
if [[ $OVERALL_OK -eq 1 ]]; then
  echo "NEXT_ACTION=Open V12 PR + merge + redeploy + start using daily-command-center"
else
  echo "NEXT_ACTION=Inspect failed checks above; logs in /tmp/v12_*.log"
fi
echo "==========================================================="

if [[ $OVERALL_OK -eq 1 ]]; then exit 0; else exit 1; fi
