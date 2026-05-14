#!/usr/bin/env bash
# Wave 8 §9 — Production Readiness Smoke
# Quick smoke test of Wave 8 readiness: docs, scripts, .gitignore, tests.
# Does NOT start servers. Does NOT call external APIs.
# Usage: bash scripts/wave8_production_readiness_smoke.sh

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0
FAIL=0
WARN=0

echo ""
echo "=== Wave 8 — Production Readiness Smoke ==="
echo "Repo: $REPO_ROOT"
echo ""

pass() { echo "  ✅ PASS  $1"; PASS=$((PASS + 1)); }
fail() { echo "  ❌ FAIL  $1 — $2"; FAIL=$((FAIL + 1)); }
warn() { echo "  ⚠️  WARN  $1 — $2"; WARN=$((WARN + 1)); }

# ── Wave 8 Docs ──────────────────────────────────────────────────────────────
cd "$REPO_ROOT"

[ -f "docs/WAVE8_CURRENT_REALITY.md" ]             && pass "docs/WAVE8_CURRENT_REALITY.md" || fail "docs/WAVE8_CURRENT_REALITY.md" "missing"
[ -f "docs/WAVE8_DEPENDENCY_AND_TOOLING_MATRIX.md" ] && pass "WAVE8_DEPENDENCY_AND_TOOLING_MATRIX.md" || fail "WAVE8_DEPENDENCY_AND_TOOLING_MATRIX.md" "missing"
[ -f "docs/wave8/dependency_tooling_matrix.json" ] && pass "dependency_tooling_matrix.json" || fail "dependency_tooling_matrix.json" "missing"
[ -f "docs/WAVE8_INTEGRATION_REGISTRY.md" ]        && pass "WAVE8_INTEGRATION_REGISTRY.md" || fail "WAVE8_INTEGRATION_REGISTRY.md" "missing"
[ -f "docs/wave8/integration_registry.yaml" ]      && pass "integration_registry.yaml" || fail "integration_registry.yaml" "missing"
[ -f "docs/WAVE8_CUSTOMER_CREDENTIAL_READINESS.md" ] && pass "WAVE8_CUSTOMER_CREDENTIAL_READINESS.md" || fail "WAVE8_CUSTOMER_CREDENTIAL_READINESS.md" "missing"
[ -f "docs/wave8/customer_credentials.example.env" ] && pass "customer_credentials.example.env" || fail "customer_credentials.example.env" "missing"
[ -f "docs/WAVE8_CUSTOMER_DATA_BOUNDARY.md" ]      && pass "WAVE8_CUSTOMER_DATA_BOUNDARY.md" || fail "WAVE8_CUSTOMER_DATA_BOUNDARY.md" "missing"
[ -f "docs/WAVE8_DPA_AND_CONSENT_READINESS.md" ]   && pass "WAVE8_DPA_AND_CONSENT_READINESS.md" || fail "WAVE8_DPA_AND_CONSENT_READINESS.md" "missing"
[ -f "docs/wave8/DPA_CHECKLIST_AR_EN.md" ]         && pass "DPA_CHECKLIST_AR_EN.md" || fail "DPA_CHECKLIST_AR_EN.md" "missing"
[ -f "docs/wave8/CONSENT_RECORD_TEMPLATE.json" ]   && pass "CONSENT_RECORD_TEMPLATE.json" || fail "CONSENT_RECORD_TEMPLATE.json" "missing"
[ -f "docs/wave8/DSR_REQUEST_TEMPLATE.md" ]        && pass "DSR_REQUEST_TEMPLATE.md" || fail "DSR_REQUEST_TEMPLATE.md" "missing"
[ -f "docs/wave8/PROOF_PUBLICATION_CONSENT_TEMPLATE.md" ] && pass "PROOF_PUBLICATION_CONSENT_TEMPLATE.md" || fail "PROOF_PUBLICATION_CONSENT_TEMPLATE.md" "missing"
[ -f "docs/wave8/WHATSAPP_CONSENT_CHECKLIST_AR_EN.md" ] && pass "WHATSAPP_CONSENT_CHECKLIST_AR_EN.md" || fail "WHATSAPP_CONSENT_CHECKLIST_AR_EN.md" "missing"
[ -f "docs/FIRST_CUSTOMER_LAUNCH_ROOM.md" ]        && pass "FIRST_CUSTOMER_LAUNCH_ROOM.md" || fail "FIRST_CUSTOMER_LAUNCH_ROOM.md" "missing"
[ -f "docs/wave8/FIRST_CUSTOMER_LAUNCH_ROOM.template.md" ] && pass "FIRST_CUSTOMER_LAUNCH_ROOM.template.md" || fail "FIRST_CUSTOMER_LAUNCH_ROOM.template.md" "missing"
[ -f "docs/WAVE8_CUSTOMER_READY_EVIDENCE_TABLE.md" ] && pass "WAVE8_CUSTOMER_READY_EVIDENCE_TABLE.md" || fail "WAVE8_CUSTOMER_READY_EVIDENCE_TABLE.md" "missing"

# ── Wave 8 Scripts ────────────────────────────────────────────────────────────
[ -f "scripts/dealix_customer_credentials_check.py" ] && pass "dealix_customer_credentials_check.py" || fail "dealix_customer_credentials_check.py" "missing"
[ -f "scripts/wave8_customer_data_boundary_check.sh" ] && pass "wave8_customer_data_boundary_check.sh" || fail "wave8_customer_data_boundary_check.sh" "missing"
[ -f "scripts/dealix_integration_plan_quality_check.py" ] && pass "dealix_integration_plan_quality_check.py" || fail "dealix_integration_plan_quality_check.py" "missing"
[ -f "scripts/wave8_production_readiness_smoke.sh" ] && pass "wave8_production_readiness_smoke.sh" || fail "wave8_production_readiness_smoke.sh" "missing"
[ -f "scripts/dealix_customer_signal_synthesis.py" ] && pass "dealix_customer_signal_synthesis.py" || fail "dealix_customer_signal_synthesis.py" "missing"
[ -f "scripts/wave8_customer_ready_verify.sh" ]     && pass "wave8_customer_ready_verify.sh" || fail "wave8_customer_ready_verify.sh" "missing"

# ── Wave 8 Tests ──────────────────────────────────────────────────────────────
[ -f "tests/test_wave8_dependency_tooling_matrix.py" ] && pass "test_wave8_dependency_tooling_matrix.py" || fail "test_wave8_dependency_tooling_matrix.py" "missing"
[ -f "tests/test_wave8_integration_registry.py" ]  && pass "test_wave8_integration_registry.py" || fail "test_wave8_integration_registry.py" "missing"
[ -f "tests/test_wave8_customer_credentials_check.py" ] && pass "test_wave8_customer_credentials_check.py" || fail "test_wave8_customer_credentials_check.py" "missing"
[ -f "tests/test_wave8_customer_data_boundary.py" ] && pass "test_wave8_customer_data_boundary.py" || fail "test_wave8_customer_data_boundary.py" "missing"
[ -f "tests/test_wave8_dpa_consent_docs.py" ]      && pass "test_wave8_dpa_consent_docs.py" || fail "test_wave8_dpa_consent_docs.py" "missing"
[ -f "tests/test_wave8_launch_room.py" ]           && pass "test_wave8_launch_room.py" || fail "test_wave8_launch_room.py" "missing"
[ -f "tests/test_wave8_customer_onboarding_wizard_hardening.py" ] && pass "test_wave8_customer_onboarding_wizard_hardening.py" || fail "test_wave8_customer_onboarding_wizard_hardening.py" "missing"
[ -f "tests/test_wave8_integration_plan_quality.py" ] && pass "test_wave8_integration_plan_quality.py" || fail "test_wave8_integration_plan_quality.py" "missing"
[ -f "tests/test_wave8_production_readiness_smoke.py" ] && pass "test_wave8_production_readiness_smoke.py" || fail "test_wave8_production_readiness_smoke.py" "missing"
[ -f "tests/test_wave8_observability_adapter_readiness.py" ] && pass "test_wave8_observability_adapter_readiness.py" || fail "test_wave8_observability_adapter_readiness.py" "missing"
[ -f "tests/test_wave8_customer_signal_synthesis.py" ] && pass "test_wave8_customer_signal_synthesis.py" || fail "test_wave8_customer_signal_synthesis.py" "missing"
[ -f "tests/test_wave8_customer_ready_verify.py" ] && pass "test_wave8_customer_ready_verify.py" || fail "test_wave8_customer_ready_verify.py" "missing"

# ── Observability Adapters ────────────────────────────────────────────────────
[ -f "auto_client_acquisition/observability_adapters/__init__.py" ] && pass "observability_adapters/__init__.py" || fail "observability_adapters/__init__.py" "missing"
[ -f "auto_client_acquisition/observability_adapters/base.py" ]     && pass "observability_adapters/base.py" || fail "observability_adapters/base.py" "missing"
[ -f "auto_client_acquisition/observability_adapters/otel_adapter.py" ] && pass "observability_adapters/otel_adapter.py" || fail "observability_adapters/otel_adapter.py" "missing"
[ -f "auto_client_acquisition/observability_adapters/langfuse_adapter.py" ] && pass "observability_adapters/langfuse_adapter.py" || fail "observability_adapters/langfuse_adapter.py" "missing"
[ -f "auto_client_acquisition/observability_adapters/redaction.py" ] && pass "observability_adapters/redaction.py" || fail "observability_adapters/redaction.py" "missing"

# ── .gitignore patterns ───────────────────────────────────────────────────────
if grep -q "data/customers/" .gitignore 2>/dev/null; then
    pass ".gitignore has data/customers/ pattern"
else
    fail ".gitignore missing data/customers/"
fi

if grep -q "\.env" .gitignore 2>/dev/null; then
    pass ".gitignore has .env pattern"
else
    fail ".gitignore missing .env"
fi

# ── Hard Gate File Check ──────────────────────────────────────────────────────
if [ -f "auto_client_acquisition/safe_send_gateway" ] || [ -d "auto_client_acquisition/safe_send_gateway" ]; then
    pass "safe_send_gateway exists"
else
    warn "safe_send_gateway" "directory/module not found at expected path"
fi

if [ -f "auto_client_acquisition/whatsapp_safe_send.py" ]; then
    if grep -q "NO_LIVE_SEND\|blocked\|BLOCKED" auto_client_acquisition/whatsapp_safe_send.py 2>/dev/null; then
        pass "whatsapp_safe_send.py has hard gate"
    else
        warn "whatsapp_safe_send.py" "hard gate pattern not found"
    fi
else
    warn "whatsapp_safe_send.py" "file not found"
fi

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo "─────────────────────────────────────────────────────────"
echo "  PASS: $PASS  |  WARN: $WARN  |  FAIL: $FAIL"
if [ "$FAIL" -eq 0 ]; then
    echo "  ✅ WAVE8_PRODUCTION_SMOKE: ALL_PASS"
else
    echo "  ❌ WAVE8_PRODUCTION_SMOKE: FAIL ($FAIL failures)"
fi
echo ""
exit $FAIL
