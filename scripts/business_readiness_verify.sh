#!/usr/bin/env bash
# =============================================================================
# Dealix Business Readiness Verifier
# PHASE 14 | Owner: Founder | Updated: 2026-05-07 v1.1
# =============================================================================
# Usage: bash scripts/business_readiness_verify.sh
# Purpose: Verify all business architecture docs exist and pass hard gates.
# v1.1: Added PDPL article check, KPI action-trigger check, SOP acceptance criteria check
# =============================================================================

set -euo pipefail

PASS=0
FAIL=0
WARN=0

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

pass() { echo -e "${GREEN}PASS${NC}  $1"; PASS=$((PASS+1)); }
fail() { echo -e "${RED}FAIL${NC}  $1"; FAIL=$((FAIL+1)); }
warn() { echo -e "${YELLOW}WARN${NC}  $1"; WARN=$((WARN+1)); }

echo "=============================================="
echo "DEALIX BUSINESS READINESS VERIFIER v1.0"
echo "Date: $(date '+%Y-%m-%d %H:%M')"
echo "=============================================="
echo ""

# =============================================================================
# SECTION 1: REQUIRED DOCS EXISTENCE
# =============================================================================
echo "--- SECTION 1: Required Business Docs ---"

REQUIRED_DOCS=(
  "docs/BUSINESS_REALITY_AUDIT.md"
  "docs/POSITIONING_AND_ICP.md"
  "docs/OFFER_LADDER_AND_PRICING.md"
  "docs/SALES_PLAYBOOK.md"
  "docs/PILOT_DELIVERY_SOP.md"
  "docs/PROOF_AND_CASE_STUDY_SYSTEM.md"
  "docs/UNIT_ECONOMICS_AND_MARGIN.md"
  "docs/CUSTOMER_SUCCESS_PLAYBOOK.md"
  "docs/AGENCY_PARTNER_PROGRAM.md"
  "docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md"
  "docs/MARKETING_AND_CONTENT_SYSTEM.md"
  "docs/90_DAY_BUSINESS_EXECUTION_PLAN.md"
  "docs/BUSINESS_KPI_DASHBOARD_SPEC.md"
  "docs/BUSINESS_READINESS_EVIDENCE_TABLE.md"
)

for doc in "${REQUIRED_DOCS[@]}"; do
  if [ -f "$doc" ]; then
    pass "EXISTS: $doc"
  else
    fail "MISSING: $doc"
  fi
done

echo ""

# =============================================================================
# SECTION 2: LEGACY DOCS (should still exist)
# =============================================================================
echo "--- SECTION 2: Legacy Core Docs ---"

LEGACY_DOCS=(
  "docs/DEALIX_OPERATING_CONSTITUTION.md"
  "docs/DPA_PILOT_TEMPLATE.md"
  "docs/BILLING_RUNBOOK.md"
)

for doc in "${LEGACY_DOCS[@]}"; do
  if [ -f "$doc" ]; then
    pass "EXISTS: $doc"
  else
    warn "MISSING (legacy): $doc"
  fi
done

echo ""

# =============================================================================
# SECTION 3: HARD GATE VIOLATIONS — NO_COLD_WHATSAPP
# =============================================================================
echo "--- SECTION 3: Hard Gate — NO_COLD_WHATSAPP ---"

# Check no file contains "cold whatsapp" enablement language (beyond policy docs)
COLD_WA=$(grep -rl "cold.*whatsapp\|whatsapp.*blast\|bulk.*whatsapp\|mass.*whatsapp" \
  --include="*.py" --include="*.js" --include="*.ts" --include="*.sh" \
  . 2>/dev/null | grep -v "DEALIX_OPERATING_CONSTITUTION\|business_readiness_verify" || true)

if [ -z "$COLD_WA" ]; then
  pass "NO_COLD_WHATSAPP: No code files enable cold WhatsApp"
else
  fail "NO_COLD_WHATSAPP VIOLATION in: $COLD_WA"
fi

echo ""

# =============================================================================
# SECTION 4: HARD GATE VIOLATIONS — NO_FAKE_PROOF
# =============================================================================
echo "--- SECTION 4: Hard Gate — NO_FAKE_PROOF ---"

FAKE_PROOF=$(grep -rl "fake.*proof\|mock.*testimonial\|synthetic.*case.study\|fabricat" \
  --include="*.py" --include="*.js" --include="*.ts" \
  . 2>/dev/null | grep -v "test_\|_test\|verify\|verif" || true)

if [ -z "$FAKE_PROOF" ]; then
  pass "NO_FAKE_PROOF: No code files generate fake proof"
else
  fail "NO_FAKE_PROOF VIOLATION in: $FAKE_PROOF"
fi

echo ""

# =============================================================================
# SECTION 5: HARD GATE VIOLATIONS — NO_GUARANTEED_CLAIMS
# =============================================================================
echo "--- SECTION 5: Hard Gate — NO_GUARANTEED_CLAIMS ---"

# Check landing pages for guaranteed claims
GUARANTEED=$(grep -rl "نضمن\|guaranteed.*result\|guarantee.*revenue\|100% guaranteed\|مضمون.*نتيجة" \
  landing/ 2>/dev/null || true)

if [ -z "$GUARANTEED" ]; then
  pass "NO_GUARANTEED_CLAIMS: No guaranteed claims in landing pages"
else
  fail "GUARANTEED_CLAIMS found in: $GUARANTEED"
fi

echo ""

# =============================================================================
# SECTION 6: HARD GATE VIOLATIONS — NO_SCRAPING
# =============================================================================
echo "--- SECTION 6: Hard Gate — NO_SCRAPING ---"

SCRAPING=$(grep -rl "auto_scrape\|linkedin_scrape\|scrape_contacts\|bulk_extract" \
  --include="*.py" --include="*.js" \
  . 2>/dev/null | grep -v "test_\|verify\|CONSTITUTION" || true)

if [ -z "$SCRAPING" ]; then
  pass "NO_SCRAPING: No scraping automation found in code"
else
  fail "SCRAPING VIOLATION in: $SCRAPING"
fi

echo ""

# =============================================================================
# SECTION 7: OFFER LADDER INTEGRITY
# =============================================================================
echo "--- SECTION 7: Offer Ladder Integrity ---"

if grep -q "499 SAR\|499SAR" docs/OFFER_LADDER_AND_PRICING.md 2>/dev/null; then
  pass "OFFER_LADDER: Sprint 499 SAR price present"
else
  fail "OFFER_LADDER: Sprint 499 SAR price missing"
fi

if grep -q "2,999\|2999" docs/OFFER_LADDER_AND_PRICING.md 2>/dev/null; then
  pass "OFFER_LADDER: Managed Ops 2999+ price present"
else
  fail "OFFER_LADDER: Managed Ops price missing"
fi

if grep -q "rev-share\|rev_share" docs/AGENCY_PARTNER_PROGRAM.md 2>/dev/null; then
  pass "AGENCY: Rev-share terms present"
else
  fail "AGENCY: Rev-share terms missing"
fi

echo ""

# =============================================================================
# SECTION 8: COMPLIANCE CHECKS
# =============================================================================
echo "--- SECTION 8: Compliance Readiness ---"

if grep -q "PDPL\|pdpl" docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md 2>/dev/null; then
  pass "COMPLIANCE: PDPL coverage in Trust Pack"
else
  fail "COMPLIANCE: PDPL not covered in Trust Pack"
fi

if grep -q "DPA\|dpa" docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md 2>/dev/null; then
  pass "COMPLIANCE: DPA coverage in Trust Pack"
else
  fail "COMPLIANCE: DPA not covered in Trust Pack"
fi

if grep -q "opt.out\|opt_out" docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md 2>/dev/null; then
  pass "COMPLIANCE: Opt-out mechanism documented"
else
  warn "COMPLIANCE: Opt-out mechanism not explicit in Trust Pack"
fi

echo ""

# =============================================================================
# SECTION 9: SALES PLAYBOOK INTEGRITY
# =============================================================================
echo "--- SECTION 9: Sales Playbook Integrity ---"

if grep -q "Qualification Checklist\|qualification_checklist\|qualification checklist" docs/SALES_PLAYBOOK.md 2>/dev/null; then
  pass "SALES: Qualification checklist present"
else
  fail "SALES: Qualification checklist missing"
fi

if grep -q "objection\|اعتراض" docs/SALES_PLAYBOOK.md 2>/dev/null; then
  pass "SALES: Objection handling present"
else
  fail "SALES: Objection handling missing"
fi

if grep -q "draft_only\|NO_LIVE_SEND" docs/PILOT_DELIVERY_SOP.md 2>/dev/null; then
  pass "DELIVERY: draft_only gate documented in SOP"
else
  fail "DELIVERY: draft_only gate not in SOP"
fi

echo ""

# =============================================================================
# SECTION 10: PROOF SYSTEM INTEGRITY
# =============================================================================
echo "--- SECTION 10: Proof System Integrity ---"

if grep -q "NO_FAKE_PROOF\|no_fake_proof\|fake proof" docs/PROOF_AND_CASE_STUDY_SYSTEM.md 2>/dev/null; then
  pass "PROOF: NO_FAKE_PROOF gate documented"
else
  fail "PROOF: NO_FAKE_PROOF gate not documented"
fi

if grep -q "consent\|موافقة" docs/PROOF_AND_CASE_STUDY_SYSTEM.md 2>/dev/null; then
  pass "PROOF: Consent requirements documented"
else
  fail "PROOF: Consent requirements missing"
fi

echo ""

# =============================================================================
# SECTION 11: PDPL ARTICLE REFERENCES IN TRUST PACK
# =============================================================================
echo "--- SECTION 11: PDPL Article References ---"

if grep -q "المادة 6\|Article 6\|المادة 9\|Article 9" docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md 2>/dev/null; then
  pass "PDPL: Article references found in Trust Pack"
else
  fail "PDPL: No article references in Trust Pack (need Art. 4/6/9/12/19)"
fi

if grep -q "المادة 19\|Article 19\|breach.*notif\|BREACH_RESPONSE" docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md 2>/dev/null; then
  pass "PDPL: Breach notification article referenced"
else
  warn "PDPL: Breach notification article not explicitly referenced"
fi

echo ""

# =============================================================================
# SECTION 12: KPI ACTION TRIGGERS
# =============================================================================
echo "--- SECTION 12: KPI Action Triggers ---"

if grep -q "Action Trigger\|action_trigger\|محفزات الإجراء\|العتبة الحمراء" docs/BUSINESS_KPI_DASHBOARD_SPEC.md 2>/dev/null; then
  pass "KPI: Action triggers documented (metric → action)"
else
  fail "KPI: No action triggers — every metric must tie to an action"
fi

echo ""

# =============================================================================
# SECTION 13: PILOT SOP ACCEPTANCE CRITERIA
# =============================================================================
echo "--- SECTION 13: SOP Acceptance Criteria ---"

if grep -q "Acceptance Criteria\|acceptance_criteria\|معايير القبول\|Minimum Completion" docs/PILOT_DELIVERY_SOP.md 2>/dev/null; then
  pass "SOP: Acceptance criteria documented"
else
  fail "SOP: Acceptance criteria missing (required by business operating standard)"
fi

if grep -q "Sprint Completion Certificate\|Sprint.*Certificate" docs/PILOT_DELIVERY_SOP.md 2>/dev/null; then
  pass "SOP: Sprint Completion Certificate referenced"
else
  warn "SOP: Sprint Completion Certificate not found"
fi

echo ""

# =============================================================================
# SECTION 14: UNIT ECONOMICS ESTIMATE LABELS
# =============================================================================
echo "--- SECTION 14: Unit Economics Estimate Labels ---"

if grep -q "تقدير\|estimate\|insufficient_data" docs/UNIT_ECONOMICS_AND_MARGIN.md 2>/dev/null; then
  pass "ECONOMICS: Figures labeled as estimates (not guarantees)"
else
  fail "ECONOMICS: Missing estimate labels on financial figures"
fi

if grep -q "تحذير\|Warning\|لا تُستخدم للاستثمار" docs/UNIT_ECONOMICS_AND_MARGIN.md 2>/dev/null; then
  pass "ECONOMICS: Financial warning present"
else
  warn "ECONOMICS: No explicit financial warning in Unit Economics"
fi

echo ""

# =============================================================================
# FINAL VERDICT
# =============================================================================
echo "=============================================="
echo "DEALIX_BUSINESS_READINESS_VERDICT"
echo "=============================================="
echo "PASS:  $PASS"
echo "FAIL:  $FAIL"
echo "WARN:  $WARN"
echo ""

if [ $FAIL -eq 0 ]; then
  echo -e "${GREEN}BUSINESS_READINESS=PASS${NC}"
  echo -e "${GREEN}SELLABLE_NOW=YES (Sprint 499 SAR — warm intros + manual payment)${NC}"
  echo -e "${GREEN}PILOT_READY=YES${NC}"
  echo -e "${GREEN}MONTHLY_READY=AFTER_2_PILOTS${NC}"
  echo -e "${GREEN}BEST_ICP=Saudi B2B founders/agencies 5-50 employees${NC}"
  echo -e "${GREEN}BEST_FIRST_OFFER=7-Day Revenue Proof Sprint 499 SAR${NC}"
  echo -e "${GREEN}NEXT_FOUNDER_ACTION=Open DAY_1_LAUNCH_KIT.md → send 5 warm intros today${NC}"
else
  echo -e "${RED}BUSINESS_READINESS=FAIL (fix $FAIL failures above)${NC}"
  exit 1
fi

if [ $WARN -gt 0 ]; then
  echo ""
  echo -e "${YELLOW}WARNINGS: $WARN items need attention (non-blocking)${NC}"
fi

echo ""
echo "Run complete. $(date '+%Y-%m-%d %H:%M:%S')"
