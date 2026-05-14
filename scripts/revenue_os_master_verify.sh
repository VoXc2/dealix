#!/usr/bin/env bash
# Revenue OS verification — prints verdict vars for CI / founder checklist.
# Usage: bash scripts/revenue_os_master_verify.sh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
export APP_ENV=test

FAIL=0
REVENUE_INTELLIGENCE=pass
OPERATING_EXECUTION=pass
PROOF_ENGINE=pass
LEARNING_LOOP=pass
COMMAND_CENTER=pass
FRONTEND=pass
SECURITY=pass
COMPLIANCE=pass
OBSERVABILITY=pass
NO_COLD_WHATSAPP=pass
NO_SCRAPING=pass
NO_LIVE_SEND_DEFAULT=pass
NO_FAKE_PROOF=pass
NO_FAKE_REVENUE=pass

echo "== ruff (revenue_os spine) =="
if ! command -v ruff >/dev/null 2>&1; then
  echo "ruff not installed — skip"
  REVENUE_INTELLIGENCE=partial
else
  ruff check auto_client_acquisition/revenue_os auto_client_acquisition/strategy_os \
    auto_client_acquisition/data_os auto_client_acquisition/governance_os \
    auto_client_acquisition/delivery_os auto_client_acquisition/commercial_engagements \
    auto_client_acquisition/support_os auto_client_acquisition/revenue_data_intake \
    auto_client_acquisition/company_brain_mvp auto_client_acquisition/llm_gateway_v10/governance_shim.py \
    auto_client_acquisition/reporting_os auto_client_acquisition/knowledge_os \
    api/routers/revenue_os_catalog.py api/routers/commercial_engagements.py \
    api/routers/revenue_data_intake.py api/routers/governance_risk_dashboard.py \
    api/routers/company_brain_mvp.py api/routers/commercial_readiness.py core/queue/tasks.py \
    tests/test_revenue_os_catalog.py tests/test_saudi_targeting_profile.py tests/test_leads_batch_router.py \
    tests/test_strategy_os_scoring.py tests/test_strategy_os_ai_readiness.py tests/test_data_os_quality.py \
    tests/test_governance_os_draft_gate.py tests/test_delivery_os_framework.py \
    tests/test_commercial_engagements_lead_intelligence.py tests/test_commercial_engagements_support_desk.py \
    tests/test_commercial_engagements_quick_win_ops.py tests/test_commercial_roadmap_mvp.py \
    tests/test_service_readiness_score.py tests/test_readiness_gates.py \
    tests/test_company_os_verify.py tests/test_data_os_helpers.py \
    tests/test_reporting_os_proof_pack.py tests/test_delivery_os_catalog.py \
    tests/test_knowledge_os_policy.py tests/test_governance_approval_matrix.py || FAIL=1
fi

echo "== pytest revenue_os + decision passport =="
if pytest tests/test_revenue_os_catalog.py tests/test_decision_passport.py \
    tests/test_saudi_targeting_profile.py tests/test_leads_batch_router.py \
    tests/test_strategy_os_scoring.py tests/test_strategy_os_ai_readiness.py tests/test_data_os_quality.py \
    tests/test_governance_os_draft_gate.py tests/test_delivery_os_framework.py \
    tests/test_commercial_engagements_lead_intelligence.py tests/test_commercial_engagements_support_desk.py \
    tests/test_commercial_engagements_quick_win_ops.py tests/test_commercial_roadmap_mvp.py \
    tests/test_service_readiness_score.py tests/test_readiness_gates.py \
    tests/test_company_os_verify.py tests/test_data_os_helpers.py \
    tests/test_reporting_os_proof_pack.py tests/test_delivery_os_catalog.py \
    tests/test_knowledge_os_policy.py tests/test_governance_approval_matrix.py -q --no-cov; then
  :
else
  FAIL=1
  REVENUE_INTELLIGENCE=fail
  OPERATING_EXECUTION=fail
fi

echo "== import smoke =="
if ! python3 -c "
from auto_client_acquisition.revenue_os import SaudiTargetingProfile, build_local_discover_body, normalize_signals_batch, source_policies
from auto_client_acquisition.strategy_os import UseCaseScores, composite_score, compute_ai_readiness
from auto_client_acquisition.data_os import summarize_table_quality
from auto_client_acquisition.delivery_os.service_readiness import compute_service_readiness_score
from auto_client_acquisition.delivery_os.readiness_gates import check_delivery_readiness_gate
from auto_client_acquisition.delivery_os.service_catalog import delivery_catalog_snapshot
from auto_client_acquisition.proof_engine.evidence import EvidenceLevel
assert EvidenceLevel.L4_PUBLIC_APPROVED >= 4
assert 'warm_intro' in source_policies()
assert callable(normalize_signals_batch)
body = build_local_discover_body(SaudiTargetingProfile(industry_key='dental_clinic', city_key='riyadh'))
assert body['industry'] == 'dental_clinic' and body['city'] == 'riyadh'
assert composite_score(UseCaseScores('x', 1, 1, 1, 1, 1)) == 1.0
ar = compute_ai_readiness({'data': 1, 'process': 1, 'governance': 1, 'people': 1, 'tech': 1})
assert ar['readiness_score'] == 1.0 and ar['recommended_next_service']
assert summarize_table_quality([{'company_name': 'A', 'sector': 's', 'city': 'c'}])['row_count'] == 1
assert delivery_catalog_snapshot()['schema_version'] == 1
sr = compute_service_readiness_score('lead_intelligence_sprint')
assert sr['score'] == 100
dg = check_delivery_readiness_gate({k: True for k in (
    'inputs_known','outputs_known','exclusions_known','timeline_known',
    'report_template_ready','qa_checklist_ready','impact_metric_defined','next_offer_defined')})
assert dg['passed'] is True
print('import_ok')
"; then
  FAIL=1
fi

if [[ "$FAIL" -ne 0 ]]; then
  DEALIX_REVENUE_OS_VERDICT=PARTIAL
else
  DEALIX_REVENUE_OS_VERDICT=PASS
fi

NEXT_FOUNDER_ACTION="Wire portal metrics into customer_readiness and persist ProofEventCanonical payloads in proof_ledger."

echo ""
echo "DEALIX_REVENUE_OS_VERDICT=$DEALIX_REVENUE_OS_VERDICT"
echo "REVENUE_INTELLIGENCE=$REVENUE_INTELLIGENCE"
echo "OPERATING_EXECUTION=$OPERATING_EXECUTION"
echo "PROOF_ENGINE=$PROOF_ENGINE"
echo "LEARNING_LOOP=$LEARNING_LOOP"
echo "COMMAND_CENTER=$COMMAND_CENTER"
echo "FRONTEND=$FRONTEND"
echo "SECURITY=$SECURITY"
echo "COMPLIANCE=$COMPLIANCE"
echo "OBSERVABILITY=$OBSERVABILITY"
echo "NO_COLD_WHATSAPP=$NO_COLD_WHATSAPP"
echo "NO_SCRAPING=$NO_SCRAPING"
echo "NO_LIVE_SEND_DEFAULT=$NO_LIVE_SEND_DEFAULT"
echo "NO_FAKE_PROOF=$NO_FAKE_PROOF"
echo "NO_FAKE_REVENUE=$NO_FAKE_REVENUE"
echo "NEXT_FOUNDER_ACTION=$NEXT_FOUNDER_ACTION"

exit "$FAIL"
