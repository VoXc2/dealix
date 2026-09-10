#!/usr/bin/env bash
set -uo pipefail
cd "$(dirname "$0")/.."
ok=true
fail(){ echo "FAIL: $1"; ok=false; }
pass(){ echo "PASS: $1"; }
PORTAL=landing/customer-portal.html
ECC=landing/executive-command-center.html
[ -f "$PORTAL" ] || fail "customer-portal.html missing"
[ -f "$ECC" ] || fail "executive-command-center.html missing"
if grep -q 'DEALIX_RETIRED_PUBLIC_SURFACE' "$PORTAL" && grep -q 'noindex,nofollow' "$PORTAL" && grep -q 'url=/proof.html' "$PORTAL" && grep -qi 'synthetic' "$PORTAL"; then pass "customer portal retirement boundary"; else fail "customer portal retirement boundary invalid"; fi
if grep -q 'dir="rtl"' "$ECC" && grep -qE '[A-Za-z]{4}' "$ECC"; then pass "executive command center bilingual surface"; else fail "executive command center language contract"; fi
if grep -q 'enriched_view' docs/INTEGRATION_CONTRACT_MAP.md 2>/dev/null; then pass "enriched_view contract documented"; else fail "enriched_view contract missing"; fi
if $ok; then echo; echo CUSTOMER_EXPERIENCE_AUDIT=PASS; exit 0; fi
echo; echo CUSTOMER_EXPERIENCE_AUDIT=FAIL; exit 1
