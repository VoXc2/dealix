"""Enterprise Sovereignty — sell only at a level you already operate.

See ``docs/sovereignty/ENTERPRISE_SOVEREIGNTY.md``. Builds on the
``command_control_os.enterprise_readiness`` ladder.
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.command_control_os.enterprise_readiness import (
    ReadinessLevel,
    can_sell_level,
)


@dataclass(frozen=True)
class SovereignEnterpriseSale:
    allowed: bool
    target_level: ReadinessLevel
    missing_requirements: tuple[str, ...]
    reason: str


def can_sell_enterprise_level(
    target: ReadinessLevel,
    *,
    operated_requirements: frozenset[str],
) -> SovereignEnterpriseSale:
    """Sovereign wrapper around ``can_sell_level``.

    Adds a human-readable reason and packages the verdict for use by
    Revenue and the Command Center.
    """

    allowed, missing = can_sell_level(
        target, operated_requirements=operated_requirements
    )
    if allowed:
        reason = "operates_required_lower_levels"
    else:
        reason = "missing_requirements_for_target_level"
    return SovereignEnterpriseSale(
        allowed=allowed,
        target_level=target,
        missing_requirements=missing,
        reason=reason,
    )
