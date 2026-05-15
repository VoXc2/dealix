#!/usr/bin/env bash
# Capability verification — service readiness + readiness gates (pytest).
# Usage: bash scripts/dealix_capability_verify.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export APP_ENV=test

FAIL=0

echo "== ruff (capability slice) =="
if command -v ruff >/dev/null 2>&1; then
  ruff check auto_client_acquisition/delivery_os/service_readiness.py \
    auto_client_acquisition/delivery_os/readiness_gates.py \
    auto_client_acquisition/delivery_os/service_catalog.py \
    auto_client_acquisition/delivery_os/delivery_checklist.py \
    auto_client_acquisition/delivery_os/qa_review.py \
    auto_client_acquisition/delivery_os/handoff.py \
    auto_client_acquisition/delivery_os/renewal_recommendation.py \
    auto_client_acquisition/data_os/import_preview.py \
    auto_client_acquisition/data_os/validation_rules.py \
    auto_client_acquisition/data_os/pii_detection.py \
    auto_client_acquisition/data_os/source_attribution.py \
    auto_client_acquisition/data_os/dedupe.py \
    auto_client_acquisition/data_os/schemas.py \
    auto_client_acquisition/reporting_os \
    auto_client_acquisition/knowledge_os \
    auto_client_acquisition/governance_os/lawful_basis.py \
    auto_client_acquisition/governance_os/approval_matrix.py \
    auto_client_acquisition/governance_os/forbidden_actions.py \
    api/routers/commercial_readiness.py api/routers/governance_risk_dashboard.py \
    api/routers/founder.py \
    scripts/verify_service_files.py scripts/verify_service_catalog.py \
    scripts/verify_governance_rules.py scripts/verify_ai_output_quality.py \
    scripts/verify_proof_pack.py scripts/verify_company_ready.py \
    scripts/verify_full_mvp_ready.py \
    tests/test_service_readiness_score.py tests/test_readiness_gates.py \
    tests/test_company_os_verify.py tests/test_data_os_helpers.py \
    tests/test_reporting_os_proof_pack.py tests/test_delivery_os_catalog.py \
    tests/test_knowledge_os_policy.py tests/test_governance_approval_matrix.py || FAIL=1
else
  echo "ruff not installed — skip"
fi

echo "== pytest capability =="
if pytest tests/test_service_readiness_score.py tests/test_readiness_gates.py \
    tests/test_company_os_verify.py tests/test_data_os_helpers.py \
    tests/test_reporting_os_proof_pack.py tests/test_delivery_os_catalog.py \
    tests/test_knowledge_os_policy.py tests/test_governance_approval_matrix.py -q --no-cov; then
  :
else
  FAIL=1
fi

echo "== verify Company OS (docs + scripts) =="
if command -v python3 >/dev/null 2>&1; then
  python3 scripts/verify_full_mvp_ready.py --skip-tests || FAIL=1
else
  py -3 scripts/verify_full_mvp_ready.py --skip-tests || FAIL=1
fi

exit "$FAIL"
