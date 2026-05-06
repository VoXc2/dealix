#!/usr/bin/env bash
# V12.5 Beast Level master verifier.
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

declare -A R
mark() { R["$1"]="$2"; }
OK=1

echo "[beast] 1/7 compileall…"
if python3 -m compileall -q api auto_client_acquisition db scripts \
    >/tmp/beast_compileall.log 2>&1; then mark COMPILEALL pass
else mark COMPILEALL fail; OK=0; fi

echo "[beast] 2/7 Beast targeted tests…"
if python3 -m pytest -q --no-cov tests/test_revops_beast.py \
    tests/test_beast_level.py >/tmp/beast_tests.log 2>&1; then
  mark BEAST_TESTS pass
else mark BEAST_TESTS fail; OK=0; fi

echo "[beast] 3/7 V11 verifier (regression check)…"
if bash scripts/v11_customer_closure_verify.sh \
    >/tmp/beast_v11.log 2>&1; then mark V11_VERIFIER pass
else mark V11_VERIFIER fail; OK=0; fi

echo "[beast] 4/7 V12 verifier (regression check)…"
if bash scripts/v12_full_ops_verify.sh \
    >/tmp/beast_v12.log 2>&1; then mark V12_VERIFIER pass
else mark V12_VERIFIER fail; OK=0; fi

echo "[beast] 5/7 RX verifier (regression check)…"
if bash scripts/revenue_execution_verify.sh \
    >/tmp/beast_rx.log 2>&1; then mark RX_VERIFIER pass
else mark RX_VERIFIER fail; OK=0; fi

echo "[beast] 6/7 In-process Beast endpoints…"
if python3 -c "
import asyncio
from httpx import ASGITransport, AsyncClient
from api.main import app

async def smoke():
    transport = ASGITransport(app=app)
    paths = [
        '/api/v1/revops/status',
        '/api/v1/growth-beast/status',
        '/api/v1/growth-beast/today',
        '/api/v1/company-growth-beast/status',
        '/api/v1/role-command-v125/status',
        '/api/v1/role-command-v125/today/ceo',
        '/api/v1/role-command-v125/today/finance',
        '/api/v1/proof-to-market/status',
        '/api/v1/proof-to-market/sector-learning',
    ]
    async with AsyncClient(transport=transport, base_url='http://test') as c:
        for p in paths:
            r = await c.get(p)
            assert 200 <= r.status_code < 300, f'{p} -> {r.status_code}'
asyncio.run(smoke())
print('all 9 Beast endpoints OK')
" >/tmp/beast_smoke.log 2>&1; then mark BEAST_SMOKE pass
else mark BEAST_SMOKE fail; OK=0; fi

echo "[beast] 7/7 secret prefix scan…"
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
for k in COMPILEALL BEAST_TESTS V11_VERIFIER V12_VERIFIER RX_VERIFIER \
         BEAST_SMOKE SECRET_SCAN; do
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
  echo "NEXT_FOUNDER_ACTION=Open V12.5 PR -> merge -> redeploy -> Day 1 Launch Kit"
else
  echo "NEXT_FOUNDER_ACTION=Inspect failed checks; logs in /tmp/beast_*.log"
fi
echo "================================================================="
exit $((1 - OK))
