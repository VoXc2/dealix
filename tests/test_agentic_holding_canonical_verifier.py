from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/ops/verify_agentic_holding_canonical_contract.py"


def _load_verifier():
    spec = importlib.util.spec_from_file_location("verify_agentic_holding_canonical_contract", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_canonical_contract_verifier_passes() -> None:
    receipt = _load_verifier().verify()

    assert receipt["verdict"] == "PASS", receipt
    assert receipt["architecture"] == "agentic_holding_sector_company_mesh"
    assert receipt["status"] == "CANONICAL"
    assert receipt["logical_agents"] == "dynamic_hierarchical_registry"
    assert receipt["runtime_workers"] == "lazy_resource_governed"
    assert receipt["blocking_guardrails"] is True
    assert receipt["end_to_end_trace"] is True
    assert receipt["token_passthrough_forbidden"] is True
    assert receipt["issuer_validation_required"] is True
    assert receipt["paid_spill_default"] is False
    assert receipt["external_authority"] == "exact_action_bound_authority"
    assert receipt["research_sources"] >= 6
    assert receipt["failures"] == []
