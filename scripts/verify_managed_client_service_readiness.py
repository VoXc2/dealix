#!/usr/bin/env python3
"""Read-only source gate for Dealix managed-client service readiness.

This deliberately separates three truths:
- managed-client service source readiness;
- shared multi-tenant SaaS/RLS readiness;
- public production release parity.
It performs no external action and never activates RLS.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial.universal_diagnostic_factory import DiagnosticDepth, UniversalDiagnosticFactory

ACTIVE_CUSTOMER_SURFACES = (
    ROOT / "scripts/create_customer_workspace.py",
    ROOT / "scripts/run_dealix_e2e_dry_run.py",
    ROOT / "scripts/delivery/create_client_workspace.py",
    *sorted((ROOT / "customers/_template").glob("*.md")),
)


def _tenant_boundary() -> dict:
    path = ROOT / "scripts/ops/verify_tenant_boundary_registry_v1.py"
    spec = importlib.util.spec_from_file_location("dealix_tenant_boundary_readiness", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load tenant boundary verifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.evaluate()


def evaluate() -> dict:
    diagnostics_all_free = all(UniversalDiagnosticFactory().is_free(depth) for depth in DiagnosticDepth)
    customer_text = "\n".join(path.read_text(encoding="utf-8") for path in ACTIVE_CUSTOMER_SURFACES)
    customer_specific_delivery = (
        "Customer-Specific Governed Delivery Scope" in customer_text
        and "customer-specific after Qualified Discovery" in customer_text
        and "30-Day Revenue Command Pilot" not in customer_text
    )
    client_source = (ROOT / "scripts/delivery/create_client_workspace.py").read_text(encoding="utf-8")
    governed_handoff = all(
        token in client_source
        for token in (
            "qualified_discovery_evidence_ref",
            "approved_scope_ref",
            "approved_named_customer_quote_ref",
            "customer_acceptance_ref",
            "payment_or_documented_start_condition_ref",
            "approved_data_boundary_ref",
        )
    )
    portal = (ROOT / "landing/customer-portal.html").read_text(encoding="utf-8")
    public_proof_safe = "/cases" in portal and "/proof-vault" not in portal and "ليست دليل عميل" in portal
    enterprise = (ROOT / "scripts/company_enterprise_ready.sh").read_text(encoding="utf-8")
    canonical_python = '.venv/bin/python' in enterprise and '"$PYTHON" -m pytest' in enterprise
    tenant = _tenant_boundary()
    managed_ready = all(
        (diagnostics_all_free, customer_specific_delivery, governed_handoff, public_proof_safe, canonical_python, tenant["inventory_sync"])
    )
    return {
        "schema": "dealix.managed_client_service_readiness.v1",
        "managed_client_service_source_ready": managed_ready,
        "diagnostics_all_free": diagnostics_all_free,
        "customer_specific_delivery": customer_specific_delivery,
        "governed_real_handoff_required": governed_handoff,
        "public_proof_boundary_safe": public_proof_safe,
        "canonical_python_launcher": canonical_python,
        "tenant_inventory_sync": tenant["inventory_sync"],
        "shared_multi_tenant_saas_ready": tenant["activation_ready"],
        "pending_tenant_rls_review": len(tenant["pending_tenant_rls_review"]),
        "rls_model_mismatch_review": len(tenant["rls_model_mismatch_review"]),
        "production_green": "SEPARATE_RELEASE_PARITY_GATE_NOT_EVALUATED",
        "external_actions_executed": 0,
    }


def main() -> int:
    result = evaluate()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    print(f"MANAGED_CLIENT_SERVICE_SOURCE_READY={'true' if result['managed_client_service_source_ready'] else 'false'}")
    print(f"SHARED_MULTI_TENANT_SAAS_READY={'true' if result['shared_multi_tenant_saas_ready'] else 'false'}")
    print(f"PENDING_TENANT_RLS_REVIEW={result['pending_tenant_rls_review']}")
    print(f"RLS_MODEL_MISMATCH_REVIEW={result['rls_model_mismatch_review']}")
    print("PRODUCTION_GREEN=SEPARATE_RELEASE_PARITY_GATE_NOT_EVALUATED")
    return 0 if result["managed_client_service_source_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
