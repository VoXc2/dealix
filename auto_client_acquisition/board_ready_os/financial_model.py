"""Financial model — minimal scale gates for board discipline."""

from __future__ import annotations

from enum import StrEnum


class RevenueLine(StrEnum):
    DIAGNOSTICS = "diagnostics"
    SPRINTS = "sprints"
    RETAINERS = "retainers"
    PLATFORM_WORKSPACE = "platform_workspace"
    ACADEMY_PARTNERS = "academy_partners"


MIN_GROSS_MARGIN_PCT_FOR_SCALE = 40.0


def revenue_line_ok_for_scale(line: RevenueLine) -> bool:
    """Later phases may be pre-revenue; still valid portfolio lines."""
    return line in RevenueLine


def unit_economics_scale_ok(
    *,
    gross_margin_pct: float,
    proof_strength_ok: bool,
    scope_creep_high: bool,
) -> tuple[bool, tuple[str, ...]]:
    """Board rule: weak margin, weak proof, or scope creep → do not scale the offer."""
    errs: list[str] = []
    if gross_margin_pct < MIN_GROSS_MARGIN_PCT_FOR_SCALE:
        errs.append("gross_margin_too_low_for_scale")
    if not proof_strength_ok:
        errs.append("proof_too_weak_for_scale")
    if scope_creep_high:
        errs.append("scope_creep_blocks_scale")
    return not errs, tuple(errs)
