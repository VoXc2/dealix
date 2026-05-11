"""Command-line interface for Saudi AI provider operating system."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

from .commercial import compute_recurring_model, generate_customer_proposal_bundle, load_intake
from .dashboards import export_dashboard_bundle
from .kpis import kpis_for_service
from .offers import build_pitch, generate_offer
from .pricing import compute_roi, package_for_segment, quote_service
from .roadmap import roadmap_for_days
from .verifier import print_verification_report, verify_sellable


def _cmd_verify(_args: argparse.Namespace) -> int:
    result = verify_sellable()
    print_verification_report(result)
    return 0 if result.sellable_now else 1


def _cmd_package(args: argparse.Namespace) -> int:
    services = package_for_segment(args.segment)
    print(f"Segment package: {args.segment}")
    total_setup = 0.0
    total_monthly = 0.0
    for service in services:
        total_setup += service["setup_fee_sar"]
        total_monthly += service["monthly_retainer_sar"]
        print(
            f"- {service['service_id']}: setup={service['setup_fee_sar']} SAR, "
            f"monthly={service['monthly_retainer_sar']} SAR, "
            f"sla={service['sla']['label']}"
        )
    print(f"Total setup: {round(total_setup, 2)} SAR")
    print(f"Total monthly: {round(total_monthly, 2)} SAR")
    return 0


def _cmd_quote(args: argparse.Namespace) -> int:
    quote = quote_service(
        service_id=args.service,
        employees=args.employees,
        discount=args.discount,
        segment=args.segment,
    )
    print(f"Service: {quote.service_id}")
    print(f"Segment: {quote.segment}")
    print(f"Setup fee (list): {quote.setup_fee_sar} SAR")
    print(f"Implementation fee (after discount): {quote.implementation_fee_sar} SAR")
    print(f"Monthly retainer: {quote.monthly_retainer_sar} SAR")
    print(f"Annual contract value: {quote.annual_contract_value_sar} SAR")
    print(f"Discount applied: {quote.discount_applied:.2f}")
    print(f"Gross margin target: {quote.gross_margin_target:.2f}")
    print(f"SELLABLE_NOW: {'true' if quote.sellable else 'false'}")
    if quote.reasons:
        for reason in quote.reasons:
            print(f"- {reason}")
    return 0 if quote.sellable else 1


def _cmd_roadmap(args: argparse.Namespace) -> int:
    phases = roadmap_for_days(args.days)
    print(f"Roadmap horizon: {args.days} days")
    for phase in phases:
        print(f"{phase['name']} ({phase['start_day']}–{phase['end_day']})")
        for outcome in phase["outcomes"]:
            print(f"- {outcome}")
    return 0


def _cmd_kpis(args: argparse.Namespace) -> int:
    kpi = kpis_for_service(args.service)
    print(f"Service: {args.service}")
    print(f"North Star: {kpi['north_star']}")
    print("Business KPIs:")
    for item in kpi["business_kpis"]:
        print(f"- {item}")
    print("Operational KPIs:")
    for item in kpi["operational_kpis"]:
        print(f"- {item}")
    print("Guardrail KPIs:")
    for item in kpi["guardrail_kpis"]:
        print(f"- {item}")
    print("Targets:")
    for item in kpi["target_benchmarks"]:
        print(f"- {item}")
    print("Evidence:")
    print("- before/after KPI baseline export")
    print("- workflow execution logs")
    print("- sampled customer conversations and CRM records")
    return 0


def _cmd_pitch(args: argparse.Namespace) -> int:
    print(build_pitch(args.service, lang=args.lang))
    return 0


def _cmd_offer(args: argparse.Namespace) -> int:
    outputs = generate_offer(args.service, args.segment, lang=args.lang)
    for name, path in outputs.items():
        print(f"{name}: {path}")
    return 0


def _cmd_roi(args: argparse.Namespace) -> int:
    projection = compute_roi(
        args.service,
        {
            "monthly_tickets": args.tickets,
            "avg_agent_cost_sar": args.agent_cost,
            "automation_rate": args.automation_rate,
            "critical_incidents_annual": args.critical_incidents_annual,
            "avg_incident_cost_sar": args.avg_incident_cost_sar,
            "prevention_rate": args.prevention_rate,
            "incident_hours_monthly": args.incident_hours_monthly,
            "cost_per_downtime_hour_sar": args.cost_per_downtime_hour_sar,
            "reduction_rate": args.reduction_rate,
            "monthly_pipeline_sar": args.monthly_pipeline_sar,
            "conversion_lift_rate": args.conversion_lift_rate,
        },
    )
    print(f"Service Family: {projection.service_family}")
    print(f"Projected Monthly Savings: {projection.monthly_savings_sar} SAR")
    print(f"Projected Annual ROI: {projection.annual_roi_sar} SAR")
    return 0


def _cmd_proposal(args: argparse.Namespace) -> int:
    intake = load_intake(Path(args.intake_file))
    outputs = generate_customer_proposal_bundle(
        service_id=args.service,
        intake=intake,
        lang=args.lang,
        segment=args.segment,
    )
    for key, path in outputs.items():
        print(f"{key}: {path}")
    return 0


def _cmd_dashboard_export(args: argparse.Namespace) -> int:
    metrics: dict = {}
    if args.metrics_json:
        metrics = json.loads(Path(args.metrics_json).read_text(encoding="utf-8"))
    outputs = export_dashboard_bundle(
        output_dir=Path(args.output_dir) if args.output_dir else None,
        metrics=metrics,
    )
    for key, path in outputs.items():
        print(f"{key}: {path}")
    return 0


def _cmd_recurring_model(args: argparse.Namespace) -> int:
    result = compute_recurring_model(
        setup_fee_sar=args.setup_fee,
        monthly_retainer_sar=args.monthly,
        months=args.months,
        expansion_rate=args.expansion_rate,
    )
    print(f"Setup Fee: {result.setup_fee_sar} SAR")
    print(f"Monthly Retainer: {result.monthly_retainer_sar} SAR")
    print(f"Months: {result.months}")
    print(f"Expansion Rate: {result.expansion_rate:.2%}")
    print(f"Projected Total Revenue: {result.total_revenue_sar} SAR")
    print(f"Projected ARR Run Rate: {result.arr_run_rate_sar} SAR")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m saudi_ai_provider",
        description="Saudi AI Provider operating CLI",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    verify = sub.add_parser("verify", help="Run strict sellable verifier")
    verify.set_defaults(func=_cmd_verify)

    package = sub.add_parser("package", help="Show recommended package by segment")
    package.add_argument("--segment", required=True, choices=["smb", "mid_market", "enterprise"])
    package.set_defaults(func=_cmd_package)

    quote = sub.add_parser("quote", help="Generate quote for a service SKU")
    quote.add_argument("--service", required=True)
    quote.add_argument("--employees", required=True, type=int)
    quote.add_argument("--discount", type=float, default=0.0)
    quote.add_argument("--segment", choices=["smb", "mid_market", "enterprise"])
    quote.set_defaults(func=_cmd_quote)

    roadmap = sub.add_parser("roadmap", help="Generate execution roadmap")
    roadmap.add_argument("--days", type=int, default=180)
    roadmap.set_defaults(func=_cmd_roadmap)

    kpis = sub.add_parser("kpis", help="Show KPI tree for service")
    kpis.add_argument("--service", required=True)
    kpis.set_defaults(func=_cmd_kpis)

    pitch = sub.add_parser("pitch", help="Generate one-line pitch for a service")
    pitch.add_argument("--service", required=True)
    pitch.add_argument("--lang", choices=["ar", "en"], default="ar")
    pitch.set_defaults(func=_cmd_pitch)

    offer = sub.add_parser("offer", help="Generate offer and SOW markdown files")
    offer.add_argument("--service", required=True)
    offer.add_argument("--segment", required=True, choices=["smb", "mid_market", "enterprise"])
    offer.add_argument("--lang", choices=["ar", "en"], default="ar")
    offer.set_defaults(func=_cmd_offer)

    generate_offer_alias = sub.add_parser(
        "generate-offer",
        help="Generate full commercial offer artifacts",
    )
    generate_offer_alias.add_argument("--service", required=True)
    generate_offer_alias.add_argument(
        "--segment", required=True, choices=["smb", "mid_market", "enterprise"]
    )
    generate_offer_alias.add_argument("--industry", default="general")
    generate_offer_alias.add_argument("--lang", choices=["ar", "en"], default="ar")
    generate_offer_alias.set_defaults(func=_cmd_offer)

    roi = sub.add_parser("roi", help="Compute ROI projection for service")
    roi.add_argument("--service", required=True)
    roi.add_argument("--tickets", type=float, default=0.0)
    roi.add_argument("--agent-cost", type=float, default=0.0, dest="agent_cost")
    roi.add_argument("--automation-rate", type=float, default=0.0, dest="automation_rate")
    roi.add_argument("--critical-incidents-annual", type=float, default=0.0)
    roi.add_argument("--avg-incident-cost-sar", type=float, default=0.0)
    roi.add_argument("--prevention-rate", type=float, default=0.0)
    roi.add_argument("--incident-hours-monthly", type=float, default=0.0)
    roi.add_argument("--cost-per-downtime-hour-sar", type=float, default=0.0)
    roi.add_argument("--reduction-rate", type=float, default=0.0)
    roi.add_argument("--monthly-pipeline-sar", type=float, default=0.0)
    roi.add_argument("--conversion-lift-rate", type=float, default=0.0)
    roi.set_defaults(func=_cmd_roi)

    proposal = sub.add_parser("proposal", help="Generate customer-specific proposal bundle")
    proposal.add_argument("--service", required=True)
    proposal.add_argument("--intake-file", required=True)
    proposal.add_argument("--segment", choices=["smb", "mid_market", "enterprise"])
    proposal.add_argument("--lang", choices=["ar", "en"], default="ar")
    proposal.set_defaults(func=_cmd_proposal)

    dashboard = sub.add_parser(
        "dashboard-export",
        help="Export executive/sales/delivery/risk dashboard JSON files",
    )
    dashboard.add_argument("--metrics-json")
    dashboard.add_argument("--output-dir")
    dashboard.set_defaults(func=_cmd_dashboard_export)

    recurring = sub.add_parser(
        "recurring-model",
        help="Project recurring managed-operations revenue model",
    )
    recurring.add_argument("--setup-fee", type=float, required=True)
    recurring.add_argument("--monthly", type=float, required=True)
    recurring.add_argument("--months", type=int, default=12)
    recurring.add_argument("--expansion-rate", type=float, default=0.05)
    recurring.set_defaults(func=_cmd_recurring_model)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
