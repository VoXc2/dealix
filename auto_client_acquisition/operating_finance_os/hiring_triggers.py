"""Hiring focus — bottleneck-driven, not hype-driven."""

from __future__ import annotations

from enum import StrEnum


class HireFocus(StrEnum):
    NONE = "none"
    DELIVERY = "delivery_analyst"
    PRODUCTIZATION = "product_engineer"
    CUSTOMER_SUCCESS = "customer_success_ai_ops"
    GOVERNANCE = "governance_reviewer"


def recommended_hire_focus(
    *,
    founder_delivery_bottleneck: bool,
    playbooks_exist: bool,
    projects_repeat: bool,
    manual_steps_repeat: bool,
    retainers_active: bool,
    enterprise_governance_load: bool,
) -> HireFocus:
    if enterprise_governance_load:
        return HireFocus.GOVERNANCE
    if retainers_active and playbooks_exist:
        return HireFocus.CUSTOMER_SUCCESS
    if manual_steps_repeat and playbooks_exist:
        return HireFocus.PRODUCTIZATION
    if founder_delivery_bottleneck and projects_repeat and playbooks_exist:
        return HireFocus.DELIVERY
    return HireFocus.NONE
