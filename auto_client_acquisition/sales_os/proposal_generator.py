"""Proposal skeleton generator — deterministic structure (copy reviewed by humans)."""

from __future__ import annotations

from auto_client_acquisition.sales_os.proposal_sections import PROPOSAL_SECTION_KEYS


def build_proposal_skeleton(*, client_label: str, sprint_name: str) -> dict[str, str]:
    """Return empty-ish sections with two non-negotiable statements prefilled."""
    out = dict.fromkeys(PROPOSAL_SECTION_KEYS, "")
    out["recommended_sprint"] = sprint_name
    out["problem"] = f"Prepared for {client_label} — complete during discovery."
    out["no_sales_guarantee_statement"] = (
        "This sprint does not promise sales outcomes. "
        "It builds a governed revenue capability and produces proof of readiness, "
        "prioritization, and next actions."
    )
    out["governance_boundaries"] = (
        "No scraping. No cold WhatsApp automation. No LinkedIn automation. "
        "No guaranteed sales claims. External actions are draft/approval-first."
    )
    return out


__all__ = ["build_proposal_skeleton"]
