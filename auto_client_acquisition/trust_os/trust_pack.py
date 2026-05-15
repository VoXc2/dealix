"""Enterprise Trust Pack — assembled procurement-facing trust document.

The Trust Pack is an 11-section governance disclosure that enterprise
procurement teams read before signing. It states plainly what Dealix
does, what it refuses to do, and how every AI run is governed.
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

_DISCLAIMER = (
    "Estimated outcomes are not guaranteed outcomes / "
    "النتائج التقديرية ليست نتائج مضمونة."
)

# The 11 non-negotiables, restated for procurement.
_NON_NEGOTIABLES: tuple[str, ...] = (
    "No scraping — web, email and LinkedIn scraping engines are forbidden.",
    "No cold WhatsApp — cold WhatsApp automation is blocked at runtime.",
    "No LinkedIn automation — LinkedIn automation is blocked at runtime.",
    "No fake / un-sourced claims — unverifiable claims are redacted.",
    "No guaranteed sales outcomes — guarantee language is never produced.",
    "No PII in logs — personal data is redacted before any persistence.",
    "No source-less knowledge answers — every AI run needs a Source Passport.",
    "No external action without approval — external sends require approval.",
    "No agent without identity — every agent has a registered identity card.",
    "No project without Proof Pack — delivery produces a scored Proof Pack.",
    "No project without Capital Asset — each engagement leaves a reusable asset.",
)


def _refuses_section() -> str:
    lines = ["Dealix refuses, by design, the following:"]
    lines.extend(f"- {rule}" for rule in _NON_NEGOTIABLES)
    return "\n".join(lines)


# Ordered (title, key, body) tuples for the 11 Trust Pack sections.
_SECTION_SPEC: tuple[tuple[str, str, str], ...] = (
    (
        "What Dealix Does",
        "what_dealix_does",
        "Dealix runs governed AI operations for revenue intelligence: it "
        "ranks accounts, drafts outreach, and assembles evidence — always "
        "under human review.",
    ),
    (
        "What Dealix Refuses",
        "what_dealix_refuses",
        _refuses_section(),
    ),
    (
        "Data Handling",
        "data_handling",
        "Customer data is tenant-scoped. Personal data is redacted before "
        "persistence and is never used to train shared models.",
    ),
    (
        "Source Passport Policy",
        "source_passport_policy",
        "No AI run executes without a validated Source Passport describing "
        "where the input data came from and the consent basis for its use.",
    ),
    (
        "Governance Runtime",
        "governance_runtime",
        "Every action passes a governance decision (allow, allow with "
        "review, require approval, draft only, or block) before it leaves "
        "the system.",
    ),
    (
        "AI Run Ledger",
        "ai_run_ledger",
        "Each AI run is recorded in an append-only, PII-redacted audit "
        "ledger so the full evidence chain can be reconstructed on demand.",
    ),
    (
        "Human Oversight",
        "human_oversight",
        "A named human owner reviews drafts and decisions. Autonomy is "
        "capped; fully autonomous operation is not offered.",
    ),
    (
        "Approval Workflow",
        "approval_workflow",
        "External sends, publications, and PII-bearing outputs are routed "
        "to an approval queue before they can leave the platform.",
    ),
    (
        "Proof Pack Standard",
        "proof_pack_standard",
        "Delivery produces a scored 14-section Proof Pack. Retainer "
        "eligibility requires a proof score of at least 80.",
    ),
    (
        "Incident Response",
        "incident_response",
        "Security and data incidents follow a documented response plan, "
        "including breach notification within 72 hours.",
    ),
    (
        "Client Responsibilities",
        "client_responsibilities",
        "Clients supply lawful data with a valid consent basis, name a "
        "workflow owner, and review outputs before external use.",
    ),
)


@dataclass(frozen=True, slots=True)
class TrustPack:
    """An assembled enterprise Trust Pack for a single prospect."""

    customer_handle: str
    generated_at: str
    sections: dict[str, str] = field(default_factory=dict)
    section_titles: dict[str, str] = field(default_factory=dict)
    governance_decision: str = "allow_with_review"

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_handle": self.customer_handle,
            "generated_at": self.generated_at,
            "sections": dict(self.sections),
            "section_titles": dict(self.section_titles),
            "governance_decision": self.governance_decision,
            "disclaimer": _DISCLAIMER,
        }

    def to_markdown(self) -> str:
        lines = [
            f"# Dealix Trust Pack — {self.customer_handle}",
            "",
            f"_Generated: {self.generated_at}_",
            "",
        ]
        for title, key, _ in _SECTION_SPEC:
            lines.append(f"## {title}")
            lines.append("")
            lines.append(self.sections.get(key, ""))
            lines.append("")
        lines.append("---")
        lines.append(f"_{_DISCLAIMER}_")
        return "\n".join(lines)


def assemble_trust_pack(*, customer_handle: str = "(prospect)") -> TrustPack:
    """Assemble the 11-section enterprise Trust Pack for a prospect."""
    sections = {key: body for _, key, body in _SECTION_SPEC}
    section_titles = {key: title for title, key, _ in _SECTION_SPEC}
    return TrustPack(
        customer_handle=customer_handle or "(prospect)",
        generated_at=datetime.now(timezone.utc).isoformat(),
        sections=sections,
        section_titles=section_titles,
        governance_decision="allow_with_review",
    )


__all__ = [
    "ENTERPRISE_TRUST_SECTIONS",
    "TRUST_PACK_MARKDOWN_PATH",
    "TrustPack",
    "assemble_trust_pack",
]
