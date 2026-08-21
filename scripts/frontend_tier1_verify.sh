#!/usr/bin/env bash
# Frontend Tier-1 verification — current quote-only first-launch contract.
#
# Greps the static HTML in landing/ to confirm the customer-facing product
# surfaces stay consistent with the canonical commercial authority: one
# Revenue + Proof + Command wedge, quote-only Pilot, hard-blocked checkout,
# approval/proof gates, and no retired fixed-price ladder.
#
# Prints PASS|FAIL per layer + a final DEALIX_FRONTEND_TIER1_VERDICT line.
# Exit 0 if all PASS, 1 if any FAIL.

set -u

QUIET=0
if [[ "${1:-}" == "--quiet" ]]; then
  QUIET=1
fi

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LANDING="$ROOT/landing"

FAILS=0
declare -a OUTPUT

emit() {
  local key="$1"
  local status="$2"
  local detail="${3:-}"
  if [[ "$status" == "FAIL" ]]; then
    FAILS=$((FAILS + 1))
  fi
  OUTPUT+=("$(printf '%s: %s' "$key" "$status")")
  if [[ -n "$detail" ]]; then
    OUTPUT+=("  └─ $detail")
  fi
}

check_present() {
  local key="$1" file="$2" pattern="$3"
  if grep -qE "$pattern" "$LANDING/$file" 2>/dev/null; then
    emit "$key" PASS
  else
    emit "$key" FAIL "missing in $file: $pattern"
  fi
}

# 1. Hero H1 word count <= 8
H1=$(awk '
  /<h1[^>]*class="hero__title"/{capture=1; next}
  capture && /<\/h1>/{capture=0; exit}
  capture{print}
' "$LANDING/index.html" | tr -d '\n' | sed -E 's/<[^>]+>//g; s/^[[:space:]]+//; s/[[:space:]]+$//')
if [[ -n "$H1" ]]; then
  WORDS=$(echo "$H1" | wc -w | tr -d ' ')
  if (( WORDS <= 8 )); then
    emit "HERO_H1_LE_8_WORDS" PASS "h1=\"$H1\" ($WORDS words)"
  else
    emit "HERO_H1_LE_8_WORDS" FAIL "h1=\"$H1\" has $WORDS words (>8)"
  fi
else
  emit "HERO_H1_LE_8_WORDS" FAIL "<h1 class=hero__title> not found"
fi

# 2. Single primary CTA in hero CTAs block
HERO_CTAS=$(awk '/<div class="hero__ctas"/,/<\/div>/' "$LANDING/index.html")
PRIMARY_COUNT=$(echo "$HERO_CTAS" | grep -cE 'btn--primary')
if (( PRIMARY_COUNT == 1 )); then
  if echo "$HERO_CTAS" | grep -E 'btn--primary' | grep -qE 'href="/diagnostic\.html"'; then
    emit "SINGLE_PRIMARY_CTA" PASS "/diagnostic.html"
  else
    emit "SINGLE_PRIMARY_CTA" FAIL "primary CTA does not target /diagnostic.html"
  fi
else
  emit "SINGLE_PRIMARY_CTA" FAIL "found $PRIMARY_COUNT primary buttons in hero (expected 1)"
fi

# 3. Nav primary links <= 7
NAV_BLOCK=$(awk '/<nav class="nav__links"/,/<\/nav>/' "$LANDING/index.html")
NAV_NO_PANEL=$(echo "$NAV_BLOCK" | awk '
  /<div class="ds-mega-menu__panel"/{skip=1}
  skip==0{print}
  /<\/div>\s*<\/div>/ && skip==1{skip=0}
')
NAV_LINKS=$(echo "$NAV_NO_PANEL" | grep -cE '<a\s+[^>]*href=')
if (( NAV_LINKS <= 7 )); then
  emit "NAV_LINKS_LE_7" PASS "$NAV_LINKS primary links"
else
  emit "NAV_LINKS_LE_7" FAIL "$NAV_LINKS primary links (>7)"
fi

# 4. WADL section present
check_present "WADL_SECTION_PRESENT" "index.html" 'id="wadl"'

# 5. WADL has DEMO label
WADL_BLOCK=$(awk '/id="wadl"/,/<\/section>/' "$LANDING/index.html")
if echo "$WADL_BLOCK" | grep -q "DEMO"; then
  emit "WADL_DEMO_LABEL" PASS
else
  emit "WADL_DEMO_LABEL" FAIL "DEMO label missing in WADL section"
fi

# 6. Customer portal: today-decision precedes ops-grid
TODAY_LINE=$(grep -nE 'id="today-decision"' "$LANDING/customer-portal.html" | head -1 | cut -d: -f1)
OPS_LINE=$(grep -nE 'id="ops-grid"' "$LANDING/customer-portal.html" | head -1 | cut -d: -f1)
if [[ -n "$TODAY_LINE" && -n "$OPS_LINE" && "$TODAY_LINE" -lt "$OPS_LINE" ]]; then
  emit "PORTAL_TODAY_DECISION_ABOVE_OPS" PASS "today-decision@$TODAY_LINE < ops-grid@$OPS_LINE"
else
  emit "PORTAL_TODAY_DECISION_ABOVE_OPS" FAIL "today-decision should precede ops-grid"
fi

# 7. Proof page L1-L5
MISSING_LEVELS=""
for L in L1 L2 L3 L4 L5; do
  if ! grep -q "$L" "$LANDING/proof.html"; then
    MISSING_LEVELS="$MISSING_LEVELS $L"
  fi
done
if [[ -z "$MISSING_LEVELS" ]]; then
  emit "PROOF_L1_TO_L5" PASS
else
  emit "PROOF_L1_TO_L5" FAIL "missing levels:$MISSING_LEVELS"
fi

# 8. Pricing exposes exactly the current quote-only launch path, not the retired ladder.
PRICING="$LANDING/pricing.html"
if grep -q "Free Mini Diagnostic" "$PRICING" \
  && grep -q "Revenue Command Pilot — 30 يومًا" "$PRICING" \
  && grep -q "Quote-only" "$PRICING" \
  && grep -q "Weekly Proof Pack" "$PRICING" \
  && grep -q "Final Proof Pack" "$PRICING"; then
  emit "PRICING_QUOTE_ONLY_PATH" PASS
else
  emit "PRICING_QUOTE_ONLY_PATH" FAIL "diagnostic / quote-only Pilot / proof path incomplete"
fi

if grep -qE '(^|[^0-9])(499|1500|2999|7999|12000)([^0-9]|$)|1,500|2,999|7,999|12,000|/checkout\.html\?tier=|SLA 99\.9%|price-lock' "$PRICING"; then
  emit "NO_RETIRED_PUBLIC_PRICING" FAIL "retired fixed-price/self-serve term found in pricing.html"
else
  emit "NO_RETIRED_PUBLIC_PRICING" PASS
fi

# 9. Checkout route is a hard-blocked information surface only.
CHECKOUT="$LANDING/checkout.html"
if grep -q "NO_LIVE_CHARGE" "$CHECKOUT" \
  && grep -q "QUOTE_ONLY" "$CHECKOUT" \
  && grep -q "NO_PUBLIC_FIXED_PRICE" "$CHECKOUT" \
  && grep -q "NO_SELF_SERVE_CHECKOUT" "$CHECKOUT" \
  && grep -q "REQUEST ≠ QUOTE ≠ INVOICE ≠ PAYMENT ≠ REVENUE" "$CHECKOUT"; then
  emit "CHECKOUT_FAIL_CLOSED" PASS
else
  emit "CHECKOUT_FAIL_CLOSED" FAIL "checkout fail-closed contract incomplete"
fi

if grep -qE '/api/v1/payment-ops/invoice-intent|TIERS=|<form|amount_sar|bank_transfer_manual|(^|[^0-9])(499|2999|7999|12000)([^0-9]|$)' "$CHECKOUT"; then
  emit "CHECKOUT_NO_PAYMENT_PATH" FAIL "payment/tier input path remains in checkout.html"
else
  emit "CHECKOUT_NO_PAYMENT_PATH" PASS
fi

# 10. Trust Center: all 8 hard gates
GATES=(NO_LIVE_SEND NO_LIVE_CHARGE NO_COLD_WHATSAPP NO_LINKEDIN_AUTOMATION NO_SCRAPING NO_FAKE_PROOF NO_FAKE_REVENUE NO_UNAPPROVED_TESTIMONIAL)
MISSING_GATES=""
for G in "${GATES[@]}"; do
  if ! grep -q "$G" "$LANDING/trust-center.html"; then
    MISSING_GATES="$MISSING_GATES $G"
  fi
done
if [[ -z "$MISSING_GATES" ]]; then
  emit "TRUST_CENTER_8_GATES" PASS
else
  emit "TRUST_CENTER_8_GATES" FAIL "missing gates:$MISSING_GATES"
fi

# 11. Services is a capability map under one product, not a parallel offer ladder.
SERVICES="$LANDING/services.html"
if grep -q "One Product" "$SERVICES" \
  && grep -q "Dealix منتج واحد" "$SERVICES" \
  && grep -q "Revenue + Proof + Command" "$SERVICES" \
  && grep -q "Company Brain + Business Graph" "$SERVICES" \
  && grep -q "Governed Execution" "$SERVICES"; then
  emit "SERVICES_ONE_PRODUCT" PASS
else
  emit "SERVICES_ONE_PRODUCT" FAIL "services.html is not a one-product capability map"
fi
if grep -qE 'سلّم العروض|Saudi Opportunity Snapshot|Revenue Proof Sprint|AI Company OS Setup|Partner & Distributor Desk|sami\.assiri11@gmail\.com' "$SERVICES"; then
  emit "NO_PARALLEL_PUBLIC_OFFERS" FAIL "retired offer ladder or personal contact remains in services.html"
else
  emit "NO_PARALLEL_PUBLIC_OFFERS" PASS
fi

# 12. Robots protects historical/operating surfaces and points at dealix.me only.
ROBOTS="$LANDING/robots.txt"
if grep -q 'Sitemap: https://dealix.me/sitemap.xml' "$ROBOTS" \
  && grep -q 'Sitemap: https://dealix.me/sitemap_dealix.xml' "$ROBOTS" \
  && grep -q 'Disallow: /checkout.html' "$ROBOTS" \
  && grep -q 'Disallow: /annual-pricing.html' "$ROBOTS" \
  && grep -q 'Disallow: /roi.html' "$ROBOTS" \
  && grep -q 'Disallow: /agency-partner.html' "$ROBOTS"; then
  emit "ROBOTS_CANONICAL_LAUNCH" PASS
else
  emit "ROBOTS_CANONICAL_LAUNCH" FAIL "robots.txt does not protect the canonical launch boundary"
fi
if grep -qE 'Sitemap: https://dealix\.(sa|ai)/' "$ROBOTS"; then
  emit "ROBOTS_NO_LEGACY_DOMAIN" FAIL "robots.txt still advertises a legacy domain"
else
  emit "ROBOTS_NO_LEGACY_DOMAIN" PASS
fi

# 13. Both compatibility sitemaps use dealix.me only and publish reviewed launch surfaces.
SITEMAP_FAIL=""
for MAP in sitemap.xml sitemap_dealix.xml; do
  for PATHNAME in / /diagnostic.html /pricing.html /services.html /proof.html /trust-center.html; do
    if ! grep -q "https://dealix.me${PATHNAME}" "$LANDING/$MAP"; then
      SITEMAP_FAIL="$SITEMAP_FAIL $MAP:$PATHNAME"
    fi
  done
  if grep -qE 'https://dealix\.(sa|ai)/' "$LANDING/$MAP"; then
    SITEMAP_FAIL="$SITEMAP_FAIL $MAP:legacy-domain"
  fi
done
if [[ -z "$SITEMAP_FAIL" ]]; then
  emit "CANONICAL_SITEMAPS" PASS
else
  emit "CANONICAL_SITEMAPS" FAIL "mismatch:$SITEMAP_FAIL"
fi

# 14. Anchor IDs preserved on homepage
ANCHORS=(pillars for-who sectors how trust proof pricing faq pilot)
MISSING_ANCHORS=""
for A in "${ANCHORS[@]}"; do
  if ! grep -q "id=\"$A\"" "$LANDING/index.html"; then
    MISSING_ANCHORS="$MISSING_ANCHORS #$A"
  fi
done
if [[ -z "$MISSING_ANCHORS" ]]; then
  emit "ANCHOR_IDS_PRESERVED" PASS
else
  emit "ANCHOR_IDS_PRESERVED" FAIL "removed anchors:$MISSING_ANCHORS"
fi

# 15. Trust Center carries a clear product identity and an explicit no-certification posture.
TRUST_BADGE_FAIL=""
for BADGE in "Saudi-first" "Approval-first" "Proof-backed"; do
  if ! grep -q "$BADGE" "$LANDING/trust-center.html"; then
    TRUST_BADGE_FAIL="$TRUST_BADGE_FAIL trust-center.html:$BADGE"
  fi
done
if ! grep -q "لا يدّعي PDPL certification" "$LANDING/trust-center.html"; then
  TRUST_BADGE_FAIL="$TRUST_BADGE_FAIL trust-center.html:no-PDPL-certification"
fi
if ! grep -q "SOC 2" "$LANDING/trust-center.html" || ! grep -q "Saudi data residency" "$LANDING/trust-center.html"; then
  TRUST_BADGE_FAIL="$TRUST_BADGE_FAIL trust-center.html:explicit-open-compliance-boundary"
fi
if [[ -z "$TRUST_BADGE_FAIL" ]]; then
  emit "TRUST_BADGES" PASS
else
  emit "TRUST_BADGES" FAIL "missing:$TRUST_BADGE_FAIL"
fi

# 16. RTL lang/dir on current Tier-1 public pages.
RTL_FAIL=""
for P in index.html services.html pricing.html proof.html trust-center.html diagnostic.html; do
  if ! grep -qE 'lang="ar"\s+dir="rtl"' "$LANDING/$P"; then
    RTL_FAIL="$RTL_FAIL $P"
  fi
done
if [[ -z "$RTL_FAIL" ]]; then
  emit "RTL_LANG_DIR" PASS
else
  emit "RTL_LANG_DIR" FAIL "missing lang/dir:$RTL_FAIL"
fi

# 17. No internal terms in current user-visible copy.
INTERNAL_TERMS="(\bv1[0-2]\b|growth_beast|stacktrace)"
INTERNAL_FAIL=""
for P in index.html services.html pricing.html proof.html trust-center.html diagnostic.html; do
  STRIPPED=$(sed -E 's/<script[^>]*>.*?<\/script>//g; s/href="[^"]*"//g' "$LANDING/$P")
  if echo "$STRIPPED" | grep -qiE "$INTERNAL_TERMS"; then
    INTERNAL_FAIL="$INTERNAL_FAIL $P"
  fi
done
if [[ -z "$INTERNAL_FAIL" ]]; then
  emit "NO_INTERNAL_TERMS" PASS "(strict polish rule covered by pytest)"
else
  emit "NO_INTERNAL_TERMS" FAIL "internal terms in:$INTERNAL_FAIL"
fi

# 18. DEMO labels on customer portal
if grep -q "src-pill" "$LANDING/customer-portal.html" && \
   grep -q "DEMO" "$LANDING/customer-portal.html"; then
  emit "DEMO_LABELS" PASS
else
  emit "DEMO_LABELS" FAIL "src-pill or DEMO marker missing on customer-portal"
fi

# 19. Mobile tap targets
if grep -qE "min-height:\s*44px" "$LANDING/assets/css/design-system.css"; then
  emit "MOBILE_TAP_TARGETS" PASS
else
  emit "MOBILE_TAP_TARGETS" FAIL "44px min-height not declared in design-system.css"
fi

# 20. No forbidden tokens on current launch surfaces.
FORBIDDEN_FAIL=""
PUBLIC_PAGES=(index.html services.html trust-center.html pricing.html proof.html diagnostic.html)
for P in "${PUBLIC_PAGES[@]}"; do
  if grep -qE '\bguarantee[d]?\b|\bblast\b' "$LANDING/$P"; then
    FORBIDDEN_FAIL="$FORBIDDEN_FAIL $P"
  fi
done
if [[ -z "$FORBIDDEN_FAIL" ]]; then
  emit "NO_FORBIDDEN_TOKENS_SHELL" PASS "(authoritative check: pytest tests/test_landing_forbidden_claims.py)"
else
  emit "NO_FORBIDDEN_TOKENS_SHELL" FAIL "leak detected in:$FORBIDDEN_FAIL"
fi

if (( FAILS == 0 )); then
  VERDICT="PASS"
elif (( FAILS <= 3 )); then
  VERDICT="PARTIAL"
else
  VERDICT="FAIL"
fi
emit "DEALIX_FRONTEND_TIER1_VERDICT" "$VERDICT" "$FAILS check(s) failed"

if (( QUIET == 0 )); then
  printf '%s\n' "${OUTPUT[@]}"
fi

if [[ "$VERDICT" == "PASS" ]]; then
  exit 0
else
  exit 1
fi
