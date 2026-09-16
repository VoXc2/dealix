#!/usr/bin/env bash
set -euo pipefail

echo "=== Dealix Daily Start ==="
date

echo ""
echo "Git status"
git status --short

echo ""
echo "Latest commits"
git log --oneline -5

echo ""
echo "PR status"
gh pr status || true

echo ""
echo "Source/runtime release truth"
python3 scripts/ops/verify_selfhost_only_runtime.py || true
python3 scripts/ops/verify_selfhosted_production_plane.py || true

echo ""
echo "Production smoke via canonical API"
python3 scripts/check_openapi_contract.py || true

echo ""
echo "CEO Command Center"
test -f ops/daily/CEO_DAILY_COMMAND_CENTER.md && echo "OK"
