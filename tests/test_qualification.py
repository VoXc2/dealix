"""Sales qualification — map ICP + risk signals to a commercial verdict."""
from __future__ import annotations

from auto_client_acquisition.sales_os.client_risk_score import ClientRiskSignals
from auto_client_acquisition.sales_os.icp_score import ICPDimensions
from auto_client_acquisition.sales_os.qualification import (
    QualificationVerdict,
    qualify_opportunity,
)


def _icp(value: int) -> ICPDimensions:
    return ICPDimensions(
        b2b_service_fit=value,
        data_maturity=value,
        governance_posture=value,
        budget_signal=value,
        decision_velocity=value,
    )


def _clean_risk() -> ClientRiskSignals:
    return ClientRiskSignals(
        wants_scraping_or_spam=False,
        wants_guaranteed_sales=False,
        unclear_pain=False,
        no_owner=False,
        data_not_ready=False,
        budget_unknown=False,
    )


def test_strong_icp_clean_risk_accepts():
    verdict, reasons = qualify_opportunity(
        icp=_icp(90), risk=_clean_risk(), accepts_governance=True, proof_path_possible=True
    )
    assert verdict == QualificationVerdict.ACCEPT
    assert "icp_ok_risk_ok" in reasons


def test_scraping_request_is_rejected():
    risk = ClientRiskSignals(
        wants_scraping_or_spam=True, wants_guaranteed_sales=False, unclear_pain=False,
        no_owner=False, data_not_ready=False, budget_unknown=False,
    )
    verdict, reasons = qualify_opportunity(
        icp=_icp(90), risk=risk, accepts_governance=True, proof_path_possible=True
    )
    assert verdict == QualificationVerdict.REJECT
    assert reasons == ("non_negotiable_risk",)


def test_guaranteed_sales_request_is_rejected():
    risk = ClientRiskSignals(
        wants_scraping_or_spam=False, wants_guaranteed_sales=True, unclear_pain=False,
        no_owner=False, data_not_ready=False, budget_unknown=False,
    )
    verdict, _ = qualify_opportunity(
        icp=_icp(90), risk=risk, accepts_governance=True, proof_path_possible=True
    )
    assert verdict == QualificationVerdict.REJECT


def test_governance_not_accepted_refers_out():
    verdict, reasons = qualify_opportunity(
        icp=_icp(90), risk=_clean_risk(), accepts_governance=False, proof_path_possible=True
    )
    assert verdict == QualificationVerdict.REFER_OUT
    assert reasons == ("governance_not_accepted",)


def test_no_proof_path_with_strong_icp_reframes():
    verdict, reasons = qualify_opportunity(
        icp=_icp(90), risk=_clean_risk(), accepts_governance=True, proof_path_possible=False
    )
    assert verdict == QualificationVerdict.REFRAME
    assert "weak_proof_path" in reasons


def test_no_proof_path_with_weak_icp_is_diagnostic_only():
    verdict, reasons = qualify_opportunity(
        icp=_icp(30), risk=_clean_risk(), accepts_governance=True, proof_path_possible=False
    )
    assert verdict == QualificationVerdict.DIAGNOSTIC_ONLY
    assert "weak_proof_path" in reasons


def test_low_icp_starts_with_diagnostic():
    verdict, reasons = qualify_opportunity(
        icp=_icp(40), risk=_clean_risk(), accepts_governance=True, proof_path_possible=True
    )
    assert verdict == QualificationVerdict.DIAGNOSTIC_ONLY
    assert "icp_low_start_with_diagnostic" in reasons


def test_mid_icp_reframes_into_a_package():
    verdict, reasons = qualify_opportunity(
        icp=_icp(50), risk=_clean_risk(), accepts_governance=True, proof_path_possible=True
    )
    assert verdict == QualificationVerdict.REFRAME
    assert "icp_mid_package_shape" in reasons
