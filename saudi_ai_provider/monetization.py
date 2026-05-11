"""P2 monetization automation: scorecard, package recommendation, and renewal orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from .catalog import load_monetization_strategy
from .commercial import _default_roi_inputs
from .pricing import compute_roi, package_for_segment, quote_service, resolve_segment_by_employees


@dataclass(frozen=True)
class ProposalScorecard:
    total_score: float
    recommendation: str
    dimension_scores: dict[str, float]
    blockers: list[str]


@dataclass(frozen=True)
class PackageRecommendation:
    segment: str
    ranked_services: list[dict[str, Any]]
    rationale: str


@dataclass(frozen=True)
class RenewalExpansionPlan:
    renewal_risk: str
    renewal_actions: list[str]
    expansion_candidates: list[str]
    next_review_date: str
    rationale: list[str]


def _parse_budget_midpoint_sar(value: Any) -> float:
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value or "").replace(",", "").strip()
    if "-" in text:
        low, high = text.split("-", 1)
        try:
            return (float(low) + float(high)) / 2
        except ValueError:
            return 0.0
    try:
        return float(text)
    except ValueError:
        return 0.0


def _urgency_score(target_deadline: str) -> float:
    if not target_deadline:
        return 50.0
    try:
        deadline = datetime.fromisoformat(target_deadline).replace(tzinfo=timezone.utc)
    except ValueError:
        return 50.0
    now = datetime.now(timezone.utc)
    days = max(0, (deadline - now).days)
    if days <= 30:
        return 90.0
    if days <= 60:
        return 75.0
    if days <= 120:
        return 60.0
    return 45.0


def _data_readiness_score(intake: dict[str, Any]) -> float:
    data_sources = intake.get("data_sources", [])
    systems = intake.get("current_systems", [])
    score = 40.0
    if isinstance(data_sources, list):
        score += min(len(data_sources) * 10, 30)
    if isinstance(systems, list):
        score += min(len(systems) * 8, 24)
    if intake.get("data_owner"):
        score += 6
    return min(score, 100.0)


def _governance_readiness_score(intake: dict[str, Any]) -> float:
    score = 40.0
    constraints = intake.get("security_constraints", [])
    if constraints:
        score += 20
    if intake.get("decision_owner"):
        score += 20
    if intake.get("final_acceptance_signer"):
        score += 20
    return min(score, 100.0)


def _strategic_fit_score(service_id: str, intake: dict[str, Any]) -> float:
    strategy = load_monetization_strategy()
    family = service_id.rsplit("_", 1)[0]
    priorities = strategy.get("priority_service_families", [])
    score = 55.0
    if family in priorities:
        score += 25
    if intake.get("sector") in {"healthcare", "banking", "logistics", "government"}:
        score += 20
    return min(score, 100.0)


def compute_proposal_scorecard(service_id: str, intake: dict[str, Any]) -> ProposalScorecard:
    strategy = load_monetization_strategy()
    weights = strategy["scorecard"]["weights"]
    thresholds = strategy["scorecard"]["thresholds"]

    employees = int(intake.get("company_size", intake.get("employees", 100)))
    segment = resolve_segment_by_employees(employees)
    quote = quote_service(service_id=service_id, employees=employees, segment=segment)

    budget_mid = _parse_budget_midpoint_sar(intake.get("budget_range_sar"))
    annual_contract = quote.annual_contract_value_sar or 1
    budget_fit = min(100.0, max(0.0, (budget_mid / annual_contract) * 100))
    urgency = _urgency_score(str(intake.get("target_deadline", "")))
    data_readiness = _data_readiness_score(intake)
    governance_readiness = _governance_readiness_score(intake)
    roi_inputs = _default_roi_inputs(service_id, intake)
    roi = compute_roi(service_id, roi_inputs)
    roi_strength = min(100.0, max(0.0, (roi.annual_roi_sar / annual_contract) * 25))
    strategic_fit = _strategic_fit_score(service_id, intake)

    dimension_scores = {
        "budget_fit": round(budget_fit, 2),
        "urgency": round(urgency, 2),
        "data_readiness": round(data_readiness, 2),
        "governance_readiness": round(governance_readiness, 2),
        "roi_strength": round(roi_strength, 2),
        "strategic_fit": round(strategic_fit, 2),
    }
    weighted = (
        dimension_scores["budget_fit"] * weights["budget_fit"]
        + dimension_scores["urgency"] * weights["urgency"]
        + dimension_scores["data_readiness"] * weights["data_readiness"]
        + dimension_scores["governance_readiness"] * weights["governance_readiness"]
        + dimension_scores["roi_strength"] * weights["roi_strength"]
        + dimension_scores["strategic_fit"] * weights["strategic_fit"]
    )
    total = round(weighted, 2)

    blockers: list[str] = []
    if budget_fit < 60:
        blockers.append("budget below suggested contract value")
    if data_readiness < 60:
        blockers.append("insufficient data readiness")
    if governance_readiness < 60:
        blockers.append("governance owner/signoff readiness is weak")

    if total >= thresholds["go"] and not blockers:
        recommendation = "GO"
    elif total >= thresholds["go_with_conditions"]:
        recommendation = "GO_WITH_CONDITIONS"
    else:
        recommendation = "HOLD"

    return ProposalScorecard(
        total_score=total,
        recommendation=recommendation,
        dimension_scores=dimension_scores,
        blockers=blockers,
    )


def recommend_auto_package(intake: dict[str, Any], max_services: int = 5) -> PackageRecommendation:
    strategy = load_monetization_strategy()
    priorities = strategy.get("priority_service_families", [])
    employees = int(intake.get("company_size", intake.get("employees", 100)))
    segment = resolve_segment_by_employees(employees)
    package = package_for_segment(segment)

    ranked: list[dict[str, Any]] = []
    for item in package:
        family = item["service_id"].rsplit("_", 1)[0]
        priority_bonus = max(0, 100 - (priorities.index(family) * 8)) if family in priorities else 40
        readiness_bonus = 10 if intake.get("decision_owner") else 0
        fit_score = round(min(100.0, priority_bonus + readiness_bonus), 2)
        ranked.append(
            {
                "service_id": item["service_id"],
                "fit_score": fit_score,
                "setup_fee_sar": item["setup_fee_sar"],
                "monthly_retainer_sar": item["monthly_retainer_sar"],
                "support_sla": item["sla"]["label"],
            }
        )

    ranked_sorted = sorted(ranked, key=lambda x: x["fit_score"], reverse=True)[:max_services]
    rationale = (
        "Recommended services prioritize governance + customer operations + observability "
        "while matching customer segment readiness."
    )
    return PackageRecommendation(segment=segment, ranked_services=ranked_sorted, rationale=rationale)


def orchestrate_renewal_expansion(customer_state: dict[str, Any]) -> RenewalExpansionPlan:
    strategy = load_monetization_strategy()
    renewal_cfg = strategy["renewal"]
    expansion_cfg = strategy["expansion"]

    service_id = str(customer_state.get("service_id", "CUSTOMER_PORTAL_GOLD")).upper()
    health = float(customer_state.get("health_score", 70))
    payment_delay = float(customer_state.get("payment_delay_days", 0))
    sla = float(customer_state.get("sla_compliance", 0.9))
    proof_events = int(customer_state.get("proof_events_count", 0))
    expansion_readiness = float(customer_state.get("expansion_readiness", 0))
    usage_growth = float(customer_state.get("usage_growth_rate", 0))

    rationale: list[str] = []
    if health >= renewal_cfg["health_thresholds"]["low_risk"] and payment_delay < renewal_cfg["payment_delay_threshold_days"]:
        renewal_risk = "LOW"
    elif health >= renewal_cfg["health_thresholds"]["medium_risk"] and sla >= renewal_cfg["sla_compliance_threshold"]:
        renewal_risk = "MEDIUM"
    else:
        renewal_risk = "HIGH"

    if renewal_risk == "LOW":
        renewal_actions = [
            "Start renewal conversation 90 days before contract end.",
            "Present ROI and proof pack to executive sponsor.",
            "Offer expansion module bundle with annual commitment."
        ]
    elif renewal_risk == "MEDIUM":
        renewal_actions = [
            "Run 30-day stabilization plan for SLA and customer health.",
            "Schedule executive recovery review within 7 days.",
            "Gate expansion until health score improves."
        ]
    else:
        renewal_actions = [
            "Trigger escalation matrix and weekly executive checkpoint.",
            "Deploy incident-recovery and trust remediation pack.",
            "Freeze expansion offers and protect base contract."
        ]
    rationale.append(f"renewal_risk={renewal_risk}, health={health}, payment_delay_days={payment_delay}, sla={sla}")

    expansion_candidates: list[str] = []
    if (
        proof_events >= expansion_cfg["minimum_proof_events"]
        and expansion_readiness >= expansion_cfg["minimum_expansion_readiness"]
        and usage_growth >= expansion_cfg["usage_growth_threshold"]
    ):
        expansion_candidates = expansion_cfg.get("adjacency_matrix", {}).get(service_id, [])
        rationale.append("Expansion conditions met from proof/readiness/usage growth.")
    else:
        rationale.append("Expansion gated until proof/readiness/usage thresholds are met.")

    review_window_days = int(customer_state.get("renewal_window_days", renewal_cfg["window_days_default"]))
    next_review_date = (
        datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        + f" (review_window_days={review_window_days})"
    )

    return RenewalExpansionPlan(
        renewal_risk=renewal_risk,
        renewal_actions=renewal_actions,
        expansion_candidates=expansion_candidates,
        next_review_date=next_review_date,
        rationale=rationale,
    )
