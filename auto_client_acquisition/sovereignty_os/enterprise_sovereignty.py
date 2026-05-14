"""Enterprise sovereignty — trust ladder alignment."""

from __future__ import annotations

from auto_client_acquisition.global_grade_os.enterprise_trust import (
    ENTERPRISE_TRUST_LADDER,
    highest_satisfied_trust_level,
    trust_level_satisfied,
)

__all__ = [
    "ENTERPRISE_TRUST_LADDER",
    "enterprise_maturity_tag",
    "enterprise_readiness_summary",
    "highest_satisfied_trust_level",
    "trust_level_satisfied",
]


def enterprise_readiness_summary(implemented: frozenset[str]) -> tuple[int, str]:
    lvl = highest_satisfied_trust_level(implemented)
    tag = enterprise_maturity_tag(lvl)
    return lvl, tag


def enterprise_maturity_tag(level: int) -> str:
    if level >= 5:
        return "enterprise_ai_os_ready_path"
    if level >= 3:
        return "control_plane_ready"
    if level >= 1:
        return "trust_pack_minimum"
    return "pre_enterprise"
