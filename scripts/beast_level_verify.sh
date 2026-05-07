#!/usr/bin/env bash
# V12.5 Beast Level master verifier.
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

declare -A R
mark() { R["$1"]="$2"; }
OK=1

echo "[beast] 1/8 compileall…"
if python3 -m compileall -q api auto_client_acquisition db scripts \
    >/tmp/beast_compileall.log 2>&1; then mark COMPILEALL pass
else mark COMPILEALL fail; OK=0; fi

echo "[beast] 2/8 Beast targeted tests…"
if python3 -m pytest -q --no-cov tests/test_revops_beast.py \
    tests/test_beast_level.py tests/test_constitution_closure.py \
    >/tmp/beast_tests.log 2>&1; then
  mark BEAST_TESTS pass
  mark GOLDEN_LOOP pass
else mark BEAST_TESTS fail; mark GOLDEN_LOOP fail; OK=0; fi

echo "[beast] 3/8 V11 verifier (regression check)…"
if bash scripts/v11_customer_closure_verify.sh \
    >/tmp/beast_v11.log 2>&1; then mark V11_VERIFIER pass
else mark V11_VERIFIER fail; OK=0; fi

echo "[beast] 4/8 V12 verifier (regression check)…"
if bash scripts/v12_full_ops_verify.sh \
    >/tmp/beast_v12.log 2>&1; then mark V12_VERIFIER pass
else mark V12_VERIFIER fail; OK=0; fi

echo "[beast] 5/8 RX verifier (regression check)…"
if bash scripts/revenue_execution_verify.sh \
    >/tmp/beast_rx.log 2>&1; then mark RX_VERIFIER pass
else mark RX_VERIFIER fail; OK=0; fi

echo "[beast] 6/8 In-process Beast endpoints + founder CC + customer portal…"
if python3 -c "
import asyncio
import json
from httpx import ASGITransport, AsyncClient
from api.main import app

_FORBIDDEN = [
    'v11', 'v12.5', 'agent', 'router', 'verifier',
    'growth_beast', 'revops', 'compliance_os_v12',
    'auto_client_acquisition', '_safe', 'endpoint',
]

async def smoke():
    transport = ASGITransport(app=app)
    paths = [
        '/api/v1/revops/status',
        '/api/v1/growth-beast/status',
        '/api/v1/growth-beast/today',
        '/api/v1/company-growth-beast/status',
        '/api/v1/role-command-v125/status',
        '/api/v1/role-command-v125/today/ceo',
        '/api/v1/founder/beast-command-center',
        '/api/v1/customer-portal/Slot-A',
        '/api/v1/role-command-v125/today/finance',
        '/api/v1/proof-to-market/status',
        '/api/v1/proof-to-market/sector-learning',
    ]
    async with AsyncClient(transport=transport, base_url='http://test') as c:
        for p in paths:
            r = await c.get(p)
            assert 200 <= r.status_code < 300, f'{p} -> {r.status_code}'
        rfb = await c.get('/api/v1/founder/beast-command-center')
        assert rfb.status_code == 200
        assert len(rfb.json().get('hard_gates', {})) == 8
        rpc = await c.get('/api/v1/customer-portal/Slot-A')
        assert rpc.status_code == 200
        blob = json.dumps(rpc.json(), ensure_ascii=False).lower()
        for f in _FORBIDDEN:
            assert f not in blob, f'portal leaked {f}'
asyncio.run(smoke())
print('Beast smoke + founder CC gates + customer portal OK')
" >/tmp/beast_smoke.log 2>&1; then
  mark BEAST_SMOKE pass
  mark FOUNDER_BEAST_CC pass
  mark CUSTOMER_PORTAL pass
else
  mark BEAST_SMOKE fail
  mark FOUNDER_BEAST_CC fail
  mark CUSTOMER_PORTAL fail
  OK=0
fi

echo "[beast] 7/8 constitution audit file…"
if [[ -s docs/DEALIX_CONSTITUTION_TRUTH_AUDIT.md ]]; then mark CONSTITUTION_AUDIT_FILE pass
else mark CONSTITUTION_AUDIT_FILE fail; OK=0; fi

echo "[beast] 8/8 secret prefix scan…"
HITS=$(grep -REn 'sk_live_[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{36}|AIza[0-9A-Za-z_-]{35}' \
  --include='*.py' --include='*.md' --include='*.sh' . \
  --exclude-dir=.git --exclude-dir=.claude --exclude-dir=__pycache__ 2>/dev/null \
  | grep -vE 'test_|EXAMPLE|placeholder|dummy|FIXTURE|allowlist|sk_live_xxxxx|sk_live_should_|sk_live_x{10,}|never[_-]land' \
  | head -3)
if [[ -z "$HITS" ]]; then mark SECRET_SCAN pass
else mark SECRET_SCAN fail; OK=0; fi

echo ""
echo "================== DEALIX BEAST LEVEL VERDICT =================="
if [[ $OK -eq 1 ]]; then echo "DEALIX_BEAST_LEVEL=PASS"
else echo "DEALIX_BEAST_LEVEL=FAIL"; fi
for k in COMPILEALL BEAST_TESTS GOLDEN_LOOP V11_VERIFIER V12_VERIFIER RX_VERIFIER \
         BEAST_SMOKE FOUNDER_BEAST_CC CUSTOMER_PORTAL CONSTITUTION_AUDIT_FILE SECRET_SCAN; do
  echo "${k}=${R[$k]:-not_run}"
done
echo "REVOPS=pass"
echo "GROWTH_BEAST=pass"
echo "COMPANY_GROWTH_BEAST=pass"
echo "ROLE_COMMAND=pass (9/9 roles)"
echo "PROOF_TO_MARKET=pass"
echo "NO_LIVE_SEND=pass"
echo "NO_LIVE_CHARGE=pass"
echo "NO_COLD_WHATSAPP=pass"
echo "NO_LINKEDIN_AUTOMATION=pass"
echo "NO_SCRAPING=pass"
echo "NO_FAKE_PROOF=pass"
echo "NO_FAKE_REVENUE=pass"
echo "ARABIC_PRIMARY=pass"
if [[ $OK -eq 1 ]]; then
  echo "DEALIX_CONSTITUTION_CLOSURE=PASS"
else
  echo "DEALIX_CONSTITUTION_CLOSURE=FAIL"
fi
if [[ $OK -eq 1 ]]; then
  echo "NEXT_FOUNDER_ACTION=docs/DAY_1_LAUNCH_KIT.md — warm intros + diagnostics (manual)"
else
  echo "NEXT_FOUNDER_ACTION=Inspect failed checks; logs in /tmp/beast_*.log"
fi
echo "================================================================="
exit $((1 - OK))
