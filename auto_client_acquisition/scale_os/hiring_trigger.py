"""Hiring recommendations ordered by sovereign scale maturity."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class HiringRole(IntEnum):
    DELIVERY_ANALYST = 1
    PRODUCT_ENGINEER = 2
    CUSTOMER_SUCCESS = 3
    GOVERNANCE_REVIEWER = 4


@dataclass(frozen=True, slots=True)
class HiringSignals:
    offer_clear: bool = True
    checklists_exist: bool = False
    repeated_projects: bool = False
    founder_bottleneck: bool = False
    manual_steps_repeat: bool = False
    modules_needed: bool = False
    retainers_active: bool = False
    workspace_critical: bool = False
    sensitive_data_or_enterprise: bool = False
    high_ai_output_review_load: bool = False


def recommend_hires(s: HiringSignals) -> list[HiringRole]:
    """Return ordered unique roles to hire; empty if offer unclear."""
    if not s.offer_clear:
        return []
    out: list[HiringRole] = []
    if s.checklists_exist and s.repeated_projects and s.founder_bottleneck:
        out.append(HiringRole.DELIVERY_ANALYST)
    if s.manual_steps_repeat and s.modules_needed:
        out.append(HiringRole.PRODUCT_ENGINEER)
    if s.retainers_active and s.workspace_critical:
        out.append(HiringRole.CUSTOMER_SUCCESS)
    if s.sensitive_data_or_enterprise and s.high_ai_output_review_load:
        out.append(HiringRole.GOVERNANCE_REVIEWER)
    seen: set[HiringRole] = set()
    unique: list[HiringRole] = []
    for r in out:
        if r not in seen:
            seen.add(r)
            unique.append(r)
    return unique
