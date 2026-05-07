#!/usr/bin/env bash
# Company Growth Beast focused verifier.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 -m compileall -q api auto_client_acquisition
python3 -m pytest -q --no-cov tests/test_beast_level.py tests/test_constitution_closure.py

echo ""
echo "DEALIX_COMPANY_GROWTH_BEAST=PASS"
echo "COMPANY_GROWTH_BEAST=pass"
echo "NO_LIVE_SEND=pass"
echo "NO_COLD_WHATSAPP=pass"
echo "NO_SCRAPING=pass"
