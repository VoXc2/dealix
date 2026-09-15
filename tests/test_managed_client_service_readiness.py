from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "verify_managed_client_service_readiness.py"


def _module():
    spec = importlib.util.spec_from_file_location("managed_client_service_readiness", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_managed_service_can_be_ready_without_claiming_shared_saas_or_production() -> None:
    result = _module().evaluate()
    assert result["managed_client_service_source_ready"] is True
    assert result["diagnostics_all_free"] is True
    assert result["customer_specific_delivery"] is True
    assert result["governed_real_handoff_required"] is True
    assert result["public_proof_boundary_safe"] is True
    assert result["canonical_python_launcher"] is True
    assert result["tenant_inventory_sync"] is True
    assert result["shared_multi_tenant_saas_ready"] is False
    assert result["pending_tenant_rls_review"] > 0
    assert result["production_green"] == "SEPARATE_RELEASE_PARITY_GATE_NOT_EVALUATED"
    assert result["external_actions_executed"] == 0


def test_active_customer_surfaces_have_no_fixed_30_day_delivery_authority() -> None:
    module = _module()
    text = "\n".join(path.read_text(encoding="utf-8") for path in module.ACTIVE_CUSTOMER_SURFACES)
    assert "30-Day Revenue Command Pilot" not in text
    assert "Customer-Specific Governed Delivery Scope" in text
    assert "customer-specific after Qualified Discovery" in text
