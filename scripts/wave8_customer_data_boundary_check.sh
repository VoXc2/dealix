#!/usr/bin/env bash
# Wave 8 §4 — Customer Data Boundary Check
# Verifies that customer data patterns are properly gitignored
# and no PII files are tracked in git.
# Usage: bash scripts/wave8_customer_data_boundary_check.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0
FAIL=0

echo ""
echo "=== Wave 8 — Customer Data Boundary Check ==="
echo ""

check() {
    local label="$1"
    local result="$2"
    if [ "$result" = "PASS" ]; then
        echo "  ✅ PASS  $label"
        PASS=$((PASS + 1))
    else
        echo "  ❌ FAIL  $label — $result"
        FAIL=$((FAIL + 1))
    fi
}

# 1. Check data/customers/** is gitignored
cd "$REPO_ROOT"
if git check-ignore -q "data/customers/test-handle/test.txt" 2>/dev/null; then
    check "data/customers/** is gitignored" "PASS"
else
    check "data/customers/** is gitignored" "Pattern not found in .gitignore"
fi

# 2. Check no real customer data tracked in git
TRACKED_CUSTOMER=$(git ls-files "data/customers/" 2>/dev/null | grep -v "^$" | head -1 || true)
if [ -z "$TRACKED_CUSTOMER" ]; then
    check "No customer data tracked in git" "PASS"
else
    check "No customer data tracked in git" "Found tracked: $TRACKED_CUSTOMER"
fi

# 3. Check .env is gitignored
if git check-ignore -q ".env" 2>/dev/null; then
    check ".env is gitignored" "PASS"
else
    check ".env is gitignored" ".env not in .gitignore"
fi

# 4. Check no .env committed
TRACKED_ENV=$(git ls-files ".env" 2>/dev/null || true)
if [ -z "$TRACKED_ENV" ]; then
    check ".env not committed to git" "PASS"
else
    check ".env not committed to git" "CRITICAL: .env is tracked!"
fi

# 5. Check proof-events JSONL is gitignored
if git check-ignore -q "docs/proof-events/test.jsonl" 2>/dev/null; then
    check "docs/proof-events/*.jsonl is gitignored" "PASS"
else
    check "docs/proof-events/*.jsonl is gitignored" "Pattern not found"
fi

# 6. Check no real secrets pattern in tracked Python files (basic scan)
SECRET_HITS=$(git ls-files "*.py" | xargs grep -l "sk_live_\|sk-ant-api\|Bearer [A-Za-z0-9]\{20,\}" 2>/dev/null | head -3 || true)
if [ -z "$SECRET_HITS" ]; then
    check "No hardcoded secrets in tracked .py files" "PASS"
else
    check "No hardcoded secrets in tracked .py files" "REVIEW: $SECRET_HITS"
fi

# 7. Check data boundary doc exists
if [ -f "$REPO_ROOT/docs/WAVE8_CUSTOMER_DATA_BOUNDARY.md" ]; then
    check "WAVE8_CUSTOMER_DATA_BOUNDARY.md exists" "PASS"
else
    check "WAVE8_CUSTOMER_DATA_BOUNDARY.md exists" "File missing"
fi

# 8. Check onboarding wizard respects data directory gitignore
if grep -q "data/customers/\*\*" "$REPO_ROOT/.gitignore" 2>/dev/null; then
    check "data/customers/** in .gitignore" "PASS"
else
    check "data/customers/** in .gitignore" "Pattern missing from .gitignore"
fi

echo ""
echo "─────────────────────────────────────────────"
echo "  PASS: $PASS  |  FAIL: $FAIL"
if [ "$FAIL" -eq 0 ]; then
    echo "  ✅ DATA_BOUNDARY: ALL_PASS"
else
    echo "  ❌ DATA_BOUNDARY: FAIL ($FAIL failures)"
fi
echo ""
exit $FAIL
