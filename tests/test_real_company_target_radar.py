from __future__ import annotations

import pytest

from dealix.commercial.real_company_target_radar import (
    RealCompanyRecord,
    RealCompanyTargetRadar,
    customer_specific_proposal_allowed,
)


def record(**overrides: object) -> RealCompanyRecord:
    payload: dict[str, object] = {
        "company_id": "sama-stcpay",
        "display_name": "Saudi Digital Payment Company (STC Pay)",
        "en_name": "Saudi Digital Payment Company (STC Pay)",
        "source_url": "https://www.sama.gov.sa/example",
        "source_authority": "SAMA",
        "source_external_id": "stcpay",
        "observed_at": "2026-09-12",
        "sector_id": "finance_fintech_insurance",
        "buyer_role_hypotheses": ["COO", "CIO"],
        "problem_hypotheses": ["PATTERN: regulated operations automation"],
        "diagnostic_families": ["ai_governance", "operations"],
        "offer_match_candidates": ["AI Company OS Setup"],
    }
    payload.update(overrides)
    return RealCompanyRecord(**payload)


def test_research_record_fails_closed_on_relationship() -> None:
    with pytest.raises(ValueError):
        record(relationship=True)


def test_radar_deduplicates_authoritative_identity() -> None:
    radar = RealCompanyTargetRadar()
    radar.add(record())
    radar.add(record(display_name="STC Pay Updated Display Name"))
    assert len(radar.records()) == 1


def test_account_plan_remains_internal_hypothesis() -> None:
    radar = RealCompanyTargetRadar([record()])
    plan = radar.build_account_plan("sama-stcpay")
    assert plan.truth_class == "INTERNAL_HYPOTHESIS"
    assert plan.customer_fact_claims_allowed is False
    assert plan.external_send_allowed is False
    assert plan.proposal_state == "ACCOUNT_PLAN_ONLY"


def test_customer_proposal_gate_requires_real_evidence() -> None:
    assert customer_specific_proposal_allowed() is False
    assert customer_specific_proposal_allowed(qualified_problem_ref="discovery:123") is False

    def resolver(ref: str):
        if ref == "discovery:123":
            return {"truth_class": "QUALIFIED_PROBLEM", "real_interaction": True}
        if ref == "email:456":
            return {"truth_class": "EXPLICIT_CUSTOMER_REQUEST", "real_interaction": True}
        return None

    assert customer_specific_proposal_allowed(
        qualified_problem_ref="discovery:123", evidence_resolver=resolver
    ) is True
    assert customer_specific_proposal_allowed(
        explicit_request_ref="email:456", evidence_resolver=resolver
    ) is True
    assert customer_specific_proposal_allowed(
        qualified_problem_ref="fake", evidence_resolver=resolver
    ) is False


def test_non_https_source_rejected() -> None:
    with pytest.raises(ValueError):
        record(source_url="http://example.com")
