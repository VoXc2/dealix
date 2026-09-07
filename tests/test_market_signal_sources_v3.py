from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "ops" / "verify_market_signal_sources_v3.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("verify_market_signal_sources_v3", MODULE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_registry_verifier_passes_current_contract(capsys):
    module = _load_module()
    module.main()
    out = capsys.readouterr().out
    assert "DEALIX_MARKET_SIGNAL_SOURCES_V3=PASS" in out
    assert "commercial_authority_from_external_sources=false" in out
    assert "default_relationship_state=RESEARCH_ONLY" in out
    assert "default_consent_state=NOT_PROVEN" in out


def test_required_contract_includes_truth_state_fields():
    module = _load_module()
    assert "relationship_state" in module.REQUIRED_SIGNAL_FIELDS
    assert "consent_state" in module.REQUIRED_SIGNAL_FIELDS
    assert "demand_grade" in module.REQUIRED_SIGNAL_FIELDS
    assert module.ALLOWED_GRADES == {"D1", "D2", "D3", "D4"}
