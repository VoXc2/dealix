"""Enterprise tier — service catalog tests.

Asserts the 5 enterprise offerings meet:
- exactly 5, all customer_journey_stage == "enterprise"
- custom pricing with populated, ordered price ranges
- Article 4: no live_send / live_charge action modes
- Article 8: no "guaranteed" / "نضمن" language anywhere
- required hard gates declared
"""

from __future__ import annotations

import re

from auto_client_acquisition.service_catalog.registry import (
    ENTERPRISE_SERVICE_IDS,
    get_offering,
    list_enterprise_offerings,
)

EXPECTED_IDS = {
    "enterprise_ai_operating_system",
    "ai_revenue_transformation",
    "company_brain_knowledge_os",
    "ai_governance_trust_program",
    "executive_intelligence_center",
}


def test_exactly_five_enterprise_offerings() -> None:
    offerings = list_enterprise_offerings()
    assert len(offerings) == 5, f"expected 5, got {len(offerings)}"
    assert ENTERPRISE_SERVICE_IDS == EXPECTED_IDS


def test_all_tagged_enterprise_stage() -> None:
    for o in list_enterprise_offerings():
        assert o.customer_journey_stage == "enterprise", o.id


def test_custom_pricing_with_ordered_ranges() -> None:
    for o in list_enterprise_offerings():
        assert o.price_unit == "custom", o.id
        assert o.price_sar == 0.0, o.id
        assert o.price_sar_min is not None and o.price_sar_max is not None, o.id
        assert 0 < o.price_sar_min <= o.price_sar_max, o.id
        if o.monthly_fee_sar_min is not None:
            assert o.monthly_fee_sar_max is not None, o.id
            assert 0 < o.monthly_fee_sar_min <= o.monthly_fee_sar_max, o.id


def test_required_hard_gates_present() -> None:
    required = {"no_live_send", "no_live_charge", "no_fake_proof", "no_scraping"}
    for o in list_enterprise_offerings():
        assert required <= set(o.hard_gates), f"{o.id} missing: {required - set(o.hard_gates)}"


def test_no_live_action_modes() -> None:
    forbidden = {"live_send", "live_charge", "auto_send", "auto_charge"}
    for o in list_enterprise_offerings():
        assert not (set(o.action_modes_used) & forbidden), o.id


def test_no_guaranteed_language() -> None:
    patterns = [
        re.compile(r"\bguarantee[ds]?\b", re.IGNORECASE),
        re.compile(r"نضمن"),
    ]
    for o in list_enterprise_offerings():
        text = " ".join([
            o.name_ar, o.name_en, o.kpi_commitment_ar, o.kpi_commitment_en,
            o.refund_policy_ar, o.refund_policy_en, *o.deliverables,
        ])
        for pat in patterns:
            m = pat.search(text)
            assert m is None, f"{o.id}: forbidden token '{m.group(0)}'"


def test_bilingual_and_estimate_flag() -> None:
    for o in list_enterprise_offerings():
        assert o.name_ar.strip() and o.name_en.strip(), o.id
        assert o.name_ar != o.name_en, o.id
        assert o.is_estimate is True, o.id


def test_get_offering_resolves_enterprise_ids() -> None:
    for sid in EXPECTED_IDS:
        assert get_offering(sid) is not None, sid
