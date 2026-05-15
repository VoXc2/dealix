"""Commercialization helpers for customer-specific proposals and recurring models."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .catalog import OFFERS_OUT_DIR, TEMPLATES_DIR
from .offers import generate_offer
from .pricing import compute_roi, parse_service_id, quote_service, resolve_segment_by_employees


@dataclass(frozen=True)
class RecurringModel:
    setup_fee_sar: float
    monthly_retainer_sar: float
    months: int
    expansion_rate: float
    total_revenue_sar: float
    arr_run_rate_sar: float


def load_intake(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    return json.loads(text)


def _to_slug(value: str) -> str:
    return "".join(c.lower() if c.isalnum() else "_" for c in value).strip("_")


def _default_roi_inputs(service_id: str, intake: dict[str, Any]) -> dict[str, float]:
    engine, _tier = parse_service_id(service_id)
    ticket_like = float(intake.get("monthly_tickets", intake.get("tickets", 10000)))
    agent_cost = float(intake.get("avg_agent_cost_sar", 15))
    automation_rate = float(intake.get("automation_rate", 0.25))
    incident_annual = float(intake.get("critical_incidents_annual", 12))
    incident_cost = float(intake.get("avg_incident_cost_sar", 25000))
    prevention_rate = float(intake.get("prevention_rate", 0.3))
    downtime_hours = float(intake.get("incident_hours_monthly", 120))
    downtime_cost = float(intake.get("cost_per_downtime_hour_sar", 3000))
    reduction_rate = float(intake.get("reduction_rate", 0.25))
    pipeline = float(intake.get("monthly_pipeline_sar", 1000000))
    conversion_lift = float(intake.get("conversion_lift_rate", 0.08))

    if engine == "CUSTOMER_PORTAL":
        return {
            "monthly_tickets": ticket_like,
            "avg_agent_cost_sar": agent_cost,
            "automation_rate": automation_rate,
        }
    if engine == "SECURITY":
        return {
            "critical_incidents_annual": incident_annual,
            "avg_incident_cost_sar": incident_cost,
            "prevention_rate": prevention_rate,
        }
    if engine == "OBSERVABILITY":
        return {
            "incident_hours_monthly": downtime_hours,
            "cost_per_downtime_hour_sar": downtime_cost,
            "reduction_rate": reduction_rate,
        }
    return {
        "monthly_pipeline_sar": pipeline,
        "conversion_lift_rate": conversion_lift,
    }


def compute_recurring_model(
    setup_fee_sar: float,
    monthly_retainer_sar: float,
    months: int,
    expansion_rate: float,
) -> RecurringModel:
    total = float(setup_fee_sar)
    current_monthly = float(monthly_retainer_sar)
    for _ in range(max(0, months)):
        total += current_monthly
        current_monthly *= (1 + expansion_rate)
    arr = current_monthly * 12
    return RecurringModel(
        setup_fee_sar=setup_fee_sar,
        monthly_retainer_sar=monthly_retainer_sar,
        months=months,
        expansion_rate=expansion_rate,
        total_revenue_sar=round(total, 2),
        arr_run_rate_sar=round(arr, 2),
    )


def generate_customer_proposal_bundle(
    *,
    service_id: str,
    intake: dict[str, Any],
    lang: str = "ar",
    segment: str | None = None,
    output_dir: Path | None = None,
) -> dict[str, Path]:
    employees = int(intake.get("company_size", intake.get("employees", 100)))
    resolved_segment = segment or resolve_segment_by_employees(employees)
    company_name = str(intake.get("company_name", "customer"))
    company_slug = _to_slug(company_name)

    target_dir = output_dir or (OFFERS_OUT_DIR / "proposals" / company_slug)
    target_dir.mkdir(parents=True, exist_ok=True)

    offer_files = generate_offer(
        service_id=service_id,
        segment=resolved_segment,
        lang=lang,
        output_dir=target_dir,
    )
    quote = quote_service(service_id=service_id, employees=employees, segment=resolved_segment)
    roi_inputs = _default_roi_inputs(service_id, intake)
    roi = compute_roi(service_id, roi_inputs)

    proposal_md = target_dir / f"{service_id.lower()}_{company_slug}_proposal.md"
    exec_summary_md = target_dir / f"{service_id.lower()}_{company_slug}_executive_summary.md"
    pricing_csv = target_dir / f"{service_id.lower()}_{company_slug}_pricing_sheet.csv"

    proposal_template = TEMPLATES_DIR / "proposal_bundle_ar.md"
    proposal_text = proposal_template.read_text(encoding="utf-8")
    replacements = {
        "{{company_name}}": company_name,
        "{{service_id}}": service_id,
        "{{segment}}": resolved_segment,
        "{{industry}}": str(intake.get("sector", intake.get("industry", "general"))),
        "{{buyer}}": str(intake.get("decision_owner", "executive_owner")),
        "{{budget_range_sar}}": str(intake.get("budget_range_sar", "N/A")),
        "{{target_deadline}}": str(intake.get("target_deadline", "N/A")),
        "{{setup_fee_sar}}": str(quote.setup_fee_sar),
        "{{monthly_retainer_sar}}": str(quote.monthly_retainer_sar),
        "{{annual_contract_value_sar}}": str(quote.annual_contract_value_sar),
        "{{monthly_roi_sar}}": str(roi.monthly_savings_sar),
        "{{annual_roi_sar}}": str(roi.annual_roi_sar),
    }
    for key, value in replacements.items():
        proposal_text = proposal_text.replace(key, value)
    proposal_md.write_text(proposal_text, encoding="utf-8")

    exec_summary_md.write_text(
        (
            f"# Executive Summary — {company_name}\n\n"
            f"- Service: {service_id}\n"
            f"- Segment: {resolved_segment}\n"
            f"- Buyer: {intake.get('decision_owner', 'executive_owner')}\n"
            f"- Monthly ROI (projected): {roi.monthly_savings_sar} SAR\n"
            f"- Annual ROI (projected): {roi.annual_roi_sar} SAR\n"
            f"- Contract Value (baseline): {quote.annual_contract_value_sar} SAR\n"
            f"- Final Acceptance Signer: {intake.get('final_acceptance_signer', 'TBD')}\n"
        ),
        encoding="utf-8",
    )

    with pricing_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "company_name",
                "service_id",
                "segment",
                "setup_fee_sar",
                "monthly_retainer_sar",
                "annual_contract_value_sar",
                "projected_monthly_roi_sar",
                "projected_annual_roi_sar",
            ]
        )
        writer.writerow(
            [
                company_name,
                service_id,
                resolved_segment,
                quote.setup_fee_sar,
                quote.monthly_retainer_sar,
                quote.annual_contract_value_sar,
                roi.monthly_savings_sar,
                roi.annual_roi_sar,
            ]
        )

    return {
        "proposal": proposal_md,
        "executive_summary": exec_summary_md,
        "pricing_sheet": pricing_csv,
        **offer_files,
    }
