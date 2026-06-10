"""Tests for sales_os qualification and proposal skeleton."""

from __future__ import annotations

from auto_client_acquisition.sales_os import (
    ClientRiskSignals,
    ICPDimensions,
    QualificationVerdict,
    build_proposal_skeleton,
    qualify_opportunity,
    render_scope_bullets,
    verdict_label_ar,
)


def test_qualify_rejects_high_risk() -> None:
    icp = ICPDimensions(80, 80, 80, 80, 80)
    risk = ClientRiskSignals(
        wants_scraping_or_spam=True,
        wants_guaranteed_sales=False,
        unclear_pain=False,
        no_owner=False,
        data_not_ready=False,
        budget_unknown=False,
    )
    v, _ = qualify_opportunity(icp=icp, risk=risk, accepts_governance=True, proof_path_possible=True)
    assert v == QualificationVerdict.REJECT


def test_qualify_accept_good_fit() -> None:
    icp = ICPDimensions(85, 70, 75, 80, 70)
    risk = ClientRiskSignals(False, False, False, False, False, False)
    v, _ = qualify_opportunity(icp=icp, risk=risk, accepts_governance=True, proof_path_possible=True)
    assert v == QualificationVerdict.ACCEPT


def test_proposal_skeleton_has_no_sales_guarantee() -> None:
    p = build_proposal_skeleton(client_label="Co", sprint_name="Revenue Intelligence Sprint")
    assert "does not promise sales outcomes" in p["no_sales_guarantee_statement"]


def test_verdict_label_ar() -> None:
    assert "تشخيص" in verdict_label_ar(QualificationVerdict.DIAGNOSTIC_ONLY)


def test_render_scope() -> None:
    b = render_scope_bullets({"included": ("scoring",), "excluded": ("scraping",)})
    assert any("scraping" in x for x in b)
