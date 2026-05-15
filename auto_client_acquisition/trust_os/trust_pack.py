"""Enterprise Trust Pack — the governed, bilingual trust brief for prospects.

``assemble_trust_pack()`` builds an 11-section pack covering what Dealix
does, what it refuses (the 11 non-negotiables), data handling, the
source-passport gate, the governance runtime, the AI run ledger, human
oversight, the approval workflow, the proof-pack standard, incident
response and client responsibilities.
"""

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

# Bilingual disclaimer carried on every governed artifact.
DISCLAIMER = (
    "Estimated outcomes are not guaranteed outcomes. "
    "/ النتائج التقديرية ليست نتائج مضمونة."
)

# The 11 non-negotiables (doctrine) — listed verbatim in the pack.
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


@dataclass
class TrustPack:
    """An assembled enterprise trust pack for one prospect."""

    customer_handle: str
    sections: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_handle": self.customer_handle,
            "disclaimer": DISCLAIMER,
            "sections": self.sections,
        }

    def to_markdown(self) -> str:
        lines = [
            f"# Dealix Enterprise Trust Pack — {self.customer_handle}",
            "",
            f"> {DISCLAIMER}",
            "",
        ]
        for key, title in _SECTION_TITLES.items():
            lines += [f"## {title}", "", self.sections.get(key, ""), ""]
        return "\n".join(lines).strip() + "\n"


def assemble_trust_pack(customer_handle: str = "prospect") -> TrustPack:
    """Assemble the 11-section enterprise trust pack."""
    refuses = "Dealix refuses, by doctrine (the 11 non-negotiables):\n" + "\n".join(
        f"- {rule}" for rule in NON_NEGOTIABLES
    )
    sections: dict[str, str] = {
        "what_dealix_does": (
            "Dealix runs a governed AI revenue operation — lead intake, ICP "
            "scoring, pain extraction, qualification and proof-backed delivery — "
            "where AI explores and recommends, deterministic workflows execute, "
            "and humans approve every external move."
        ),
        "what_dealix_refuses": refuses,
        "data_handling": (
            "Customer data is tenant-isolated, PDPL-aligned, and never used to "
            "train shared models. PII is redacted from logs and from retrieved "
            "snippets; S3-sensitive data does not cross KSA borders without a "
            "lawful basis and a DPA."
        ),
        "source_passport_policy": (
            "No data enters AI processing without a Source Passport declaring "
            "origin, owner, allowed use, sensitivity and retention. An invalid "
            "or missing passport blocks the run."
        ),
        "governance_runtime": (
            "Every action passes the governance runtime (decide()), which "
            "returns one of allow / allow_with_review / draft_only / "
            "require_approval / redact / block / escalate before anything runs."
        ),
        "ai_run_ledger": (
            "Every agent run is recorded with its inputs, outputs, tool calls "
            "(intended vs actual) and the resulting governance decision — an "
            "append-only, auditable trail."
        ),
        "human_oversight": (
            "A human owns every external commitment. Drafts are prepared by AI "
            "and released only after founder/operator review."
        ),
        "approval_workflow": (
            "require_approval / escalate decisions enter the Approval Center "
            "with a TTL; an authorised approver must grant or reject before the "
            "action proceeds."
        ),
        "proof_pack_standard": (
            "Every engagement ships a 14-section Proof Pack with sources, "
            "content hashes and a bilingual memo; estimated value is never "
            "presented as verified value."
        ),
        "incident_response": (
            "Incidents follow the rollback runbook: detect, triage, contain, "
            "notify (including SDAIA where required) and roll back — with a "
            "post-incident review."
        ),
        "client_responsibilities": (
            "The client provides accurate source data with a valid passport, "
            "names a workflow owner, and reviews approval items within the "
            "agreed window."
        ),
    }
    return TrustPack(customer_handle=customer_handle, sections=sections)


__all__ = [
    "DISCLAIMER",
    "ENTERPRISE_TRUST_SECTIONS",
    "NON_NEGOTIABLES",
    "TRUST_PACK_MARKDOWN_PATH",
    "TrustPack",
    "assemble_trust_pack",
]
