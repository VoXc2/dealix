"""Evidence collection — the source data that justifies the score.

Every claim in the Full-Ops Score must trace back to a verifiable
data source. This module returns those sources for /evidence endpoint.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.full_ops_radar.health_checks import (
    run_all_health_checks,
)


def collect_evidence() -> dict[str, Any]:
    """Return the evidence bundle: per-layer module path + check timestamp."""
    checks = run_all_health_checks()
    evidence_lines: list[dict[str, Any]] = []
    for c in checks:
        layer = c["layer"]
        evidence_lines.append({
            "layer": layer,
            "available": c["available"],
            "evidence_kind": "module_import_check",
            "evidence_source": _layer_to_module(layer),
            "max_weight": c["max_weight"],
        })
    return {
        "evidence_count": len(evidence_lines),
        "evidence": evidence_lines,
        "policy": "every_score_traceable_to_module_import",
    }


def _layer_to_module(layer: str) -> str:
    return {
        "leadops": "auto_client_acquisition.leadops_spine",
        "customer_brain": "auto_client_acquisition.customer_brain",
        "service_sessions": "auto_client_acquisition.service_sessions",
        "approval_center": "auto_client_acquisition.approval_center",
        "payment_ops": "auto_client_acquisition.payment_ops",
        "support": "auto_client_acquisition.support_inbox",
        "proof_ledger": "auto_client_acquisition.proof_ledger",
        "customer_portal": "api.routers.customer_company_portal",
        "executive_dashboard": "auto_client_acquisition.executive_pack_v2",
        "safety_compliance": "auto_client_acquisition.whatsapp_safe_send",
    }.get(layer, "unknown")
