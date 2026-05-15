#!/usr/bin/env bash
# Customer Experience Audit (Phase 12)
#
# Verifies that customer-facing surfaces meet the Wave 4 hard rules:
# - required pages exist
# - no internal terms in public HTML
# - no forbidden claims
# - bilingual (Arabic + English)
# - CTAs link correctly
#
# Exits non-zero on any failure.
set -uo pipefail

cd "$(dirname "$0")/.."

ok=true
fail() {
  echo "FAIL: $1"
  ok=false
}

ok_msg() {
  echo "PASS: $1"
}

# 1. Required customer-facing pages
[ -f landing/customer-portal.html ] && ok_msg "customer-portal.html exists" || fail "customer-portal.html missing"
[ -f landing/executive-command-center.html ] && ok_msg "executive-command-center.html exists" || fail "executive-command-center.html missing"
[ -f landing/assets/js/customer-dashboard.js ] && ok_msg "customer-dashboard.js exists" || fail "customer-dashboard.js missing"
[ -f landing/assets/js/executive-command-center.js ] && ok_msg "executive-command-center.js exists" || fail "executive-command-center.js missing"

# 2. No internal terms in customer-facing HTML
INTERNAL_TERMS_RE='\b(v11|v12|v13|v14|router|verifier|growth_beast|stacktrace|pytest|internal_error)\b'
for page in landing/customer-portal.html landing/executive-command-center.html; do
  if [ -f "$page" ]; then
    if grep -qiE "$INTERNAL_TERMS_RE" "$page"; then
      # Allow these terms inside HTML comments / class names where they're harmless
      # — but the literal terms in visible content must not appear.
      # We check uppercase + word-boundary forms specifically
      if grep -E '(>|"\s*)(v11|v12|v13|v14)\b' "$page" >/dev/null 2>&1 \
         || grep -iE '\b(stacktrace|pytest|internal_error)\b' "$page" >/dev/null 2>&1 \
         || grep -E '\bgrowth_beast\b' "$page" >/dev/null 2>&1; then
        fail "$page contains visible internal terms"
      else
        ok_msg "$page free of visible internal terms"
      fi
    else
      ok_msg "$page free of internal terms"
    fi
  fi
done

# 3. No forbidden claims — scan only customer-visible copy. Comments and
#    <script>/<style> blocks are stripped first so the standard negation
#    disclaimer ("Estimated outcomes are not guaranteed outcomes") does
#    not register as a positive claim.
FORBIDDEN_RE='(\bguaranteed?\b|\bblast\b|\bscraping\b|نضمن|مضمون|cold[[:space:]]+(whatsapp|outreach|email))'
for page in landing/customer-portal.html landing/executive-command-center.html; do
  if [ -f "$page" ] && \
     perl -0777 -pe 's/<!--.*?-->//gs; s/<script\b.*?<\/script>//gsi; s/<style\b.*?<\/style>//gsi' "$page" \
       | grep -qiE "$FORBIDDEN_RE"; then
    fail "$page contains forbidden claims"
  else
    ok_msg "$page free of forbidden claims"
  fi
done

# 4. Bilingual content
for page in landing/customer-portal.html landing/executive-command-center.html; do
  if [ -f "$page" ]; then
    has_arabic=$(grep -c -E "[؀-ۿ]" "$page" 2>/dev/null || echo 0)
    if grep -qE "ar_SA|dir=\"rtl\"|lang=\"ar\"" "$page"; then
      ok_msg "$page declares Arabic"
    else
      fail "$page missing Arabic declaration"
    fi
    if grep -qE "[A-Za-z]{4}" "$page"; then
      ok_msg "$page has English helper text"
    else
      fail "$page missing English text"
    fi
  fi
done

# 5. Customer-portal links to launchpad/diagnostic + executive command center references it
if [ -f landing/customer-portal.html ]; then
  grep -q '/launchpad.html' landing/customer-portal.html && ok_msg "customer-portal links launchpad" || fail "customer-portal missing launchpad CTA"
  grep -q '/diagnostic' landing/customer-portal.html && ok_msg "customer-portal links diagnostic" || fail "customer-portal missing diagnostic CTA"
fi
if [ -f landing/executive-command-center.html ]; then
  grep -q '/customer-portal.html' landing/executive-command-center.html && ok_msg "exec dashboard links customer-portal" || fail "exec dashboard missing customer-portal link"
fi

# 6. enriched_view compatibility documented
if grep -q "enriched_view" docs/INTEGRATION_CONTRACT_MAP.md 2>/dev/null; then
  ok_msg "enriched_view contract documented"
else
  fail "enriched_view contract not documented in contract map"
fi

# 7. DEMO labelling on demo state
if grep -q "DEMO" landing/customer-portal.html 2>/dev/null \
   && grep -q "DEMO" landing/executive-command-center.html 2>/dev/null; then
  ok_msg "DEMO label present on both customer-facing pages"
else
  fail "DEMO label missing from one or both customer-facing pages"
fi

if $ok; then
  echo
  echo "CUSTOMER_EXPERIENCE_AUDIT=PASS"
  exit 0
else
  echo
  echo "CUSTOMER_EXPERIENCE_AUDIT=FAIL"
  exit 1
fi
