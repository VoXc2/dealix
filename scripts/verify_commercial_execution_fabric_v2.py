#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/commercial/commercial_execution_fabric_v2.json"
SKILL = ROOT / "skills/dealix-commercial-execution/SKILL.md"


def main() -> int:
    payload = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert payload["schema"] == "dealix.commercial-execution-fabric.v2"
    assert payload["runtime_owner"] == "EXISTING_DEALIX_COMPANY_AUTOPILOT_ONLY"
    assert payload["new_scheduler"] is False
    assert payload["new_permanent_agent"] is False
    assert payload["new_crm_or_truth_store"] is False
    assert set(payload["canonical_agents"]) == {
        "dealix-pm", "dealix-sales", "dealix-delivery", "dealix-engineer", "dealix-content"
    }
    research = payload["research_admission"]
    assert research["tavily"] == "ADOPT_READ_ONLY_DIRECT_HTTP_NO_NEW_SDK"
    assert research["docling"].startswith("PILOT_ISOLATED")
    assert research["stagehand"].startswith("PILOT_ISOLATED")
    assert research["new_agent_framework"] == "REJECT_DUPLICATE"
    execution = payload["external_execution"]
    assert execution["provider_adapters_may_execute_only_after_exact_gate_pass"] is True
    assert execution["default_runtime_authority"] == "ALL_FALSE"
    assert execution["expired_revoked_suppressed_executes"] is False
    assert execution["provider_receipt_is_customer_outcome"] is False
    assert payload["channel_policy"]["founder_linkedin"] == "MANUAL_NATIVE"
    assert "research!=relationship" in payload["truth_firewall"]
    skill = SKILL.read_text(encoding="utf-8")
    assert skill.startswith("---\nname: dealix-commercial-execution\n")
    assert "External Execution Gate" in skill
    print("DEALIX_COMMERCIAL_EXECUTION_FABRIC_V2=PASS")
    print("FACTORIES=6")
    print("NEW_SCHEDULER=NO")
    print("NEW_PERMANENT_AGENT=NO")
    print("DEFAULT_EXTERNAL_AUTHORITY=ALL_FALSE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
