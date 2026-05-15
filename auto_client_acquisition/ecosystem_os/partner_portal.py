"""Partner portal (phase) — surface checklist for future distribution hub."""

from __future__ import annotations

PARTNER_PORTAL_SIGNALS: tuple[str, ...] = (
    "partner_leads",
    "certification_status",
    "approved_materials",
    "proof_templates",
    "qa_submissions",
    "commission_status",
)


def partner_portal_coverage_score(signals_tracked: frozenset[str]) -> int:
    if not PARTNER_PORTAL_SIGNALS:
        return 0
    n = sum(1 for s in PARTNER_PORTAL_SIGNALS if s in signals_tracked)
    return (n * 100) // len(PARTNER_PORTAL_SIGNALS)
