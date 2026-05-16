"""Trust and assurance dashboard — approval + compliance snapshot (read-only)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.governance_os.workflow_control_registry import workflow_controls

router = APIRouter(prefix="/api/v1/trust", tags=["trust"])


@router.get("/dashboard")
def get_trust_dashboard() -> dict[str, Any]:
    """Client-facing trust signals — no PII; aggregate counts only."""
    domains = (
        "revenue_outreach",
        "procurement_intake",
        "delivery_execution",
        "support_desk_resolution",
    )
    governed = []
    for domain in domains:
        rules = workflow_controls(domain)
        governed.append(
            {
                "domain": domain,
                "approval_required_rules": sum(1 for r in rules if r.approval_required),
                "governed": len(rules) > 0,
            }
        )
    return {
        "approval_first": True,
        "cold_outreach_automation": False,
        "workflow_domains": governed,
        "pdpl_contactability_ref": "docs/ops/PDPL_CLOSURE_CHECKLIST_AR.md",
        "trust_pack_ref": "docs/strategic/ENTERPRISE_TRUST_COMPLIANCE_PACK_AR.md",
    }
