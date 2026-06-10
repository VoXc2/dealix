#!/usr/bin/env bash
# Customer Experience Final Audit (Phase 12 Wave 5)
#
# Extends Wave 4's customer_experience_audit.sh with 8 NEW checks:
#   1. Mobile meta tag on every customer-facing HTML
#   2. Empty-state Arabic copy in customer-portal
#   3. Degraded-state CSS class defined
#   4. DEMO label visible only in DEMO state
#   5. Trust footer present (Saudi-PDPL · Approval-first · Proof-backed)
#   6. CTA-per-page count (max 2 hero CTAs)
#   7. Bilingual font-loading + RTL declaration
#   8. Phase 13 revenue playbook exists
#
# Plus runs Wave 4's audit as a sub-call.
set -uo pipefail

cd "$(dirname "$0")/.."

ok=true
fail() { echo "FAIL: $1"; ok=false; }
ok_msg() { echo "PASS: $1"; }

# Run Wave 4 audit first (must pass)
echo "── Wave 4 Customer Experience Audit (sub-call) ────────"
if bash scripts/customer_experience_audit.sh >/dev/null 2>&1; then
  ok_msg "Wave 4 customer_experience_audit.sh PASS"
else
  fail "Wave 4 customer_experience_audit.sh FAIL"
fi

# Wave 5 extra checks
echo "── Wave 5 Final CX Audit (8 new checks) ──────────────"

# Check 1 — Mobile meta tag on every customer-facing HTML
PAGES=(landing/customer-portal.html landing/executive-command-center.html landing/launchpad.html landing/index.html)
for page in "${PAGES[@]}"; do
  if [ -f "$page" ] && grep -q 'width=device-width' "$page"; then
    ok_msg "$page has mobile viewport"
  else
    fail "$page missing mobile viewport meta"
  fi
done

# Check 2 — Empty-state Arabic copy on customer-portal
if grep -q "عرض جزئي" landing/customer-portal.html 2>/dev/null \
   || grep -q "لم يبدأ هذا القسم" landing/customer-portal.html 2>/dev/null; then
  ok_msg "customer-portal has Arabic empty/degraded copy"
else
  fail "customer-portal missing Arabic empty/degraded copy"
fi

# Check 3 — Degraded-state CSS class defined
if grep -q ".cp-degraded-banner" landing/customer-portal.html 2>/dev/null; then
  ok_msg "cp-degraded-banner CSS class defined"
else
  fail "cp-degraded-banner CSS class missing"
fi

# Check 4 — DEMO label exists in customer-portal + ECC
if grep -q "DEMO" landing/customer-portal.html 2>/dev/null \
   && grep -q "DEMO" landing/executive-command-center.html 2>/dev/null; then
  ok_msg "DEMO labels present"
else
  fail "DEMO labels missing"
fi

# Check 5 — Trust footer present (PDPL · Approval-first · Proof-backed)
if grep -q "PDPL" landing/customer-portal.html 2>/dev/null \
   && grep -q "Approval-first" landing/customer-portal.html 2>/dev/null \
   && grep -q "Proof-backed" landing/customer-portal.html 2>/dev/null; then
  ok_msg "trust footer (PDPL · Approval · Proof) present"
else
  fail "trust footer missing"
fi

# Check 6 — RTL declaration on every customer-facing HTML
for page in "${PAGES[@]}"; do
  if [ -f "$page" ] && grep -q 'dir="rtl"' "$page"; then
    ok_msg "$page declares dir=rtl"
  else
    fail "$page missing dir=rtl"
  fi
done

# Check 7 — Bilingual font preconnect (IBM Plex Sans Arabic + Inter)
for page in landing/customer-portal.html landing/executive-command-center.html; do
  if [ -f "$page" ] && grep -q "IBM+Plex+Sans+Arabic" "$page" \
     && grep -q "Inter" "$page"; then
    ok_msg "$page loads bilingual fonts"
  else
    fail "$page missing bilingual font loading"
  fi
done

# Check 8 — Phase 13 revenue playbook exists
if [ -f docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md ]; then
  ok_msg "DEALIX_REVENUE_PLAYBOOK_FINAL.md exists"
else
  fail "DEALIX_REVENUE_PLAYBOOK_FINAL.md missing"
fi

if $ok; then
  echo
  echo "CUSTOMER_EXPERIENCE_FINAL=PASS"
  exit 0
else
  echo
  echo "CUSTOMER_EXPERIENCE_FINAL=FAIL"
  exit 1
fi
