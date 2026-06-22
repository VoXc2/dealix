from __future__ import annotations

from .firmographic_engine import firmographic_score
from .intent_engine import intent_score
from .schemas import ComplianceDecision, LeadCompany, PriorityBucket, ScoreBreakdown, SignalRecord
from .technographic_engine import technographic_score


def score_lead(lead: LeadCompany, signals: list[SignalRecord], compliance: ComplianceDecision, deliverability_risk: int) -> ScoreBreakdown:
    fit = round((firmographic_score(lead) + technographic_score(lead)) / 2)
    intent = intent_score(signals)
    urgency = min(100, intent + (15 if any(signal.signal_name == "broken_form" and signal.detected for signal in signals) else 0))
    revenue_potential = min(100, fit + (10 if lead.sector in {"SaaS", "real estate", "clinics"} else 0))
    engagement = 70 if lead.metadata.get("inbound") else 35
    data_quality = 85 if lead.domain and lead.company_name else 55
    compliance_risk = 90 if not compliance.allowed else 20
    penalties: list[str] = []
    if not compliance.allowed:
        penalties.append("compliance_block")
    if deliverability_risk > 70:
        penalties.append("deliverability_risk")
    weighted = round((fit * 0.22) + (intent * 0.18) + (urgency * 0.16) + (revenue_potential * 0.16) + (engagement * 0.1) + (data_quality * 0.08) + ((100 - compliance_risk) * 0.05) + ((100 - deliverability_risk) * 0.05))
    if not compliance.allowed:
        bucket = PriorityBucket.blocked
    elif weighted >= 80:
        bucket = PriorityBucket.p0_now
    elif weighted >= 65:
        bucket = PriorityBucket.p1_this_week
    elif weighted >= 45:
        bucket = PriorityBucket.p2_nurture
    else:
        bucket = PriorityBucket.p3_low_priority
    return ScoreBreakdown(fit=fit, intent=intent, urgency=urgency, revenue_potential=revenue_potential, engagement=engagement, data_quality=data_quality, compliance_risk=compliance_risk, deliverability_risk=deliverability_risk, final_priority=bucket, penalties=penalties)