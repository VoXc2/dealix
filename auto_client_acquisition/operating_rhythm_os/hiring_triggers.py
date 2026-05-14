"""Hiring rhythm — explicit repeat thresholds; playbook gate first."""

from __future__ import annotations

from auto_client_acquisition.operating_finance_os.hiring_triggers import HireFocus


def consider_delivery_analyst(*, stable_checklist_projects: int) -> bool:
    return stable_checklist_projects >= 3


def consider_product_engineer(*, manual_step_repeat_count: int) -> bool:
    return manual_step_repeat_count >= 5


def consider_customer_success(*, retainers_with_monthly_cadence: int) -> bool:
    return retainers_with_monthly_cadence >= 2


def consider_governance_reviewer(*, enterprise_governance_load: bool) -> bool:
    return enterprise_governance_load


def consider_partner_manager(*, active_partners_qualified_leads: int) -> bool:
    return active_partners_qualified_leads >= 3


def rhythm_hire_focus(
    *,
    stable_checklist_projects: int,
    playbooks_exist: bool,
    manual_step_repeat_count: int,
    retainers_with_monthly_cadence: int,
    enterprise_governance_load: bool,
    founder_delivery_bottleneck: bool,
) -> HireFocus:
    """Priority stack aligned with docs/operating_rhythm/HIRING_RHYTHM.md."""
    if not playbooks_exist:
        return HireFocus.NONE
    if consider_governance_reviewer(enterprise_governance_load=enterprise_governance_load):
        return HireFocus.GOVERNANCE
    if consider_customer_success(
        retainers_with_monthly_cadence=retainers_with_monthly_cadence
    ):
        return HireFocus.CUSTOMER_SUCCESS
    if consider_product_engineer(manual_step_repeat_count=manual_step_repeat_count):
        return HireFocus.PRODUCTIZATION
    if consider_delivery_analyst(
        stable_checklist_projects=stable_checklist_projects
    ) and founder_delivery_bottleneck:
        return HireFocus.DELIVERY
    return HireFocus.NONE
