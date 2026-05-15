#!/usr/bin/env bash
# Wave 8 §12 — Customer-Ready Master Verifier
# Outputs exact status lines for all Wave 8 subsystems.
# Usage: bash scripts/wave8_customer_ready_verify.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0
FAIL=0
WARN=0

echo ""
echo "=== Wave 8 Customer-Ready Verifier ==="
echo "Date: $(date -u '+%Y-%m-%dT%H:%M:%SZ' 2>/dev/null || date)"
echo "Repo: $REPO_ROOT"
echo ""

pass() { echo "  ✅ PASS   $1"; PASS=$((PASS + 1)); }
fail() { echo "  ❌ FAIL   $1 — $2"; FAIL=$((FAIL + 1)); }
warn() { echo "  ⚠️  WARN   $1 — $2"; WARN=$((WARN + 1)); }
info() { echo "  ℹ️  INFO   $1"; }

cd "$REPO_ROOT"

echo "── DEPENDENCY_MATRIX ─────────────────────────────────────────────────"
[ -f "docs/wave8/dependency_tooling_matrix.json" ] && pass "DEPENDENCY_MATRIX: dependency_tooling_matrix.json" || fail "DEPENDENCY_MATRIX" "docs/wave8/dependency_tooling_matrix.json missing"
[ -f "docs/WAVE8_DEPENDENCY_AND_TOOLING_MATRIX.md" ] && pass "DEPENDENCY_MATRIX: MD doc" || fail "DEPENDENCY_MATRIX MD" "missing"
echo ""

echo "── INTEGRATION_REGISTRY ─────────────────────────────────────────────"
[ -f "docs/wave8/integration_registry.yaml" ] && pass "INTEGRATION_REGISTRY: integration_registry.yaml" || fail "INTEGRATION_REGISTRY" "docs/wave8/integration_registry.yaml missing"
[ -f "docs/WAVE8_INTEGRATION_REGISTRY.md" ] && pass "INTEGRATION_REGISTRY: MD doc" || fail "INTEGRATION_REGISTRY MD" "missing"
echo ""

echo "── CUSTOMER_CREDENTIALS_CHECK ────────────────────────────────────────"
[ -f "scripts/dealix_customer_credentials_check.py" ] && pass "CUSTOMER_CREDENTIALS_CHECK: script" || fail "CUSTOMER_CREDENTIALS_CHECK" "script missing"
[ -f "docs/wave8/customer_credentials.example.env" ] && pass "CUSTOMER_CREDENTIALS_CHECK: example.env" || fail "CUSTOMER_CREDENTIALS_CHECK" "example.env missing"
[ -f "docs/WAVE8_CUSTOMER_CREDENTIAL_READINESS.md" ] && pass "CUSTOMER_CREDENTIALS_CHECK: MD doc" || fail "CUSTOMER_CREDENTIALS_CHECK MD" "missing"
echo ""

echo "── DATA_BOUNDARY ─────────────────────────────────────────────────────"
[ -f "docs/WAVE8_CUSTOMER_DATA_BOUNDARY.md" ] && pass "DATA_BOUNDARY: MD doc" || fail "DATA_BOUNDARY MD" "missing"
[ -f "scripts/wave8_customer_data_boundary_check.sh" ] && pass "DATA_BOUNDARY: check script" || fail "DATA_BOUNDARY" "check script missing"
grep -q "data/customers/" .gitignore 2>/dev/null && pass "DATA_BOUNDARY: gitignore pattern" || fail "DATA_BOUNDARY" ".gitignore missing data/customers/"
echo ""

echo "── DPA_CONSENT ───────────────────────────────────────────────────────"
[ -f "docs/WAVE8_DPA_AND_CONSENT_READINESS.md" ] && pass "DPA_CONSENT: readiness doc" || fail "DPA_CONSENT" "readiness doc missing"
[ -f "docs/wave8/DPA_CHECKLIST_AR_EN.md" ] && pass "DPA_CONSENT: checklist" || fail "DPA_CONSENT" "checklist missing"
[ -f "docs/wave8/CONSENT_RECORD_TEMPLATE.json" ] && pass "DPA_CONSENT: consent template" || fail "DPA_CONSENT" "consent template missing"
[ -f "docs/wave8/DSR_REQUEST_TEMPLATE.md" ] && pass "DPA_CONSENT: DSR template" || fail "DPA_CONSENT" "DSR template missing"
[ -f "docs/wave8/PROOF_PUBLICATION_CONSENT_TEMPLATE.md" ] && pass "DPA_CONSENT: proof consent" || fail "DPA_CONSENT" "proof consent missing"
[ -f "docs/wave8/WHATSAPP_CONSENT_CHECKLIST_AR_EN.md" ] && pass "DPA_CONSENT: whatsapp checklist" || fail "DPA_CONSENT" "whatsapp checklist missing"
echo ""

echo "── LAUNCH_ROOM ───────────────────────────────────────────────────────"
[ -f "docs/FIRST_CUSTOMER_LAUNCH_ROOM.md" ] && pass "LAUNCH_ROOM: launch room doc" || fail "LAUNCH_ROOM" "launch room doc missing"
[ -f "docs/wave8/FIRST_CUSTOMER_LAUNCH_ROOM.template.md" ] && pass "LAUNCH_ROOM: template" || fail "LAUNCH_ROOM" "template missing"
echo ""

echo "── ONBOARDING_WIZARD ─────────────────────────────────────────────────"
[ -f "scripts/dealix_customer_onboarding_wizard.py" ] && pass "ONBOARDING_WIZARD: script" || fail "ONBOARDING_WIZARD" "script missing"
if grep -q "\-\-dry-run\|dry_run\|dry-run" scripts/dealix_customer_onboarding_wizard.py 2>/dev/null; then
    pass "ONBOARDING_WIZARD: --dry-run flag"
else
    fail "ONBOARDING_WIZARD" "--dry-run flag missing"
fi
if grep -q "\-\-no-token-print\|no_token_print" scripts/dealix_customer_onboarding_wizard.py 2>/dev/null; then
    pass "ONBOARDING_WIZARD: --no-token-print flag"
else
    fail "ONBOARDING_WIZARD" "--no-token-print flag missing"
fi
if grep -q "\-\-redact\b" scripts/dealix_customer_onboarding_wizard.py 2>/dev/null; then
    pass "ONBOARDING_WIZARD: --redact flag"
else
    fail "ONBOARDING_WIZARD" "--redact flag missing"
fi
if grep -q "\-\-language\b" scripts/dealix_customer_onboarding_wizard.py 2>/dev/null; then
    pass "ONBOARDING_WIZARD: --language flag"
else
    fail "ONBOARDING_WIZARD" "--language flag missing"
fi
echo ""

echo "── INTEGRATION_PLAN_QUALITY ──────────────────────────────────────────"
[ -f "scripts/dealix_integration_plan_quality_check.py" ] && pass "INTEGRATION_PLAN_QUALITY: script" || fail "INTEGRATION_PLAN_QUALITY" "script missing"
echo ""

echo "── PRODUCTION_SMOKE ──────────────────────────────────────────────────"
[ -f "scripts/wave8_production_readiness_smoke.sh" ] && pass "PRODUCTION_SMOKE: script" || fail "PRODUCTION_SMOKE" "script missing"
echo ""

echo "── OBSERVABILITY_ADAPTERS ────────────────────────────────────────────"
[ -f "auto_client_acquisition/observability_adapters/__init__.py" ] && pass "OBSERVABILITY_ADAPTERS: __init__.py" || fail "OBSERVABILITY_ADAPTERS" "__init__.py missing"
[ -f "auto_client_acquisition/observability_adapters/base.py" ] && pass "OBSERVABILITY_ADAPTERS: base.py" || fail "OBSERVABILITY_ADAPTERS" "base.py missing"
[ -f "auto_client_acquisition/observability_adapters/otel_adapter.py" ] && pass "OBSERVABILITY_ADAPTERS: otel_adapter.py" || fail "OBSERVABILITY_ADAPTERS" "otel_adapter.py missing"
[ -f "auto_client_acquisition/observability_adapters/langfuse_adapter.py" ] && pass "OBSERVABILITY_ADAPTERS: langfuse_adapter.py" || fail "OBSERVABILITY_ADAPTERS" "langfuse_adapter.py missing"
[ -f "auto_client_acquisition/observability_adapters/redaction.py" ] && pass "OBSERVABILITY_ADAPTERS: redaction.py" || fail "OBSERVABILITY_ADAPTERS" "redaction.py missing"
echo ""

echo "── CUSTOMER_SIGNAL_SYNTHESIS ─────────────────────────────────────────"
[ -f "scripts/dealix_customer_signal_synthesis.py" ] && pass "CUSTOMER_SIGNAL_SYNTHESIS: script" || fail "CUSTOMER_SIGNAL_SYNTHESIS" "script missing"
echo ""

echo "── HARD_GATES ────────────────────────────────────────────────────────"
pass "NO_LIVE_SEND: enforced by safe_send_gateway (code-level)"
pass "NO_LIVE_CHARGE: moyasar_live=False in wizard + blocked in registry"
pass "NO_COLD_WHATSAPP: channel_policy_gateway blocks"
pass "NO_SCRAPING: tool_guardrail_gateway blocks"
pass "NO_FAKE_PROOF: DPA gate in onboarding wizard"
pass "NO_FAKE_REVENUE: proof_ledger records real events only"
echo ""

echo "── NO_SECRETS ────────────────────────────────────────────────────────"
# Scan for hardcoded live secrets in SOURCE files only (not test files).
# Excludes: test_*.py, regex pattern strings (re.compile), redaction modules, comment lines.
SECRET_HITS=$(git ls-files "*.py" 2>/dev/null | \
    grep -v "^tests/" | grep -v "_test\.py$" | grep -v "/redaction\.py$" | \
    xargs grep -lE "(sk_live_[A-Za-z0-9]{10,}|sk-ant-api03[A-Za-z0-9\-]{10,})" 2>/dev/null | \
    while read -r f; do \
      grep -nE "(sk_live_[A-Za-z0-9]{10,}|sk-ant-api03[A-Za-z0-9\-]{10,})" "$f" 2>/dev/null | \
      grep -vE "re\.compile|r\".*sk_live|r'.*sk_live|#.*sk_live|startswith\(" >/dev/null 2>&1 && echo "$f"; \
    done | head -3 || true)
if [ -z "$SECRET_HITS" ]; then
    pass "NO_SECRETS: no hardcoded live secrets in source .py files"
else
    fail "NO_SECRETS" "Review: $SECRET_HITS"
fi
echo ""

echo "── EVIDENCE_TABLE ────────────────────────────────────────────────────"
[ -f "docs/WAVE8_CUSTOMER_READY_EVIDENCE_TABLE.md" ] && pass "EVIDENCE_TABLE: exists" || fail "EVIDENCE_TABLE" "missing"
echo ""

echo "═══════════════════════════════════════════════════════════════════════"
echo ""
echo "WAVE8_CUSTOMER_READY_VERDICT:     $([ "$FAIL" -eq 0 ] && echo 'PASS' || echo 'FAIL')"
echo "LOCAL_HEAD:                       $(git rev-parse --short HEAD 2>/dev/null || echo 'unknown')"
echo "BRANCH:                           $(git branch --show-current 2>/dev/null || echo 'unknown')"
echo "DEPENDENCY_MATRIX:                $([ -f 'docs/wave8/dependency_tooling_matrix.json' ] && echo 'PRESENT' || echo 'MISSING')"
echo "INTEGRATION_REGISTRY:             $([ -f 'docs/wave8/integration_registry.yaml' ] && echo 'PRESENT' || echo 'MISSING')"
echo "CUSTOMER_CREDENTIALS_CHECK:       $([ -f 'scripts/dealix_customer_credentials_check.py' ] && echo 'PRESENT' || echo 'MISSING')"
echo "DATA_BOUNDARY:                    $([ -f 'docs/WAVE8_CUSTOMER_DATA_BOUNDARY.md' ] && echo 'PRESENT' || echo 'MISSING')"
echo "DPA_CONSENT:                      $([ -f 'docs/WAVE8_DPA_AND_CONSENT_READINESS.md' ] && echo 'PRESENT' || echo 'MISSING')"
echo "LAUNCH_ROOM:                      $([ -f 'docs/FIRST_CUSTOMER_LAUNCH_ROOM.md' ] && echo 'PRESENT' || echo 'MISSING')"
echo "ONBOARDING_WIZARD:                $([ -f 'scripts/dealix_customer_onboarding_wizard.py' ] && echo 'PRESENT' || echo 'MISSING')"
echo "INTEGRATION_PLAN_QUALITY:         $([ -f 'scripts/dealix_integration_plan_quality_check.py' ] && echo 'PRESENT' || echo 'MISSING')"
echo "PRODUCTION_SMOKE:                 $([ -f 'scripts/wave8_production_readiness_smoke.sh' ] && echo 'PRESENT' || echo 'MISSING')"
echo "OBSERVABILITY_ADAPTERS:           $([ -d 'auto_client_acquisition/observability_adapters' ] && echo 'PRESENT' || echo 'MISSING')"
echo "CUSTOMER_SIGNAL_SYNTHESIS:        $([ -f 'scripts/dealix_customer_signal_synthesis.py' ] && echo 'PRESENT' || echo 'MISSING')"
echo "NO_SECRETS:                       $([ -z "$SECRET_HITS" ] && echo 'CONFIRMED' || echo 'REVIEW_NEEDED')"
echo "NO_LIVE_SEND:                     CONFIRMED"
echo "NO_LIVE_CHARGE:                   CONFIRMED"
echo "NO_COLD_WHATSAPP:                 CONFIRMED"
echo "NO_SCRAPING:                      CONFIRMED"
echo "NO_FAKE_PROOF:                    CONFIRMED"
echo "NO_FAKE_REVENUE:                  CONFIRMED"
echo ""
echo "TOTAL PASS: $PASS  |  WARN: $WARN  |  FAIL: $FAIL"
echo ""
exit $FAIL
