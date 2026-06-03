"""Opportunity cost — project acceptance vs strategic capital focus."""

from __future__ import annotations


def opportunity_acceptance_ok(
    *,
    builds_strategic_asset: bool,
    buyer_clear: bool,
    proof_likely_useful: bool,
    likely_annoying_revenue: bool,
    playbook_potential: bool,
    sector_strategic: bool = True,
) -> tuple[bool, tuple[str, ...]]:
    """Weak signals + annoying revenue pattern → defer or shrink engagement."""
    blockers: list[str] = []
    if not buyer_clear:
        blockers.append("buyer_unclear")
    if likely_annoying_revenue and not builds_strategic_asset:
        blockers.append("annoying_revenue_without_strategic_asset")
    if not proof_likely_useful and not playbook_potential:
        blockers.append("low_learning_per_dollar")
    if not sector_strategic and not builds_strategic_asset:
        blockers.append("sector_not_strategic")
    return not blockers, tuple(blockers)
