from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "ops" / "verify_supply_chain_lab_v1.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("verify_supply_chain_lab_v1", MODULE_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_supply_chain_manifest_is_fail_closed(capsys):
    module = _load_module()
    module.main()
    out = capsys.readouterr().out
    assert "DEALIX_SUPPLY_CHAIN_LAB_V1=PASS" in out
    assert "production_mutation=false" in out
    assert "customer_effects=false" in out
    assert "auto_remediation=false" in out


def test_required_tools_are_bounded_to_one_lab():
    module = _load_module()
    assert module.REQUIRED_COMPONENTS == {
        "osv-scanner",
        "syft",
        "grype",
        "github-artifact-attestations",
    }
