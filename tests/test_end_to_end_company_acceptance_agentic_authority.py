from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data/ops/end_to_end_company_acceptance_v1.json"
VERIFY = ROOT / "scripts/ops/verify_end_to_end_company_acceptance_v1.py"


def test_e2e_contract_marks_five_names_as_legacy_aliases_only() -> None:
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    authority = data["agent_authority"]
    assert data["canonical_agents_semantics"] == "LEGACY_EXECUTOR_ALIASES_ONLY_NOT_LOGICAL_FLEET_AUTHORITY"
    assert authority["fixed_five_fleet_authority"] is False
    assert authority["logical_agent_authority"] == "dealix.agentic_holding.runtime.build_current_registry"
    assert authority["runtime_capacity_authority"] == "ResourceGovernor + Session Factory"
    assert authority["deep_wip_3_semantics"] == "ECONOMIC_FOCUS_HEURISTIC_ONLY_NOT_RUNTIME_CAPACITY"
    assert "30-Day" not in data["service_scope_model"]["paid_entry"]


def test_e2e_verifier_reports_current_authority_not_fixed_five() -> None:
    result = subprocess.run([sys.executable, str(VERIFY)], cwd=ROOT, text=True, capture_output=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert "logical_agent_authority=AGENTIC_HOLDING_REGISTRY" in result.stdout
    assert "legacy_executor_aliases=5" in result.stdout
    assert "runtime_capacity_authority=RESOURCE_GOVERNOR_SESSION_FACTORY" in result.stdout
    assert "agents=5" not in result.stdout
