"""Enterprise trust pack — section outline plus a deterministic assembler."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

ENTERPRISE_TRUST_SECTIONS: tuple[str, ...] = (
    "what_dealix_does",
    "what_dealix_does_not_do",
    "data_handling",
    "ai_governance",
    "proof",
    "human_oversight",
)

TRUST_PACK_MARKDOWN_PATH = "docs/trust/ENTERPRISE_TRUST_PACK.md"

NON_NEGOTIABLES: tuple[str, ...] = (
    "No scraping",
    "No cold WhatsApp",
    "No LinkedIn automation",
    "No fake / un-sourced claims",
    "No guaranteed sales outcomes",
    "No PII in logs",
    "No source-less knowledge answers",
    "No external action without approval",
    "No agent without identity",
    "No project without Proof Pack",
    "No project without Capital Asset",
)

_DISCLAIMER_EN = "Estimated outcomes are not guaranteed outcomes"
_DISCLAIMER_AR = "النتائج التقديرية ليست نتائج مضمونة"

_SECTION_TITLES: dict[str, str] = {
    "what_dealix_does": "What Dealix Does",
    "what_dealix_refuses": "What Dealix Refuses",
    "data_handling": "Data Handling",
    "source_passport_policy": "Source Passport Policy",
    "governance_runtime": "Governance Runtime",
    "ai_run_ledger": "AI Run Ledger",
    "human_oversight": "Human Oversight",
    "approval_workflow": "Approval Workflow",
    "proof_pack_standard": "Proof Pack Standard",
    "incident_response": "Incident Response",
    "client_responsibilities": "Client Responsibilities",
}


@dataclass(frozen=True, slots=True)
class TrustPack:
    """Assembled trust pack for an enterprise procurement preview."""

    customer_handle: str | None
    sections: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_handle": self.customer_handle,
            "sections": self.sections,
            "disclaimer_en": _DISCLAIMER_EN,
            "disclaimer_ar": _DISCLAIMER_AR,
        }

    def to_markdown(self) -> str:
        handle = self.customer_handle or "enterprise prospect"
        lines: list[str] = [f"# Dealix Trust Pack — {handle}", ""]
        for key in _SECTION_TITLES:
            lines.append(f"## {_SECTION_TITLES[key]}")
            body = self.sections[key]
            if isinstance(body, (list, tuple)):
                lines.extend(f"- {item}" for item in body)
            else:
                lines.append(str(body))
            lines.append("")
        lines.extend(
            [
                "## Disclaimer",
                _DISCLAIMER_EN + ".",
                _DISCLAIMER_AR + ".",
            ]
        )
        return "\n".join(lines)


def assemble_trust_pack(customer_handle: str | None = None) -> TrustPack:
    """Build the 11-section trust pack (deterministic, no live data)."""
    sections: dict[str, Any] = {
        "what_dealix_does": (
            "Dealix builds source-backed revenue intelligence for Saudi B2B "
            "service businesses, with governance and proof at every step."
        ),
        "what_dealix_refuses": list(NON_NEGOTIABLES),
        "data_handling": (
            "Client data stays tenant-scoped. PII never enters logs. "
            "External use of PII requires explicit approval."
        ),
        "source_passport_policy": (
            "Every knowledge source carries a Source Passport. No passport "
            "means no AI answer is produced from that source."
        ),
        "governance_runtime": (
            "Every action passes the governance runtime, which returns one of "
            "seven decisions and blocks forbidden channels and unsafe claims."
        ),
        "ai_run_ledger": (
            "Every AI run is recorded with an identity, inputs and decision so "
            "actions are auditable after the fact."
        ),
        "human_oversight": (
            "A human reviews and approves outputs before any external action. "
            "Automation never sends without sign-off."
        ),
        "approval_workflow": (
            "External actions and PII use route through an approval matrix; "
            "high-risk steps require named approver confirmation."
        ),
        "proof_pack_standard": (
            "Every project ships a 14-section Proof Pack with a score and tier "
            "so claims are evidenced, not asserted."
        ),
        "incident_response": (
            "Incidents are logged, triaged and disclosed to the client with a "
            "remediation plan; no silent failure."
        ),
        "client_responsibilities": (
            "Clients provide lawful, consented data, name an owner, and accept "
            "the governance model before delivery begins."
        ),
    }
    return TrustPack(customer_handle=customer_handle, sections=sections)


__all__ = [
    "ENTERPRISE_TRUST_SECTIONS",
    "NON_NEGOTIABLES",
    "TRUST_PACK_MARKDOWN_PATH",
    "TrustPack",
    "assemble_trust_pack",
]
