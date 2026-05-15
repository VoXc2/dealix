from __future__ import annotations

import json

from saudi_ai_provider.enterprise_playbook import generate_enterprise_playbook_bundle


def test_generate_enterprise_playbook_bundle_creates_all_required_outputs(tmp_path) -> None:
    intake = json.loads(
        """
        {
          "company_name": "Alpha KSA",
          "company_size": 250,
          "sector": "technology",
          "decision_owner": "COO",
          "budget_range_sar": "400000-650000",
          "target_deadline": "2026-12-31"
        }
        """
    )
    bundle = generate_enterprise_playbook_bundle(
        service_id="CUSTOMER_PORTAL_GOLD",
        intake=intake,
        profile="hybrid_governed_execution",
        output_dir=tmp_path,
    )

    assert bundle.profile == "hybrid_governed_execution"
    assert bundle.proposal.exists()
    assert bundle.sow.exists()
    assert bundle.kpi_contract.exists()
    assert bundle.governance_contract.exists()

    kpi_text = bundle.kpi_contract.read_text(encoding="utf-8")
    governance_text = bundle.governance_contract.read_text(encoding="utf-8")
    assert "KPI Contract" in kpi_text
    assert "Governance Contract" in governance_text
    assert "hybrid_governed_execution" in governance_text
