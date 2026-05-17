"""Founder lead scoring — additive intake formula + classification bands."""

from __future__ import annotations

from auto_client_acquisition.crm_v10.founder_lead_scoring import score_founder_lead
from auto_client_acquisition.crm_v10.pipeline_view import LeadClassification


def test_zero_signals_drops():
    r = score_founder_lead()
    assert r.score == 0
    assert r.classification == LeadClassification.DROP.value


def test_qualified_a_at_threshold():
    # decision_maker 3 + is_b2b 3 + has_crm 3 + uses_ai 3 = 12 → qualified_A.
    r = score_founder_lead(
        decision_maker=True,
        is_b2b=True,
        has_crm_or_revenue_process=True,
        uses_or_plans_ai=True,
    )
    assert r.score == 12
    assert r.classification == LeadClassification.QUALIFIED_A.value


def test_qualified_b_band():
    # is_b2b 3 + has_crm 3 + in_gcc 2 = 8 → qualified_B.
    r = score_founder_lead(
        is_b2b=True, has_crm_or_revenue_process=True, in_gcc=True
    )
    assert r.score == 8
    assert r.classification == LeadClassification.QUALIFIED_B.value


def test_nurture_band():
    # is_b2b 3 + in_gcc 2 = 5 → nurture.
    r = score_founder_lead(is_b2b=True, in_gcc=True)
    assert r.score == 5
    assert r.classification == LeadClassification.NURTURE.value


def test_below_nurture_drops():
    # is_b2b 3 + urgent 2 - vague_curiosity 2 = 3 → drop.
    r = score_founder_lead(is_b2b=True, urgent_within_30_days=True, vague_curiosity=True)
    assert r.score == 3
    assert r.classification == LeadClassification.DROP.value


def test_negative_signals_pull_score_down():
    # Without negatives this lead scores 9 (nurture). no_company + student
    # subtract 6, dropping it to 3 — below the nurture floor.
    r = score_founder_lead(
        decision_maker=True,
        is_b2b=True,
        has_crm_or_revenue_process=True,
        no_company=True,
        student_or_jobseeker=True,
    )
    assert r.score == 9 - 6
    assert r.classification == LeadClassification.DROP.value


def test_partner_flag_overrides_classification():
    r = score_founder_lead(decision_maker=True, is_partner=True)
    assert r.classification == LeadClassification.PARTNER_CANDIDATE.value
    # score is still computed and reported
    assert r.score == 3
    assert any("flagged_partner" in reason for reason in r.reasons)


def test_max_score():
    r = score_founder_lead(
        decision_maker=True,
        is_b2b=True,
        has_crm_or_revenue_process=True,
        uses_or_plans_ai=True,
        in_gcc=True,
        urgent_within_30_days=True,
        budget_5k_plus_sar=True,
    )
    assert r.score == 18
    assert r.classification == LeadClassification.QUALIFIED_A.value
