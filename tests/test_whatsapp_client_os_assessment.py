"""WhatsApp Client OS — readiness assessment scoring + recommendation."""

from __future__ import annotations

from auto_client_acquisition.service_catalog.registry import SERVICE_IDS
from auto_client_acquisition.whatsapp_client_os import assessment as asmt
from auto_client_acquisition.whatsapp_client_os.assessment import AXIS_ORDER, axis_spec


def _answers(option_index: int) -> list:
    """Build a full answer set picking the same option index per axis."""
    out = []
    for ax in AXIS_ORDER:
        opts = axis_spec(ax)["options"]
        opt = opts[min(option_index, len(opts) - 1)]
        out.append(asmt.make_answer(ax, opt["id"]))
    return out


def test_ten_axes_present() -> None:
    assert len(AXIS_ORDER) == 10


def test_high_readiness_scores_high_low_risk() -> None:
    score = asmt.score_assessment(_answers(0))  # highest-readiness option each
    assert score.overall >= 75
    assert score.risk == "low"
    assert 0 <= score.revenue_readiness <= 100


def test_low_readiness_scores_low_high_risk_free_diagnostic() -> None:
    answers = _answers(99)  # lowest-readiness option each (index clamps to last)
    score = asmt.score_assessment(answers)
    assert score.overall < 45
    assert score.risk == "high"
    rec = asmt.recommend_offer(score, answers)
    assert rec["offer_id"] == "free_mini_diagnostic"


def test_recommendation_is_a_real_catalog_id() -> None:
    for idx in range(4):
        answers = _answers(idx)
        score = asmt.score_assessment(answers)
        rec = asmt.recommend_offer(score, answers)
        assert rec["offer_id"] in SERVICE_IDS
        assert rec["offer_name_ar"]  # bilingual name attached
        assert rec["rationale_ar"]  # never empty — evidence for the pick
        assert rec["required_permissions"]


def test_followup_gap_recommends_sprint() -> None:
    # Leads present + weak follow-up → governed 30-day Revenue Command Pilot.
    answers = [
        asmt.make_answer("lead_flow", "lead_flow_high"),
        asmt.make_answer("channel_chaos", "channel_many"),
        asmt.make_answer("follow_up", "follow_up_no"),
        asmt.make_answer("crm", "crm_none"),
        asmt.make_answer("decision_maker", "dm_clear"),
        asmt.make_answer("offer_clarity", "offer_clear"),
        asmt.make_answer("reporting", "report_none"),
        asmt.make_answer("automation_readiness", "auto_some"),
        asmt.make_answer("compliance_privacy", "comp_none"),
        asmt.make_answer("urgency", "urgency_now"),
    ]
    score = asmt.score_assessment(answers)
    rec = asmt.recommend_offer(score, answers)
    assert rec["offer_id"] in {"revenue_command_pilot_30d", "data_to_revenue_pack_1500"}
    assert rec["offer_id"] in SERVICE_IDS


def test_sensitive_data_forces_high_risk_and_warning() -> None:
    answers = _answers(0)
    # override compliance axis to a sensitive option
    answers = [a for a in answers if a.axis != "compliance_privacy"]
    answers.append(asmt.make_answer("compliance_privacy", "comp_high"))
    assert asmt.has_sensitive_data(answers) is True
    score = asmt.score_assessment(answers)
    assert score.risk == "high"
    rec = asmt.recommend_offer(score, answers)
    assert any("حسّاسة" in r for r in rec["rationale_ar"])


def test_build_assessment_is_complete_when_all_axes_answered() -> None:
    a = asmt.build_assessment(client_handle="966500000000", answers=_answers(0))
    assert a.completed is True
    assert a.score is not None
    assert a.recommended_offer in SERVICE_IDS
    assert a.evidence_level == "L1"


def test_partial_assessment_is_not_complete() -> None:
    partial = [asmt.make_answer("lead_flow", "lead_flow_high")]
    a = asmt.build_assessment(client_handle="x", answers=partial)
    assert a.completed is False


def test_next_axis_and_progress() -> None:
    assert asmt.next_axis([]) == AXIS_ORDER[0]
    assert asmt.progress([]) == (0, 10)
    assert asmt.next_axis(list(AXIS_ORDER)) is None


def test_customer_facing_recommendations_never_expose_legacy_fixed_price_offers() -> None:
    for idx in range(4):
        answers = _answers(idx)
        score = asmt.score_assessment(answers)
        rec = asmt.recommend_offer(score, answers)
        assert rec["offer_id"] in {"free_mini_diagnostic", "revenue_command_pilot_30d"}
        rendered = str(rec)
        for retired_price in ("1500", "2999", "7500"):
            assert retired_price not in rendered


def test_high_readiness_routes_to_discovery_then_customer_specific_pilot_quote() -> None:
    answers = _answers(0)
    score = asmt.score_assessment(answers)
    rec = asmt.recommend_offer(score, answers)
    assert rec["offer_id"] == "revenue_command_pilot_30d"
    rationale = " ".join(rec["rationale_ar"])
    assert "customer-specific quote" in rationale
    assert "discovery" in rationale
