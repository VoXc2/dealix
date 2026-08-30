#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/commercial/autonomous_commercial_activation_v1.json"


def main() -> int:
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert data["schema"] == "dealix.autonomous-commercial-activation.v1"
    assert data["portfolio_objective"] == "CASH_READY_AUTONOMOUS_DEALIX_COMPANY"
    assert data["runtime_owner"] == "EXISTING_DEALIX_COMPANY_AUTOPILOT_ONLY"
    assert data["new_scheduler"] is False
    assert data["new_permanent_agent"] is False
    assert data["new_crm_or_truth_store"] is False
    assert len(data["canonical_agents"]) == 5
    assert data["research_adapter_decision"]["selected_first_pilot"] == "TAVILY_READ_ONLY"
    assert data["research_adapter_decision"]["parallel_install_all_candidates"] is False
    assert data["approval_minimization"]["broad_blanket_authority_allowed"] is False
    assert data["approval_minimization"]["expired_or_revoked_approval_executes"] is False
    assert all(value is False for value in data["external_effect_defaults"].values())
    assert data["negotiation"]["reuse_existing_engine"] is True
    assert data["negotiation"]["autonomous_final_price_discount_legal_payment"] is False
    assert data["self_improvement"]["simulated_metrics_can_authorize_mutation"] is False
    print("DEALIX_AUTONOMOUS_COMMERCIAL_ACTIVATION_V1=PASS")
    print("RUNTIME_OWNER=EXISTING_COMPANY_AUTOPILOT")
    print("WEB_RESEARCH_ADAPTER_FIRST_PILOT=TAVILY_READ_ONLY")
    print("EXTERNAL_EFFECT_DEFAULTS=ALL_FALSE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
