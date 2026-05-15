"""Enterprise trust pack — section outline + deterministic assembler.

``assemble_trust_pack`` produces a ``TrustPack`` for enterprise procurement
reviews: 11 sections covering what Dealix does, what it refuses, data handling,
governance runtime and the 11 non-negotiables. Deterministic — no LLM.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
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

# The 11 non-negotiables — single source for the "what_dealix_refuses" section.
NON_NEGOTIABLES: tuple[str, ...] = (
    "No scraping — no web / LinkedIn / email scraping engines.",
    "No cold WhatsApp — cold WhatsApp outreach is blocked at runtime.",
    "No LinkedIn automation — LinkedIn automation is blocked at runtime.",
    "No fake / un-sourced claims — guaranteed sales language is redacted.",
    "No guaranteed sales outcomes — outcomes are estimated, never guaranteed.",
    "No PII in logs — personal data is redacted before persistence.",
    "No source-less knowledge answers — every AI use needs a Source Passport.",
    "No external action without approval — sends / publishes require approval.",
    "No agent without identity — every agent has a registered identity card.",
    "No project without Proof Pack — delivery is closed with a Proof Pack.",
    "No project without Capital Asset — every engagement leaves a reusable asset.",
)

# Section titles + body text. Keys are the canonical 11 section ids.
_SECTIONS: dict[str, tuple[str, str]] = {
    "what_dealix_does": (
        "What Dealix Does",
        "Dealix runs a governed, human-supervised revenue intelligence service. "
        "It ranks opportunities, drafts Arabic outreach, and assembles auditable "
        "Proof Packs from customer-provided, source-passported data.",
    ),
    "what_dealix_refuses": (
        "What Dealix Refuses",
        "Dealix enforces 11 non-negotiables at runtime:\n"
        + "\n".join(f"- {rule}" for rule in NON_NEGOTIABLES),
    ),
    "data_handling": (
        "Data Handling",
        "Customer data is tenant-scoped and PII-redacted before any log write. "
        "Processing aligns with PDPL; data is retained only as long as the "
        "engagement requires and is deletable on request.",
    ),
    "source_passport_policy": (
        "Source Passport Policy",
        "No AI run executes without a validated Source Passport describing the "
        "data origin, consent basis and quality. Source-less knowledge answers "
        "are refused.",
    ),
    "governance_runtime": (
        "Governance Runtime",
        "Every action passes the governance runtime, which returns one of seven "
        "decisions (allow, allow_with_review, draft_only, require_approval, "
        "redact, block, escalate). Forbidden channels and unsafe claims are "
        "blocked deterministically.",
    ),
    "ai_run_ledger": (
        "AI Run Ledger",
        "Every AI run is recorded as an append-only, tenant-scoped audit event "
        "with its source references and governance decision, enabling full "
        "replay for enterprise audit.",
    ),
    "human_oversight": (
        "Human Oversight",
        "Dealix is human-supervised. External sends and publications require "
        "explicit founder / operator approval; no automated cold outreach is "
        "performed.",
    ),
    "approval_workflow": (
        "Approval Workflow",
        "External actions enter an approval queue. An accountable human reviews "
        "and explicitly approves before any send or publish. Approvals are "
        "logged with actor identity and timestamp.",
    ),
    "proof_pack_standard": (
        "Proof Pack Standard",
        "Each engagement closes with a 14-section Proof Pack carrying a score "
        "and tier. Estimated value is never promoted to verified value without "
        "a source reference.",
    ),
    "incident_response": (
        "Incident Response",
        "Security and data incidents follow a documented response procedure, "
        "including customer and authority notification within 72 hours where "
        "PDPL requires it.",
    ),
    "client_responsibilities": (
        "Client Responsibilities",
        "The client provides accurate, lawfully-obtained data with a valid "
        "consent basis, reviews drafts before any approved send, and signs off "
        "on published proof.",
    ),
}


@dataclass
class TrustPack:
    """Assembled enterprise trust pack for one prospect / customer."""

    customer_handle: str
    generated_at: str
    sections: dict[str, str] = field(default_factory=dict)
    non_negotiables: list[str] = field(default_factory=list)
    section_outline: tuple[str, ...] = ENTERPRISE_TRUST_SECTIONS

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_handle": self.customer_handle,
            "generated_at": self.generated_at,
            "sections": dict(self.sections),
            "non_negotiables": list(self.non_negotiables),
            "section_outline": list(self.section_outline),
        }

    def to_markdown(self) -> str:
        lines: list[str] = []
        lines.append(f"# Dealix Trust Pack — {self.customer_handle}")
        lines.append("")
        lines.append(f"**Generated:** {self.generated_at}")
        lines.append("")
        for key, body in self.sections.items():
            title = _SECTIONS.get(key, (key.replace("_", " ").title(), ""))[0]
            lines.append(f"## {title}")
            lines.append("")
            lines.append(body)
            lines.append("")
        lines.append("---")
        lines.append(
            "_Estimated outcomes are not guaranteed outcomes. "
            "النتائج التقديرية ليست نتائج مضمونة._"
        )
        return "\n".join(lines)


def assemble_trust_pack(customer_handle: str = "prospect") -> TrustPack:
    """Assemble the 11-section enterprise trust pack. Deterministic."""
    handle = customer_handle or "prospect"
    sections = {key: body for key, (_title, body) in _SECTIONS.items()}
    return TrustPack(
        customer_handle=handle,
        generated_at=datetime.now(timezone.utc).isoformat(),
        sections=sections,
        non_negotiables=list(NON_NEGOTIABLES),
    )


__all__ = [
    "ENTERPRISE_TRUST_SECTIONS",
    "NON_NEGOTIABLES",
    "TRUST_PACK_MARKDOWN_PATH",
    "TrustPack",
    "assemble_trust_pack",
]
