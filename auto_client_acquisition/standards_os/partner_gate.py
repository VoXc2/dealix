"""Partner certification gate — covenant rules (delegates to ecosystem_os)."""

from __future__ import annotations

from auto_client_acquisition.ecosystem_os.partner_score import (
    PARTNER_GATE_CRITERIA,
    partner_gate_passes,
)

PARTNER_COVENANT_RULES = PARTNER_GATE_CRITERIA


def partner_certification_gate(criteria_met: frozenset[str]) -> tuple[bool, tuple[str, ...]]:
    """Partner must satisfy the same covenant checklist before certified delivery."""
    return partner_gate_passes(criteria_met)
