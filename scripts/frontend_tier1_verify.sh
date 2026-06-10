#!/usr/bin/env bash
# Frontend Tier-1 verification — Revenue Command Center redesign (May 2026).
#
# Greps the static HTML in landing/ to confirm the Tier-1 contract holds:
# repositioned hero, simplified nav, WhatsApp Decision Layer, anchor pricing,
# L1-L5 proof ladder, 8 hard gates, agency-partner page, redirect from
# partners.html, footer trust badges, no internal terms, no forbidden tokens.
#
# Prints PASS|FAIL per layer + a final DEALIX_FRONTEND_TIER1_VERDICT line.
# Exit 0 if all PASS, 1 if any FAIL.
#
# Usage:
#   bash scripts/frontend_tier1_verify.sh
#   bash scripts/frontend_tier1_verify.sh --quiet   # suppress per-line output

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

# Helper: assert pattern present in file.
check_present() {
  local key="$1" file="$2" pattern="$3"
  if grep -qE "$pattern" "$LANDING/$file" 2>/dev/null; then
    emit "$key" PASS
  else
    emit "$key" FAIL "missing in $file: $pattern"
  fi
}

# Helper: assert pattern absent from file.
check_absent() {
  local key="$1" file="$2" pattern="$3"
  if grep -qE "$pattern" "$LANDING/$file" 2>/dev/null; then
    emit "$key" FAIL "unexpected in $file: $pattern"
  else
    emit "$key" PASS
  fi
}

# 1. Hero H1 word count <= 8 (Tier-1 benchmark)
# H1 may span multiple lines; capture between class="hero__title" opening tag
# and the next </h1>.
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

# 2. Single primary CTA in hero CTAs block (links to /diagnostic.html)
HERO_CTAS=$(awk '/<div class="hero__ctas"/,/<\/div>/' "$LANDING/index.html")
PRIMARY_COUNT=$(echo "$HERO_CTAS" | grep -cE 'btn--primary')
DIAG_TARGET=$(echo "$HERO_CTAS" | grep -cE 'href="/diagnostic\.html"[^>]*btn--primary|btn--primary[^>]*href="/diagnostic\.html"|href="/diagnostic\.html"[^>]*btn[^"]*--primary')
# more lenient: a single link with btn--primary AND href=/diagnostic.html
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
# Strip the mega-menu panel before counting
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

# 8. Pricing 6 tiers
PLAN_COUNT=$(grep -cE '<div class="plan(\s[^"]*)?"' "$LANDING/pricing.html")
if (( PLAN_COUNT >= 6 )); then
  emit "PRICING_6_TIERS" PASS "$PLAN_COUNT .plan cards"
else
  emit "PRICING_6_TIERS" FAIL "$PLAN_COUNT .plan cards (<6)"
fi

# 9. Pricing partner-tier first (anchor pricing)
FIRST_PLAN=$(awk '/<div class="plans">/,/<!-- Negation/' "$LANDING/pricing.html" | grep -A 30 '<div class="plan' | head -30)
if echo "$FIRST_PLAN" | grep -qE 'Executive Command Center|12,000|Partner'; then
  emit "PRICING_PARTNER_FIRST" PASS
else
  emit "PRICING_PARTNER_FIRST" FAIL "first .plan card should be top-tier (Partner / Executive Command Center / 12,000)"
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

# 11. Agency Partner page exists
if [[ -f "$LANDING/agency-partner.html" ]]; then
  emit "AGENCY_PARTNER_EXISTS" PASS
else
  emit "AGENCY_PARTNER_EXISTS" FAIL "landing/agency-partner.html missing"
fi

# 12. Partners redirect
if grep -q 'http-equiv="refresh"' "$LANDING/partners.html" && \
   grep -q '/agency-partner.html' "$LANDING/partners.html"; then
  emit "PARTNERS_REDIRECT" PASS
else
  emit "PARTNERS_REDIRECT" FAIL "partners.html should be a meta-refresh redirect to /agency-partner.html"
fi

# 13. Sitemaps updated
if grep -q "/agency-partner.html" "$LANDING/sitemap.xml" && \
   grep -q "/agency-partner.html" "$LANDING/sitemap_dealix.xml"; then
  emit "SITEMAP_UPDATED" PASS
else
  emit "SITEMAP_UPDATED" FAIL "one or both sitemap files missing /agency-partner.html"
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

# 15. Footer trust badges on Tier-1 pages
TIER1_PAGES=(agency-partner.html trust-center.html)
BADGE_FAIL=""
for P in "${TIER1_PAGES[@]}"; do
  for BADGE in "Saudi-PDPL" "Approval-first" "Proof-backed"; do
    if ! grep -q "$BADGE" "$LANDING/$P"; then
      BADGE_FAIL="$BADGE_FAIL $P:$BADGE"
    fi
  done
done
if [[ -z "$BADGE_FAIL" ]]; then
  emit "FOOTER_TRUST_BADGES" PASS
else
  emit "FOOTER_TRUST_BADGES" FAIL "missing:$BADGE_FAIL"
fi

# 16. RTL lang/dir on all Tier-1 pages
RTL_FAIL=""
for P in index.html customer-portal.html pricing.html proof.html trust-center.html diagnostic.html agency-partner.html; do
  if ! grep -qE 'lang="ar"\s+dir="rtl"' "$LANDING/$P"; then
    RTL_FAIL="$RTL_FAIL $P"
  fi
done
if [[ -z "$RTL_FAIL" ]]; then
  emit "RTL_LANG_DIR" PASS
else
  emit "RTL_LANG_DIR" FAIL "missing lang/dir:$RTL_FAIL"
fi

# 17. No internal terms in user-visible copy (excludes legitimate hrefs +
# script API paths, which test_frontend_professional_polish allows).
INTERNAL_TERMS="(\bv1[0-2]\b|growth_beast|stacktrace)"
INTERNAL_FAIL=""
for P in index.html customer-portal.html pricing.html proof.html trust-center.html agency-partner.html; do
  # Strip <script>...</script> blocks and href="..." attribute values, then scan
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

# 19. Mobile tap targets — design-system.css has min-height 44px on .ds-wadl__chip
if grep -qE "min-height:\s*44px" "$LANDING/assets/css/design-system.css"; then
  emit "MOBILE_TAP_TARGETS" PASS
else
  emit "MOBILE_TAP_TARGETS" FAIL "44px min-height not declared in design-system.css"
fi

# 20. No forbidden tokens (delegated to pytest test) — just sanity-grep here
FORBIDDEN_FAIL=""
# Each forbidden token is allowed only in its allowlisted file (per pytest).
# This shell check only flags egregious leaks. Real authority is pytest.
PUBLIC_PAGES=(index.html agency-partner.html trust-center.html pricing.html proof.html customer-portal.html diagnostic.html)
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

# Final verdict
if (( FAILS == 0 )); then
  VERDICT="PASS"
elif (( FAILS <= 3 )); then
  VERDICT="PARTIAL"
else
  VERDICT="FAIL"
fi
emit "DEALIX_FRONTEND_TIER1_VERDICT" "$VERDICT" "$FAILS check(s) failed"

# Output
if (( QUIET == 0 )); then
  printf '%s\n' "${OUTPUT[@]}"
fi

if [[ "$VERDICT" == "PASS" ]]; then
  exit 0
else
  exit 1
fi
