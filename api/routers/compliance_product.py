"""Compliance product surface — PDPL checklist, Trust Pack summary, ZATCA posture.

Read-only endpoints for Saudi moat / enterprise procurement. No PII returned.
"""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.compliance_os.consent_ledger import ALL_BASES, LawfulBasis
from auto_client_acquisition.compliance_os.data_subject_requests import DSR_TYPES, SLA_DAYS
from auto_client_acquisition.compliance_os.ropa import build_ropa
from auto_client_acquisition.compliance_os.vendor_registry import DEFAULT_VENDORS, vendors_summary
from auto_client_acquisition.trust_os.trust_pack import (
    TRUST_PACK_MARKDOWN_PATH,
    assemble_trust_pack,
)

router = APIRouter(prefix="/api/v1/compliance-product", tags=["compliance-product"])

_REPO_ROOT = Path(__file__).resolve().parents[2]

_ENTERPRISE_PACKAGE_PATHS: tuple[str, ...] = (
    "docs/transformation/enterprise_package/pilot_scope_template.md",
    "docs/transformation/enterprise_package/trust_compliance_pack_template.md",
    "docs/transformation/enterprise_package/procurement_response_kit_template.md",
    "docs/transformation/enterprise_package/roi_realization_narrative_template.md",
    "docs/commercial/operations/TRUST_PACK_PROPOSAL_AR.md",
    "docs/trust/ENTERPRISE_TRUST_PACK.md",
)


def _module_present(name: str) -> bool:
    try:
        importlib.import_module(name)
        return True
    except Exception:
        return False


def build_pdpl_checklist() -> dict[str, Any]:
    """ROPA + consent + DSR checklist from compliance_os (no live PII)."""
    ropa = build_ropa(
        customer_id="dealix_platform",
        customer_name="Dealix Platform",
        dpo_name="Founder (interim DPO)",
        dpo_email="privacy@dealix.me",
    )
    return {
        "governance_decision": "allow",
        "ropa": {
            "summary": ropa.to_json(),
            "activity_count": len(ropa.activities),
            "export_formats": ["json", "csv"],
        },
        "consent": {
            "lawful_bases": list(ALL_BASES),
            "record_types": ["consent_granted", "opt_out", "lawful_basis_set"],
            "default_basis_b2b": LawfulBasis.LEGITIMATE_INTEREST,
            "channels": ["email", "whatsapp", "linkedin", "all"],
            "policy_ar": "موافقة صريحة أو مصلحة مشروعة مسجّلة قبل أي تواصل خارجي",
        },
        "dsr": {
            "types": list(DSR_TYPES),
            "sla_days_by_type": dict(SLA_DAYS),
            "workflow": ["open", "in_progress", "awaiting_verification", "completed", "rejected"],
            "sop_ref": "docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md",
        },
        "vendors": {
            "summary": vendors_summary(),
            "registered_count": len(DEFAULT_VENDORS),
        },
        "founder_checklist_ref": "docs/commercial/operations/founder_pdpl_compliance_pass.yaml",
    }


def build_trust_pack_summary() -> dict[str, Any]:
    """Enterprise Trust Pack + linked doc paths (read-only assembly)."""
    pack = assemble_trust_pack(customer_handle="enterprise_prospect")
    doc_inventory: list[dict[str, Any]] = []
    for rel in _ENTERPRISE_PACKAGE_PATHS:
        path = _REPO_ROOT / rel
        doc_inventory.append(
            {
                "path": rel.replace("\\", "/"),
                "exists": path.is_file(),
                "size_bytes": path.stat().st_size if path.is_file() else 0,
            }
        )
    return {
        "governance_decision": pack.governance_decision,
        "trust_pack": pack.to_dict(),
        "markdown_canonical_path": TRUST_PACK_MARKDOWN_PATH,
        "enterprise_package_docs": doc_inventory,
        "non_negotiables_count": 11,
        "disclaimer_ar": "حPack ثقة — ليس شهادة امتثال قانونية",
    }


def build_zatca_readiness() -> dict[str, Any]:
    """Read-only ZATCA e-invoicing posture (module presence + policy refs)."""
    zatca_ok = _module_present("integrations.zatca")
    return {
        "governance_decision": "allow",
        "phase_2_e_invoice": {
            "implemented": zatca_ok,
            "evidence": "integrations.zatca (UBL 2.1 XML builder, QR TLV, invoice chaining)",
        },
        "fatoorah_api": {
            "implemented": zatca_ok,
            "evidence": "integrations.zatca Fatoorah client for B2B clearance + B2C reporting",
        },
        "invoice_chaining": {
            "implemented": zatca_ok,
            "note": "Previous invoice hash on every invoice (Phase 2 mandate)",
        },
        "retention_years": 6,
        "router_ref": "/api/v1/zatca",
        "policy_docs": [
            "docs/ops/RAILWAY_PRODUCTION_POLICY_AR.md",
            "docs/commercial/operations/TRUST_PACK_PROPOSAL_AR.md",
        ],
    }


@router.get("/pdpl-checklist")
async def pdpl_checklist() -> dict[str, Any]:
    """ROPA / consent / DSR checklist from compliance_os."""
    return build_pdpl_checklist()


@router.get("/trust-pack")
async def trust_pack_summary() -> dict[str, Any]:
    """Enterprise Trust Pack summary + linked documentation paths."""
    return build_trust_pack_summary()


@router.get("/zatca-readiness")
async def zatca_readiness() -> dict[str, Any]:
    """Read-only ZATCA e-invoicing posture."""
    return build_zatca_readiness()
