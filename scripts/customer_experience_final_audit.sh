#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$0")/.."
ok=true
fail(){ echo "FAIL: $1"; ok=false; }
pass(){ echo "PASS: $1"; }
if bash scripts/customer_experience_audit.sh >/dev/null 2>&1; then pass "current customer experience audit"; else fail "current customer experience audit"; fi
PORTAL=landing/customer-portal.html
if grep -q 'DEALIX_RETIRED_PUBLIC_SURFACE' "$PORTAL" && grep -q 'url=/proof.html' "$PORTAL"; then pass "retired portal stays fail closed"; else fail "retired portal drift"; fi
for page in landing/index.html landing/diagnostic.html landing/pricing.html landing/proof.html; do
  if [ -f "$page" ] && grep -q 'width=device-width' "$page" && grep -q 'dir="rtl"' "$page"; then pass "$page mobile RTL"; else fail "$page public surface contract"; fi
done
if [ -f docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md ]; then pass "revenue playbook exists"; else fail "revenue playbook missing"; fi
if $ok; then echo; echo CUSTOMER_EXPERIENCE_FINAL=PASS; exit 0; fi
echo; echo CUSTOMER_EXPERIENCE_FINAL=FAIL; exit 1
