"""Qualification — map discovery answers to a commercial verdict (no LLM)."""

from __future__ import annotations

from enum import StrEnum

from auto_client_acquisition.sales_os.client_risk_score import ClientRiskSignals, client_risk_score
from auto_client_acquisition.sales_os.icp_score import ICPDimensions, icp_score


class QualificationVerdict(StrEnum):
    ACCEPT = "accept"
    DIAGNOSTIC_ONLY = "diagnostic_only"
    REFRAME = "reframe"
    REJECT = "reject"
    REFER_OUT = "refer_out"


def qualify_opportunity(
    *,
    icp: ICPDimensions,
    risk: ClientRiskSignals,
    accepts_governance: bool,
    proof_path_possible: bool,
) -> tuple[QualificationVerdict, tuple[str, ...]]:
    reasons: list[str] = []
    icp_s = icp_score(icp)
    r = client_risk_score(risk)
    if risk.wants_scraping_or_spam or risk.wants_guaranteed_sales:
        return QualificationVerdict.REJECT, ("non_negotiable_risk",)
    if r >= 55:
        return QualificationVerdict.REJECT, ("high_client_risk",)
    if not accepts_governance:
        return QualificationVerdict.REFER_OUT, ("governance_not_accepted",)
    if not proof_path_possible:
        reasons.append("weak_proof_path")
        if icp_s < 50:
            return QualificationVerdict.DIAGNOSTIC_ONLY, tuple(reasons)
        return QualificationVerdict.REFRAME, tuple(reasons)
    if icp_s < 45:
        return QualificationVerdict.DIAGNOSTIC_ONLY, ("icp_low_start_with_diagnostic",)
    if icp_s < 60:
        return QualificationVerdict.REFRAME, ("icp_mid_package_shape",)
    return QualificationVerdict.ACCEPT, ("icp_ok_risk_ok",)


__all__ = ["QualificationVerdict", "qualify_opportunity"]
