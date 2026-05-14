"""Compliance Index — maps PDPL articles + ZATCA Phase 2 requirements to
repo evidence (file paths, test files, code refs).

Used by the Trust Pack PDF for enterprise procurement reviews.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class ComplianceItem:
    framework: str  # PDPL | ZATCA | Internal
    reference: str  # e.g. "PDPL Article 5"
    requirement: str
    evidence_paths: list[str] = field(default_factory=list)
    test_paths: list[str] = field(default_factory=list)
    status: str = "implemented"  # implemented | partial | pending

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ComplianceIndex:
    customer_id: str
    generated_at: str
    items: list[ComplianceItem] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "generated_at": self.generated_at,
            "items": [i.to_dict() for i in self.items],
            "by_framework": self._by_framework(),
        }

    def _by_framework(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for i in self.items:
            out[i.framework] = out.get(i.framework, 0) + 1
        return out


# Static map of compliance items. Updates here when new tests/modules land.
_STATIC_ITEMS = (
    # PDPL articles
    ComplianceItem(
        framework="PDPL",
        reference="Article 5 — Consent",
        requirement="Explicit consent before processing personal data.",
        evidence_paths=[
            "auto_client_acquisition/consent_table.py",
            "auto_client_acquisition/customer_data_plane/consent_registry.py",
        ],
        test_paths=["tests/test_pii_external_requires_approval.py"],
        status="implemented",
    ),
    ComplianceItem(
        framework="PDPL",
        reference="Article 13 — Right to Erasure",
        requirement="Customer-initiated deletion request handled.",
        evidence_paths=["api/routers/pdpl_dsar.py"],
        test_paths=["tests/test_pdpl_dsar.py"],
        status="implemented",
    ),
    ComplianceItem(
        framework="PDPL",
        reference="Article 14 — Data Portability",
        requirement="Customer can export their data in a portable format.",
        evidence_paths=["api/routers/pdpl_dsar.py"],
        test_paths=["tests/test_pdpl_dsar.py"],
        status="partial",
    ),
    ComplianceItem(
        framework="PDPL",
        reference="Article 18 — Audit Trail",
        requirement="Every data access + decision recorded.",
        evidence_paths=[
            "auto_client_acquisition/auditability_os/audit_event.py",
            "auto_client_acquisition/auditability_os/evidence_chain.py",
            "auto_client_acquisition/proof_ledger/file_backend.py",
        ],
        test_paths=["tests/test_audit_export.py"],
        status="implemented",
    ),
    ComplianceItem(
        framework="PDPL",
        reference="Article 21 — Breach Notification (72h)",
        requirement="Customer + authority notified within 72h.",
        evidence_paths=["docs/ops/INCIDENT_RESPONSE_QUICKCARD.md"],
        test_paths=[],
        status="documented",
    ),
    # ZATCA Phase 2
    ComplianceItem(
        framework="ZATCA",
        reference="Phase 2 — E-Invoicing",
        requirement="UBL 2.1 XML + TLV QR code on every B2B invoice.",
        evidence_paths=["integrations/zatca.py", "api/routers/zatca.py"],
        test_paths=["tests/test_zatca_invoice.py", "tests/test_zatca_phase2.py"],
        status="implemented",
    ),
    # Internal non-negotiables
    ComplianceItem(
        framework="Internal",
        reference="No scraping",
        requirement="Forbid web/LinkedIn/email scraping engines.",
        evidence_paths=[
            "auto_client_acquisition/governance_os/channel_policy.py",
            "auto_client_acquisition/governance_os/runtime_decision.py",
        ],
        test_paths=["tests/test_no_scraping_engine.py"],
        status="implemented",
    ),
    ComplianceItem(
        framework="Internal",
        reference="No cold WhatsApp automation",
        requirement="Cold WhatsApp blocked at runtime.",
        evidence_paths=[
            "auto_client_acquisition/whatsapp_safe_send.py",
            "auto_client_acquisition/governance_os/channel_policy.py",
        ],
        test_paths=["tests/test_no_cold_whatsapp.py"],
        status="implemented",
    ),
    ComplianceItem(
        framework="Internal",
        reference="No LinkedIn automation",
        requirement="LinkedIn automation blocked at runtime.",
        evidence_paths=["auto_client_acquisition/governance_os/channel_policy.py"],
        test_paths=["tests/test_no_linkedin_automation.py"],
        status="implemented",
    ),
    ComplianceItem(
        framework="Internal",
        reference="No fake / unsourced claims",
        requirement="Guaranteed sales language redacted.",
        evidence_paths=["auto_client_acquisition/governance_os/claim_safety.py"],
        test_paths=["tests/test_no_guaranteed_claims.py"],
        status="implemented",
    ),
    ComplianceItem(
        framework="Internal",
        reference="No PII in logs",
        requirement="PII redacted before persistence.",
        evidence_paths=[
            "auto_client_acquisition/customer_data_plane/pii_redactor.py",
            "auto_client_acquisition/friction_log/sanitizer.py",
            "api/middleware/bopla_redaction.py",
        ],
        test_paths=["tests/test_friction_log.py"],
        status="implemented",
    ),
    ComplianceItem(
        framework="Internal",
        reference="No source-less AI",
        requirement="Every AI use requires a Source Passport.",
        evidence_paths=["auto_client_acquisition/data_os/source_passport.py"],
        test_paths=["tests/test_no_source_passport_no_ai.py"],
        status="implemented",
    ),
    ComplianceItem(
        framework="Internal",
        reference="No external action without approval",
        requirement="External send / publish requires approval_center.",
        evidence_paths=[
            "auto_client_acquisition/approval_center/",
            "auto_client_acquisition/safe_send_gateway/",
        ],
        test_paths=["tests/test_pii_external_requires_approval.py"],
        status="implemented",
    ),
    ComplianceItem(
        framework="Internal",
        reference="No agent without identity",
        requirement="Every agent has a registered AgentCard with kill_switch_owner.",
        evidence_paths=[
            "auto_client_acquisition/agent_os/agent_card.py",
            "auto_client_acquisition/agent_os/agent_registry.py",
        ],
        test_paths=["tests/test_agent_os.py"],
        status="implemented",
    ),
    ComplianceItem(
        framework="Internal",
        reference="No project without Proof Pack",
        requirement="Retainer eligibility requires proof_score >= 80.",
        evidence_paths=["auto_client_acquisition/proof_os/proof_pack.py"],
        test_paths=["tests/test_proof_pack_required.py"],
        status="implemented",
    ),
    ComplianceItem(
        framework="Internal",
        reference="No project without Capital Asset",
        requirement="Every engagement registers >= 1 reusable asset.",
        evidence_paths=["auto_client_acquisition/capital_os/capital_ledger.py"],
        test_paths=["tests/test_delivery_sprint.py"],
        status="implemented",
    ),
)


def build_compliance_index(*, customer_id: str = "(generic)") -> ComplianceIndex:
    return ComplianceIndex(
        customer_id=customer_id,
        generated_at=datetime.now(timezone.utc).isoformat(),
        items=list(_STATIC_ITEMS),
    )


__all__ = ["ComplianceIndex", "ComplianceItem", "build_compliance_index"]
